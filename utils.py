import string


def clean_sentence(s):
    symb = "!@#%*&()[]{}/?²\"\'#№.,:;%*()<>\n₽1234567890-+–«»\"\\"
    for c in symb:
        s = s.replace(c, "")
    s = s.replace('\xa0', " ")

    return s.lower().strip()


def clean_text(text):
    res = ""
    for i in range(len(text)):
        clean = clean_sentence(text[i])
        if len(clean) > 0:
            res += " " + clean
    return res.strip(), len(text), len(res.split())
