import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. KONFIGURASI HALAMAN & DATA
# ==========================================
st.set_page_config(page_title="Dashboard Analisis Data", layout="wide")

st.title("📊 Latihan Visualisasi Data Python")
st.markdown("""
Dashboard ini mendemonstrasikan integrasi **Matplotlib (OO Style)** dan
**Seaborn** ke dalam aplikasi web interaktif menggunakan Streamlit.
""")

sns.set_theme(style="whitegrid")

# Sidebar untuk kontrol global
st.sidebar.header("Parameter Global")
sampel_data = st.sidebar.slider("Jumlah Sampel Data", 50, 1000, 100)

# ==========================================
# 2. MATPLOTLIB: OBJECT ORIENTED STYLE
# ==========================================
st.header("A. Visualisasi Matematika (Matplotlib OO)")
st.caption("Mendemonstrasikan penggunaan `plt.subplots()` untuk kontrol penuh.")

col1, col2 = st.columns([2, 1])

with col1:
    # Generate data dummy
    x = np.linspace(0, 10, sampel_data)
    y_sin = np.sin(x)
    y_cos = np.cos(x)

    # Figure dan Axes (OO Style)
    fig_mpl, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    # Grafik 1: Line chart
    ax1.plot(x, y_sin, label="Sinus", color="#1f77b4", linewidth=2)
    ax1.plot(x, y_cos, label="Cosinus", color="#ff7f0e", linestyle="--")
    ax1.set_title("Gelombang Trigonometri")
    ax1.set_xlabel("Waktu (t)")
    ax1.set_ylabel("Amplitudo")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Grafik 2: Scatter plot data acak
    rng = np.random.RandomState(42)
    x_scatter = rng.rand(50)
    y_scatter = rng.rand(50)
    colors = rng.rand(50)
    area = (30 * rng.rand(50)) ** 2

    ax2.scatter(
        x_scatter, y_scatter, s=area, c=colors,
        alpha=0.5, cmap="viridis"
    )
    ax2.set_title("Sebaran Data Acak")
    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")

    fig_mpl.tight_layout()
    st.pyplot(fig_mpl)
    plt.close(fig_mpl)

with col2:
    st.info("""
    **Konsep OO Style**

    Berbeda dengan `plt.plot()` biasa, kita mendefinisikan `fig` dan `ax`
    secara eksplisit. Cara ini memudahkan pengaturan beberapa grafik
    dalam satu kanvas (*subplots*).
    """)

# ==========================================
# 3. SEABORN: STATISTICAL EDA
# ==========================================
st.divider()
st.header("B. Analisis Statistik (Seaborn)")
st.caption("Visualisasi distribusi dan korelasi menggunakan dataset Tips.")

@st.cache_data
def load_tips_data():
    return sns.load_dataset("tips")

try:
    df_tips = load_tips_data()
except Exception:
    st.error(
        "Dataset 'tips' belum berhasil dimuat. Periksa koneksi internet, "
        "lalu jalankan ulang aplikasi. Seaborn biasanya mengunduh dataset "
        "ini saat pertama kali digunakan."
    )
    st.stop()

if st.checkbox("Tampilkan Dataset (5 baris pertama)"):
    st.dataframe(df_tips.head())

row2_col1, row2_col2 = st.columns(2)

# Grafik 1: Histogram distribusi tagihan
with row2_col1:
    st.subheader("1. Distribusi Tagihan")
    fig_sb1, ax_sb1 = plt.subplots(figsize=(6, 4))
    sns.histplot(
        data=df_tips,
        x="total_bill",
        kde=True,
        hue="time",
        palette="magma",
        ax=ax_sb1
    )
    ax_sb1.set_title("Distribusi Total Tagihan")
    ax_sb1.set_xlabel("Total Tagihan")
    ax_sb1.set_ylabel("Frekuensi")
    fig_sb1.tight_layout()
    st.pyplot(fig_sb1)
    plt.close(fig_sb1)
    st.markdown("**Insight:** Grafik membandingkan distribusi tagihan saat Lunch dan Dinner.")

# Grafik 2: Scatter plot hubungan tagihan dan tip
with row2_col2:
    st.subheader("2. Hubungan Tagihan & Tip")
    filter_gender = st.radio(
        "Pilih Gender:",
        ["Male", "Female"],
        horizontal=True
    )
    subset_data = df_tips[df_tips["sex"] == filter_gender]

    fig_sb2, ax_sb2 = plt.subplots(figsize=(6, 4))
    sns.scatterplot(
        data=subset_data,
        x="total_bill",
        y="tip",
        hue="smoker",
        style="day",
        s=100,
        ax=ax_sb2
    )
    ax_sb2.set_title(f"Tagihan dan Tip — {filter_gender}")
    ax_sb2.set_xlabel("Total Tagihan")
    ax_sb2.set_ylabel("Tip")
    ax_sb2.legend(
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        borderaxespad=0
    )
    fig_sb2.tight_layout()
    st.pyplot(fig_sb2)
    plt.close(fig_sb2)

# ==========================================
# 4. KORELASI (HEATMAP)
# ==========================================
st.subheader("3. Matriks Korelasi")
col_corr1, col_corr2 = st.columns([1, 2])

with col_corr1:
    st.markdown("""
    Heatmap membantu melihat arah dan kekuatan hubungan antarvariabel numerik.

    - **Mendekati +1:** hubungan positif kuat.
    - **Mendekati -1:** hubungan negatif kuat.
    - **Mendekati 0:** hubungan linear lemah.
    """)

with col_corr2:
    fig_corr, ax_corr = plt.subplots(figsize=(8, 4))
    corr = df_tips.corr(numeric_only=True)
    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        ax=ax_corr
    )
    ax_corr.set_title("Matriks Korelasi Dataset Tips")
    fig_corr.tight_layout()
    st.pyplot(fig_corr)
    plt.close(fig_corr)

# Footer
st.divider()
st.caption("Modul Praktikum Visualisasi Data | Informatika")
