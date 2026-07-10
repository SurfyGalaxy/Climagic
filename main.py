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
for paragraph in paragraphs:
    data = {
"text": '',
"fullstops": 0,
"exclamation": 0,
"question": 0,
"punctuation_percent": 0.0
}
    fullstop = 0
    exclamation = 0
    question = 0
    temp = []
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
    
    raw_words = paragraph.split()

    
    percent = ((exclamation + question) / (fullstop + exclamation + question)) * 100

    data["text"] = word_list
    data["fullstops"] = fullstop
    data["exclamation"] = exclamation
    data["question"] = question
    data["punctuation_percent"] = percent
    text.append(data)

print(text[0])


# text[paragraph][sentence][word]
