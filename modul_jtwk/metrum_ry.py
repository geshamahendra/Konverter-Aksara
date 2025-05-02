import re

def parse_metrum_slots(metrum_line):
    symbol_map = {'–': True, '⏑': False}
    return [symbol_map.get(c, False) for c in metrum_line if c in symbol_map]

def extract_vowel_slots(text_line):
    vokal_regex = (
        r'(?:(?<=\s)(r|R)[iy]'         # ry atau Ry setelah spasi
        r'|(?<!\S)[rR][iy]'            # ry atau Ry di awal baris
        r'|[ywYW]\b\s+[āaîiūueoâṛṝ]'   # w atau y di akhir kata + spasi + vokal
        r'|[āaîiūueoâṛṝ])'             # vokal biasa
    )
    matches = list(re.finditer(vokal_regex, text_line))
    return [(m.start(), m.group()) for m in matches]

def find_ry_positions_full(text_line):
    return [(m.start(), m.group()) for m in re.finditer(r'(?<!\S)([rR][iy])', text_line)]

def should_replace_ry_fixed(ry_pos, vowel_slots, metrum_slots):
    for i, (start, _) in enumerate(vowel_slots):
        if start >= ry_pos:
            return i < len(metrum_slots) and metrum_slots[i]
    return False

def proses_ry_metrum(text):
    lines = text.splitlines()
    output = []
    i = 0

    while i < len(lines):
        line = lines[i]
        output.append(line)

        if re.match(r'<.*?>', line):
            if i + 1 < len(lines) and re.search(r'[–⏑]', lines[i + 1]):
                metrum_line = lines[i + 1]
                output.append(metrum_line)

                if i + 2 < len(lines):
                    text_line = lines[i + 2]

                    if not metrum_line.strip().startswith("⏑"):
                        metrum_slots = parse_metrum_slots(metrum_line)
                        vowel_slots = extract_vowel_slots(text_line)
                        ry_positions = find_ry_positions_full(text_line)

                        offset = 0
                        for pos, ry_text in ry_positions:
                            real_pos = pos + offset
                            if should_replace_ry_fixed(real_pos, vowel_slots, metrum_slots):
                                replacement = 'rī' if ry_text[0].islower() else 'Rī'
                                text_line = text_line[:real_pos] + replacement + text_line[real_pos + len(ry_text):]
                                offset += len(replacement) - len(ry_text)

                    output.append(text_line)
                    i += 2
                else:
                    i += 1
        i += 1

    return "\n".join(output)
