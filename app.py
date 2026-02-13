import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kader HMI - Cabang Ciputat", layout="wide")

# set header image (small hero) from `data/background.jpg`
def set_header_image(image_path: str = "data/background.jpg", height_px: int = 220):
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        import base64
        b64 = base64.b64encode(data).decode()
        css = f"""
        <style>
        /* page header (hero) - show full image without cropping */
        .page-header {{
            width: 100%;
            height: {height_px}px;
            background-image: url('data:image/jpg;base64,{b64}');
            background-size: contain; /* ensure whole image is visible */
            background-repeat: no-repeat;
            background-position: center center;
            border-radius: 10px;
            position: relative;
            margin-bottom: 1.2rem;
            overflow: hidden;
        }}
        .page-header .overlay {{
            position: absolute;
            inset: 0;
            background: linear-gradient(to bottom right, rgba(0,0,0,0.15), rgba(0,0,0,0.05));
        }}
        .page-header .title {{
            position: relative;
            color: #ffffff;
            padding: 1.5rem 2rem;
            font-size: 1.5rem;
            font-weight: 700;
            line-height: 1.2;
        }}
        /* set body/main container transparency to 50% so header shows through */
        .stApp .main .block-container {{
            background-color: rgba(255,255,255,0.5); /* 50% transparent */
            padding: 1rem 1.25rem;
            border-radius: 8px;
        }}
        </style>
        <div class="page-header">
          <div class="overlay"></div>
          <div class="title">Database Kader HMI — Cabang Ciputat</div>
        </div>
        """
        st.markdown(css, unsafe_allow_html=True)
    except FileNotFoundError:
        # silently ignore if no image
        pass

set_header_image()

@st.cache_data
def load_data(path_or_buffer):
    # accepts a path or file-like buffer from uploader
    return pd.read_csv(path_or_buffer)

# allow upload; fallback to bundled CSV
uploaded = st.sidebar.file_uploader("Unggah CSV data kader (opsional)", type=["csv"])
DF = load_data(uploaded) if uploaded is not None else load_data('data/kaders_hmi_ciputat.csv')

# komisariat→kampus mapping (must be defined before any validation)
KOMISARIAT_TO_KAMPUS = {
    "Komfakdisa": ["UIN"],
    "Komfaksy": ["UIN"],
    "Komtar": ["UIN"],
    "Komfakda": ["UIN"],
    "Komfastek": ["UIN"],
    "Kafeis": ["UIN"],
    "Kofah": ["UIN"],
    "Komfakdik": ["UIN"],
    "Kompsi": ["UIN"],
    "Kolega": ["STIE GANESHA"],
    "Komipam": ["UNPAM"],
    "Komfaktek": ["UNPAM"],
    "Komfisip": ["UIN"],
    "kotaro": ["STAN"],
    "Komfatma": ["STAI MULA SADRA"],
    "Komici": ["UMJ"],
}

# If an uploaded CSV uses legacy/full names (e.g. "Komisariat Ekonomi"),
# automatically accept and normalize them by adding them to the mapping
# using the campus values present in the uploaded dataset. This keeps
# strict validation while being tolerant to previously-used labels.
def normalize_unknown_komisariat_labels(df):
    if 'Asal Komisariat' not in df.columns or 'Kampus' not in df.columns:
        return df

    unknown = [k for k in df['Asal Komisariat'].dropna().unique() if k not in KOMISARIAT_TO_KAMPUS]
    for kom in unknown:
        campuses = sorted(df.loc[df['Asal Komisariat'] == kom, 'Kampus'].dropna().unique())
        # add to mapping so validation accepts these labels
        KOMISARIAT_TO_KAMPUS[kom] = campuses if len(campuses) > 0 else ["(unknown)"]

    return df

DF = normalize_unknown_komisariat_labels(DF)
KOMISARIAT_OPTIONS = ["Semua"] + list(KOMISARIAT_TO_KAMPUS.keys())
# strict validation for uploaded dataset (reject if invalid)
def validate_strict(df):
    required_cols = {'Asal Komisariat', 'Kampus'}
    if not required_cols.issubset(set(df.columns)):
        st.error("CSV harus memiliki kolom: 'Asal Komisariat' dan 'Kampus'. Perbaiki file dan unggah ulang.")
        st.stop()

    # unknown komisariat values
    komisariat_vals = set(df['Asal Komisariat'].dropna().unique())
    known_komisariat = set(KOMISARIAT_TO_KAMPUS.keys())
    unknown_kom = sorted(list(komisariat_vals - known_komisariat))
    if unknown_kom:
        st.error(f"Ditemukan komisariat tidak dikenal: {', '.join(unknown_kom)}. Perbaiki file dan unggah ulang.")
        st.stop()

    # kampus must match expected mapping for each komisariat
    bad_rows = []
    for i, row in df.iterrows():
        kom = row['Asal Komisariat']
        kamp = row['Kampus']
        expected = KOMISARIAT_TO_KAMPUS.get(kom)
        if expected and kamp not in expected:
            bad_rows.append((i, kom, kamp, expected[0]))
    if bad_rows:
        st.error("Ditemukan baris dengan Kampus yang tidak sesuai untuk Komisariat mereka. Contoh:")
        sample = pd.DataFrame(bad_rows, columns=['_index','Asal Komisariat','Kampus (file)','Kampus (expected)']).drop(columns=['_index'])
        # show sample with numbering starting at 1
        sample_display = sample.reset_index(drop=True).copy()
        sample_display.insert(0, 'No', sample_display.index + 1)
        st.dataframe(sample_display)
        st.error("Perbaiki Kampus pada file CSV agar sesuai mapping komisariat→institusi, lalu unggah ulang.")
        st.stop()

    return df

DF = validate_strict(DF)

st.title("Database Kader HMI — Cabang Ciputat")
st.markdown("Data dasar kader untuk visualisasi, filter, dan ringkasan LK (Latihan Kader)")

# --- komisariat → kampus mapping and sidebar filters (mapping defined earlier)

with st.sidebar:
    st.header("Filter")
    komisariat = st.selectbox("Asal Komisariat", options=KOMISARIAT_OPTIONS, index=0)
    tahun = st.multiselect("Tahun Kaderisasi", options=sorted(DF['Tahun Kaderisasi'].unique()), default=sorted(DF['Tahun Kaderisasi'].unique()))

    # limit campus choices when a specific komisariat is selected
    if komisariat != "Semua":
        kampus_default = KOMISARIAT_TO_KAMPUS.get(komisariat, [])
        kampus = st.multiselect("Kampus", options=sorted(DF['Kampus'].unique()), default=kampus_default)
    else:
        kampus = st.multiselect("Kampus", options=sorted(DF['Kampus'].unique()), default=sorted(DF['Kampus'].unique()))

    lk_filter = st.multiselect("Status LK (pilih untuk filter)", options=["Selesai","Belum"], default=["Selesai","Belum"])
    search = st.text_input("Cari nama / NIK")

# --- apply filters
if komisariat == "Semua":
    df = DF[DF['Tahun Kaderisasi'].isin(tahun) & DF['Kampus'].isin(kampus)]
else:
    df = DF[(DF['Asal Komisariat'] == komisariat) & DF['Tahun Kaderisasi'].isin(tahun) & DF['Kampus'].isin(kampus)]

if search:
    df = df[df['Nama'].str.contains(search, case=False, na=False) | df['NIK'].astype(str).str.contains(search)]
# apply LK filter (rows kept if any LK column matches selected statuses)
if lk_filter and not df.empty:
    lk_mask = df[['LK 1','LK 2','LK 3']].apply(lambda col: col.isin(lk_filter))
    df = df[lk_mask.any(axis=1)]

# --- KPIs + LK summary
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Kader", len(df))
col2.metric("Tahun Terbanyak", df['Tahun Kaderisasi'].mode().iat[0] if not df.empty else "-")
col3.metric("Komisariat Terbanyak", df['Asal Komisariat'].mode().iat[0] if not df.empty else "-")
# LK completion rates
def pct_done(col):
    if df.empty:
        return 0
    return int(100 * (df[col] == 'Selesai').sum() / len(df))
col4.metric("Rata-rata LK1/2/3 selesai (%)", f"{pct_done('LK 1')}% / {pct_done('LK 2')}% / {pct_done('LK 3')}%")

st.markdown("---")

# --- table + download + quick stats
st.subheader("Tabel Data")
# show numbering from 1 in the displayed table (do not modify the downloadable CSV)
df_display = df.reset_index(drop=True).copy()
df_display.insert(0, 'No', df_display.index + 1)
st.dataframe(df_display, use_container_width=True)

# prepare downloadable CSV with 1-based numbering
csv_df = df.reset_index(drop=True).copy()
csv_df.insert(0, 'No', csv_df.index + 1)
csv = csv_df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download CSV (filtered)", data=csv, file_name='kaders_hmi_ciputat_filtered.csv', mime='text/csv')

# quick aggregates
st.subheader("Ringkasan LK")
lk_counts = pd.DataFrame({
    'LK': ['LK 1','LK 2','LK 3'],
    'Selesai': [ (df['LK 1']=='Selesai').sum(), (df['LK 2']=='Selesai').sum(), (df['LK 3']=='Selesai').sum() ],
    'Belum': [ (df['LK 1']=='Belum').sum(), (df['LK 2']=='Belum').sum(), (df['LK 3']=='Belum').sum() ]
})
# add numbering starting from 1
lk_counts.insert(0, 'No', range(1, len(lk_counts) + 1))
st.table(lk_counts)

# --- simple charts
st.subheader("Visualisasi")
cols = st.columns(2)
with cols[0]:
    st.bar_chart(df['Tahun Kaderisasi'].value_counts().sort_index())
with cols[1]:
    st.bar_chart(df['Asal Komisariat'].value_counts())

st.caption("Kolom LK 1/2/3 menunjukkan status pelaksanaan latihan kader (Selesai/Belum). Gunakan uploader untuk mengganti dataset sementara.")
