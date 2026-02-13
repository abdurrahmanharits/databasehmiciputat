import streamlit as st
import pandas as pd

st.set_page_config(page_title="Kader HMI - Cabang Ciputat", layout="wide")

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

DF = load_data('data/kaders_hmi_ciputat.csv')

st.title("Database Kader HMI — Cabang Ciputat")
st.markdown("Data dasar kader untuk visualisasi dan filter sederhana")

# --- sidebar filters
with st.sidebar:
    st.header("Filter")
    komisariat = st.multiselect("Asal Komisariat", options=sorted(DF['Asal Komisariat'].unique()), default=sorted(DF['Asal Komisariat'].unique()))
    tahun = st.multiselect("Tahun Kaderisasi", options=sorted(DF['Tahun Kaderisasi'].unique()), default=sorted(DF['Tahun Kaderisasi'].unique()))
    kampus = st.multiselect("Kampus", options=sorted(DF['Kampus'].unique()), default=sorted(DF['Kampus'].unique()))
    search = st.text_input("Cari nama / NIK")

# --- apply filters
df = DF[DF['Asal Komisariat'].isin(komisariat) & DF['Tahun Kaderisasi'].isin(tahun) & DF['Kampus'].isin(kampus)]
if search:
    df = df[df['Nama'].str.contains(search, case=False, na=False) | df['NIK'].astype(str).str.contains(search)]

# --- KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Kader", len(df))
col2.metric("Tahun Terbanyak", df['Tahun Kaderisasi'].mode().iat[0] if not df.empty else "-")
col3.metric("Komisariat Terbanyak", df['Asal Komisariat'].mode().iat[0] if not df.empty else "-")

st.markdown("---")

# --- table + download
st.subheader("Tabel Data")
st.dataframe(df.reset_index(drop=True), use_container_width=True)

csv = df.to_csv(index=False).encode('utf-8')
st.download_button(label="Download CSV (filtered)", data=csv, file_name='kaders_hmi_ciputat_filtered.csv', mime='text/csv')

# --- simple charts
st.subheader("Visualisasi")
cols = st.columns(2)
with cols[0]:
    st.bar_chart(df['Tahun Kaderisasi'].value_counts().sort_index())
with cols[1]:
    st.bar_chart(df['Asal Komisariat'].value_counts())

st.caption("Kolom LK 1/2/3 menunjukkan status pelaksanaan latihan kader (Selesai/Belum)")
