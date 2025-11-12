import streamlit as st
import requests
import pandas as pd
from io import StringIO
import json

# --- Kredensial dan Konstanta ---
# Pastikan Anda memasukkan ini di Streamlit Cloud Secrets!
WORKBOOK_ID = "urvny1df90546b51d4b899a0540380cabd33e"
WORKSHEET_NAME = "CAR! DATA"

st.set_page_config(layout="centered")

# --- 1. FUNGSI PENANGANAN ZOHO API ---

@st.cache_data(ttl=3500) 
def get_access_token():
    """Menggunakan Refresh Token untuk mendapatkan Access Token baru dari Zoho."""
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
            st.error("Gagal mendapatkan Access Token baru. Cek Refresh Token.")
            return None
    except Exception as e:
        # Jika kode dijalankan secara lokal tanpa secrets.toml, ini akan muncul.
        st.error("Error: Tidak dapat mengakses Zoho Secrets. Pastikan file secrets.toml atau Streamlit Secrets sudah terisi.")
        return None

@st.cache_data(ttl=600) 
def fetch_zoho_data(workbook_id, worksheet_name):
    """Mengambil data dari Zoho Sheet sebagai Pandas DataFrame (CSV format)."""
    access_token = get_access_token()
    if not access_token:
        return pd.DataFrame()

    # Endpoint untuk mengambil data sebagai CSV
    api_url = f"https://sheet.zoho.com/api/v2/{workbook_id}/data/{worksheet_name}"
    
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Accept": "text/csv" # Minta respons dalam format CSV
    }

    try:
        data_response = requests.get(api_url, headers=headers)
        data_response.raise_for_status()
        
        # Baca data CSV langsung ke Pandas DataFrame
        csv_data = StringIO(data_response.text)
        # Gunakan header=None karena data yang diambil adalah nilai-nilai sel,
        # dan kita asumsikan struktur datanya sudah diketahui.
        # Anda mungkin perlu menyesuaikan pemetaan kolom di bawah!
        df = pd.read_csv(csv_data, header=None) 

        # Asumsi kolom (sesuaikan dengan Worksheet "CARI DATA" Anda!):
        # Kolom 0: NAMA, Kolom 1: BULAN, Kolom 2: JUMAT KE, Kolom 3: TANGGUNGAN, dst.
        
        # NOTE: Jika data Anda memiliki header di baris pertama, gunakan header=0 di pd.read_csv
        # dan ubah index kolom di bawah. 
        # Karena kita berasumsi data sheet di "CARI DATA" berisi output yang Anda inginkan:
        
        # Kita perlu mengasumsikan kolom di sheet yang digunakan untuk PENCARIAN
        
        return df

    except requests.exceptions.RequestException as e:
        st.error(f"Gagal mengambil data dari Zoho Sheet: {e}")
        st.json(data_response.text) # Tampilkan respons error API jika ada
        return pd.DataFrame()

# --- 2. FUNGSI INPUT DATA KE ZOHO SHEET (Opsional tapi penting) ---

def input_data_to_zoho(workbook_id, worksheet_name, data_to_insert):
    """Mengirim data baru ke Zoho Sheet menggunakan API."""
    access_token = get_access_token()
    if not access_token:
        return False, "Gagal mendapatkan Access Token."

    url = f"https://sheet.zoho.com/api/v2/workbooks/{workbook_id}/worksheets/{worksheet_name}/rows"
    
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}",
        "Content-Type": "application/json"
    }

    # Format data yang akan diinsert (ini contoh, harus sesuai dengan kolom sheet Anda)
    payload = {
        "data": [data_to_insert], 
        "skip_row_header": True
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        
        if response.status_code == 200:
            return True, "Data berhasil diinput ke Zoho Sheet!"
        else:
            return False, f"Gagal input data. Status: {response.status_code}"

    except requests.exceptions.RequestException as e:
        return False, f"Error saat input data API: {e}"


# --- 3. LAYOUT APLIKASI STREAMLIT UTAMA ---

def app_layout(df):
    
    st.title("💰 Pencarian dan Input Data Infaq Arrahman")
    st.markdown("---")

    # --- Bagian A: PENCARIAN TANGGUNGAN INFAQ ---
    
    # Asumsi data di worksheet CARI DATA Anda memiliki 3 kolom pertama sebagai input (Nama, Bulan, Jumat Ke)
    # dan sisanya sebagai output (Tanggungan, Total Setahun, dll).
    
    # Ambil nilai unik untuk dropdown (Asumsi: di sheet CARI DATA sudah ada semua pilihan)
    # Anda harus mengasumsikan data kolom yang berisi NAMA, BULAN, JUMAT KE
    
    # Karena kita tidak tahu persis struktur kolom di sheet CARI DATA, kita akan membuat dropdown dummy
    # yang nilainya *mungkin* ada di worksheet Anda untuk pencarian (dropdown filter).
    
    # *Anda harus mengganti list ini dengan nilai unik dari kolom NAMA, BULAN, JUMAT KE di sheet Anda.*
    nama_options = ["SUMARNO", "SANTUN", "Nama Lain 1", "Nama Lain 2"] 
    bulan_options = ["JANUARI", "FEBRUARI", "AGUSTUS", "OKTOBER"]
    jumat_options = [1, 2, 3, 4, 5]

    st.header("PENCARIAN TANGGUNGAN INFAQ")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_nama_cari = st.selectbox("NAMA", options=nama_options, key="nama_cari")
    with col2:
        selected_bulan_cari = st.selectbox("BULAN", options=bulan_options, key="bulan_cari")
    with col3:
        selected_jumat_cari = st.selectbox("JUMAT KE", options=jumat_options, key="jumat_cari")
    
    st.markdown("---")

    # --- Simulasi Pencarian Data ---
    
    # Dalam aplikasi nyata, Anda akan memfilter 'df' berdasarkan selected_nama_cari, dll.
    # Karena data yang Anda berikan adalah screenshot, kita akan meniru hasilnya.
    # Anda perlu mengimplementasikan logika filtering Pandas di sini:
    # filtered_data = df[(df['NAMA'] == selected_nama_cari) & (df['BULAN'] == selected_bulan_cari) & (df['JUMAT KE'] == selected_jumat_cari)]
    
    # KARENA KITA TIDAK TAHU STRUKTUR KOLOM: kita tampilkan data simulasi
    tanggungan_val = "LUNAS" if selected_nama_cari == "SUMARNO" else "Rp -87000"
    total_setahun_val = "Rp -20000" if selected_nama_cari == "SUMARNO" else "Rp 1500000"

    # Gunakan layout kotak menarik seperti gambar
    st.markdown(f"**TANGGUNGAN:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`{tanggungan_val}`")
    st.markdown(f"**TOTAL SETAHUN:** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`{total_setahun_val}`")
    
    st.markdown("---")

    # --- Bagian B: PEMBAYARAN DAN INPUT DATA INFAQ ---

    st.header("PEMBAYARAN DAN INPUT DATA INFAQ")
    
    # Form untuk Input Data
    with st.form("input_infaq_form", clear_on_submit=True):
        
        col4, col5 = st.columns(2)
        
        with col4:
            nama_input = st.selectbox("NAMA", options=nama_options, key="nama_input", help="Pilih nama yang akan menginput infaq.")
            bulan_input = st.selectbox("BULAN", options=bulan_options, key="bulan_input")
            jumlah_bayar = st.number_input("JUMLAH BAYAR (Opsional)", min_value=0, value=0)
            
        with col5:
            jumat_input = st.selectbox("JUMAT KE", options=jumat_options, key="jumat_input")
            jumlah_infaq = st.number_input("JUMLAH INFAQ", min_value=0, value=0)
            tanggungan_input = st.text_input("TANGGUNGAN (dari hasil pencarian)", value=tanggungan_val, disabled=True)
            input_data = st.number_input("INPUT DATA (Angka yang akan diinput)", min_value=0, value=0)

        st.markdown("")
        submitted = st.form_submit_button("INPUT")
        
        if submitted:
            st.warning("Fungsi input belum diaktifkan. Anda harus mengetahui urutan kolom yang tepat di Sheet Tujuan.")
            # Data yang akan diinput ke Sheet Tujuan Anda (misalnya: Sheet 'Transaksi')
            # data_payload = {
            #     "Nama": nama_input,
            #     "Bulan": bulan_input,
            #     "Jumat Ke": jumat_input,
            #     "Jumlah Bayar": jumlah_bayar,
            #     "Jumlah Infaq": jumlah_infaq,
            #     "Tanggungan": tanggungan_input,
            #     "Input Data": input_data
            # }
            
            # success, message = input_data_to_zoho(WORKBOOK_ID, "NAMA_SHEET_TUJUAN", data_payload) 
            # if success:
            #     st.success(message)
            # else:
            #     st.error(message)


def main():
    # Mengambil ID Workbook dari konstanta di atas
    workbook_id = WORKBOOK_ID 
    worksheet_name = WORKSHEET_NAME
    
    # Ambil data dari Zoho Sheet
    data_df = fetch_zoho_data(workbook_id, worksheet_name)
    
    if not data_df.empty:
        app_layout(data_df)
    else:
        st.error("Gagal memuat data dari Zoho Sheet. Cek kredensial dan koneksi.")

if __name__ == "__main__":

    main()
