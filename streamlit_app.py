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
        "Upload 5 File PNL",
        type=["xlsx"],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.markdown("### 📅 Pilih Bulan")

        selected_months = st.multiselect(
            "",
            [
                "Jan-26",
                "Feb-26",
                "Mar-26",
                "Apr-26",
                "May-26",
                "Jun-26",
                "Jul-26",
                "Aug-26",
                "Sep-26",
                "Oct-26",
                "Nov-26",
                "Dec-26",
                "YTD"
            ],
            default=[
                "Jan-26",
                "Feb-26",
                "Mar-26",
                "Apr-26"
            ]
        )

        st.markdown("### 📊 Pilih Metric")

        selected_metrics = st.multiselect(
            "",
            [
                "REVENUE",
                "EBIT",
                "EBIT %"
            ],
            default=[
                "REVENUE",
                "EBIT",
                "EBIT %"
            ]
        )

        if st.button("🚀 GENERATE SUMMARY"):

            final_data = []

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

                service_header = raw.iloc[4]
                month_header = raw.iloc[5]
                metric_header = raw.iloc[6]

                for row_idx in range(7, len(raw)):

                    row = raw.iloc[row_idx]

                    service = str(row[2]).strip()
                    customer = str(row[3]).strip()

                    if (
                        customer == ""
                        or customer.upper() == "NAN"
                        or "TOTAL" in customer.upper()
                    ):
                        continue

                    result = {

                        "ENTITY": entity,
                        "SERVICE": service,
                        "CUSTOMER": customer,
                        "PNL Afiliasi": "",
                        "Vertical 2": "",
                        "Existing/ Whitesheet": ""

                    }

                    for col in range(4, len(raw.columns)):

                        month = str(
                            month_header[col]
                        ).strip()

                        metric = str(
                            metric_header[col]
                        ).upper().strip()

                        if (
                            month
                            not in selected_months
                        ):
                            continue

                        if (
                            metric
                            not in selected_metrics
                        ):
                            continue

                        new_col = (
                            f"{metric}_{month}"
                        )

                        result[new_col] = row[col]

                    final_data.append(
                        result
                    )

            df_final = pd.DataFrame(
                final_data
            )

            st.markdown(
                "## 📊 SUMMARY RESULT"
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Total Entity",
                df_final["ENTITY"].nunique()
            )

            c2.metric(
                "Total Customer",
                len(df_final)
            )

            c3.metric(
                "Total Column",
                len(df_final.columns)
            )

            st.dataframe(
                df_final,
                use_container_width=True
            )

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
