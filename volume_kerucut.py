import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from io import BytesIO

# ---------------------- Fungsi Inti ----------------------
def hitung_volume_kerucut(r, h):
    return (1/3) * pi * (r**2) * h

def buat_figure_kerucut(r, h, elev=25, azim=45):
    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, projection='3d')

    theta = np.linspace(0, 2*np.pi, 80)
    z = np.linspace(0, h, 80)
    theta_grid, z_grid = np.meshgrid(theta, z)
    r_grid = r * (1 - z_grid / h)

    x = r_grid * np.cos(theta_grid)
    y = r_grid * np.sin(theta_grid)

    ax.plot_surface(x, y, z_grid, color='orange', alpha=0.8)

    # tutup bawah
    theta2 = np.linspace(0, 2*np.pi, 80)
    x2 = r * np.cos(theta2)
    y2 = r * np.sin(theta2)
    z2 = np.zeros_like(theta2)
    ax.plot_trisurf(x2, y2, z2, color='orange', alpha=0.8)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z (Tinggi)')
    ax.set_title('Kerucut 3D')
    ax.view_init(elev=elev, azim=azim)
    return fig

# ---------------------- GUI Streamlit ----------------------
st.set_page_config(page_title="Volume Kerucut", layout="wide")
st.title("📐 Kalkulator Volume Kerucut")
st.write("Masukkan jari-jari dan tinggi kerucut untuk menghitung volumenya.")

col1, col2 = st.columns(2)

with col1:
    r = st.number_input("Jari-jari (r)", min_value=0.0, value=5.0, step=0.1)
    h = st.number_input("Tinggi (h)", min_value=0.0, value=10.0, step=0.1)
    hitung = st.button("Hitung Volume")

    if hitung:
        if r <= 0 or h <= 0:
            st.error("Jari-jari dan tinggi harus lebih besar dari 0!")
        else:
            volume = hitung_volume_kerucut(r, h)
            st.success(f"Volume Kerucut = {volume:.4f} satuan³")

with col2:
    elev = st.slider("Elevasi", 0, 90, 25)
    azim = st.slider("Azimuth", -180, 180, 45)

    if r > 0 and h > 0:
        fig = buat_figure_kerucut(r, h, elev, azim)
        st.pyplot(fig)

        # Simpan gambar ke buffer untuk diunduh
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)

        st.download_button(
            label="💾 Unduh Gambar Kerucut",
            data=buf,
            file_name="kerucut_3D.png",
            mime="image/png"
        )

st.caption("Rumus: V = (1/3) × π × r² × h")
