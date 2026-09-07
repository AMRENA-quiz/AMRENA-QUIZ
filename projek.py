import random
import string
import json
import os
import time
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="QUIZ'ARN", page_icon="🏔️", layout="wide")

# --- CUSTOM CSS DENGAN BACKGROUND ANIMASI KEREN & MODERN ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* BACKGROUND ANIMASI GRADASI BERGERAK (TIDAK MEMBOSANKAN) */
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #312e81, #1e3a8a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #ffffff;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* KUSTOM HEADER KANAN ATAS (USER INFO) */
    .top-bar-container {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 15px;
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(10px);
        padding: 10px 20px;
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        margin-bottom: 20px;
    }

    .user-badge {
        font-weight: 700;
        color: #38bdf8;
        font-size: 15px;
    }

    .coin-badge {
        background: rgba(245, 158, 11, 0.2);
        border: 1px solid #f59e0b;
        color: #fbbf24;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 14px;
    }

    /* TEKS INPUT DAN DROPDOWN */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(15, 23, 42, 0.9) !important;
        color: #ffffff !important;
        border: 1px solid #38bdf8 !important;
        border-radius: 10px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    label {
        color: #f8fafc !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }

    /* STYLING KARTU PILIHAN PERAN DENGAN EFEK GLOW */
    .role-card {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 16px;
        padding: 30px 24px;
        text-align: center;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    
    .role-card:hover {
        transform: translateY(-5px);
        border-color: #38bdf8;
        box-shadow: 0 12px 40px rgba(56, 189, 248, 0.2);
    }

    .role-title {
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 12px;
        color: #ffffff;
    }

    .role-desc {
        font-size: 14px;
        color: #cbd5e1;
        line-height: 1.5;
    }

    .auth-card {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
        margin: auto;
        max-width: 500px;
    }

    .question-box {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        font-size: 26px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(56, 189, 248, 0.3);
        border: 3px solid #38bdf8;
    }

    .climb-box {
        background: rgba(15, 23, 42, 0.85);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 25px;
        border: 2px solid #f59e0b;
        color: #fbbf24;
        box-shadow: 0 5px 20px rgba(245, 158, 11, 0.2);
    }

    .rank-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(8px);
        padding: 15px 25px;
        border-radius: 15px;
        margin-bottom: 12px;
        border-left: 8px solid #38bdf8;
        border-top: 1px solid rgba(255,255,255,0.1);
        border-right: 1px solid rgba(255,255,255,0.1);
        border-bottom: 1px solid rgba(255,255,255,0.1);
        font-size: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .my-rank {
        background: rgba(245, 158, 11, 0.2) !important;
        border-left: 8px solid #fbbf24 !important;
        border: 2px solid #fbbf24;
    }

    .waiting-box {
        background: rgba(15, 23, 42, 0.8);
        backdrop-filter: blur(10px);
        border: 2px dashed #f59e0b;
        padding: 35px;
        border-radius: 20px;
        text-align: center;
        margin-top: 20px;
    }

    .stButton>button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNGSI TEXT-TO-SPEECH ---
def speak(text):
    if text:
        js_code = f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{text}");
            msg.lang = "id-ID";
            msg.rate = 1.0;
            window.speechSynthesis.speak(msg);
        </script>
        """
        components.html(js_code, height=0)

# --- DATABASE PENYIMPANAN SERVER (JSON) ---
USERS_FILE = "users_db.json"
ROOMS_FILE = "rooms_db.json"

# --- HELPER AKUN USERS ---
def get_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def update_user_coins_and_skins(username, earned_coins, new_skin=None):
    users = get_users()
    if username in users:
        if "coins" not in users[username]:
            users[username]["coins"] = 0
        if "skins" not in users[username]:
            users[username]["skins"] = ["🏔️ Penjelajah Gunung Standard"]
        
        users[username]["coins"] += earned_coins
        if new_skin and new_skin not in users[username]["skins"]:
            users[username]["skins"].append(new_skin)
            
        save_users(users)

# --- HELPER KUIS ROOMS ---
def get_rooms():
    if not os.path.exists(ROOMS_FILE):
        return {}
    try:
        with open(ROOMS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_all_rooms(rooms):
    with open(ROOMS_FILE, "w") as f:
        json.dump(rooms, f)

def save_room(pin, data):
    rooms = get_rooms()
    rooms[pin] = data
    save_all_rooms(rooms)

def submit_score(pin, player_name, avatar, score, altitude):
    rooms = get_rooms()
    if pin in rooms:
        if "players" not in rooms[pin]:
            rooms[pin]["players"] = {}
        rooms[pin]["players"][player_name] = {
            "avatar": avatar,
            "score": score,
            "altitude": altitude
        }
        save_all_rooms(rooms)

# --- INISIALISASI SESSION STATE ---
if "logged_user" not in st.session_state:
    st.session_state.logged_user = None

if "selected_role" not in st.session_state:
    st.session_state.selected_role = None

if "game_state" not in st.session_state:
    st.session_state.game_state = "LOBBY"

if "last_ranks" not in st.session_state:
    st.session_state.last_ranks = {}

# ==========================================
# HEADER KANAN ATAS (JIKA SUDAH LOGIN)
# ==========================================
if st.session_state.logged_user:
    users_data = get_users()
    user_info = users_data.get(st.session_state.logged_user, {})
    total_coins = user_info.get("coins", 0)
    
    st.markdown(f"""
        <div class='top-bar-container'>
            <span class='user-badge'>👤 {st.session_state.logged_user}</span>
            <span class='coin-badge'>🪙 {total_coins} Poin</span>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# MODUL 1: AUTHENTICATION (LOGIN & REGISTER)
# ==========================================
if st.session_state.logged_user is None:
    st.markdown("<h1 style='text-align: center; color: #ffffff; font-size: 42px; font-weight: 800; text-shadow: 0 2px 10px rgba(56, 189, 248, 0.5);'>🏔️ QUIZ'ARN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1; font-size: 18px;'>Silakan Daftar Nama Terlebih Dahulu, Lalu Login</p>", unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        auth_tab1, auth_tab2 = st.tabs(["🔑 Masuk (Login)", "📝 Daftar Nama Baru"])

        with auth_tab1:
            st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
            st.subheader("Masuk dengan Nama Terdaftar")
            login_username = st.text_input("Masukkan Nama Kamu:", key="login_u")
            
            if st.button("🚀 MASUK", type="primary", key="btn_login_submit", use_container_width=True):
                users = get_users()
                clean_name = login_username.strip()
                if not clean_name:
                    st.error("Masukkan nama kamu terlebih dahulu!")
                elif clean_name in users:
                    st.session_state.logged_user = clean_name
                    st.rerun()
                else:
                    st.error("❌ Nama ini belum terdaftar! Silakan daftar terlebih dahulu.")
            st.markdown("</div>", unsafe_allow_html=True)

        with auth_tab2:
            st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
            st.subheader("Daftar Akun Baru")
            reg_username = st.text_input("Buat Nama Akun Baru:", key="reg_u")

            if st.button("➕ DAFTAR AKUN", key="btn_reg_submit", use_container_width=True):
                users = get_users()
                clean_name = reg_username.strip()
                if not clean_name:
                    st.error("Nama tidak boleh kosong!")
                elif clean_name in users:
                    st.warning("Nama ini sudah terdaftar!")
                else:
                    users[clean_name] = {
                        "registered": True,
                        "coins": 100,
                        "skins": ["🏔️ Penjelajah Gunung Standard"]
                    }
                    save_users(users)
                    st.success(f"🎉 Akun '{clean_name}' berhasil dibuat (+100 Koin Bonus)! Silakan Login.")
            st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# MODUL 2: PILIH PERAN & TOKO SKIN LEGEND
# ==========================================
elif st.session_state.selected_role is None:
    st.markdown("<h1 style='text-align: center; color: #ffffff; font-size: 42px; font-weight: 800; margin-top:10px; text-shadow: 0 2px 10px rgba(56, 189, 248, 0.5);'>🏔️ QUIZ'ARN</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #e2e8f0; font-size: 18px; margin-bottom: 30px;'>Pilih peran kamu atau kunjungi Toko Skin:</p>", unsafe_allow_html=True)

    main_menu_tab1, main_menu_tab2 = st.tabs(["🎮 Pilih Peran Game", "🛒 Toko Skin Legend"])

    with main_menu_tab1:
        c_left, c_mid1, c_mid2, c_right = st.columns([1, 4, 4, 1])

        with c_mid1:
            st.markdown("""
                <div class='role-card'>
                    <div>
                        <div class='role-title'>🧑‍💻 Pengembang (Host)</div>
                        <div class='role-desc'>Buat soal, kontrol kapan game dimulai, dan pantau Peringkat Juara (Leaderboard).</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Masuk sebagai Pengembang", key="btn_role_host", use_container_width=True):
                st.session_state.selected_role = "HOST"
                st.rerun()

        with c_mid2:
            st.markdown("""
                <div class='role-card'>
                    <div>
                        <div class='role-title'>🎮 Anggota (Pemain)</div>
                        <div class='role-desc'>Masukkan Kode PIN dari Pengembang dan kumpulkan poin untuk ditukar skin legend.</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Masuk sebagai Pemain", key="btn_role_player", use_container_width=True):
                st.session_state.selected_role = "PLAYER"
                st.rerun()

    with main_menu_tab2:
        st.subheader("🛒 Toko Penukaran Skin Legend")
        st.write("Tukar poin yang kamu kumpulkan dari kuis dengan skin karakter legend eksklusif!")
        
        users_data = get_users()
        current_user_data = users_data.get(st.session_state.logged_user, {})
        my_coins = current_user_data.get("coins", 0)
        my_skins = current_user_data.get("skins", [])

        legend_shop = {
            "🏔️ Pendaki Gunung Everest": {"price": 2000, "desc": "Penakluk puncak tertinggi di dunia bersalju abadi."},
            "⚡ Dewa Petir Zeus": {"price": 1500, "desc": "Karakter petir super cepat penakluk rintangan."},
            "👑 Ksatria Naga Emas": {"price": 1000, "desc": "Armor naga emas berkilau lambang juara sejati."},
            "🌌 Pengelana Luar Angkasa": {"price": 800, "desc": "Astronot penjelajah galaksi tak terbatas."}
        }

        col_shop1, col_shop2 = st.columns(2)
        for idx, (skin_name, skin_info) in enumerate(legend_shop.items()):
            target_col = col_shop1 if idx % 2 == 0 else col_shop2
            with target_col:
                owned = skin_name in my_skins
                st.markdown(f"""
                    <div style='background: rgba(255,255,255,0.06); backdrop-filter: blur(8px); padding: 20px; border-radius: 14px; border: 1px solid rgba(56,189,248,0.3); margin-bottom: 15px;'>
                        <h3>{skin_name}</h3>
                        <p style='color: #cbd5e1; font-size: 13px;'>{skin_info['desc']}</p>
                        <p style='color: #fbbf24; font-weight: 700;'>Harga: 🪙 {skin_info['price']} Poin</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if owned:
                    st.success("✅ Sudah Dimiliki (Aktif)")
                else:
                    if st.button(f"Tukar dengan Skin Ini", key=f"buy_{idx}"):
                        if my_coins >= skin_info['price']:
                            users_data[st.session_state.logged_user]["coins"] -= skin_info['price']
                            if "skins" not in users_data[st.session_state.logged_user]:
                                users_data[st.session_state.logged_user]["skins"] = []
                            users_data[st.session_state.logged_user]["skins"].append(skin_name)
                            save_users(users_data)
                            st.success(f"🎉 Berhasil menukar skin {skin_name}!")
                            st.rerun()
                        else:
                            st.error("❌ Poin kamu belum cukup untuk menukar skin legend ini. Mainkan lebih banyak kuis!")

    st.markdown("<br><hr>", unsafe_allow_html=True)
    col_out1, col_out2, col_out3 = st.columns([4, 2, 4])
    with col_out2:
        if st.button("🚪 Keluar / Logout Akun", use_container_width=True):
            st.session_state.logged_user = None
            st.session_state.selected_role = None
            st.session_state.game_state = "LOBBY"
            st.rerun()

# ==========================================
# MODUL 3: DASHBOARD ISI SESUAI PERAN
# ==========================================
else:
    st.sidebar.title(f"👤 {st.session_state.logged_user}")
    st.sidebar.write(f"Peran Aktif: **{'Pengembang' if st.session_state.selected_role == 'HOST' else 'Pemain'}**")
    
    if st.sidebar.button("🔄 Ganti Peran / Menu Toko"):
        st.session_state.selected_role = None
        st.session_state.game_state = "LOBBY"
        st.rerun()

    if st.sidebar.button("🚪 Keluar / Logout"):
        st.session_state.logged_user = None
        st.session_state.selected_role = None
        st.session_state.game_state = "LOBBY"
        st.rerun()

    # ------------------------------------------
    # MODUL PEMAIN
    # ------------------------------------------
    if st.session_state.selected_role == "PLAYER":
        if st.session_state.game_state == "LOBBY":
            st.title("🎯 Masuk ke Game Kuis")
            
            input_pin = st.text_input("Masukkan Kode PIN Game:", max_chars=6, key="p_pin")

            users_data = get_users()
            user_skins = users_data.get(st.session_state.logged_user, {}).get("skins", ["🏔️ Penjelajah Gunung Standard"])

            st.write("### 🧙‍♂️ Pilih Skin Karakter Kamu:")
            selected_avatar = st.selectbox("Pilih Skin yang Ingin Digunakan:", user_skins, key="p_avatar")

            if st.button("🚀 MASUK RUANG TUNGGU", type="primary", key="p_enter"):
                active_rooms = get_rooms()
                if input_pin in active_rooms:
                    st.session_state.active_pin = input_pin
                    st.session_state.player_name = st.session_state.logged_user
                    st.session_state.player_avatar = selected_avatar
                    st.session_state.current_q = 0
                    st.session_state.score = 0
                    st.session_state.altitude = 0
                    st.session_state.game_state = "WAITING_ROOM"
                    st.rerun()
                else:
                    st.error("Kode PIN tidak ditemukan! Periksa kembali PIN dari Pengembang.")

        elif st.session_state.game_state == "WAITING_ROOM":
            pin = st.session_state.active_pin
            active_rooms = get_rooms()

            if pin not in active_rooms:
                st.error("PIN/Kuis sudah dihapus!")
                st.session_state.game_state = "LOBBY"
                st.rerun()

            room_data = active_rooms[pin]
            status_game = room_data.get("status", "WAITING")

            if status_game == "STARTED":
                st.session_state.game_state = "PLAYING"
                st.rerun()

            st.markdown(f"""
                <div class='waiting-box'>
                    <h2 style='color:#fbbf24;'>⏳ MENUNGGU PENGEMBANG...</h2>
                    <p style='font-size:18px;'>Halo <b>{st.session_state.player_avatar} {st.session_state.player_name}</b>, kamu sudah berhasil masuk!</p>
                    <p style='color:#cbd5e1;'>Silakan tunggu Pengembang menekan tombol <b>'MULAI GAME'</b>.</p>
                </div>
            """, unsafe_allow_html=True)
            
            time.sleep(2)
            st.rerun()

        elif st.session_state.game_state == "PLAYING":
            pin = st.session_state.active_pin
            active_rooms = get_rooms()
            
            if pin not in active_rooms:
                st.error("PIN tidak ditemukan!")
                st.session_state.game_state = "LOBBY"
                st.rerun()

            room_data = active_rooms[pin]
            soal_list = room_data["soal"]
            mode = room_data["mode"]
            q_idx = st.session_state.current_q
            q_data = soal_list[q_idx]

            st.caption(f"Karakter: **{st.session_state.player_avatar} {st.session_state.player_name}** | Mode: **{mode}** | PIN: **{pin}**")
            
            if "Gunung" in mode or "Mendaki" in mode:
                progress = (q_idx) / len(soal_list)
                st.markdown(f"""
                    <div class='climb-box'>
                        ⛰️ Ketinggian {st.session_state.player_avatar}: <b>{st.session_state.altitude} Meter</b> Menuju Puncak 🌟
                    </div>
                """, unsafe_allow_html=True)
                st.progress(progress, text=f"Progres Pendakian Gunung ({q_idx}/{len(soal_list)} Soal)")

            st.markdown(f"<div class='question-box'>{q_data['question']}</div>", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            user_choice = None

            with col1:
                if st.button(f"🔺 {q_data['options'][0]}", key="btn_q_0", use_container_width=True):
                    user_choice = q_data['options'][0]
                if st.button(f"🔷 {q_data['options'][1]}", key="btn_q_1", use_container_width=True):
                    user_choice = q_data['options'][1]

            with col2:
                if st.button(f"🟡 {q_data['options'][2]}", key="btn_q_2", use_container_width=True):
                    user_choice = q_data['options'][2]
                if st.button(f"🟩 {q_data['options'][3]}", key="btn_q_3", use_container_width=True):
                    user_choice = q_data['options'][3]

            if user_choice:
                if user_choice == q_data["answer"]:
                    st.session_state.score += 1000
                    st.session_state.altitude += 500
                    st.success("🏔️ BENAR! Kamu makin dekat ke puncak! (+500m)")
                else:
                    st.error(f"❌ SALAH! Jawaban benar: {q_data['answer']}")

                submit_score(pin, st.session_state.player_name, st.session_state.player_avatar, st.session_state.score, st.session_state.altitude)

                if q_idx + 1 < len(soal_list):
                    st.session_state.current_q += 1
                    st.rerun()
                else:
                    earned_coins_from_game = st.session_state.score // 10
                    update_user_coins_and_skins(st.session_state.logged_user, earned_coins_from_game)
                    st.session_state.game_state = "RESULT"
                    st.rerun()

        elif st.session_state.game_state == "RESULT":
            st.balloons()
            pin = st.session_state.active_pin
            active_rooms = get_rooms()
            
            st.markdown("<h1 style='text-align: center; color: #fbbf24;'>🏔️ PENDAKIAN GUNUNG SELESAI! 🏆</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: #f1f5f9;'>Selamat {st.session_state.player_avatar} {st.session_state.player_name}, kamu berhasil mencapai puncak setinggi {st.session_state.altitude} Meter!</h3>", unsafe_allow_html=True)

            st.metric(label="Total Skor Poin Kamu", value=f"{st.session_state.score} Poin")
            st.info(f"🎁 Selamat! Kamu mendapatkan tambahan koin akun dari sesi ini!")

            st.divider()
            st.subheader("🏆 PAPAN PERINGKAT PEMAIN (LEADERBOARD)")

            if pin in active_rooms and "players" in active_rooms[pin]:
                players = active_rooms[pin]["players"]
                sorted_players = sorted(players.items(), key=lambda x: x[1]["score"], reverse=True)
                
                medals = ["🥇", "🥈", "🥉"]
                for idx, (p_name, p_info) in enumerate(sorted_players, start=1):
                    icon = medals[idx-1] if idx <= 3 else f"#{idx}"
                    is_me = (p_name == st.session_state.player_name)
                    avatar = p_info.get("avatar", "🏔️")
                    
                    if is_me:
                        st.markdown(f"""
                            <div class='rank-card my-rank'>
                                <b>{icon} {avatar} {p_name} (KAMU)</b> 
                                <span><b>{p_info['score']} Poin</b> ({p_info['altitude']}m) ✨</span>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div class='rank-card'>
                                <b>{icon} {avatar} {p_name}</b> 
                                <span><b>{p_info['score']} Poin</b> ({p_info['altitude']}m)</span>
                            </div>
                        """, unsafe_allow_html=True)

            if st.button("🔄 Main Lagi", key="btn_play_again"):
                st.session_state.game_state = "LOBBY"
                st.rerun()

    # ------------------------------------------
    # MODUL PENGEMBANG (HOST)
    # ------------------------------------------
    elif st.session_state.selected_role == "HOST":
        st.title("🛠️ Control Room Pengembang")

        tab1, tab2, tab3 = st.tabs(["🎮 Kontrol & Live Leaderboard", "✏️ Kelola & Edit / Hapus Kuis Saya", "➕ Buat Kuis Baru"])

        with tab1:
            st.subheader("📡 Live Leaderboard & Kontrol Game")
            all_rooms = get_rooms()
            my_rooms = {k: v for k, v in all_rooms.items() if v.get("owner") == st.session_state.logged_user}

            if my_rooms:
                selected_pin = st.selectbox("Pilih Kode PIN Game Anda:", list(my_rooms.keys()), key="select_pin_tab1")
                room = my_rooms[selected_pin]
                current_status = room.get("status", "WAITING")

                st.write(f"Status Game PIN **{selected_pin}**: **{'🟢 BERJALAN' if current_status == 'STARTED' else '🟡 MENUNGGU DIMULAI'}**")

                c_btn1, c_btn2, c_btn3 = st.columns(3)
                with c_btn1:
                    if st.button("▶️ MULAI GAME SEKARANG", type="primary", use_container_width=True):
                        all_rooms[selected_pin]["status"] = "STARTED"
                        save_all_rooms(all_rooms)
                        st.success("Game Dimulai!")
                        st.rerun()
                with c_btn2:
                    if st.button("⏸️ RESET KE RUANG TUNGGU", use_container_width=True):
                        all_rooms[selected_pin]["status"] = "WAITING"
                        save_all_rooms(all_rooms)
                        st.warning("Game dikembalikan ke Ruang Tunggu.")
                        st.rerun()
                with c_btn3:
                    is_live = st.checkbox("🔴 Aktifkan Live Mode & Suara", value=True)

                st.divider()
                board = st.empty()

                def update_leaderboard_live():
                    rooms_now = get_rooms()
                    r_data = rooms_now.get(selected_pin, {})
                    players_data = r_data.get("players", {})

                    with board.container():
                        if players_data:
                            sorted_players = sorted(players_data.items(), key=lambda x: x[1]["score"], reverse=True)
                            current_ranks = {p_name: idx + 1 for idx, (p_name, _) in enumerate(sorted_players)}
                            
                            announcement = ""
                            for p_name, new_rank in current_ranks.items():
                                if p_name in st.session_state.last_ranks:
                                    old_rank = st.session_state.last_ranks[p_name]
                                    if new_rank < old_rank:
                                        passed = old_rank - new_rank
                                        if new_rank == 1:
                                            announcement = f"Luar biasa! {p_name} memimpin di posisi pertama!"
                                        else:
                                            announcement = f"{p_name} menyusul {passed} pemain dan menempati posisi ke {new_rank}!"
                                        break
                                else:
                                    if new_rank == 1:
                                        announcement = f"{p_name} memimpin di posisi pertama!"

                            st.session_state.last_ranks = current_ranks

                            if announcement and is_live:
                                speak(announcement)
                                st.toast(f"🔊 Narator: {announcement}")

                            st.subheader("🥇 LEADERBOARD REAL-TIME")
                            podium_icons = ["🥇 Juara 1", "🥈 Juara 2", "🥉 Juara 3"]
                            
                            for idx, (p_name, p_info) in enumerate(sorted_players[:3]):
                                av = p_info.get("avatar", "🏔️")
                                st.success(f"**{podium_icons[idx]}**: {av} **{p_name}** | Skor: **{p_info['score']} Poin** ({p_info['altitude']}m)")

                            if len(sorted_players) > 3:
                                st.subheader("📋 Pemain Lainnya:")
                                for idx, (p_name, p_info) in enumerate(sorted_players[3:], start=4):
                                    av = p_info.get("avatar", "🏔️")
                                    st.write(f"**#{idx}** {av} **{p_name}** — {p_info['score']} Poin ({p_info['altitude']}m)")
                        else:
                            st.info("Belum ada pemain yang masuk/menyelesaikan kuis ini.")

                update_leaderboard_live()

                if is_live:
                    time.sleep(3)
                    st.rerun()

            else:
                st.warning("Anda belum memiliki kuis yang diterbitkan.")

        with tab2:
            st.subheader("⚙️ Kelola & Edit Kuis Milik Anda")
            all_rooms = get_rooms()
            my_rooms = {k: v for k, v in all_rooms.items() if v.get("owner") == st.session_state.logged_user}

            if my_rooms:
                edit_pin = st.selectbox("Pilih Kuis (PIN) yang Ingin Dikelola:", list(my_rooms.keys()), key="select_pin_tab2")
                room_to_edit = all_rooms[edit_pin]
                soal_list = room_to_edit.get("soal", [])
                players_in_room = room_to_edit.get("players", {})

                with st.expander("🚨 HAPUS KUIS / ROOM INI SEUTUHNYA", expanded=False):
                    st.error(f"⚠️ Hapus PIN {edit_pin} beserta seluruh data kuis dan pemain secara permanen.")
                    if st.button(f"🗑️ Hapus Kuis PIN {edit_pin} Sekarang", type="primary", key="btn_del_room"):
                        del all_rooms[edit_pin]
                        save_all_rooms(all_rooms)
                        st.success(f"Kuis PIN {edit_pin} berhasil dihapus!")
                        st.rerun()

                st.divider()
                st.write("### 👥 Kelola & Hapus Pemain")
                if players_in_room:
                    col_p1, col_p2 = st.columns([2, 1])
                    with col_p1:
                        player_to_remove = st.selectbox("Pilih Pemain:", list(players_in_room.keys()), key="select_player_del")
                    with col_p2:
                        st.write("")
                        st.write("")
                        if st.button("❌ Hapus Pemain Ini", key="btn_del_player"):
                            del all_rooms[edit_pin]["players"][player_to_remove]
                            save_all_rooms(all_rooms)
                            st.success(f"Pemain '{player_to_remove}' berhasil dihapus!")
                            st.rerun()
                else:
                    st.info("Belum ada pemain di kuis ini.")

                st.divider()
                st.write("### 📝 Edit / Hapus Soal")
                st.info(f"Kuis **PIN {edit_pin}** memiliki **{len(soal_list)} soal**.")

                with st.expander("➕ Tambah Soal Baru ke Kuis Ini"):
                    new_q = st.text_input("Pertanyaan Baru:", key="add_q")
                    o1 = st.text_input("Pilihan 1 (Merah):", key="add_o1")
                    o2 = st.text_input("Pilihan 2 (Biru):", key="add_o2")
                    o3 = st.text_input("Pilihan 3 (Kuning):", key="add_o3")
                    o4 = st.text_input("Pilihan 4 (Hijau):", key="add_o4")
                    ans_choice = st.selectbox("Kunci Jawaban:", ["Pilihan 1", "Pilihan 2", "Pilihan 3", "Pilihan 4"], key="add_ans")

                    if st.button("💾 Simpan Soal Baru", key="btn_save_new_q"):
                        if new_q and o1 and o2 and o3 and o4:
                            mapping = {"Pilihan 1": o1, "Pilihan 2": o2, "Pilihan 3": o3, "Pilihan 4": o4}
                            all_rooms[edit_pin]["soal"].append({
                                "question": new_q,
                                "options": [o1, o2, o3, o4],
                                "answer": mapping[ans_choice]
                            })
                            save_all_rooms(all_rooms)
                            st.success("Soal baru berhasil ditambahkan!")
                            st.rerun()
                        else:
                            st.error("Semua kolom harus diisi!")

                for idx, item in enumerate(soal_list):
                    with st.expander(f"Soal #{idx+1}: {item['question']}"):
                        eq = st.text_input("Pertanyaan:", value=item["question"], key=f"eq_{edit_pin}_{idx}")
                        eo1 = st.text_input("Pilihan 1:", value=item["options"][0], key=f"eo1_{edit_pin}_{idx}")
                        eo2 = st.text_input("Pilihan 2:", value=item["options"][1], key=f"eo2_{edit_pin}_{idx}")
                        eo3 = st.text_input("Pilihan 3:", value=item["options"][2], key=f"eo3_{edit_pin}_{idx}")
                        eo4 = st.text_input("Pilihan 4:", value=item["options"][3], key=f"eo4_{edit_pin}_{idx}")

                        try:
                            curr_ans_idx = item["options"].index(item["answer"])
                        except ValueError:
                            curr_ans_idx = 0

                        eans = st.selectbox("Kunci Jawaban:", ["Pilihan 1", "Pilihan 2", "Pilihan 3", "Pilihan 4"], index=curr_ans_idx, key=f"eans_{edit_pin}_{idx}")

                        col_update, col_delete = st.columns(2)
                        with col_update:
                            if st.button("💾 Simpan Perubahan", key=f"btn_upd_{edit_pin}_{idx}"):
                                mapping = {"Pilihan 1": eo1, "Pilihan 2": eo2, "Pilihan 3": eo3, "Pilihan 4": eo4}
                                all_rooms[edit_pin]["soal"][idx] = {
                                    "question": eq,
                                    "options": [eo1, eo2, eo3, eo4],
                                    "answer": mapping[eans]
                                }
                                save_all_rooms(all_rooms)
                                st.success(f"Soal #{idx+1} diperbarui!")
                                st.rerun()

                        with col_delete:
                            if st.button("🗑️ Hapus Soal", key=f"btn_del_q_{edit_pin}_{idx}"):
                                all_rooms[edit_pin]["soal"].pop(idx)
                                save_all_rooms(all_rooms)
                                st.warning(f"Soal #{idx+1} dihapus!")
                                st.rerun()
            else:
                st.warning("Anda belum memiliki kuis untuk dikelola.")

        with tab3:
            st.subheader("Buat Kuis Baru")
            if "draft_soal" not in st.session_state:
                st.session_state.draft_soal = []

            mode_game = st.selectbox("🎮 Pilih Mode Game:", ["🏔️ Petualangan Mendaki Gunung", "🎯 Mode Klasik (Kahoot Style)"], key="create_mode")

            st.write("---")
            soal = st.text_input("Pertanyaan Kuis:", key="c_q")
            a = st.text_input("Pilihan 1 (🔺 Merah):", key="c_a")
            b = st.text_input("Pilihan 2 (🔷 Biru):", key="c_b")
            c = st.text_input("Pilihan 3 (🟡 Kuning):", key="c_c")
            d = st.text_input("Pilihan 4 (🟩 Hijau):", key="c_d")
            kunci = st.selectbox("Kunci Jawaban Benar:", ["Pilihan 1", "Pilihan 2", "Pilihan 3", "Pilihan 4"], key="c_kunci")

            if st.button("➕ Tambahkan ke Draft Soal", key="btn_add_draft"):
                if soal and a and b and c and d:
                    mapping = {"Pilihan 1": a, "Pilihan 2": b, "Pilihan 3": c, "Pilihan 4": d}
                    st.session_state.draft_soal.append({
                        "question": soal,
                        "options": [a, b, c, d],
                        "answer": mapping[kunci]
                    })
                    st.success("Soal berhasil ditambahkan ke draft!")
                    st.rerun()
                else:
                    st.error("Semua kolom pertanyaan dan pilihan wajib diisi!")

            st.write(f"**Draft Soal Dibuat:** {len(st.session_state.draft_soal)} Soal")

            if len(st.session_state.draft_soal) > 0:
                if st.button("🚀 TERBITKAN GAME & GENERATE PIN", type="primary", key="btn_publish"):
                    kode_pin = ''.join(random.choices(string.digits, k=6))
                    
                    room_data = {
                        "owner": st.session_state.logged_user,
                        "status": "WAITING",
                        "mode": mode_game,
                        "soal": list(st.session_state.draft_soal),
                        "players": {}
                    }
                    save_room(kode_pin, room_data)

                    st.session_state.draft_soal = []
                    st.success(f"🎉 Game Berhasil Diterbitkan!\n\n🔑 BAGIKAN KODE PIN INI KE PEMAIN: **{kode_pin}**")
