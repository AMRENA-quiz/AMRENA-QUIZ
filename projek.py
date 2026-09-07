import random
import string
import streamlit as st

st.set_page_config(page_title="Game Quiz Interaktif", page_icon="🏔️", layout="centered")

# --- CUSTOM CSS (Styling Background & Game Effects) ---
st.markdown("""
    <style>
    /* Background Gradient Menarik */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    
    /* Box Pertanyaan */
    .question-box {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: #222;
        margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }
    
    /* Card Container Tampilan Awal */
    .role-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        margin-bottom: 20px;
    }

    /* Box Indikator Pendakian Gunung */
    .climb-box {
        background: rgba(0, 0, 0, 0.4);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 20px;
        border: 2px solid #ffd700;
    }

    /* Kustomisasi 4 Tombol Pilihan Jawaban */
    div[key="btn_0"] > button { background-color: #e21b3c !important; color: white !important; height: 70px; font-size: 18px; font-weight: bold; border-radius: 10px; border: none; }
    div[key="btn_1"] > button { background-color: #1368ce !important; color: white !important; height: 70px; font-size: 18px; font-weight: bold; border-radius: 10px; border: none; }
    div[key="btn_2"] > button { background-color: #d89e00 !important; color: white !important; height: 70px; font-size: 18px; font-weight: bold; border-radius: 10px; border: none; }
    div[key="btn_3"] > button { background-color: #26890c !important; color: white !important; height: 70px; font-size: 18px; font-weight: bold; border-radius: 10px; border: none; }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE SEMENTARA (SESSION STATE) ---
if "rooms" not in st.session_state:
    st.session_state.rooms = {}  # Format: {"KODE_PIN": {"soal": [], "mode": "MENDAKI"}}

if "user_role" not in st.session_state:
    st.session_state.user_role = None  # None, "DEV", atau "PLAYER"

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
        st.markdown("<div class='role-card'><h3>👨‍💻 Pengembang (Host)</h3><p>Buat soal kuis, pilih metode game (Mendaki/Klasik), dan bagikan Kode PIN ke pemain.</p></div>", unsafe_allow_html=True)
        if st.button("Masuk sebagai Pengembang", use_container_width=True):
            st.session_state.user_role = "DEV"
            st.rerun()

    with col2:
        st.markdown("<div class='role-card'><h3>🎮 Anggota (Pemain)</h3><p>Masukkan Kode PIN dari pengembang dan nama kamu untuk mulai bertualang mengerjakan kuis.</p></div>", unsafe_allow_html=True)
        if st.button("Masuk sebagai Pemain", use_container_width=True):
            st.session_state.user_role = "PLAYER"
            st.rerun()

# ==========================================
# MODUL 1: PENGEMBANG (MEMBUAT SOAL & MODE GAME)
# ==========================================
elif st.session_state.user_role == "DEV":
    st.sidebar.title("👨‍💻 Pengembang")
    if st.sidebar.button("⬅️ Kembali ke Menu Utama"):
        st.session_state.user_role = None
        st.rerun()

    st.title("🛠️ Pengaturan Kuis & Metode Game")

    # Inisialisasi draft soal untuk room baru
    if "draft_soal" not in st.session_state:
        st.session_state.draft_soal = []

    # Pilihan Metode Game
    mode_game = st.selectbox("🎮 Pilih Metode/Gaya Permainan:", ["🏔️ Petualangan Mendaki Gunung", "🎯 Mode Klasik (Kahoot Style)"])

    with st.form("form_buat_soal", clear_on_submit=True):
        st.subheader("Tambah Pertanyaan Baru")
        soal = st.text_input("Pertanyaan:")
        a = st.text_input("Pilihan 1 (🔺 Merah):")
        b = st.text_input("Pilihan 2 (🔷 Biru):")
        c = st.text_input("Pilihan 3 (🟡 Kuning):")
        d = st.text_input("Pilihan 4 (🟩 Hijau):")
        kunci = st.selectbox("Kunci Jawaban Benar:", ["Pilihan 1", "Pilihan 2", "Pilihan 3", "Pilihan 4"])

        if st.form_submit_button("➕ Tambah Soal ke Draft"):
            if soal and a and b and c and d:
                mapping = {"Pilihan 1": a, "Pilihan 2": b, "Pilihan 3": c, "Pilihan 4": d}
                st.session_state.draft_soal.append({
                    "question": soal,
                    "options": [a, b, c, d],
                    "answer": mapping[kunci]
                })
                st.success("Soal berhasil ditambahkan ke draft!")
            else:
                st.error("Semua kolom pertanyaan dan pilihan wajib diisi!")

    st.divider()
    st.write(f"**Draft Soal Saat Ini:** {len(st.session_state.draft_soal)} Soal")

    # Generate Kode PIN & Simpan Room
    if len(st.session_state.draft_soal) > 0:
        if st.button("🚀 Terbitkan Game & Dapatkan Kode PIN", type="primary"):
            kode_pin = ''.join(random.choices(string.digits, k=6))
            st.session_state.rooms[kode_pin] = {
                "soal": list(st.session_state.draft_soal),
                "mode": mode_game
            }
            st.session_state.draft_soal = []
            st.success(f"🎉 Game Berhasil Diterbitkan!\n\n🔑 BAGIKAN KODE PIN INI KE PEMAIN: **{kode_pin}**")

    # Daftar Room yang Aktif
    if st.session_state.rooms:
        st.subheader("📋 Daftar Kode Game Aktif:")
        for pin, room_info in st.session_state.rooms.items():
            st.info(f"🔑 Kode PIN: **{pin}** | Mode: {room_info['mode']} | Total Soal: {len(room_info['soal'])}")

# ==========================================
# MODUL 2: ANGGOTA / PEMAIN
# ==========================================
elif st.session_state.user_role == "PLAYER":
    st.sidebar.title("🎮 Pemain")
    if st.sidebar.button("⬅️ Keluar ke Menu Utama"):
        st.session_state.user_role = None
        st.session_state.game_state = "LOBBY"
        st.rerun()

    # LAYAR 1: LOBBY MASUK PIN
    if st.session_state.game_state == "LOBBY":
        st.title("🎯 Masuk ke Game Kuis")
        input_pin = st.text_input("Masukkan Kode PIN Game:", max_chars=6)
        input_nama = st.text_input("Masukkan Nama Kamu:")

        if st.button("🚀 MULAI PETUALANGAN", type="primary"):
            if input_pin in st.session_state.rooms:
                if input_nama.strip():
                    st.session_state.active_pin = input_pin
                    st.session_state.player_name = input_nama
                    st.session_state.current_q = 0
                    st.session_state.score = 0
                    st.session_state.altitude = 0  # Ketinggian untuk mode mendaki
                    st.session_state.game_state = "PLAYING"
                    st.rerun()
                else:
                    st.warning("Nama tidak boleh kosong!")
            else:
                st.error("Kode PIN tidak ditemukan! Minta kode yang benar ke Pengembang.")

    # LAYAR 2: PENGERJAAN QUIZ
    elif st.session_state.game_state == "PLAYING":
        pin = st.session_state.active_pin
        room_data = st.session_state.rooms[pin]
        soal_list = room_data["soal"]
        mode = room_data["mode"]
        q_idx = st.session_state.current_q
        q_data = soal_list[q_idx]

        st.caption(f"Pemain: **{st.session_state.player_name}** | Mode: **{mode}** | Kode PIN: **{pin}**")
        
        # --- TAMPILAN KHUSUS MODE MENDAKI GUNUNG ---
        if "Mendaki" in mode:
            progress = (q_idx) / len(soal_list)
            st.markdown(f"""
                <div class='climb-box'>
                    🏕️ Ketinggian Pendakian: <b>{st.session_state.altitude} Meter</b> dari Puncak 🏔️
                </div>
            """, unsafe_allow_html=True)
            st.progress(progress, text=f"Progres Menuju Puncak Gunung ({q_idx}/{len(soal_list)} Soal)")

        # Box Pertanyaan
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
                st.session_state.altitude += 500  # Tambah 500 meter per jawaban benar
                st.success("✨ BENAR! Kamu makin dekat ke puncak gunung! (+500m)")
            else:
                st.error(f"❌ SALAH! Kamu bertahan di posisi sekarang. Jawaban benar: {q_data['answer']}")

            if q_idx + 1 < len(soal_list):
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.session_state.game_state = "RESULT"
                st.rerun()

    # LAYAR 3: HASIL PENDAKIAN / SKOR AKHIR
    elif st.session_state.game_state == "RESULT":
        st.balloons()
        pin = st.session_state.active_pin
        room_data = st.session_state.rooms[pin]
        mode = room_data["mode"]
        
        if "Mendaki" in mode:
            st.markdown("<h1 style='text-align: center; color: white;'>🏔️ PENDAKIAN SELESAI! 🏆</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: white;'>Selamat {st.session_state.player_name}, kamu berhasil mencapai ketinggian {st.session_state.altitude} Meter!</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h1 style='text-align: center; color: white;'>🏆 KUIS SELESAI 🏆</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: white;'>Kerja Bagus, {st.session_state.player_name}!</h3>", unsafe_allow_html=True)

        st.metric(label="Total Skor Poin", value=f"{st.session_state.score} Poin")

        if st.button("🔄 Main Lagi / Coba Kode PIN Lain"):
            st.session_state.game_state = "LOBBY"
            st.rerun()