import streamlit as st
import math

# === Konfigurasi Halaman Streamlit ===
st.set_page_config(
    page_title="Kalkulator Lingkaran",
    layout="centered"
)

# --- Judul dan Deskripsi ---
st.title("🔴 Kalkulator Lingkaran Modern")
st.markdown("Aplikasi sederhana untuk menghitung **Luas** dan **Keliling** lingkaran.")

# --- Input Jari-jari ---
st.header("Masukkan Input")
# Gunakan st.number_input untuk input angka yang lebih baik
r = st.number_input("Masukkan Jari-jari (r):", min_value=0.0, step=0.1, value=0.0, format="%.2f")

# --- Fungsi Perhitungan ---
def hitung_lingkaran(r_val):
    """Menghitung luas dan keliling lingkaran."""
    if r_val <= 0:
        # Mengembalikan None atau nilai default jika input tidak valid
        return None, None
    
    luas = math.pi * r_val**2
    keliling = 2 * math.pi * r_val
    return luas, keliling

# --- Tombol Hitung ---
if st.button("✨ Hitung"):
    if r > 0:
        luas_hasil, keliling_hasil = hitung_lingkaran(r)
        
        # --- Hasil ---
        st.header("Hasil Perhitungan")
        
        # Menggunakan st.metric atau st.info untuk menampilkan hasil
        st.metric(label="Luas Lingkaran", value=f"{luas_hasil:.2f} cm²", delta=f"π ≈ {math.pi:.4f}")
        st.metric(label="Keliling Lingkaran", value=f"{keliling_hasil:.2f} cm", delta=f"2π ≈ {2*math.pi:.4f}")
        
        st.balloons() # Efek visual
        
    else:
        st.error("❌ Jari-jari harus lebih dari 0 untuk melakukan perhitungan.")

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Dibuat dengan Python • Menggunakan Streamlit</p>", unsafe_allow_html=True)