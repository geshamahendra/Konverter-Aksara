import subprocess
import sys
import os
import time

root_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(root_path)

# Daftar file Python yang ingin dijalankan satu per satu
file_list = [
    "skrip/latin_ke_jtwk.py",
    #"skrip/jtwk_ke_latin_normal.py",
    "skrip/jtwk_ke_jawa.py",
    "skrip/jawa_ke_jawarepha.py",
    "skrip/jawa_ke_bali.py",
    "skrip/jawa_ke_kawi.py",
    "skrip/jawa_ke_jawadhuwung.py"
]

start_time = time.time()  # Mulai timer total

for file in file_list:
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = root_path

        file_start = time.time()  # Timer per file
        subprocess.run(["python3", file], check=True, env=env)
        file_end = time.time()

        duration = file_end - file_start
        print(f"{file} selesai dijalankan dalam {duration:.2f} detik.")

    except subprocess.CalledProcessError as e:
        print(f"Error terjadi saat menjalankan {file}: {e}")
        break  # Hentikan jika ada error

end_time = time.time()  # Akhiri timer total
total_time = end_time - start_time
print(f"\nTotal waktu eksekusi seluruh skrip: {total_time:.2f} detik")