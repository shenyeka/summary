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
        "Upload File Summary",
        type=["xlsx"],
        accept_multiple_files=True
    )

    if uploaded_files:

        try:

            all_data = []

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

                header_row = 6
                data_start = 7

                headers = raw.iloc[header_row]

                # =====================
                # Cari kolom utama
                # =====================

                service_col = None
                customer_col = None

                for col in range(len(headers)):

                    value = str(
                        headers[col]
                    ).upper()

                    if "SERVICE" in value:

                        service_col = col

                    if "CUSTOMER" in value:

                        customer_col = col

                if customer_col is None:
                    continue

                # =====================
                # Build Data
                # =====================

                for idx in range(
                    data_start,
                    len(raw)
                ):

                    row = raw.iloc[idx]

                    customer = row[
                        customer_col
                    ]

                    if pd.isna(customer):
                        continue

                    result = {

                        "ENTITY": entity,

                        "SERVICE":
                        row[service_col]
                        if service_col is not None
                        else "",

                        "CUSTOMER":
                        customer,

                        "PNL Afiliasi": "",

                        "Vertical 2": "",

                        "Existing/ Whitesheet": ""

                    }

                    # =====================
                    # Ambil semua metric
                    # =====================

                    for col in range(
                        len(raw.columns)
                    ):

                        metric = str(
                            headers[col]
                        ).upper()

                        value = row[col]

                        if (
                            metric
                            not in
                            [
                                "REVENUE",
                                "EBIT",
                                "EBIT %"
                            ]
                        ):
                            continue

                        month = raw.iloc[5, col]

                        if pd.isna(month):
                            continue

                        # =====================
                        # Nama bulan
                        # =====================

                        if (
                            str(month)
                            .upper()
                            .strip()
                            == "YTD"
                        ):

                            month_name = "YTD"

                        else:

                            try:

                                month_name = pd.to_datetime(
                                    month
                                ).strftime(
                                    "%b-%y"
                                ).upper()

                            except:

                                month_name = (
                                    str(month)
                                    .upper()
                                )

                        col_name = (
                            f"{metric}_{month_name}"
                        )

                        result[
                            col_name
                        ] = value

                    all_data.append(
                        result
                    )

            # =====================
            # MERGE
            # =====================

            df_final = pd.DataFrame(
                all_data
            )

            st.markdown(
                "## 📊 SUMMARY"
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Total Entity",
                df_final[
                    "ENTITY"
                ].nunique()
            )

            c2.metric(
                "Total Customer",
                len(df_final)
            )

            c3.metric(
                "Total Column",
                len(df_final.columns)
            )

            st.markdown(
                "## 📋 PREVIEW"
            )

            st.dataframe(
                df_final,
                use_container_width=True
            )

            # =====================
            # DOWNLOAD
            # =====================

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
                label="⬇️ Download Summary",
                data=output.getvalue(),
                file_name="SUMMARY_ALL_PNL.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:

            st.error(
                f"Error : {e}"
            )

    else:

        st.info(
            "Upload file PUJA, PSR, PFU, PIR, dan MLD terlebih dahulu."
        )
