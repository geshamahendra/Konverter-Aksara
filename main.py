import subprocess
import sys
import os

root_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(root_path)

# Daftar file Python yang ingin dijalankan satu per satu
file_list = ["skrip/latin_ke_jtwk.py", "skrip/jtwk_ke_jawa.py", "skrip/jawa_ke_bali.py", "skrip/jawa_ke_kawi.py", "skrip/jtwk_ke_jawarepha.py", "skrip/jtwk_ke_latin_normal.py", "skrip/jtwk_ke_jawadhuwung.py"]

for file in file_list:
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = root_path
        
        subprocess.run(["python3", file], check=True, env=env)
        print(f"{file} selesai dijalankan.")
    except subprocess.CalledProcessError as e:
        print(f"Error terjadi saat menjalankan {file}: {e}")
        break  # Hentikan jika ada error
