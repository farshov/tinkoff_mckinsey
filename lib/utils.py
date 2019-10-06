import string
import re


def clean_sentence(s):
    # symb = "!@#%*&()[]{}/?²\"\'#№.,:;%*()<>\n₽1234567890-+–«»\"\\qwertyuiopasdfghjklzxcvbnm"
    # symb = "йцукенгшщзхъфывапролджэёячсмитьбю"
    s = s.lower()
    #for c in symb:
        #s = s.replace(c, "")
    s = re.sub('[^йцукенгшщзхъфывапролджэёячсмитьбю]', ' ', s)
    # s = s.replace('\xa0', " ")

    return s.lower().strip()
    

def clean_text(text):
    res = []
    num_words = 0
    for i in range(len(text)):
        clean = clean_sentence(text[i])
        if len(clean) > 0:
            clean = clean.split()
            # no n_grams for single characters
            for w in clean:
                if len(w) < 2:
                    continue
            res.append(clean)
            num_words += len(clean)
    return res, num_words
