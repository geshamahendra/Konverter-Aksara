import grapheme
import sys
import os
import re

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

def insert_spaces_by_cursor(text):
    # Pisahkan berdasarkan grapheme cluster dan tambahkan spasi antar karakter
    result = ' '.join(grapheme.graphemes(text))
    
    # Hapus spasi di sekitar karakter tertentu
    target_chars = "꧀꧈꧉꧊꧋꧌꧍꧁꧂꧃꧄꧅꧐꧑꧒꧓꧔꧕꧖꧗꧘꧙‍꧇᭄᭞᭟᭚᭽꧌꧍᭛᭜᭾᭐᭑᭒᭓᭔᭕᭖᭗᭘᭙‍᭝𑽁𑽉𑽊𑽃𑽄꧌꧍𑽇𑽍𑽅𑽆𑽐𑽑𑽒𑽓𑽔𑽕𑽖𑽗𑽘𑽙‍𑽋𑽂"  # Karakter yang tidak boleh memiliki spasi di sekitarnya
    pattern = rf"(?<=[{target_chars}])[ \t]+|[ \t]+(?=[{target_chars}])"  # Hanya spasi & tab, bukan newline
    result = re.sub(pattern, '', result)

    # Hapus spasi setelah '꧀'
    #result = re.sub(r'꧀ ', '꧀', result)
    #result = re.sub(r' ꧉', '꧉', result)
    #result = re.sub(r' ꧈', '꧈', result)
    #result = re.sub(r'', '꧀', result)

    return result

def process_file(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        processed_text = insert_spaces_by_cursor(text)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed_text)
        
        print(f"Processing complete! Output saved to: {output_file}")
    
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Contoh penggunaan
input_file = "pengolah_output/input_spasi.txt"
output_file = "pengolah_output/output_spasi.txt"

process_file(input_file, output_file)
