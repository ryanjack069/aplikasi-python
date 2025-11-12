import streamlit as st
import requests
import pandas as pd
from io import StringIO
import json

# --- PENTING: st.set_page_config HARUS DI SINI! ---
st.set_page_config(layout="centered", title="Pencarian dan Input Data Infaq Arrahman")
# --------------------------------------------------

# --- Kredensial dan Konstanta ---
# SUMBER DATA UTAMA (Database Transaksi)
WORKSHEET_NAME_DB = "DB BAYAR" 
WORKSHEET_NAME_INPUT = "PEMBAYARAN INFAQ" # Asumsi worksheet tujuan input adalah ini

# --- 1. FUNGSI PENANGANAN ZOHO API ---

@st.cache_data(ttl=3500) 
def get_access_token():
    # ... (Fungsi ini tetap sama)
    try:
        secrets = st.secrets["zoho_api"]
        url = "https://accounts.zoho.com/oauth/v2/token"
        payload = {
            'client_id': secrets["client_id"],
            'client_secret': secrets["client_secret"],
            'refresh_token': secrets["refresh_token"],
            'grant_type': 'refresh_token'
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()
        data = response.json()
        if 'access_token' in data:
            return data['access_token']
        else:
            st.error("Gagal mendapatkan Access Token baru. Respons API: " + str(data))
            return None
    except Exception as e:
        st.error(f"Error saat mengambil token. Cek Streamlit Secrets. Error: {e}")
        return None

@st.cache_data(ttl=600) 
def fetch_zoho_data(workbook_id, worksheet_name):
    """Mengambil data dari Zoho Sheet sebagai Pandas DataFrame dari WORKSHEET_NAME_DB."""
    access_token = get_access_token()
    if not access_token:
        return pd.DataFrame()

    api_url = f"https://sheet.zoho.com/api/v2/workbooks/{workbook_id}/worksheets/{worksheet_name}/rows"
    
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Accept": "text/csv" 
    }

    try:
        data_response = requests.get(api_url, headers=headers)
        data_response.raise_for_status() 
        
        csv_data = StringIO(data_response.text)
        # Asumsi baris pertama di DB BAYAR adalah header
        df = pd.read_csv(csv_data) 
        
        return df

    except requests.exceptions.RequestException as e:
        st.error(f"Gagal mengambil data dari Zoho Sheet: {e}")
        st.error(f"URL yang dicoba: {api_url}")
        try:
            st.json(json.loads(data_response.text))
        except:
             st.info("Pastikan nama Worksheet DB BAYAR dan Workbook ID sudah benar, serta izin berbagi sudah diberikan.")
        return pd.DataFrame()

# --- 2. FUNGSI INPUT DATA KE ZOHO SHEET (Placeholder) ---
# ... (Fungsi ini tetap sama untuk saat ini)
def input_data_to_zoho(workbook_id, target_worksheet_name, data_to_insert):
    st.warning("Fungsi Input Data saat ini dinonaktifkan.")
    return False, "Input dinonaktifkan"


# --- 3. LAYOUT APLIKASI STREAMLIT UTAMA ---

def app_layout(df):
    
    st.title("💰 Pencarian dan Input Data Infaq Arrahman")
    st.markdown("---")

    # --- Ambil nilai unik untuk dropdown dari DataFrame (DB BAYAR) ---
    try:
        # PENTING: Asumsi kolom index (0, 1, 2) di DB BAYAR adalah NAMA, BULAN, JUMAT KE
        nama_options = df.iloc[:, 0].dropna().unique().tolist()
        bulan_options = df.iloc[:, 1].dropna().unique().tolist()
        jumat_options = df.iloc[:, 2].dropna().unique().tolist()
    except IndexError:
        st.warning("Gagal mengidentifikasi kolom NAMA, BULAN, JUMAT KE di DB BAYAR.")
        # Fallback values
        nama_options = ["SUMARNO", "SANTUN", "LAINNYA"] 
        bulan_options = ["JANUARI", "FEBRUARI", "AGUSTUS", "OKTOBER"]
        jumat_options = [1, 2, 3, 4, 5]


    # --- Bagian A: PENCARIAN TANGGUNGAN INFAQ ---
    st.header("PENCARIAN TANGGUNGAN INFAQ")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_nama_cari = st.selectbox("NAMA", options=nama_options, key="nama_cari")
    with col2:
        selected_bulan_cari = st.selectbox("BULAN", options=bulan_options, key="bulan_cari")
    with col3:
        selected_jumat_cari = st.selectbox("JUMAT KE", options=jumat_options, key="jumat_cari")
    
    # --- Logika Pencarian Data (Filter DB BAYAR) ---
    
    tanggungan_val = "Data Tidak Ditemukan"
    total_setahun_val = "-"
    
    try:
        # Filter DataFrame DB BAYAR
        filtered_data = df[
            (df.iloc[:, 0].astype(str) == str(selected_nama_cari)) &
            (df.iloc[:, 1].astype(str) == str(selected_bulan_cari)) &
            (df.iloc[:, 2].astype(str) == str(selected_jumat_cari))
        ]
        
        if not filtered_data.empty:
            # Asumsi Tanggungan di Kolom ke-4 (Index 3) dan Total Setahun di Kolom ke-5 (Index 4) di DB BAYAR
            # Catatan: Ini adalah asumsi. Anda mungkin perlu menyesuaikan index kolom ini!
            tanggungan_val = filtered_data.iloc[0, 3] 
            total_setahun_val = filtered_data.iloc[0, 4]
        
    except Exception as e:
        st.error(f"Error saat memfilter data: {e}")
        
    # Tampilkan Hasil 
    st.markdown("---")
    with st.container(border=True):
        st.subheader("HASIL PENCARIAN")
        st.markdown(f"**TANGGUNGAN:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`{tanggungan_val}`")
        st.markdown(f"**TOTAL SETAHUN:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`{total_setahun_val}`")
    st.markdown("---")

    # --- Bagian B: PEMBAYARAN DAN INPUT DATA INFAQ ---
    st.header("PEMBAYARAN DAN INPUT DATA INFAQ")
    
    with st.form("input_infaq_form", clear_on_submit=True):
        
        col4, col5 = st.columns(2)
        
        with col4:
            nama_input = st.selectbox("NAMA", options=nama_options, key="nama_input")
            bulan_input = st.selectbox("BULAN", options=bulan_options, key="bulan_input")
            jumlah_bayar = st.number_input("JUMLAH BAYAR (Opsional)", min_value=0, value=0)
            
        with col5:
            jumat_input = st.selectbox("JUMAT KE", options=jumat_options, key="jumat_input")
            jumlah_infaq = st.number_input("JUMLAH INFAQ", min_value=0, value=0)
            st.text_input("TANGGUNGAN (dari hasil pencarian)", value=str(tanggungan_val), disabled=True) 
            input_data = st.number_input("INPUT DATA (Angka yang akan diinput)", min_value=0, value=0)

        st.markdown("")
        submitted = st.form_submit_button("INPUT")
        
        if submitted:
            # Input data akan diarahkan ke worksheet lain (misal: 'PEMBAYARAN INFAQ')
            success, message = input_data_to_zoho(st.secrets["zoho_api"]["workbook_id"], WORKSHEET_NAME_INPUT, None) 
            if success:
                st.success(message)
            else:
                st.error(message)


def main():
    workbook_id = st.secrets["zoho_api"]["workbook_id"] 
    
    # Mengambil data dari DB BAYAR
    data_df = fetch_zoho_data(workbook_id, WORKSHEET_NAME_DB)
    
    if not data_df.empty:
        st.info(f"Data Worksheet '{WORKSHEET_NAME_DB}' berhasil dimuat. ({len(data_df)} baris, {len(data_df.columns)} kolom)")
        app_layout(data_df)
    else:
        st.error("Gagal memuat data dari Zoho Sheet. Pastikan izin berbagi sudah diberikan ke Client ID aplikasi Anda.")

if __name__ == "__main__":
    main()
