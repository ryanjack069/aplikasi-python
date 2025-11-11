import streamlit as st
import math
import matplotlib.pyplot as plt

# === Konfigurasi Halaman Streamlit ===
st.set_page_config(
    page_title="Kalkulator Lingkaran",
    layout="centered"
)

# --- Judul dan Deskripsi ---
st.title("🔴 Kalkulator Lingkaran Interaktif")
st.markdown("Aplikasi untuk menghitung **Luas** dan **Keliling** lingkaran, dilengkapi dengan **Visualisasi**.")

# --- Diagram Visualisasi Lingkaran ---
st.header("Konsep Lingkaran")
# Menyisipkan diagram visual yang Anda minta
st.markdown("Berikut adalah ilustrasi standar lingkaran dengan jari-jari (r):")


# --- Input Jari-jari ---
st.header("Masukkan Input")
r = st.number_input("Masukkan Jari-jari (r) untuk lingkaran Anda:", min_value=0.0, step=0.1, value=5.0, format="%.2f")

# --- Fungsi Perhitungan ---
def hitung_lingkaran(r_val):
    """Menghitung luas dan keliling lingkaran."""
    if r_val <= 0:
        return None, None
    
    luas = math.pi * r_val**2
    keliling = 2 * math.pi * r_val
    return luas, keliling

# --- Fungsi Visualisasi 2D Sederhana (Matplotlib) ---
def gambar_lingkaran(r_val):
    """Menggambar lingkaran 2D menggunakan Matplotlib."""
    if r_val <= 0:
        return None
        
    fig, ax = plt.subplots()
    
    # Menggambar lingkaran
    circle = plt.Circle((0, 0), r_val, color='blue', fill=False, linewidth=2)
    ax.add_artist(circle)
    
    # Menggambar garis jari-jari
    ax.plot([0, r_val], [0, 0], 'r--')
    
    # Menambahkan label 'r'
    ax.text(r_val / 2, 0.5, f'r = {r_val}', color='red', fontsize=12, ha='center')
    
    # Mengatur batas plot agar lingkaran terlihat proporsional
    limit = r_val * 1.2
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_aspect('equal', adjustable='box')
    ax.set_title(f"Visualisasi Lingkaran (r = {r_val})")
    ax.grid(True)
    
    return fig

# --- Tombol Hitung dan Tampilkan Hasil ---
if st.button("✨ Hitung & Visualisasikan"):
    if r > 0:
        luas_hasil, keliling_hasil = hitung_lingkaran(r)
        
        # --- Hasil ---
        st.header("Hasil Perhitungan")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Luas Lingkaran (A)", value=f"{luas_hasil:.2f} cm²")
        with col2:
            st.metric(label="Keliling Lingkaran (K)", value=f"{keliling_hasil:.2f} cm")
        
        st.info(f"Menggunakan $\pi \approx {math.pi:.4f}$")

        # --- Visualisasi ---
        st.header("Visualisasi 2D")
        fig_lingkaran = gambar_lingkaran(r)
        if fig_lingkaran:
            # Menampilkan plot Matplotlib di Streamlit
            st.pyplot(fig_lingkaran)
        
        st.balloons()
        
    else:
        st.error("❌ Jari-jari harus lebih dari 0.0 untuk melakukan perhitungan dan visualisasi.")

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Dibuat dengan Python • Menggunakan Streamlit & Matplotlib</p>", unsafe_allow_html=True)