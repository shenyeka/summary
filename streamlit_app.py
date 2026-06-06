import streamlit as st
import pandas as pd
import io

pip install streamlit-aggrid

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

    import pandas as pd
    from io import BytesIO

    st.header("📂 Merge Data ke Template")

    uploaded_file = st.file_uploader(
        "Upload File Excel",
        type=["xlsx", "xls"]
    )

    if uploaded_file is not None:

        # =========================
        # BACA FILE
        # =========================
        df = pd.read_excel(uploaded_file)

        st.subheader("Preview Data")

        st.dataframe(
            df,
            use_container_width=True,
            height=500
        )

        st.divider()

        # =========================
        # TEMPLATE STANDAR
        # =========================
        template_columns = [

            "Ignore",

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

        st.subheader("🛠 Mapping Kolom")

        mapping = {}

        for col in df.columns:

            mapping[col] = st.selectbox(
                f"{col}",
                template_columns,
                key=f"map_{col}"
            )

        st.divider()

        # =========================
        # GENERATE TEMPLATE
        # =========================
        if st.button("🚀 Generate Template"):

            result = pd.DataFrame()

            used_targets = []

            for source_col, target_col in mapping.items():

                if target_col != "Ignore":

                    if target_col in used_targets:

                        st.error(
                            f"Kolom '{target_col}' dipilih lebih dari sekali."
                        )
                        st.stop()

                    result[target_col] = df[source_col]
                    used_targets.append(target_col)

            st.success("Template berhasil dibuat")

            st.subheader("Hasil Template")

            st.dataframe(
                result,
                use_container_width=True
            )

            # =========================
            # DOWNLOAD
            # =========================
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
                label="📥 Download Template",
                data=output.getvalue(),
                file_name="Template_Hasil.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
