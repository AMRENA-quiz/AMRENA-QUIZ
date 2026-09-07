import random
import string
import json
import os
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

# --- SISTEM DATABASE PENYIMPANAN SERVER (JSON) ---
DB_FILE = "rooms_db.json"

def get_rooms():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_room(pin, data):
    rooms = get_rooms()
    rooms[pin] = data
    with open(DB_FILE, "w") as f:
        json.dump(rooms, f)

# Preset Soal bawaan (PIN: 123456) agar selalu ada soal siap pakai
DEFAULT_ROOMS = {
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

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump(DEFAULT_ROOMS, f)

# Inisialisasi Session State
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
        st.markdown("<div class='role-card'><h3>👨‍💻 Pengembang (Host)</h3><p>Buat soal kuis kamu sendiri, pilih mode game, dan dapatkan Kode PIN.</p></div>", unsafe_allow_html=True)
        if st.button("Masuk sebagai Pengembang", use_container_width=True):
            st.session_state.user_role = "DEV"
            st.rerun()

    with col2:
        st.markdown("<div class='role-card'><h3>🎮 Anggota (Pemain)</h3><p>Masukkan Kode PIN dari Pengembang dan nama kamu untuk mulai bertualang.</p></div>", unsafe_allow_html=True)
        if st.button("Masuk sebagai Pemain", use_container_width=True):
            st.session_state.user_role = "PLAYER"
            st.rerun()

# ==========================================
# MODUL 1: PENGEMBANG (INPUT SOAL SENDIRI)
# ==========================================
elif st.session_state.user_role == "DEV":
    st.sidebar.title("👨‍💻 Pengembang")
    if st.sidebar.button("⬅️ Kembali ke Menu Utama"):
        st.session_state.user_role = None
        st.rerun()

    st.title("🛠️ Buat Kuis & Soal Sendiri")

    if "draft_soal" not in st.session_state:
        st.session_state.draft_soal = []

    mode_game = st.selectbox("🎮 Pilih Metode/Gaya Permainan:", ["🏔️ Petualangan Mendaki Gunung", "🎯 Mode Klasik (Kahoot Style)"])

    # Form Pembuatan Soal
    with st.form("form_buat_soal", clear_on_submit=True):
        st.subheader("Tambah Pertanyaan")
        soal = st.text_input("Pertanyaan:")
        a = st.text_input("Pilihan 1 (🔺 Merah):")
        b = st.text_input("Pilihan 2 (🔷 Biru):")
        c = st.text_input("Pilihan 3 (🟡 Kuning):")
        d = st.text_input("Pilihan 4 (🟩 Hijau):")
        kunci = st.selectbox("Kunci Jawaban Benar:", ["Pilihan 1", "Pilihan 2", "Pilihan 3", "Pilihan 4"])

        if st.form_submit_button("➕ Tambahkan Soal ini"):
            if soal and a and b and c and d:
                mapping = {"Pilihan 1": a, "Pilihan 2": b, "Pilihan 3": c, "Pilihan 4": d}
                st.session_state.draft_soal.append({
                    "question": soal,
                    "options": [a, b, c, d],
                    "answer": mapping[kunci]
                })
                st.success("Soal berhasil ditambahkan ke daftar draft!")
            else:
                st.error("Semua kolom (pertanyaan & 4 pilihan) wajib diisi!")

    st.divider()
    st.write(f"**Jumlah Soal Dibuat Saat Ini:** {len(st.session_state.draft_soal)} Soal")

    # Tampilkan Preview Soal
    for idx, s in enumerate(st.session_state.draft_soal):
        st.write(f"{idx+1}. **{s['question']}** (Kunci: {s['answer']})")

    # Terbitkan Kuis & Bikin PIN
    if len(st.session_state.draft_soal) > 0:
        if st.button("🚀 TERBITKAN GAME & BUAT KODE PIN", type="primary"):
            kode_pin = ''.join(random.choices(string.digits, k=6))
            
            # Simpan ke File Database Server
            room_data = {
                "mode": mode_game,
                "soal": list(st.session_state.draft_soal)
            }
            save_room(kode_pin, room_data)

            st.session_state.draft_soal = []
            st.success(f"🎉 Game Berhasil Diterbitkan!\n\n🔑 BAGIKAN KODE PIN INI KE PEMAIN: **{kode_pin}**")

    # Tampilkan Daftar Semua Room Aktif
    all_rooms = get_rooms()
    if all_rooms:
        st.subheader("📋 Daftar PIN Game Aktif:")
        for pin_code, r_info in all_rooms.items():
            st.info(f"🔑 PIN: **{pin_code}** | Mode: {r_info['mode']} | Total Soal: {len(r_info['soal'])}")

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
        input_pin = st.text_input("Masukkan Kode PIN Game:", max_chars=6)
        input_nama = st.text_input("Masukkan Nama Kamu:")

        if st.button("🚀 MULAI PETUALANGAN", type="primary"):
            active_rooms = get_rooms()
            if input_pin in active_rooms:
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
                st.error("Kode PIN tidak ditemukan! Pastikan Pengembang sudah menekan tombol 'Terbitkan Game'.")

    # LAYAR 2: PENGERJAAN QUIZ
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
        active_rooms = get_rooms()
        mode = active_rooms[pin]["mode"] if pin in active_rooms else "Kuis"
        
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
            
