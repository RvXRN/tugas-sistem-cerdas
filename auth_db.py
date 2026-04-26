import sqlite3

# 1. Koneksi ke Database User
def get_auth_conn():
    return sqlite3.connect('users_data.db')

# 2. Buat Tabel User (Dijalankan saat startup)
def create_usertable():
    conn = get_auth_conn()
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT PRIMARY KEY, password TEXT, role TEXT)')
    conn.commit()
    conn.close()

# 3. Fungsi Tambah User (Register)
def add_userdata(username, password, role):
    conn = get_auth_conn()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO userstable(username, password, role) VALUES (?,?,?)', (username, password, role))
        conn.commit()
        return True
    except:
        return False # Return False jika username sudah ada (karena PRIMARY KEY)
    finally:
        conn.close()

# 4. Fungsi Verifikasi Login
def login_user(username, password):
    conn = get_auth_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM userstable WHERE username =? AND password =?', (username, password))
    data = c.fetchone()
    conn.close()
    return data