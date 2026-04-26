import streamlit as st
import pandas as pd
import os
from nilai_db import *
from auth_db import *
from io import BytesIO
from datetime import datetime
# --- 1. CONFIG & DARK THEME INJECTION ---
st.set_page_config(page_title="Gradbit Dark Mode", layout="wide")

# Memanggil file CSS Dark Mode Biru
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Inisialisasi Database
init_db()
create_usertable()

# --- 2. LOGIKA PENILAIAN (Rule-Based) ---
def tentukan_grade(nilai):
    if nilai >= 85: return "A", "Istimewa", "#00FF7F" # Hijau Neon
    elif nilai >= 75: return "B", "Sangat Baik", "#1E90FF" # Biru Elektrik
    elif nilai >= 65: return "C", "Cukup", "#FFA500" # Orange
    elif nilai >= 50: return "D", "Kurang", "#AAAAAA" # Abu-abu
    else: return "E", "Gagal", "#FF4B4B" # Merah

def main():
    # Cek apakah user sudah login atau belum
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        # --- HALAMAN LOGIN & REGISTER (TAMPILAN GELAP) ---
        _, center_col, _ = st.columns([1, 3, 1]) 
        with center_col:
            st.image("Gradbit.png", width=150)
            st.markdown("<h2 style='text-align: center; color: #1E90FF;'>Gradbit LOGIN</h2>", unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["Masuk", "Daftar Akun"])
            
            with tab1:
                u = st.text_input("Username", key="l_user")
                p = st.text_input("Password", type='password', key="l_pass")
                if st.button("Login Sekarang", use_container_width=True):
                    res = login_user(u, p)
                    if res:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = res[0]
                        st.session_state['role'] = res[2]
                        st.rerun()
                    else:
                        st.error("Username atau Password salah!")

            with tab2:
                new_u = st.text_input("Buat Username", key="r_user")
                new_p = st.text_input("Buat Password", type='password', key="r_pass")
                role = st.selectbox("Daftar sebagai", ["User", "Admin"], key="r_role")
                if st.button("Daftar Akun", use_container_width=True):
                    if add_userdata(new_u, new_p, role):
                        st.success("Berhasil! Silakan kembali ke tab Masuk.")
                    else:
                        st.warning("Username sudah terpakai.")

    else:
        # --- HALAMAN UTAMA (SETELAH LOGIN) ---
        # Sidebar Area
        st.sidebar.markdown(f"<h2 style='color: #1E90FF;'>Gradbit</h2>", unsafe_allow_html=True)
        st.sidebar.write(f"Selamat Datang, **{st.session_state['username']}**")
        st.sidebar.info(f"Role: {st.session_state['role']}")
        
        if st.sidebar.button("Keluar (Logout)", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

        st.title("🎓 Dashboard Penilaian Mahasiswa")

        # Logika Hak Akses: Hanya Admin yang bisa lihat Form Input
        if st.session_state['role'] == "Admin":
            with st.expander("Form Input Nilai (Admin Only)"):
                with st.form("input_nilai", clear_on_submit=True):
                    nama = st.text_input("Nama Mahasiswa")
                    nim = st.text_input("NIM")
                    c1, c2, c3 = st.columns(3)
                    tgs = c1.number_input("Tugas", 0, 100)
                    uts = c2.number_input("UTS", 0, 100)
                    uas = c3.number_input("UAS", 0, 100)
                    
                    if st.form_submit_button("Hitung & Simpan"):
                        n_akhir = (tgs * 0.3) + (uts * 0.3) + (uas * 0.4)
                        grade, ket, warna = tentukan_grade(n_akhir)
                        
                        if add_nilai(nama, nim, tgs, uts, uas, n_akhir, grade):
                            st.markdown(f"""
                                <div style="background-color: #1C2128; padding: 20px; border-radius: 10px; border-left: 10px solid {warna}; border-top: 1px solid #30363D; border-right: 1px solid #30363D; border-bottom: 1px solid #30363D;">
                                    <h3 style="color:{warna}; margin:0;">Grade: {grade}</h3>
                                    <p style="color:white;">Mahasiswa <b>{nama}</b> dinyatakan <b>{ket}</b>.</p>
                                </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("Gagal! NIM sudah ada di database.")
        else:
            st.info("Akses Terbatas: Anda hanya dapat melihat daftar nilai.")

        # Menampilkan Tabel Bisa dilihat Admin & User
        st.subheader("📊 Tabel Hasil Studi")
        data = view_nilai()

        if data:
            # 1. Buat DataFrame
            df = pd.DataFrame(data, columns=["Nama", "NIM", "Tugas", "UTS", "UAS", "Akhir", "Grade"])
            
            # 2. Ubah Index mulai dari 1
            df.index = df.index + 1
            
            # 3. Tampilkan Tabel
            st.dataframe(df, use_container_width=True)

            # 4. Logic Export ke Excel (Pake BytesIO biar gak nyampah file di server)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=True, sheet_name='Hasil_Studi')
            
            processed_data = output.getvalue()

            # 5. Tombol Download
            st.download_button(
                label="📥 Download Excel",
                data=processed_data,
                file_name=f"hasil_studi_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.write("Belum ada data.")

if __name__ == '__main__':
    main()