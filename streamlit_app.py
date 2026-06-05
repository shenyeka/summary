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

    st.markdown("""
    <div class='header-container'>
        MERGE DATA
    </div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload File Excel",
        type=["xlsx"],
        accept_multiple_files=True
    )

    if uploaded_files:

        merged_df = pd.DataFrame()

        for file in uploaded_files:

            df = pd.read_excel(file)

            df["SOURCE FILE"] = file.name

            merged_df = pd.concat(
                [merged_df, df],
                ignore_index=True
            )

        # ================= SUMMARY =================

        total_file = len(uploaded_files)
        total_row = len(merged_df)
        total_col = len(merged_df.columns)
        total_duplicate = merged_df.duplicated().sum()

        st.markdown("## 📊 SUMMARY")

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Total File", total_file)
        c2.metric("Total Row", f"{total_row:,}")
        c3.metric("Total Column", total_col)
        c4.metric("Duplicate", total_duplicate)

        # ================= PREVIEW =================

        st.markdown("## 📋 PREVIEW DATA")

        st.dataframe(
            merged_df,
            use_container_width=True
        )

        # ================= DOWNLOAD =================

        output = io.BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            merged_df.to_excel(
                writer,
                index=False
            )

        st.download_button(
            "⬇️ Download Merge Result",
            data=output.getvalue(),
            file_name="merged_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:

        st.info(
            "Silakan upload file terlebih dahulu."
        )
