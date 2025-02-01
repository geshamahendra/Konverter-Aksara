# Mapping devanagari to latin
devanagari_to_latin = {
    'क': 'k', 'ख': 'kh', 'ग': 'g', 'घ': 'gh', 'ङ': 'ṅ',
    'च': 'c', 'छ': 'ch', 'ज': 'j', 'झ': 'jh', 'ञ': 'ñ',
    'ट': 'ṭ', 'ठ': 'ṭh', 'ड': 'ḍ', 'ढ': 'ḍh', 'ण': 'ṇ',
    'त': 't', 'थ': 'th', 'द': 'd', 'ध': 'dh', 'न': 'n',
    'प': 'p', 'फ': 'ph', 'ब': 'b', 'भ': 'bh', 'म': 'm',
    'य': 'y', 'र': 'r', 'ल': 'l', 'व': 'w', 'श': 'ś',
    'ष': 'ṣ', 'स': 's', 'ह': 'h',
    
    # Independent vowels
    'अ': 'a', 'आ': 'ā', 'इ': 'i', 'ई': 'ī', 'उ': 'u', 'ऊ': 'ū',
    'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
    'ऋ': 'ṛ', 'ॠ': 'ṝ', 'ऌ': 'ḷ', 'ॡ': 'ḹ',
    
    # Matras (vowel signs)
    'ा': 'ā', 'ि': 'i', 'ी': 'ī', 'ु': 'u', 'ू': 'ū',
    'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au', 
    'ः':'ḥ', 'ँ':'ṃ', 'ं':'ṃ', '':'',
    'ृ': 'ṛ', 'ॄ': 'ṝ', 'ॢ': 'ḷ', 'ॣ': 'ḹ',
    
    # Virama (to suppress inherent vowel)
    '्': '',
    
    # Punctuation
    '।': '.', '॥': '..', ',': ',', ' ': ' ', 'ऽ': "'",

    # Letters with nuqtah
    'क़': 'q', 'ख़': 'ḵh', 'ग़': 'ġ', 'ज़': 'z', 'ड़': 'ṛ', 'ढ़': 'ṛh', 'फ़': 'f', 'य़': 'ẏ',

    # Numbers
    '०': '0', '१' : '1', '२' : '2', '३' : '3', '४' : '4',
    '५' : '5', '६' : '6', '७' : '7', '८' : '8', '९' : '9'
}

# Function to convert Devanagari to Latin
def convert_devanagari_to_latin(text):
    output = []
    skip_next = False
    
    for i, char in enumerate(text):
        if skip_next:
            skip_next = False
            continue
        
        if char in devanagari_to_latin:
            if char == '्':  # Virama, remove inherent vowel
                if output:
                    output[-1] = output[-1][:-1]  # Remove inherent 'a'
                continue
            
            if i + 1 < len(text) and text[i + 1] in {'ा', 'ि', 'ी', 'ु', 'ू', 'े', 'ै', 'ो', 'ौ', 'ृ', 'ॄ', 'ॢ', 'ॣ'}:
                output.append(devanagari_to_latin[char] + devanagari_to_latin[text[i + 1]])
                skip_next = True  # Skip next character (matra already handled)
            else:
                output.append(devanagari_to_latin[char] + ('a' if char in 'कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहक़ख़ग़ज़ड़ढ़फ़य़' else ''))
        else:
            output.append(char)  # Keep unknown characters as is
    
    return "".join(output)
# Function to process input file and write to output file
def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        text = infile.read()
    
    latin_text = convert_devanagari_to_latin(text)
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write(latin_text)

# Example usage
if __name__ == "__main__":
    input_filename = "input_devanagri.txt"  # Change as needed
    output_filename = "output/output_devanagri.txt"  # Change as needed 
    process_file(input_filename, output_filename)