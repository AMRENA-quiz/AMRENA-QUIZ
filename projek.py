import random
import string
import json
import os
import streamlit as st

st.set_page_config(page_title="QUIZ'ARN", page_icon="🏔️", layout="centered")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; }
    .question-box { background-color: white; padding: 25px; border-radius: 15px; text-align: center; font-size: 24px; font-weight: bold; color: #222; margin-bottom: 20px; box-shadow: 0 8px 16px rgba(0,0,0,0.3); }
    .role-card { background: rgba(255, 255, 255, 0.15); backdrop-filter: blur(10px); padding: 20px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.3); margin-bottom: 20px; }
    .climb-box { background: rgba(0, 0, 0, 0.4); padding: 20px; border-radius: 15px; text-align: center; font-size: 20px; font-weight: bold; margin-bottom: 20px; border: 2px solid #ffd700; }
    .rank-card { background: rgba(255, 255, 255, 0.2); backdrop-filter: blur(5px); padding: 12px 20px; border-radius: 10px; margin-bottom: 8px; border-left: 6px solid #ffd700; font-size: 18px; }
    .my-rank { background: rgba(255, 215, 0, 0.3) !important; border: 2px solid #ffd700 !important; font-weight: bold; }
    .waiting-box { background: rgba(255, 255, 255, 0.1); border: 2px dashed #ffd700; padding: 30px; border-radius: 15px; text-align: center; margin-top: 20px; }
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

def save_all_rooms(rooms):
    with open(DB_FILE, "w") as f:
        json.dump(rooms, f)

def save_room(pin, data):
    rooms = get_rooms()
    rooms[pin] = data
    save_all_rooms(rooms)

def submit_score(pin, player_name, score, altitude):
    rooms = get_rooms()
    if pin in rooms:
        if "players" not in rooms[pin]:
            rooms[pin]["players"] = {}
        rooms[pin]["players"][player_name] = {
            "score": score,
            "altitude": altitude
        }
        save_all_rooms(rooms)

# Preset Soal bawaan (PIN: 123456)
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
            },
            {
                "question": "Warna campuran Biru dan Kuning adalah?",
                "options": ["Merah", "Hijau", "Ungu", "Cokelat"],
                "answer": "Hijau"
            }
        ],
        "players": {}
    }
}

if not os.path.exists(DB_FILE):
    save_all_rooms(DEFAULT_ROOMS)

# Inisialisasi Session State
if "user_role" not in st.session_state:
    st.session_state.user_role = None

if "game_state" not in st.session_state:
    st.session_state.game_state = "LOBBY"

# ==========================================
# HALAMAN UTAMA: PILIH PERAN
# ==========================================
if st.session_state.user_role is None:
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        else:
            st.markdown("<h1 style='text-align: center; color: white;'>🏔️ QUIZ'ARN</h1>", unsafe_allow_html=True)
            
    st.markdown("<p style='text-align: center; color: #f0f0f0;'>Pilih peran kamu untuk melanjutkan:</p>", unsafe_allow_html=True)
    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='role-card'><h3>👨‍💻 Pengembang (Host)</h3><p>Buat soal, edit soal yang ada, kontrol game, dan pantau Leaderboard.</p></div>", unsafe_allow_html=True)
        if st.button("Masuk sebagai Pengembang", use_container_width=True):
            st.session_state.user_role = "DEV"
            st.rerun()

    with col2:
        st.markdown("<div class='role-card'><h3>🎮 Anggota (Pemain)</h3><p>Masukkan Kode PIN dari Pengembang dan tunggu hingga game dimulai.</p></div>", unsafe_allow_html=True)
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

    tab1, tab2, tab3 = st.tabs(["🎮 Kontrol & Pantau Game", "✏️ Kelola & Edit Soal", "➕ Buat Kuis Baru"])

    # --- TAB 1: KONTROL GAME ---
    with tab1:
        st.subheader("📡 Kontrol Real-Time Game")
        all_rooms = get_rooms()
        if all_rooms:
            selected_pin = st.selectbox("Pilih Kode PIN Game:", list(all_rooms.keys()), key="select_pin_tab1")
            
            room = all_rooms[selected_pin]
            players_data = room.get("players", {})
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
                if st.button("🔄 Refresh Data Pemain", use_container_width=True):
                    st.rerun()

            st.divider()

            col_a, col_b = st.columns(2)
            col_a.metric("Jumlah Pemain Terdata", len(players_data))
            col_b.metric("Total Soal Dalam Game", len(room.get("soal", [])))

            st.divider()

            if players_data:
                sorted_players = sorted(players_data.items(), key=lambda x: x[1]["score"], reverse=True)
                st.subheader("🥇 LEADERBOARD PERINGKAT")
                podium_icons = ["🥇 Juara 1", "🥈 Juara 2", "🥉 Juara 3"]
                for idx, (p_name, p_info) in enumerate(sorted_players[:3]):
                    st.success(f"**{podium_icons[idx]}**: **{p_name}** | Skor: **{p_info['score']} Poin** ({p_info['altitude']}m)")

                if len(sorted_players) > 3:
                    st.subheader("📋 Pemain Lainnya:")
                    for idx, (p_name, p_info) in enumerate(sorted_players[3:], start=4):
                        st.write(f"**#{idx} {p_name}** — {p_info['score']} Poin ({p_info['altitude']}m)")
            else:
                st.info("Belum ada pemain yang menyelesaikan kuis ini.")
        else:
            st.warning("Belum ada Kuis yang diterbitkan.")

    # --- TAB 2: EDIT & TAMBAH SOAL DARI KUIS YANG SUDAH ADA ---
    with tab2:
        st.subheader("✏️ Edit & Tambah Soal Kuis")
        all_rooms = get_rooms()
        if all_rooms:
            edit_pin = st.selectbox("Pilih Kuis (PIN) yang Mau Di-edit:", list(all_rooms.keys()), key="select_pin_tab2")
            room_to_edit = all_rooms[edit_pin]
            soal_list = room_to_edit.get("soal", [])

            st.info(f"Kuis **PIN {edit_pin}** saat ini punya **{len(soal_list)} soal**.")

            # Form Tambah Soal Baru ke PIN ini
            with st.expander("➕ Tambah Soal Baru ke Kuis Ini"):
                with st.form("form_tambah_soal_pin"):
                    new_q = st.text_input("Pertanyaan Baru:")
                    o1 = st.text_input("Pilihan 1 (Merah):")
                    o2 = st.text_input("Pilihan 2 (Biru):")
                    o3 = st.text_input("Pilihan 3 (Kuning):")
                    o4 = st.text_input("Pilihan 4 (Hijau):")
                    ans_choice = st.selectbox("Kunci Jawaban:", ["Pilihan 1", "Pilihan 2", "Pilihan 3", "Pilihan 4"])

                    if st.form_submit_button("Simpan Soal Baru"):
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
                            st.error("Semua field wajib diisi!")

            st.divider()
            st.write("### 📝 Daftar Soal Saat Ini:")

            # Menampilkan & Mengedit Soal yang Sudah Ada
            for idx, item in enumerate(soal_list):
                with st.expander(f"Soal #{idx+1}: {item['question']}"):
                    with st.form(key=f"edit_form_{edit_pin}_{idx}"):
                        eq = st.text_input("Pertanyaan:", value=item["question"])
                        eo1 = st.text_input("Pilihan 1:", value=item["options"][0])
                        eo2 = st.text_input("Pilihan 2:", value=item["options"][1])
                        eo3 = st.text_input("Pilihan 3:", value=item["options"][2])
                        eo4 = st.text_input("Pilihan 4:", value=item["options"][3])

                        # Cari indeks jawaban benar saat ini
                        try:
                            curr_ans_idx = item["options"].index(item["answer"])
                        except ValueError:
                            curr_ans_idx = 0

                        eans = st.selectbox("Kunci Jawaban:", ["Pilihan 1", "Pilihan 2", "Pilihan 3", "Pilihan 4"], index=curr_ans_idx)

                        col_save, col_del = st.columns(2)
                        with col_save:
                            btn_update = st.form_submit_button("💾 Update Soal Ini")
                        with col_del:
                            btn_delete = st.form_submit_button("🗑️ Hapus Soal Ini")

                        if btn_update:
                            mapping = {"Pilihan 1": eo1, "Pilihan 2": eo2, "Pilihan 3": eo3, "Pilihan 4": eo4}
                            all_rooms[edit_pin]["soal"][idx] = {
                                "question": eq,
                                "options": [eo1, eo2, eo3, eo4],
                                "answer": mapping[eans]
                            }
                            save_all_rooms(all_rooms)
                            st.success(f"Soal #{idx+1} berhasil diperbarui!")
                            st.rerun()

                        if btn_delete:
                            all_rooms[edit_pin]["soal"].pop(idx)
                            save_all_rooms(all_rooms)
                            st.warning(f"Soal #{idx+1} berhasil dihapus!")
                            st.rerun()
        else:
            st.warning("Belum ada Kuis yang tersedia untuk di-edit.")

    # --- TAB 3: BUAT KUIS BARU ---
    with tab3:
        st.subheader("Buat Kuis Baru")
        if "draft_soal" not in st.session_state:
            st.session_state.draft_soal = []

        mode_game = st.selectbox("🎮 Pilih Metode Game:", ["🏔️ Petualangan Mendaki Gunung", "🎯 Mode Klasik (Kahoot Style)"])

        with st.form("form_buat_soal", clear_on_submit=True):
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
                    st.success("Soal berhasil ditambahkan ke draft!")
                else:
                    st.error("Semua kolom pertanyaan dan pilihan wajib diisi!")

        st.write(f"**Draft Soal Dibuat:** {len(st.session_state.draft_soal)} Soal")

        if len(st.session_state.draft_soal) > 0:
            if st.button("🚀 TERBITKAN GAME & BUAT KODE PIN", type="primary"):
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

    # LAYAR 1: INPUT PIN & NAMA
    if st.session_state.game_state == "LOBBY":
        st.title("🎯 Masuk ke Game Kuis")
        input_pin = st.text_input("Masukkan Kode PIN Game:", max_chars=6)
        input_nama = st.text_input("Masukkan Nama Kamu:")

        if st.button("🚀 MASUK RUANG TUNGGU", type="primary"):
            active_rooms = get_rooms()
            if input_pin in active_rooms:
                if input_nama.strip():
                    st.session_state.active_pin = input_pin
                    st.session_state.player_name = input_nama.strip()
                    st.session_state.current_q = 0
                    st.session_state.score = 0
                    st.session_state.altitude = 0
                    st.session_state.game_state = "WAITING_ROOM"
                    st.rerun()
                else:
                    st.warning("Nama tidak boleh kosong!")
            else:
                st.error("Kode PIN tidak ditemukan! Periksa kembali PIN kamu.")

    # LAYAR 2: RUANG TUNGGU
    elif st.session_state.game_state == "WAITING_ROOM":
        pin = st.session_state.active_pin
        active_rooms = get_rooms()

        if pin not in active_rooms:
            st.error("PIN tidak ditemukan!")
            st.session_state.game_state = "LOBBY"
            st.rerun()

        room_data = active_rooms[pin]
        status_game = room_data.get("status", "WAITING")

        if status_game == "STARTED":
            st.session_state.game_state = "PLAYING"
            st.rerun()

        st.markdown(f"""
            <div class='waiting-box'>
                <h2>⏳ MENUNGGU PENGEMBANG...</h2>
                <p>Halo <b>{st.session_state.player_name}</b>, kamu sudah berhasil masuk!</p>
                <p>Silakan tunggu Pengembang menekan tombol <b>'MULAI GAME'</b> di layar pengembang.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        if st.button("🔄 Cek Apakah Game Sudah Dimulai"):
            st.rerun()

    # LAYAR 3: PENGERJAAN QUIZ
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

            if q_idx + 1 < len(soal_list):
                st.session_state.current_q += 1
                st.rerun()
            else:
                submit_score(pin, st.session_state.player_name, st.session_state.score, st.session_state.altitude)
                st.session_state.game_state = "RESULT"
                st.rerun()

    # LAYAR 4: HASIL & PERINGKAT PEMAIN
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

        st.metric(label="Total Skor Poin Kamu", value=f"{st.session_state.score} Poin")

        st.divider()
        st.subheader("🏆 PAPAN PERINGKAT PEMAIN (LEADERBOARD)")
        
        if st.button("🔄 Perbarui Peringkat"):
            st.rerun()

        if pin in active_rooms and "players" in active_rooms[pin]:
            players = active_rooms[pin]["players"]
            sorted_players = sorted(players.items(), key=lambda x: x[1]["score"], reverse=True)
            
            medals = ["🥇", "🥈", "🥉"]
            my_rank = None

            for idx, (p_name, p_info) in enumerate(sorted_players, start=1):
                icon = medals[idx-1] if idx <= 3 else f"#{idx}"
                is_me = (p_name == st.session_state.player_name)
                
                if is_me:
                    my_rank = idx
                    st.markdown(f"""
                        <div class='rank-card my-rank'>
                            <b>{icon} {p_name} (KAMU)</b> — {p_info['score']} Poin ({p_info['altitude']}m) ✨
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class='rank-card'>
                            <b>{icon} {p_name}</b> — {p_info['score']} Poin ({p_info['altitude']}m)
                        </div>
                    """, unsafe_allow_html=True)

            if my_rank:
                st.info(f"🎯 Posisi Kamu Saat Ini: **Peringkat ke-{my_rank}** dari **{len(sorted_players)} Pemain**")

        if st.button("🔄 Main Lagi", key="btn_play_again"):
            st.session_state.game_state = "LOBBY"
            st.rerun()
            
