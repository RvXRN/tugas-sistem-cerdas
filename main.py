import streamlit as st
import time
st.title("🧠 Mental State Analyzer")

kondisi_tidur = st.selectbox("Bagaimana kualitas tidur Anda?", ["Cukup", "Kurang"], key="tidur")
level_motivasi = st.selectbox("Bagaimana tingkat motivasi Anda hari ini?", ["Tinggi", "Rendah"], key="motivasi")

st.divider() 

if st.button("Jalankan Analisis", type="primary"):
    
    with st.spinner("Menganalisis kondisi mental Anda..."):
        time.sleep(2) 

    if kondisi_tidur == "Cukup" and level_motivasi == "Tinggi":
        st.balloons() 
        st.success("### STATUS: PEAK PERFORMANCE")
        st.markdown("""
        **Analisis Psikologi:**
        Anda sedang berada dalam kondisi *Flow State*. Fokus Anda maksimal dan energi mental Anda penuh.
        
        **Saran Tindakan:**
        1. Kerjakan tugas yang paling sulit atau butuh kreativitas tinggi sekarang.
        2. Hindari gangguan (HP/Social Media) agar momentum ini tidak hilang.
        3. Manfaatkan untuk 'menabung' progres pekerjaan buat hari esok.
        """)
    
    elif kondisi_tidur == "Cukup" and level_motivasi == "Rendah":
        st.info("STATUS: FISIK OKE, MENTAL REHAT")
        st.write("Fisik Anda segar, tapi mungkin Anda sedang bosan. Coba cari inspirasi baru atau ganti suasana kerja.")
        
    else:
        st.warning("Tetap semangat! Jangan terlalu memaksakan diri jika kondisi tidak prima.")