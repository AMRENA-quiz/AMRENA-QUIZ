import random
import string
import json
import os
import time
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="QUIZ'ARN", page_icon="🏔️", layout="centered")

# --- CUSTOM CSS DENGAN PERBAIKAN KONTRAS TEKS & FORM ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e1b4b, #311042, #0f172a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #ffffff;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* FIX TERUTAMA: TEKS INPUT, TEXTAREA, DAN SELECTBOX AGAR JERNIH DAN KONTRAS */
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

    /* TAB DENGAN TEKS TERANG */
    .stTabs [data-baseweb="tab-list"] button {
        color: #94a3b8 !important;
        font-weight: 700 !important;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #38bdf8 !important;
        border-bottom-color: #38bdf8 !important;
    }

    .role-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
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
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        border: 3px solid #38bdf8;
    }

    .climb-box {
        background: rgba(15, 23, 42, 0.85);
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 25px;
        border: 2px solid #f59e0b;
        color: #fbbf24;
    }

    .rank-card {
        background: rgba(255, 255, 255, 0.08);
        padding: 15px 25px;
        border-radius: 15px;
        margin-bottom: 12px;
        border-left: 8px solid #38bdf8;
        font-size: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .my-rank {
        background: rgba(245, 158, 11, 0.25) !important;
        border-left: 8px solid #fbbf24 !important;
        border: 2px solid #fbbf24;
    }

    .waiting-box {
        background: rgba(255, 255, 255, 0.05);
        border: 2px dashed #f59e0b;
        padding: 35px;
        border-radius: 20px;
        text-align: center;
        margin-top: 20px;
    }

    .stButton>button {
        border-radius: 12px !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- FUNKSI TEXT-TO-SPEECH ---
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
DB_FILE = "rooms_db.json"

def get_rooms():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_all_rooms(rooms):
    with open(DB_FILE, "w") as f:
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

DEFAULT_ROOMS = {
    "123456": {
        "status": "WAITING",
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
            }
        ],
        "players": {}
    }
}

if not os.path.exists(DB_FILE):
    save_all_rooms(DEFAULT_ROOMS)

# Inisialisasi State Peringkat
if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "game_state" not in st.session_state:
    st.session_state.game_state = "LOBBY"

if "last_ranks" not in st.session_state:
    st.session_state.last_ranks = {}

# ==========================================
# HALAMAN UTAMA: PILIH PERAN
# ==========================================
if st.session_state.user_role is None:
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        else:
            st.markdown("<h1 style='text-align: center; color: #38bdf8; font-size: 42px; font-weight: 800;'>🏔️ QUIZ'ARN</h1>", unsafe_allow_html=True)
            
    st.markdown("<p style='text-align: center; color: #cbd5e1; font-size: 18px;'>Game Kuis Interaktif & Petualangan Mendaki Gunung</p>", unsafe_allow_html=True)
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='role-card'><h3>👨‍💻 Pengembang (Host)</h3><p style='color:#cbd5e1;'>Kelola soal, hapus kuis/pemain, dan pantau klasemen live.</p></div>", unsafe_allow_html=True)
        if st.button("Masuk sebagai Pengembang", use_container_width=True):
            st.session_state.user_role = "DEV"
            st.rerun()

    with col2:
        st.markdown("<div class='role-card'><h3>🎮 Anggota (Pemain)</h3><p style='color:#cbd5e1;'>Pilih avatar jagoanmu, masukkan PIN, dan raih puncak gunung!</p></div>", unsafe_allow_html=True)
        if st.button("Masuk sebagai Pemain", use_container_width=True):
            st.session_state.user_role = "PLAYER"
            st.rerun()

# ==========================================
# MODUL 1: PENGEMBANG (CONTROL ROOM & EDIT)
# ==========================================
elif st.session_state.user_role == "DEV":
    st.sidebar.title("👨‍💻 Pengembang")
    if st.sidebar.button("⬅️ Kembali ke Menu Utama"):
        st.session_state.user_role = None
        st.rerun()

    st.title("🛠️ Control Room Pengembang")

    tab1, tab2, tab3 = st.tabs(["🎮 Kontrol & Live Leaderboard", "✏️ Kelola & Edit / Hapus Data", "➕ Buat Kuis Baru"])

    # --- TAB 1: KONTROL GAME & LIVE LEADERBOARD ---
    with tab1:
        st.subheader("📡 Live Leaderboard & Kontrol Game")
        all_rooms = get_rooms()
        if all_rooms:
            selected_pin = st.selectbox("Pilih Kode PIN Game:", list(all_rooms.keys()), key="select_pin_tab1")
            
            room = all_rooms[selected_pin]
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
                            av = p_info.get("avatar", "🧑‍🚀")
                            st.success(f"**{podium_icons[idx]}**: {av} **{p_name}** | Skor: **{p_info['score']} Poin** ({p_info['altitude']}m)")

                        if len(sorted_players) > 3:
                            st.subheader("📋 Pemain Lainnya:")
                            for idx, (p_name, p_info) in enumerate(sorted_players[3:], start=4):
                                av = p_info.get("avatar", "🧑‍🚀")
                                st.write(f"**#{idx}** {av} **{p_name}** — {p_info['score']} Poin ({p_info['altitude']}m)")
                    else:
                        st.info("Belum ada pemain yang masuk/menyelesaikan kuis.")

            update_leaderboard_live()

            if is_live:
                time.sleep(3)
                st.rerun()

        else:
            st.warning("Belum ada Kuis yang diterbitkan.")

    # --- TAB 2: EDIT & HAPUS (LOGIKA TERBAIKI TANPA FORM CRASH) ---
    with tab2:
        st.subheader("⚙️ Kelola, Edit & Hapus Kuis / Pemain")
        all_rooms = get_rooms()
        if all_rooms:
            edit_pin = st.selectbox("Pilih Kuis (PIN) yang Ingin Dikelola:", list(all_rooms.keys()), key="select_pin_tab2")
            room_to_edit = all_rooms[edit_pin]
            soal_list = room_to_edit.get("soal", [])
            players_in_room = room_to_edit.get("players", {})

            # 1. HAPUS KUIS
            with st.expander("🚨 HAPUS KUIS / ROOM INI SEUTUHMUS", expanded=False):
                st.error(f"⚠️ Hapus PIN {edit_pin} beserta seluruh data kuis dan pemain secara permanen.")
                if st.button(f"🗑️ Hapus Kuis PIN {edit_pin} Sekarang", type="primary", key="btn_del_room"):
                    del all_rooms[edit_pin]
                    save_all_rooms(all_rooms)
                    st.success(f"Kuis PIN {edit_pin} berhasil dihapus!")
                    st.rerun()

            st.divider()

            # 2. KELOLA & HAPUS PEMAIN
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

                if st.button("🔄 Reset Semua Pemain", key="btn_reset_all_players"):
                    all_rooms[edit_pin]["players"] = {}
                    save_all_rooms(all_rooms)
                    st.warning("Semua data pemain di kuis ini telah di-reset!")
                    st.rerun()
            else:
                st.info("Belum ada pemain di kuis ini.")

            st.divider()

            # 3. KELOLA & EDIT / HAPUS SOAL
            st.write("### 📝 Edit / Hapus Soal")
            st.info(f"Kuis **PIN {edit_pin}** memiliki **{len(soal_list)} soal**.")

            # TAMBAH SOAL BARU
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

            # DAFTAR SOAL TERTERA (EDIT ATAU HAPUS PER SOAL)
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
                        if st.button("💾 Simpan Perubahan Soal", key=f"btn_upd_{edit_pin}_{idx}"):
                            mapping = {"Pilihan 1": eo1, "Pilihan 2": eo2, "Pilihan 3": eo3, "Pilihan 4": eo4}
                            all_rooms[edit_pin]["soal"][idx] = {
                                "question": eq,
                                "options": [eo1, eo2, eo3, eo4],
                                "answer": mapping[eans]
                            }
                            save_all_rooms(all_rooms)
                            st.success(f"Soal #{idx+1} berhasil diperbarui!")
                            st.rerun()

                    with col_delete:
                        if st.button("🗑️ Hapus Soal Ini", key=f"btn_del_q_{edit_pin}_{idx}"):
                            all_rooms[edit_pin]["soal"].pop(idx)
                            save_all_rooms(all_rooms)
                            st.warning(f"Soal #{idx+1} berhasil dihapus!")
                            st.rerun()
        else:
            st.warning("Belum ada Kuis yang tersedia untuk dikelola.")

    # --- TAB 3: BUAT KUIS BARU ---
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
                    "status": "WAITING",
                    "mode": mode_game,
                    "soal": list(st.session_state.draft_soal),
                    "players": {}
                }
                save_room(kode_pin, room_data)

                st.session_state.draft_soal = []
                st.success(f"🎉 Game Berhasil Diterbitkan!\n\n🔑 BAGIKAN KODE PIN INI KE PEMAIN: **{kode_pin}**")

# ==========================================
# MODUL 2: ANGGOTA / PEMAIN
# ==========================================
elif st.session_state.user_role == "PLAYER":
    st.sidebar.title("🎮 Pemain")
    if st.sidebar.button("⬅️ Keluar ke Menu Utama"):
        st.session_state.user_role = None
        st.session_state.game_state = "LOBBY"
        st.rerun()

    if st.session_state.game_state == "LOBBY":
        st.title("🎯 Masuk ke Game Kuis")
        
        input_pin = st.text_input("Masukkan Kode PIN Game:", max_chars=6, key="p_pin")
        input_nama = st.text_input("Masukkan Nama Kamu:", key="p_name")

        st.write("### 🧙‍♂️ Pilih Karakter Kamu:")
        avatars = [
            "🧗‍♂️ Pendaki Expert", "🧙‍♂️ Penyihir", "🥷 Ninja", 
            "🧑‍🚀 Astronaut", "🤠 Koboi", "🦁 Singa Berani", 
            "🤖 Robot Super", "🦸‍♂️ Super Hero"
        ]
        selected_avatar = st.selectbox("Pilih Avatar Karakter:", avatars, key="p_avatar")

        if st.button("🚀 MASUK RUANG TUNGGU", type="primary", key="p_enter"):
            active_rooms = get_rooms()
            if input_pin in active_rooms:
                if input_nama.strip():
                    st.session_state.active_pin = input_pin
                    st.session_state.player_name = input_nama.strip()
                    st.session_state.player_avatar = selected_avatar.split()[0]
                    st.session_state.current_q = 0
                    st.session_state.score = 0
                    st.session_state.altitude = 0
                    st.session_state.game_state = "WAITING_ROOM"
                    st.rerun()
                else:
                    st.warning("Nama tidak boleh kosong!")
            else:
                st.error("Kode PIN tidak ditemukan!")

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
        
        if "Mendaki" in mode:
            progress = (q_idx) / len(soal_list)
            st.markdown(f"""
                <div class='climb-box'>
                    🏕️ Ketinggian {st.session_state.player_avatar}: <b>{st.session_state.altitude} Meter</b> dari Puncak 🏔️
                </div>
            """, unsafe_allow_html=True)
            st.progress(progress, text=f"Progres Menuju Puncak Gunung ({q_idx}/{len(soal_list)} Soal)")

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
                st.success("✨ BENAR! Kamu makin dekat ke puncak gunung! (+500m)")
            else:
                st.error(f"❌ SALAH! Jawaban benar: {q_data['answer']}")

            submit_score(pin, st.session_state.player_name, st.session_state.player_avatar, st.session_state.score, st.session_state.altitude)

            if q_idx + 1 < len(soal_list):
                st.session_state.current_q += 1
                st.rerun()
            else:
                st.session_state.game_state = "RESULT"
                st.rerun()

    elif st.session_state.game_state == "RESULT":
        st.balloons()
        pin = st.session_state.active_pin
        active_rooms = get_rooms()
        mode = active_rooms[pin]["mode"] if pin in active_rooms else "Kuis"
        
        if "Mendaki" in mode:
            st.markdown("<h1 style='text-align: center; color: #fbbf24;'>🏔️ PENDAKIAN SELESAI! 🏆</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center; color: #f1f5f9;'>Selamat {st.session_state.player_avatar} {st.session_state.player_name}, kamu berhasil mencapai ketinggian {st.session_state.altitude} Meter!</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🏆 KUIS SELESAI 🏆</h1>", unsafe_allow_html=True)

        st.metric(label="Total Skor Poin Kamu", value=f"{st.session_state.score} Poin")

        st.divider()
        st.subheader("🏆 PAPAN PERINGKAT PEMAIN (LEADERBOARD)")

        if pin in active_rooms and "players" in active_rooms[pin]:
            players = active_rooms[pin]["players"]
            sorted_players = sorted(players.items(), key=lambda x: x[1]["score"], reverse=True)
            
            medals = ["🥇", "🥈", "🥉"]
            for idx, (p_name, p_info) in enumerate(sorted_players, start=1):
                icon = medals[idx-1] if idx <= 3 else f"#{idx}"
                is_me = (p_name == st.session_state.player_name)
                avatar = p_info.get("avatar", "🧑‍🚀")
                
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
            
