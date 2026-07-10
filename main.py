import nltk

string = """:crux: 2 Big Announcements For Crux! :crux: 

First Up: Horizons Crux parents call!

Horizons Crux is coming up soon and we're hosting a parents call at 5:00pm AEST on Sunday the 5th of July! We'll be going over our event logistics and will be answering any questions and concerns your parents might have about the event.

You can RSVP here!

(If your parent isn't able to make it, don't fret! We'll be recording the Zoom meeting and sharing our slides afterwards. We also have a parents guide available.)

Second Cooler Announcement: Hour Extension + Get the ability to pelt water balloons at your favourite organisers!

Since a lot of people have hours stuck in review, we are extending the deadline to buy your ticket so you only need to have 35 hours approved by the time of the event in order to participate :yay: . All you need to do is fill out this form and we will get back to you about it!

As an apology for taking so long with review and everything else we have been delayed on, everyone who comes to Crux is allowed to pelt a water balloon at an organiser(@TheVirtuoso) of choice.

Come to Crux, the best horizons event down under."""

paragraphs = string.split("\n\n")
text = []
total_fullstops = 0
total_exclamation = 0
total_question = 0
total_word_count = 0
total_nouns = 0
total_verbs = 0
total_fullcaps = 0
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
"noun_density": 0,
"verb_density": 0,
"fullcaps": 0,
"fullcaps_density": 0
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
    for sentence in temp:
        sentence = sentence[0]
        words = sentence.split()
        word_list.append(words)

        for word in words:
            if word.isupper():
                fullcaps += 1
    
    
    raw_words = paragraph.split()
    tag_words = nltk.pos_tag(raw_words)

    for word, tag in tag_words:
        if tag.startswith("NN"):
            nouns += 1
        elif tag.startswith("VB"):
            verbs += 1
    word_count = len(raw_words)
    punc_percent = (exclamation + question) / (fullstop + exclamation + question)
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

    data["text"] = paragraph
    data["fullstops"] = fullstop
    data["exclamation"] = exclamation
    data["question"] = question
    data["punctuation_percent"] = punc_percent
    data["word_count"] = word_count
    data["nouns"] = nouns
    data["verbs"] = verbs
    data["noun_density"] = nound
    data["verb_density"] = verbd
    data["fullcaps"] = fullcaps
    data["fullcaps_density"] = fcapsd
    text.append(data)

total_punc_percent = ((total_exclamation + total_question) / (total_fullstops + total_exclamation + total_question)) * 100
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
noun_density = total_noun_density, 
verb_density = total_verb_density,
fullcaps = total_fullcaps,
fullcaps_density = total_fcapsd
))

print(text)
# text[paragraph][sentence][word]
