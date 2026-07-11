import nltk

string = """q q q

a

a"""

def add_word(word: str, word_list: list[tuple(str, int)]) -> list[tuple(str, int)]:
    for words in word_list:
        if words[0] == word:
            index = word_list.index(words)
            value = words[1]
            word_list[index] = (word, value + 1)
            return word_list
    word_list.append((word, 1))
    return word_list


def process_text(string: str) -> list:
    paragraphs = string.split("\n\n")
    text = []
    total_fullstops = 0
    total_exclamation = 0
    total_question = 0
    total_word_count = 0
    total_nouns = 0
    total_verbs = 0
    total_fullcaps = 0
    total_unique_words = set()
    total_repeated_word = []

    for paragraph in paragraphs:
        data = {
    "text": '',
    "fullstops": 0,
    "exclamation": 0,
    "question": 0,
    "punctuation_percent": 0.0,
    "word_count": 0,
    "nouns": 0,
    "verbs": 0,
    "fullcaps": 0,
    "noun_density": 0,
    "verb_density": 0,
    "fullcaps_density": 0,
    "unique_words": set(),
    "repeated_words": []
    }
        fullstop = 0
        exclamation = 0
        question = 0
        nouns = 0
        verbs = 0
        temp = []
        fullcaps = 0

        for char in paragraph:
            if char == '.':
                fullstop += 1
            elif char == '!':
                exclamation += 1
            elif char == '?':
                question += 1
        a = paragraph.split(". ")
        for b in a:
            c = b.split("! ")
            for d in c:
                e = d.split("? ")
                for f in e:
                    temp.append(e)
        
        word_list = []
        unique_words = set()
        repeated_words = []
        for sentence in temp:
            sentence = sentence[0]
            words = sentence.split()
            word_list.append(words)

            for word in words:
                if word.isupper():
                    fullcaps += 1

                b = True
                for a in repeated_words:
                    if a[0] == word:
                        b = False
                if b and (word not in unique_words):
                    unique_words.add(word)
                else:
                    if word in unique_words:
                        unique_words.remove(word)
                    add_word(word, repeated_words)
                    if b:
                        add_word(word, repeated_words)
                    

        raw_words = paragraph.split()
        tag_words = nltk.pos_tag(raw_words)

        for word, tag in tag_words:
            if tag.startswith("NN"):
                nouns += 1
            elif tag.startswith("VB"):
                verbs += 1
        word_count = len(raw_words)
        try:
            punc_percent = (exclamation + question) / (fullstop + exclamation + question)
        except ZeroDivisionError:
            punc_percent = 0
        
        nound = (nouns / word_count)
        verbd = (verbs / word_count)
        fcapsd = (fullcaps / word_count)

        total_fullstops += fullstop
        total_exclamation += exclamation
        total_question += question
        total_word_count += word_count
        total_nouns += nouns
        total_verbs += verbs
        total_fullcaps += fullcaps

        for word in unique_words:
            new = True
            if word in total_unique_words:
                total_unique_words.remove(word)
                add_word(word, total_repeated_word)
                for a in repeated_words:
                    if a[0] == word:
                        new = False
                if new:
                    add_word(word, total_repeated_word)
            else:
                total_unique_words.add(word)
        
        for word in repeated_words:
            times = word[1]
            actual_word = word[0]
            while times > 0:
                add_word(actual_word, total_repeated_word)
                times -= 1

        data["text"] = paragraph
        data["fullstops"] = fullstop
        data["exclamation"] = exclamation
        data["question"] = question
        data["punctuation_percent"] = punc_percent
        data["word_count"] = word_count
        data["nouns"] = nouns
        data["verbs"] = verbs
        data["fullcaps"] = fullcaps
        data["noun_density"] = nound
        data["verb_density"] = verbd
        data["fullcaps_density"] = fcapsd
        data["unique_words"] = unique_words
        data["repeated_words"] = repeated_words
        text.append(data)

    try:
        total_punc_percent = ((total_exclamation + total_question) / (total_fullstops + total_exclamation + total_question)) * 100
    except ZeroDivisionError:
        total_punc_percent = 0
    
    total_noun_density = (total_nouns / total_word_count)
    total_verb_density = (total_verbs / total_word_count)
    total_fcapsd = (total_fullcaps / total_word_count)


    text.append(dict(
    fullstops = total_fullstops, 
    exclamation = total_exclamation, 
    question = total_question, 
    punctuation_percent = total_punc_percent, 
    word_count = total_word_count, 
    nouns = total_nouns, 
    verbs = total_verbs, 
    fullcaps = total_fullcaps,
    noun_density = total_noun_density, 
    verb_density = total_verb_density,
    fullcaps_density = total_fcapsd,
    unique_words = total_unique_words,
    repeated_words = total_repeated_word
    ))

    return text

print(process_text(string))
