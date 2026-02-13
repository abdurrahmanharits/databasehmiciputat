import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kader HMI - Cabang Ciputat", layout="wide")

@st.cache_data
def load_data(path_or_buffer):
    # accepts a path or file-like buffer from uploader
    return pd.read_csv(path_or_buffer)

# allow upload; fallback to bundled CSV
uploaded = st.sidebar.file_uploader("Unggah CSV data kader (opsional)", type=["csv"])
DF = load_data(uploaded) if uploaded is not None else load_data('data/kaders_hmi_ciputat.csv')

st.title("Database Kader HMI — Cabang Ciputat")
st.markdown("Data dasar kader untuk visualisasi, filter, dan ringkasan LK (Latihan Kader)")

# --- sidebar filters
KOMISARIAT_OPTIONS = [
    "Semua",
    "Komfakdisa",
    "Komfaksy",
    "Komtar",
    "Komfakda",
    "Komfastek",
    "Kafeis",
    "Kofah",
    "Komfakdik",
    "Kompsi",
    "Kolega",
    "Komipam",
    "Komfaktek",
    "Komfisip",
    "kotaro",
    "Komfatma",
    "Komici",
]
with st.sidebar:
    st.header("Filter")
    komisariat = st.selectbox("Asal Komisariat", options=KOMISARIAT_OPTIONS, index=0)
    tahun = st.multiselect("Tahun Kaderisasi", options=sorted(DF['Tahun Kaderisasi'].unique()), default=sorted(DF['Tahun Kaderisasi'].unique()))
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
st.dataframe(df.reset_index(drop=True), use_container_width=True)

csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download CSV (filtered)", data=csv, file_name='kaders_hmi_ciputat_filtered.csv', mime='text/csv')

# quick aggregates
st.subheader("Ringkasan LK")
lk_counts = pd.DataFrame({
    'LK': ['LK 1','LK 2','LK 3'],
    'Selesai': [ (df['LK 1']=='Selesai').sum(), (df['LK 2']=='Selesai').sum(), (df['LK 3']=='Selesai').sum() ],
    'Belum': [ (df['LK 1']=='Belum').sum(), (df['LK 2']=='Belum').sum(), (df['LK 3']=='Belum').sum() ]
})
st.table(lk_counts)

# --- simple charts
st.subheader("Visualisasi")
cols = st.columns(2)
with cols[0]:
    st.bar_chart(df['Tahun Kaderisasi'].value_counts().sort_index())
with cols[1]:
    st.bar_chart(df['Asal Komisariat'].value_counts())

st.caption("Kolom LK 1/2/3 menunjukkan status pelaksanaan latihan kader (Selesai/Belum). Gunakan uploader untuk mengganti dataset sementara.")
