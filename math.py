import time

import random

import os



# Warna ANSI

RED = "\033[31m"

GREEN = "\033[32m"

YELLOW = "\033[33m"

CYAN = "\033[36m"

RESET = "\033[0m"



TOTAL_SOAL = 50

BATAS_WAKTU = 10 * 60  # 10 menit



# Lokasi folder score di tempat file ini berada

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FOLDER = os.path.join(BASE_DIR, "scores")





def ensure_score_folder():

    """Pastikan folder scores ada"""

    if not os.path.exists(FOLDER):

        os.makedirs(FOLDER)





def get_user_file(nama):

    safe = "".join(c for c in nama if c.isalnum() or c in "-_").lower()

    return os.path.join(FOLDER, f"{safe}.txt")





def load_highscore():

    """Ambil high score dari semua pemain"""

    ensure_score_folder()

    highest = 0

    

    # Periksa apakah folder ada dan berisi file

    if not os.path.exists(FOLDER) or not os.listdir(FOLDER):

        return 0

        

    for file in os.listdir(FOLDER):

        path = os.path.join(FOLDER, file)

        if os.path.isfile(path) and file.endswith('.txt'):

            try:

                with open(path, "r") as f:

                    for line in f:

                        line = line.strip()

                        if line.isdigit():

                            nilai = int(line)

                            if nilai > highest:

                                highest = nilai

            except (IOError, ValueError):

                continue

    return highest





def save_score(nama, nilai):

    """Simpan nilai pemain ke file masing-masing"""

    ensure_score_folder()

    filepath = get_user_file(nama)

    with open(filepath, "a") as f:

        f.write(str(nilai) + "\n")





def show_leaderboard():

    """Tampilkan 5 pemain terbaik"""

    ensure_score_folder()

    scores = []

    

    if not os.path.exists(FOLDER):

        print(f"{YELLOW}Belum ada data pemain!{RESET}")

        return

        

    for file in os.listdir(FOLDER):

        path = os.path.join(FOLDER, file)

        if os.path.isfile(path) and file.endswith('.txt'):

            nama_user = file[:-4]  # Remove .txt

            try:

                with open(path, "r") as f:

                    for line in f:

                        line = line.strip()

                        if line.isdigit():

                            scores.append((nama_user, int(line)))

            except (IOError, ValueError):

                continue

    

    if not scores:

        print(f"{YELLOW}Belum ada data skor!{RESET}")

        return

    

    # Urutkan dan ambil 5 terbaik

    scores.sort(key=lambda x: x[1], reverse=True)

    

    print(f"{YELLOW}\n=== LEADERBOARD TOP 5 ==={RESET}")

    for I, (name, score) in enumerate(scores[:5], 1):

        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🎖"

        color = GREEN if I == 1 else YELLOW if I == 2 else CYAN if I == 3 else RESET

        print(f"{color}{medal} {I}. {name}: {score}{RESET}")





def main_game():

    print(f"{YELLOW}=== MATH QUIZ CHALLENGE ==={RESET}")

    nama = input(f"{CYAN}Masukkan nama kamu: {RESET}").strip()



    if not nama:

        nama = "Player"



    print(f"{YELLOW}\nHalo {GREEN}{nama}{YELLOW}! Siap untuk 50 soal dalam 10 menit?\n{RESET}")

    print(f"{CYAN}Kerjakan sebanyak mungkin sebelum waktu habis!{RESET}")

    print(f"{YELLOW}Ketik 'skip' untuk melewati soal, 'quit' untuk berhenti{RESET}\n")



    benar = 0

    salah = 0

    skipped = 0



    start_time = time.time()



    try:

        for I in range(1, TOTAL_SOAL + 1):

            # Hitung waktu tersisa

            elapsed_time = time.time() - start_time

            waktu_tersisa = BATAS_WAKTU - elapsed_time

            

            if waktu_tersisa <= 0:

                print(f"{RED}\n⏳ Waktu habis!{RESET}")

                break



            # Tampilkan progress dan waktu

            print(f"{CYAN}Soal {I}/{TOTAL_SOAL} | Waktu tersisa: {int(waktu_tersisa//60)}:{int(waktu_tersisa%60):02d} | Benar: {benar} | Salah: {salah}{RESET}")

            

            # Generate soal

            a = random.randint(1, 100)

            b = random.randint(1, 100)

            operasi = random.choice(["+", "-", "*"])



            if operasi == "+":

                jawaban_benar = a + b

            elif operasi == "-":

                jawaban_benar = a - b

            else:

                jawaban_benar = a * b



            print(f"{YELLOW}{a} {operasi} {b} = ?{RESET}")



            try:

                jawab = input("Jawab: ").strip()

                

                # Handle skip/quit

                if jawab.lower() in ['skip', 'lewati']:

                    print(f"{YELLOW}Soal dilewati{RESET}\n")

                    skipped += 1

                    continue

                elif jawab.lower() in ['quit', 'keluar', 'stop', 'berhenti']:

                    print(f"{YELLOW}Kuis dihentikan oleh user{RESET}\n")

                    break

                    

                if jawab.lstrip("-").isdigit():

                    if int(jawab) == jawaban_benar:

                        print(f"{GREEN}✔ Benar!{RESET}\n")

                        benar += 1

                    else:

                        print(f"{RED}✘ Salah! Jawaban benar: {jawaban_benar}{RESET}\n")

                        salah += 1

                else:

                    print(f"{RED}✘ Input tidak valid! Dihitung salah.{RESET}\n")

                    salah += 1

                    

            except KeyboardInterrupt:

                print(f"{YELLOW}\nKuis dihentikan oleh user{RESET}")

                break

                

    except KeyboardInterrupt:

        print(f"{YELLOW}\nKuis dihentikan{RESET}")



    # Hitung nilai akhir

    total_dikerjakan = benar + salah

    if total_dikerjakan > 0:

        nilai = int((benar / total_dikerjakan) * 100)

    else:

        nilai = 0



    elapsed_time = time.time() - start_time

    waktu_str = f"{int(elapsed_time//60)}:{int(elapsed_time%60):02d}"



    # Tampilkan hasil akhir

    print(f"{YELLOW}\n=== HASIL AKHIR — {GREEN}{nama}{YELLOW} ==={RESET}")

    print(f"{GREEN}Benar: {benar}{RESET}")

    print(f"{RED}Salah: {salah}{RESET}")

    if skipped > 0:

        print(f"{YELLOW}Dilewati: {skipped}{RESET}")

    print(f"{CYAN}Nilai Akhir: {nilai}{RESET}")

    print(f"{CYAN}Waktu: {waktu_str}{RESET}")



    # Simpan skor

    save_score(nama, nilai)



    # Tampilkan highscore global

    global_high = load_highscore()

    print(f"{YELLOW}\n== HIGH SCORE SYSTEM =={RESET}")

    print(f"{CYAN}High Score Global: {global_high}{RESET}")



    if nilai > global_high:

        print(f"{GREEN}🎉 KAMU MEMECAHKAN HIGH SCORE GLOBAL!{RESET}")

    elif nilai == global_high and nilai > 0:

        print(f"{YELLOW}🎯 Sama dengan high score global!{RESET}")

    elif nilai < global_high and global_high > 0:

        print(f"{YELLOW}💪 Butuh {global_high - nilai + 1} point lagi untuk menang!{RESET}")



    return nilai





def show_rules():

    """Tampilkan aturan permainan"""

    print(f"{YELLOW}\n=== ATURAN PERMAINAN ==={RESET}")

    print(f"{CYAN}• 50 soal matematika (+, -, ×){RESET}")

    print(f"{CYAN}• Waktu: 10 menit{RESET}")

    print(f"{CYAN}• Nilai = (Jawaban Benar / Total Dikerjakan) × 100{RESET}")

    print(f"{CYAN}• Ketik 'skip' untuk melewati soal{RESET}")

    print(f"{CYAN}• Ketik 'quit' untuk berhenti lebih awal{RESET}")

    print(f"{CYAN}• Skor disimpan otomatis{RESET}")





# =====================

#      MENU UTAMA

# =====================

def main():

    while True:

        ensure_score_folder()

        print(f"{YELLOW}\n=== MATH QUIZ CHALLENGE ==={RESET}")

        print(f"{CYAN}1. Main Game{RESET}")

        print(f"{CYAN}2. Lihat Leaderboard{RESET}")

        print(f"{CYAN}3. Aturan Permainan{RESET}")

        print(f"{CYAN}4. Keluar{RESET}")

        

        pilihan = input(f"{YELLOW}Pilih menu (1-4): {RESET}").strip()

        

        if pilihan == "1":

            main_game()

        elif pilihan == "2":

            show_leaderboard()

        elif pilihan == "3":

            show_rules()

        elif pilihan == "4":

            print(f"{CYAN}Terima kasih sudah bermain!{RESET}")

            break

        else:

            print(f"{RED}Pilihan tidak valid!{RESET}")

        

        input(f"{YELLOW}Tekan Enter untuk melanjutkan…{RESET}")





if __name__ == "__main__":

    main()