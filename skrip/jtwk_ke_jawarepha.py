import sys
import os
import re

# Tambahkan direktori proyek ke sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(root_path)

def latin_to_jawa(text, line_spacing):
    #text = re.sub(r'ṙ', 'r\u200D', text, flags=re.IGNORECASE)
    #text = re.sub(r'ꦫ꧀ꦪ', '~', text)
    text = re.sub(r'ꦪꦾꦂ', 'ꦫ꧀ꦪꦾ', text)
    text = re.sub(r'ꦫ꧀ꦮ', 'ꦫ꧀ꦮ\u200D', text)
    text = re.sub('ꦫ꧀ꦪ', 'ꦫꦾ', text)

    #text = re.sub(r'ꦿ', '꧀ꦫ', text, flags=re.IGNORECASE)
    #text = re.sub(r'ꦾ', '꧀ꦪ', text, flags=re.IGNORECASE)
    
    text = re.sub(r'ꦂ', 'ꦂ\u200D', text, flags=re.IGNORECASE)#layar ke layar
    #text = re.sub(r'ꦂ', 'ꦫ꧀', text, flags=re.IGNORECASE) #layar ke ra pangku

    #text = re.sub(r'ꦫ꧀ꦪ', '\u200Cꦫ꧀ꦮ\u200D', text)

    #kembalikan ry
    #text = re.sub('~', 'ꦫꦾ', text)



    return text

def convert_file(input_file, output_file, line_spacing=2):
    with open(input_file, 'r', encoding='utf-8') as infile:
        text = infile.read()

    converted_text = latin_to_jawa(text, line_spacing)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(converted_text)

if __name__ == "__main__":
    input_file = 'output/output_jawa.txt'  # path file input 
    output_file = 'output/output_jawarepha.txt'  # path file output 
    line_spacing = 1

    convert_file(input_file, output_file, line_spacing)
    print("Konversi selesai. Hasil disimpan di:", output_file)



        