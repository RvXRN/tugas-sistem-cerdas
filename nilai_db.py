import sqlite3

# 1. Koneksi ke Database Nilai
def get_nilai_conn():
    return sqlite3.connect('penilaian.db')

# 2. Inisialisasi Tabel Nilai (Jalankan saat startup)
def init_db():
    conn = get_nilai_conn()
    c = conn.cursor()
    # Tabel ini menyimpan Nama, NIM, Nilai Tugas, UTS, UAS, Nilai Akhir, dan Grade
    c.execute('''CREATE TABLE IF NOT EXISTS nilai_mhs 
                 (nama TEXT, nim TEXT PRIMARY KEY, tugas REAL, uts REAL, uas REAL, akhir REAL, grade TEXT)''')
    conn.commit()
    conn.close()

# 3. Fungsi Tambah/Simpan Nilai (Create)
def add_nilai(nama, nim, tugas, uts, uas, akhir, grade):
    conn = get_nilai_conn()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO nilai_mhs VALUES (?,?,?,?,?,?,?)', 
                  (nama, nim, tugas, uts, uas, akhir, grade))
        conn.commit()
        return True
    except:
        return False # False jika NIM sudah ada (Duplicate)
    finally:
        conn.close()

# 4. Fungsi Ambil Semua Data (Read)
def view_nilai():
    conn = get_nilai_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM nilai_mhs')
    data = c.fetchall()
    conn.close()
    return data

# 5. Fungsi Hapus Data (Delete) - Tambahan buat syarat CRUD
def delete_data(nim):
    conn = get_nilai_conn()
    c = conn.cursor()
    c.execute('DELETE FROM nilai_mhs WHERE nim=?', (nim,))
    conn.commit()
    conn.close()