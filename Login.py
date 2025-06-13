import streamlit as st
from auth import verify_user, add_user
import time

# Konfigurasi halaman
st.set_page_config(page_title="SafePayAI - Login", layout="centered")

# CSS untuk styling
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Muat CSS dari file eksternal
load_css("style.css")

# Inisialisasi session_state untuk auth_page
if 'auth_page' not in st.session_state:
    st.session_state.auth_page = "login"
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Fungsi Header dengan tombol di kanan atas
# col1, col2 = st.columns([6, 1])
header_col1, header_col2 = st.columns([6, 2.5])
with header_col1:
    st.markdown("""
        <div class="logo" style="display:flex; align-items:center; gap:10px; font-size:24px;">
            <img src="https://img.icons8.com/ios-filled/50/lock--v1.png" width="30px"/>
            <b>SafePayAI</b>
        </div>
    """, unsafe_allow_html=True)

with header_col2:
    btn1, btn2 = st.columns([1, 1])
    with btn1:
        sign_in_clicked = st.button("Sign in", key="signin")
    with btn2:
        register_clicked = st.button("Register", key="register")

# Tangani aksi tombol
if sign_in_clicked:
    st.session_state.auth_page = "login"
if register_clicked:
    st.session_state.auth_page = "register"

# Divider
st.markdown('<hr class="divider">', unsafe_allow_html=True)

def show_login():
    st.markdown("""
        <div class="form-box">
            <h2>Sign in</h2>
    """, unsafe_allow_html=True)
    # Divider
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Form login
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Masukkan username Anda")
        password = st.text_input("Password", type="password", placeholder="Masukkan password Anda")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login berhasil! Mengarahkan ke dashboard...")
                time.sleep(1)
                st.switch_page("pages/Dashboard.py")
            else:
                st.error("Username atau password salah")
    
    # Link lupa password
    st.markdown('<div class="forgot-password">Forgot password?</div>', unsafe_allow_html=True)

def show_register():
    st.markdown("""
        <div class="form-box">
            <h2>Register</h2>
    """, unsafe_allow_html=True)
    
    with st.form("register_form"):
        new_username = st.text_input("Username", placeholder="Buat username baru")
        new_password = st.text_input("Password", type="password", placeholder="Buat password baru")
        confirm_password = st.text_input("Konfirmasi Password", type="password", placeholder="Konfirmasi password")
        name = st.text_input("Nama Lengkap", placeholder="Nama lengkap pengguna")
        role = st.selectbox("Role", ["analyst", "admin"])
        submit_button = st.form_submit_button("Daftarkan")
        
        if submit_button:
            if new_password != confirm_password:
                st.error("Password dan konfirmasi password tidak sama")
            elif len(new_password) < 6:
                st.error("Password harus minimal 6 karakter")
            else:
                if add_user(new_username, new_password, name, role):
                    st.success("User berhasil didaftarkan!")
                else:
                    st.error("Username sudah digunakan")

# login()
# Main App
def main():
    if not st.session_state.logged_in:
        if st.session_state.auth_page == "login":
            show_login()
        else:
            show_register()
    else:
        st.switch_page("pages/dashboard.py")

if __name__ == "__main__":
    main()