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
elif menu == "MERGE DATA":

    import pandas as pd
    import streamlit as st
    from io import BytesIO
    from st_aggrid import AgGrid, GridOptionsBuilder

    st.header("MERGE DATA")

    uploaded_file = st.file_uploader(
        "Upload Excel",
        type=["xlsx", "xls"]
    )

    if uploaded_file is not None:

        # ==========================
        # BACA FILE
        # ==========================
        df = pd.read_excel(uploaded_file)

        st.subheader("Preview Data")

        gb = GridOptionsBuilder.from_dataframe(df)

        gb.configure_selection(
            selection_mode="single",
            use_checkbox=False
        )

        grid_response = AgGrid(
            df,
            gridOptions=gb.build(),
            height=500,
            fit_columns_on_grid_load=False
        )

        # ==========================
        # INISIALISASI SESSION
        # ==========================
        if "mapping" not in st.session_state:
            st.session_state.mapping = {}

        st.divider()

        st.subheader("Pilih Kolom Dari File")

        source_col = st.selectbox(
            "Kolom File",
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

        target_col = st.selectbox(
            "Masukkan Ke Kolom Template",
            template_cols
        )

        if st.button("➕ ADD TO TEMPLATE"):

            st.session_state.mapping[target_col] = source_col

            st.success(
                f"{source_col} ➜ {target_col}"
            )

        st.divider()

        st.subheader("Mapping Saat Ini")

        if st.session_state.mapping:

            mapping_df = pd.DataFrame(
                [
                    [k, v]
                    for k, v in st.session_state.mapping.items()
                ],
                columns=[
                    "Template Column",
                    "Source Column"
                ]
            )

            st.dataframe(
                mapping_df,
                use_container_width=True
            )

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
                    index=False,
                    sheet_name="Template"
                )

            st.download_button(
                "📥 Download Template",
                output.getvalue(),
                file_name="Template_Hasil.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # ==========================
        # RESET MAPPING
        # ==========================
        if st.button("🗑 Reset Mapping"):

            st.session_state.mapping = {}

            st.rerun()
