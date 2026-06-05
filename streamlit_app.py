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

        # =====================================
        # SCAN KOLOM SEMUA FILE
        # =====================================

        all_columns = set()
        file_data = {}

        for file in uploaded_files:

            df = pd.read_excel(file)

            file_data[file.name] = df

            all_columns.update(df.columns.tolist())

        all_columns = sorted(
            [str(col) for col in all_columns]
        )

        st.markdown("## ⚙️ PILIH KOLOM")

        selected_columns = st.multiselect(
            "Pilih kolom yang ingin diambil",
            options=all_columns
        )

        st.markdown("## ➕ KOLOM TAMBAHAN")

        add_entity = st.checkbox(
            "Tambahkan ENTITY",
            value=True
        )

        add_service = st.checkbox(
            "Tambahkan SERVICE",
            value=True
        )

        add_afiliasi = st.checkbox(
            "PNL Afiliasi",
            value=True
        )

        add_vertical = st.checkbox(
            "Vertical 2",
            value=True
        )

        add_existing = st.checkbox(
            "Existing/ Whitesheet",
            value=True
        )

        # =====================================
        # GENERATE
        # =====================================

        if st.button("🚀 GENERATE SUMMARY"):

            final_df = pd.DataFrame()

            for filename, df in file_data.items():

                temp = pd.DataFrame()

                # ==========================
                # ENTITY
                # ==========================

                entity = (
                    filename
                    .split(" ")[0]
                    .upper()
                )

                if add_entity:

                    temp["ENTITY"] = entity

                # ==========================
                # KOLOM PILIHAN USER
                # ==========================

                for col in selected_columns:

                    if col in df.columns:

                        temp[col] = df[col]

                # ==========================
                # SERVICE
                # ==========================

                if add_service:

                    service_col = None

                    for col in df.columns:

                        if (
                            "SERVICE"
                            in str(col).upper()
                        ):

                            service_col = col
                            break

                    if service_col:

                        temp["SERVICE"] = (
                            df[service_col]
                        )

                    else:

                        temp["SERVICE"] = ""

                # ==========================
                # KOLOM KOSONG
                # ==========================

                if add_afiliasi:

                    temp["PNL Afiliasi"] = ""

                if add_vertical:

                    temp["Vertical 2"] = ""

                if add_existing:

                    temp[
                        "Existing/ Whitesheet"
                    ] = ""

                final_df = pd.concat(
                    [
                        final_df,
                        temp
                    ],
                    ignore_index=True
                )

            # =====================================
            # SUMMARY
            # =====================================

            st.markdown("## 📊 SUMMARY")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Total File",
                len(uploaded_files)
            )

            c2.metric(
                "Total Row",
                len(final_df)
            )

            c3.metric(
                "Total Column",
                len(final_df.columns)
            )

            # =====================================
            # PREVIEW
            # =====================================

            st.markdown("## 📋 PREVIEW")

            st.dataframe(
                final_df,
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

                final_df.to_excel(
                    writer,
                    index=False
                )

            st.download_button(
                label="⬇️ Download Summary",
                data=output.getvalue(),
                file_name="SUMMARY_ALL_PNL.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    else:

        st.info(
            "Silakan upload file terlebih dahulu."
        )
