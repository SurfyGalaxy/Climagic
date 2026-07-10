string = """:crux: 2 Big Announcements For Crux! :crux: 

First Up: Horizons Crux parents call!

Horizons Crux is coming up soon and we're hosting a parents call at 5:00pm AEST on Sunday the 5th of July! We'll be going over our event logistics and will be answering any questions and concerns your parents might have about the event.

You can RSVP here!

(If your parent isn't able to make it, don't fret! We'll be recording the Zoom meeting and sharing our slides afterwards. We also have a parents guide available.)

Second Cooler Announcement: Hour Extension + Get the ability to pelt water balloons at your favourite organisers!

Since a lot of people have hours stuck in review, we are extending the deadline to buy your ticket so you only need to have 35 hours approved by the time of the event in order to participate :yay: . All you need to do is fill out this form and we will get back to you about it!

As an apology for taking so long with review and everything else we have been delayed on, everyone who comes to Crux is allowed to pelt a water balloon at an organiser(@TheVirtuoso) of choice.

Come to Crux, the best horizons event down under."""

def split_but_better(string, split):
    temp = string
    output = []
    for words in temp:
            b = []
            for e in words:
                    b.append(e)
            output.append(b)
    return output


def split_string(string):
    punctuation = ["! ", "? "]

    temp = []
    a = []
    for words in paragraphs:
        temp.append(words.split(". "))

    return split_but_better(split_but_better(temp, "! "), "? ")

paragraphs = string.split("\n\n")
sentences = split_string(string)

text = []
for e in sentences:
    one = []
    for a in e:
        one.append(a.split())
    text.append(one)
print(text[0][0][0])

# text[paragraph][sentence][word]
