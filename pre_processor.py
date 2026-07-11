import nltk
from nltk.corpus import cmudict
import yaml
from types import SimpleNamespace
nltk.download('cmudict')
cmu = cmudict.dict()

with open("config.yaml") as f:
    _config_data = yaml.safe_load(f)
config = SimpleNamespace(**_config_data)

string = """The quick brown fox jumps over the lazy dog"""

def add_word(word: str, word_list: list[tuple(str, int)]) -> list[tuple(str, int)]:
    for words in word_list:
        if words[0] == word:
            index = word_list.index(words)
            value = words[1]
            word_list[index] = (word, value + 1)
            return word_list
    word_list.append((word, 1))
    return word_list

def syllable_count(word: str) -> int:
    word = word.lower()
    
    if word in cmu:
        return [len([list for list in pron if list[-1].isdigit()]) for pron in cmu[word]][0]
    return 0

def get_kinclaid_grade(kinclaid: float) -> str:
    if kinclaid > 90:
        kinclaid_grade = "5th graders and under"
    elif 90 <= kinclaid > 80:
        kinclaid_grade = "6th graders"
    elif 80 <= kinclaid > 70:
        kinclaid_grade = "7th graders"
    elif 70 <= kinclaid > 60:
        kinclaid_grade = "8th/9th graders"
    elif 60 <= kinclaid > 50:
        kinclaid_grade = "10th graders"
    elif 50 <= kinclaid > 30:
        kinclaid_grade = "College students"
    elif 30 <= kinclaid > 10:
        kinclaid_grade = "College graduates"
    else:
        kinclaid_grade = "Professionals"
    return kinclaid_grade

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
    paragraph_count = 0
    total_syllables = 0
    total_sentences = 0

    for paragraph in paragraphs:
        data = {
    "text": '',
    "fullstops": 0,
    "exclamation": 0,
    "question": 0,
    "punctuation_percent": 0.0,
    "word_count": 0,
    "sentence_count": 0,
    "avg_sentence_len": 0,
    "nouns": 0,
    "verbs": 0,
    "fullcaps": 0,
    "noun_density": 0,
    "verb_density": 0,
    "fullcaps_density": 0,
    "kinclaid_reading_ease": 0.0,
    "kinclaid_grade": '',
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
        syllables = 0
        sentences = 0
        sentence_word = 0

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
            sentences += 1
            sentence = sentence[0]
            words = sentence.split()
            word_list.append(words)

            for word in words:
                if word.isupper():
                    fullcaps += 1

                word = word.lower()

                if word not in config.EXCLUDED_WORDS: # Counting words
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
                sentence_word += 1
                syllables += syllable_count(word)
        
        kinclaid = round(206.835 - 1.015 * (sentence_word / sentences) - 84.6 * (syllables / sentence_word), 2)
        kinclaid_grade = get_kinclaid_grade(kinclaid)
        

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
        avg_sent_len = (word_count / sentences)

        total_fullstops += fullstop
        total_exclamation += exclamation
        total_question += question
        total_word_count += word_count
        total_nouns += nouns
        total_verbs += verbs
        total_fullcaps += fullcaps
        total_sentences += sentences
        total_syllables += syllables

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
        
        paragraph_count += 1

        data["text"] = paragraph
        data["fullstops"] = fullstop
        data["exclamation"] = exclamation
        data["question"] = question
        data["punctuation_percent"] = punc_percent
        data["word_count"] = word_count
        data["sentence_count"] = sentences
        data["avg_sentence_len"] = avg_sent_len
        data["nouns"] = nouns
        data["verbs"] = verbs
        data["fullcaps"] = fullcaps
        data["noun_density"] = nound
        data["verb_density"] = verbd
        data["fullcaps_density"] = fcapsd
        data["kinclaid_reading_ease"] = kinclaid
        data["kinclaid_grade"] = kinclaid_grade
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
    total_kinclaid = round(206.835 - 1.015 * (total_word_count / total_sentences) - 84.6 * (total_syllables / total_word_count), 2)
    total_kinclaid_grade = get_kinclaid_grade(total_kinclaid)
    total_avg_sent_len = (total_word_count / total_sentences)


    text.append(dict(
    fullstops = total_fullstops, 
    exclamation = total_exclamation, 
    question = total_question, 
    punctuation_percent = total_punc_percent, 
    word_count = total_word_count, 
    sentence_count = total_sentences,
    avg_sentence_len = total_avg_sent_len,
    paragraph_count = paragraph_count,
    nouns = total_nouns, 
    verbs = total_verbs, 
    fullcaps = total_fullcaps,
    noun_density = total_noun_density, 
    verb_density = total_verb_density,
    fullcaps_density = total_fcapsd,
    kinclaid_reading_ease = total_kinclaid,
    kinclaid_grade = total_kinclaid_grade,
    unique_words = total_unique_words,
    repeated_words = total_repeated_word
    ))
    return text

if __name__ == "__main__":
    data = process_text(string)
    print(data)