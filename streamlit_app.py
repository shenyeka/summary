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
        MERGE DATA SUMMARY
    </div>
    """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "Upload File PNL",
        type=["xlsx"],
        accept_multiple_files=True
    )

    if uploaded_files:

        # =====================================
        # SCAN HEADER FILE PERTAMA
        # =====================================

        raw_first = pd.read_excel(
            uploaded_files[0],
            header=None
        )

        month_row = raw_first.iloc[5]
        metric_row = raw_first.iloc[6]

        available_columns = {}

        for col in range(len(raw_first.columns)):

            month = str(month_row[col]).strip()
            metric = str(metric_row[col]).strip()

            if metric.upper() in [
                "REVENUE",
                "EBIT",
                "EBIT %"
            ]:

                header_name = f"{metric} {month}"

                available_columns[
                    header_name
                ] = col

        st.markdown("## 📊 PILIH KOLOM")

        selected_columns = st.multiselect(
            "Kolom yang akan diambil",
            list(available_columns.keys())
        )

        if st.button("🚀 GENERATE SUMMARY"):

            final_result = []

            # =====================================
            # LOOP SEMUA FILE
            # =====================================

            for file in uploaded_files:

                entity = (
                    file.name
                    .split(" ")[0]
                    .upper()
                )

                raw = pd.read_excel(
                    file,
                    header=None
                )

                # SERVICE merged cell
                raw[3] = raw[3].ffill()

                month_row = raw.iloc[5]
                metric_row = raw.iloc[6]

                file_mapping = {}

                for col in range(
                    len(raw.columns)
                ):

                    month = str(
                        month_row[col]
                    ).strip()

                    metric = str(
                        metric_row[col]
                    ).strip()

                    if metric.upper() in [
                        "REVENUE",
                        "EBIT",
                        "EBIT %"
                    ]:

                        file_mapping[
                            f"{metric} {month}"
                        ] = col

                # =====================================
                # LOOP CUSTOMER
                # =====================================

                for r in range(
                    7,
                    len(raw)
                ):

                    service = str(
                        raw.iloc[r,3]
                    ).strip()

                    customer = str(
                        raw.iloc[r,4]
                    ).strip()

                    row_text = (
                        service + " " + customer
                    ).upper()

                    # skip kosong
                    if (
                        customer == ""
                        or customer.upper() == "NAN"
                    ):
                        continue

                    # skip total
                    if "TOTAL" in row_text:
                        continue

                    temp = {

                        "ENTITY":
                        entity,

                        "SERVICE":
                        service,

                        "CUSTOMER":
                        customer,

                        "PNL Afiliasi":
                        "",

                        "Vertical 2":
                        "",

                        "Existing/Whitesheet":
                        ""

                    }

                    # ==========================
                    # KOLOM YANG DIPILIH USER
                    # ==========================

                    for col_name in selected_columns:

                        if (
                            col_name
                            in file_mapping
                        ):

                            excel_col = (
                                file_mapping[
                                    col_name
                                ]
                            )

                            temp[
                                col_name
                            ] = raw.iloc[
                                r,
                                excel_col
                            ]

                    final_result.append(
                        temp
                    )

            # =====================================
            # DATAFRAME AKHIR
            # =====================================

            df_final = pd.DataFrame(
                final_result
            )

            st.markdown(
                "## 📋 SUMMARY RESULT"
            )

            st.dataframe(
                df_final,
                use_container_width=True
            )

            # =====================================
            # DOWNLOAD
            # =====================================

            output = io.BytesIO()

            with pd.ExcelWriter(
                output,
                engine="openpyxl"
            ) as writer:

                df_final.to_excel(
                    writer,
                    index=False
                )

            st.download_button(
                "⬇️ Download Summary",
                output.getvalue(),
                "SUMMARY_ALL_PNL.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    else:

        st.info(
            "Upload file terlebih dahulu."
        )
