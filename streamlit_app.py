import streamlit as st
import pandas as pd
import io

# ================= CONFIG =================
st.set_page_config(
    page_title="Data Merge Dashboard",
    page_icon="📊",
    layout="wide"
)

# ================= SESSION =================
if "menu" not in st.session_state:
    st.session_state.menu = "HOME"

# ================= CSS =================
st.markdown("""
<style>

html, body, [class*="css"]{
    background: linear-gradient(135deg,#0a1931,#16213e);
    color:white;
    font-family:'Poppins',sans-serif;
}

.header-container{
    background: linear-gradient(135deg,#0a1931,#1f4068);
    color:#ffd369;
    padding:2rem;
    border-radius:15px;
    text-align:center;
    font-size:28px;
    font-weight:bold;
    margin-bottom:30px;
}

.menu-card{
    background:#112240;
    border-radius:15px;
    padding:2rem;
    text-align:center;
    border:1px solid rgba(255,211,105,0.2);
}

.stButton > button{
    background:#ffd369;
    color:#0a1931;
    border:none;
    border-radius:10px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
with st.sidebar:

    st.markdown("## 📋 MENU")

    selected = st.radio(
        "",
        [
            "HOME",
            "MERGE DATA"
        ]
    )

    st.session_state.menu = selected

menu = st.session_state.menu

# ================= HOME =================
if menu == "HOME":

    st.markdown("""
    <div class='header-container'>
        DATA MERGE DASHBOARD
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='menu-card'>
        <h2 style='color:#ffd369'>MERGE DATA</h2>
        <p>Upload beberapa file Excel dan gabungkan menjadi satu file.</p>
    </div>
    """, unsafe_allow_html=True)

# ================= MERGE DATA =================
elif menu == "MERGE DATA":

    st.header("MERGE DATA")

    uploaded_file = st.file_uploader(
        "Upload File Excel",
        type=["xlsx", "xls"]
    )

    if uploaded_file is not None:

        df = pd.read_excel(uploaded_file, header=None)

        st.subheader("Preview Data Awal")
        st.dataframe(df.head(20))

        if st.button("Proses Merge Data"):

            # Cari baris header customer
            header_row = None

            for i in range(len(df)):
                row_text = " ".join(df.iloc[i].astype(str))

                if "CUSTOMER" in row_text.upper():
                    header_row = i
                    break

            if header_row is None:
                st.error("Header CUSTOMER tidak ditemukan")
                st.stop()

            # Ambil header
            header = df.iloc[header_row]

            # Data setelah header
            data = df.iloc[header_row + 1:].copy()

            # Set header
            data.columns = header

            # Hapus kolom kosong
            data = data.dropna(axis=1, how="all")

            # Hapus baris kosong
            data = data.dropna(how="all")

            # Forward fill untuk merged cell
            data = data.ffill()

            st.success("Merge Data Berhasil")

            st.subheader("Hasil")
            st.dataframe(data)

            output = BytesIO()

            with pd.ExcelWriter(
                output,
                engine="openpyxl"
            ) as writer:

                data.to_excel(
                    writer,
                    sheet_name="Merged_Data",
                    index=False
                )

            st.download_button(
                "Download Hasil",
                output.getvalue(),
                file_name="merged_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
