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

    uploaded_file = st.file_uploader(
        "Upload File Excel",
        type=["xlsx"]
    )

    if uploaded_file:

        # ======================================
        # BACA FILE
        # ======================================

        df = pd.read_excel(
            uploaded_file,
            header=None
        )

        st.markdown("## 📋 PREVIEW DATA")

        st.dataframe(
            df,
            use_container_width=True,
            height=400
        )

        # ======================================
        # PILIH KOLOM
        # ======================================

        st.markdown("## ⚙️ Mapping Kolom")

        col_options = list(df.columns)

        service_col = st.selectbox(
            "SERVICE",
            col_options
        )

        customer_col = st.selectbox(
            "CUSTOMER",
            col_options,
            index=min(4, len(col_options)-1)
        )

        rev_jan_col = st.selectbox(
            "Revenue Jan",
            col_options
        )

        ebit_jan_col = st.selectbox(
            "EBIT Jan",
            col_options
        )

        rev_feb_col = st.selectbox(
            "Revenue Feb",
            col_options
        )

        ebit_feb_col = st.selectbox(
            "EBIT Feb",
            col_options
        )

        # ======================================
        # BARIS DATA
        # ======================================

        start_row = st.number_input(
            "Data mulai dari baris",
            min_value=1,
            value=8
        )

        # ======================================
        # GENERATE
        # ======================================

        if st.button("🚀 GENERATE TEMPLATE"):

            temp = df.iloc[start_row-1:].copy()

            result = pd.DataFrame()

            result["ENTITY"] = ""

            result["SERVICE"] = temp[
                service_col
            ]

            result["CUSTOMER"] = temp[
                customer_col
            ]

            result["PNL Afiliasi"] = ""

            result["Vertical 2"] = ""

            result["Existing/Whitesheet"] = ""

            result["Revenue Jan"] = temp[
                rev_jan_col
            ]

            result["EBIT Jan"] = temp[
                ebit_jan_col
            ]

            result["Revenue Feb"] = temp[
                rev_feb_col
            ]

            result["EBIT Feb"] = temp[
                ebit_feb_col
            ]

            # ==================================
            # HAPUS TOTAL
            # ==================================

            result = result[
                ~result["CUSTOMER"]
                .astype(str)
                .str.upper()
                .str.contains(
                    "TOTAL",
                    na=False
                )
            ]

            st.markdown(
                "## 📊 HASIL TEMPLATE"
            )

            st.dataframe(
                result,
                use_container_width=True
            )

            output = io.BytesIO()

            with pd.ExcelWriter(
                output,
                engine="openpyxl"
            ) as writer:

                result.to_excel(
                    writer,
                    index=False
                )

            st.download_button(
                "⬇️ Download Template",
                output.getvalue(),
                "summary_template.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
