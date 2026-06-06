import streamlit as st
import pandas as pd
from io import BytesIO

# ================= CONFIG =================
st.set_page_config(
    page_title="Data Merge Dashboard",
    page_icon="📊",
    layout="wide"
)

# ================= SESSION =================
if "menu" not in st.session_state:
    st.session_state.menu = "HOME"

if "mapping" not in st.session_state:
    st.session_state.mapping = {}

# ================= CSS =================
st.markdown("""
<style>

html, body, [class*="css"]{
    background: linear-gradient(135deg,#0a1931,#16213e);
    color:white;
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

# ======================================================
# HOME
# ======================================================
if menu == "HOME":

    st.markdown("""
    <div class="header-container">
        📊 DATA MERGE DASHBOARD
    </div>
    """, unsafe_allow_html=True)

    st.info("Upload file Excel pada menu MERGE DATA")

# ======================================================
# MERGE DATA
# ======================================================
elif menu == "MERGE DATA":

    st.header("📂 MERGE DATA")

    uploaded_file = st.file_uploader(
        "Upload File Excel",
        type=["xlsx", "xls"]
    )

    if uploaded_file is not None:

        # ==========================
        # BACA FILE
        # ==========================
        df = pd.read_excel(uploaded_file)

        st.subheader("Preview Data")

        st.dataframe(
            df,
            use_container_width=True,
            height=500
        )

        st.divider()

        # ==========================
        # PILIH KOLOM DARI FILE
        # ==========================
        col1, col2 = st.columns(2)

        with col1:
            source_col = st.selectbox(
                "Kolom Dari File",
                df.columns
            )

        template_cols = [
            "Entity",
            "Service",
            "Customer",
            "Afiliasi",
            "Vertical",

            "Revenue Jan",
            "EBIT Jan",
            "EBIT % Jan",

            "Revenue Feb",
            "EBIT Feb",
            "EBIT % Feb",

            "Revenue Mar",
            "EBIT Mar",
            "EBIT % Mar",

            "Revenue Apr",
            "EBIT Apr",
            "EBIT % Apr",

            "Revenue May",
            "EBIT May",
            "EBIT % May",

            "Revenue Jun",
            "EBIT Jun",
            "EBIT % Jun",

            "Revenue Jul",
            "EBIT Jul",
            "EBIT % Jul",

            "Revenue Aug",
            "EBIT Aug",
            "EBIT % Aug",

            "Revenue Sep",
            "EBIT Sep",
            "EBIT % Sep",

            "Revenue Oct",
            "EBIT Oct",
            "EBIT % Oct",

            "Revenue Nov",
            "EBIT Nov",
            "EBIT % Nov",

            "Revenue Dec",
            "EBIT Dec",
            "EBIT % Dec",

            "Revenue YTD",
            "EBIT YTD",
            "EBIT % YTD"
        ]

        with col2:
            target_col = st.selectbox(
                "Masukkan Ke Template",
                template_cols
            )

        # ==========================
        # ADD MAPPING
        # ==========================
        if st.button("➕ ADD TO TEMPLATE"):

            st.session_state.mapping[target_col] = source_col

            st.success(
                f"{source_col} ➜ {target_col}"
            )

        st.divider()

        # ==========================
        # TAMPILKAN MAPPING
        # ==========================
        st.subheader("📋 Mapping Saat Ini")

        if len(st.session_state.mapping) > 0:

            mapping_df = pd.DataFrame(
                list(st.session_state.mapping.items()),
                columns=[
                    "Template Column",
                    "Source Column"
                ]
            )

            st.dataframe(
                mapping_df,
                use_container_width=True
            )

        else:
            st.info("Belum ada mapping.")

        st.divider()

        # ==========================
        # GENERATE TEMPLATE
        # ==========================
        if st.button("🚀 GENERATE TEMPLATE"):

            result = pd.DataFrame()

            for target, source in st.session_state.mapping.items():

                result[target] = df[source]

            st.subheader("Hasil Template")

            st.dataframe(
                result,
                use_container_width=True
            )

            output = BytesIO()

            with pd.ExcelWriter(
                output,
                engine="openpyxl"
            ) as writer:

                result.to_excel(
                    writer,
                    sheet_name="Template",
                    index=False
                )

            st.download_button(
                "📥 Download Template",
                output.getvalue(),
                file_name="Template_Hasil.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # ==========================
        # RESET
        # ==========================
        if st.button("🗑 RESET MAPPING"):

            st.session_state.mapping = {}

            st.rerun()
