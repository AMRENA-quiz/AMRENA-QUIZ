import streamlit as st

st.set_page_config(page_title="Game Quiz Interaktif", page_icon="🏔️", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; }
    .question-box { background-color: white; padding: 25px; border-radius: 15px; text-align: center; font-size: 24px; font-weight: bold; color: #222; margin-bottom: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.3); }
    .role-card { background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(10px); padding: 20px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.3); margin-bottom: 20px; }
    .climb-box { background: rgba(0, 0, 0, 0.4); padding: 20px; border-radius: 15px; text-align: center; font-size: 20px; font-weight: bold; margin-bottom: 20px; border: 2px solid #ffd700; }
    div[key="btn_0"] > button { background-color: #e21b3c !important; color: white !important; height: 70px; font-size: 18px; font-weight: bold; border-radius: 10px; border: none; }
    div[key="btn_1"] > button { background-color: #1368ce !important; color: white !important; height: 70px; font-size: 18px; font-weight: bold; border-radius: 10px; border: none; }
    div[key="btn_2"] > button { background-color: #d89e00 !important; color: white !important; height: 70px; font-size: 18px; font-weight: bold; border-radius: 10px; border: none; }
    div[key="btn_3"] > button { background-color: #26890c !important; color: white !important; height: 70px; font-size: 18px; font-weight: bold; border-radius: 10px; border: none; }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE SOAL PERMANEN ---
PRESET_ROOMS = {
    "123456": {
        "mode": "🏔️ Petualangan Mendaki Gunung",
        "soal": [
            {
                "question": "Apa ibu kota negara Indonesia saat ini?",
                "options": ["Jakarta", "Nusantara", "Bandung", "Surabaya"],
                "answer": "Jakarta"
            },
            {
                "question": "Berapakah hasil dari 15 x 4?",
                "options": ["50", "55", "60", "65"],
                "answer": "60"
            },
            {
                "question": "Warna campuran Biru dan Kuning adalah?",
                "options": ["Merah", "Hijau", "Ungu", "Cokelat"],
                "answer": "Hijau"
            }
        ]
    }
}

if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "game_state" not in st.session_state:
    st.session_state.game_state = "LOBBY"

# ==========================================
# HALAMAN UTAMA: PILIH PERAN
# ==========================================
if st.session_state.user_role is None:
    st.markdown("<h1 style='text-align: center; color: white;'>🏔️ QUIZ ADVENTURE GAME</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #f0f0f0;'>Pilih peran kamu untuk melanjutkan:</p>", unsafe_allow_html=True)
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='role-card'><h3>👨‍💻 Pengembang (Host)</h3><p>Lihat daftar PIN aktif dan instruksi game.</p></div>", unsafe_allow_html=True)
        if st.button("Masuk sebagai Pengembang", use_container_width=True):
            st.session_state.user_role = "DEV"
            st.rerun()

    with col2:
        st.markdown("<div class='role-card'><h3>🎮 Anggota (Pemain)</h3><p>Masukkan Kode PIN dan nama kamu untuk mulai bermain.</p></div>", unsafe_allow_html=True)
        if st.button("Masuk sebagai Pemain", use_container_width=True):
            st.session_state.user_role = "PLAYER"
            st.rerun()

# ==========================================
# MODUL 1: PENGEMBANG
# ==========================================
elif st.session_state.user_role == "DEV":
    st.sidebar.title("👨‍💻 Pengembang")
    if st.sidebar.button("⬅️ Kembali ke Menu Utama"):
        st.session_state.user_role = None
        st.rerun()

    st.title("📋 Daftar Kode PIN Aktif")
    st.success("🔑 PIN AKTIF UTAMA: **123456**")
    st.info("Gunakan PIN **123456** di HP pemain untuk langsung mencoba kuis pendakian gunung!")

# ==========================================
# MODUL 2: ANGGOTA / PEMAIN
# ==========================================
elif st.session_state.user_role == "PLAYER":
    st.sidebar.title("🎮 Pemain")
    if st.sidebar.button("⬅️ Keluar ke Menu Utama"):
        st.session_state.user_role = None
        st.session_state.game_state = "LOBBY"
        st.rerun()

    # LAYAR 1: LOBBY
    if st.session_state.game_state == "LOBBY":
        st.title("🎯 Masuk ke Game Kuis")
        input_pin = st.text_input("Masukkan Kode PIN Game (Contoh: 123456):", max_chars=6)
        input_nama = st.text_input("Masukkan Nama Kamu:")

        if st.button("🚀 MULAI PETUALANGAN", type="primary"):
            if input_pin in PRESET_ROOMS:
                if input_nama.strip():
                    st.session_state.active_pin = input_pin
                    st.session_state.player_name = input_nama
                    st.session_state.current_q = 0
                    st.session_state.score = 0
                    st.session_state.altitude = 0
                    st.session_state.game_state = "PLAYING"
                    st.rerun()
                else:
                    st.warning("Nama tidak boleh kosong!")
            else:
                st.error("Kode PIN salah! Masukkan kode PIN aktif: **123456**")

    # LAYAR 2: PENGERJAAN QUIZ
    elif st.session_state.game_state == "PLAYING":
        pin = st.session_state.active_pin
        room_data = PRESET_ROOMS[pin]
        soal_list = room_data["soal"]
        mode = room_data["mode"]
        q_idx = st.session_state.current_q
        q_data = soal_list[q_idx]

        st.caption(f"Pemain: **{st.session_state.player_name}** | Mode: **{mode}** | Kode PIN: **{pin}**")
        
        if "Mendaki" in mode:
            progress = (q_idx) / len(soal_list)
            st.markdown(f"""
                <div class='climb-box'>
                    🏕️ Ketinggian Pendakian: <b>{st.session_state.altitude} Meter</b> dari Puncak 🏔️
                </div>
            """, unsafe_allow_html=True)
            st.progress(progress, text=f"Progres Menuju Puncak Gunung ({q_idx}/{len(soal_list)} Soal)")

        st.markdown(f"<div class='question-box'>{q_data['question']}</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        user_choice = None

        with col1:
            if st.button(f"🔺 {q_data['options'][0]}", key="btn_0", use_container_width=True):
                user_choice = q_data['options'][0]
            if st.button(f"🔷 {q_data['options'][1]}", key="btn_1", use_container_width=True):
                user_choice = q_data['options'][1]

        with col2:
            if st.button(f"🟡 {q_data['options'][2]}", key="btn_2", use_container_width=True):
                user_choice = q_data['options'][2]
            if st.button(f"🟩 {q_data['options'][3]}", key="btn_3", use_container_width=True):
                user_choice = q_data['options'][3]

        if user_choice:
            if user_choice == q_data["answer"]:
                st.session_state.score += 1000
                st.session_state.altitude += 500
                st.success("✨ BENAR! Kamu makin dekat ke puncak gunung! (+500m)")
            else:
                st.error(f"❌ SALAH! Jawaban benar: {q_data['answer']}")

            if q_idx + 1 < len(soal_list):
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.session_state.game_state = "RESULT"
                st.rerun()

    # LAYAR 3: HASIL
    elif st.session_state.game_state == "RESULT":
        st.balloons()
        pin = st.session_state.active_pin
        room_data = PRESET_ROOMS[pin]
        mode = room_data["mode"]
        
        if "Mendaki" in mode:
            st.markdown("<h1 style='text-align: center; color: white;'>🏔️ PENDAKIAN SELESAI! 🏆</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: white;'>Selamat {st.session_state.player_name}, kamu berhasil mencapai ketinggian {st.session_state.altitude} Meter!</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h1 style='text-align: center; color: white;'>🏆 KUIS SELESAI 🏆</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: white;'>Kerja Bagus, {st.session_state.player_name}!</h3>", unsafe_allow_html=True)

        st.metric(label="Total Skor Poin", value=f"{st.session_state.score} Poin")

        if st.button("🔄 Main Lagi"):
            st.session_state.game_state = "LOBBY"
            st.rerun()
            
