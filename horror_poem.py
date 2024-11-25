# Afamdi Achufusi
# M7-Poetry-Slam
# Description: This poem generator simply produces a lyric poem that tries to scare you. The irony/humor in this poem 
# generator however is that it uses one of the most heartwarming and calming pieces of text to help achieve this! After 
# producing a poem, the poem generator is able to evaluate its poem based on the poem’s Horror Level and Quality. Finally, 
# the poem generator will actually speak the poem out loud.

import spacy
import contractions
import random
from textblob import TextBlob
import language_tool_python
import os
from flask import Flask, render_template


# Inspiring Set ("The Christmas Song" by Mel Torme)
inspiring_set = """Chestnuts roasting on an open fire
Jack Frost nipping at your nose
Yuletide carols being sung by a choir
And folks dressed up like Eskimos"""

# List of each line in the inspiring set
inspiring_set_lines = inspiring_set.split('\n')

# List of scary onomatepia words
onomatepia_list = ["Creak", "Thud", "Snap", "Crunch", "Aaah",
                   "Bam", "Bang", "Screech", "Hiss", "Slap", 
                   "Clatter", "Boom", "Clop", "Boo", "Scratch", 
                    "Snarl", "Scrape", "HaHaHa", "Whoosh",
                   "Creak", "Oooo", "Skitter", "Blare"]

# List of scary adjectives
general_adjective_list = ["Eerie", "Macabre", "Bloodcurdling", "Haunting", "Sinister", 
                  "Chilling", "Creepy", "Gloomy", "Ominous", "Unholy", 
                  "Ghastly", "Nightmarish", "Grim", "Terrifying", "Frightening", 
                  "Dreadful", "Spine-chilling", "Dismal", "Lurking", "Abominable", 
                  "Malevolent", "Monstrous", "Hair-raising", "Dread-inducing", "Disembodied", 
                  "Grisly", "Foreboding", "Petrifying", "Wicked", "Vile", 
                  "Rotten", "Twisted", "Horrific", "Unnatural", "Gory", 
                  "Putrid", "Flesh-chilling", "Shadowy", "Disturbing", "Suffocating", 
                  "Repulsive", "Tormented", "Grotesque", "Terrifying", "Appalling", 
                  "Cursed", "Sickening", "Stifling", "Abysmal", "Nightmarish"]

# List of scary nouns
noun_list = ["Vampires", "Werewolves", "Zombies", "Ghosts", "Witches",
             "Demons", "Mummies", "Monsters", "Bats", "Monsters", 
             "Scarecrows", "Spiders", "Insects", "Phantoms", "Hellhounds",
             "Hidden Creatures", "Ghouls", "Poltergeists", "Evil Spirits", "Trolls"]

# List of scary verbs (that are followed by nouns)
verb_list_for_nouns = ["attack", "bewilder", "chase", "devour", "haunt",
    "frighten", "harass", "daunt", "horrify", "intimidate", "overwhelm", "petrify", 
    "scare", "strike", "spook", "stun", "terrify", "trap", "overwhelm"]

# List of scary verbs (that are followed by prepositions)
verb_list_for_preposition = ["blow",  "disappear", "creep", "stalk", "sneak", "lurk", "whisper", "crawl", "howl", "hover", "screech", "scream", "jab", "glare", "prowl", "emerge", "chuckle"]

# List of scary proper nouns
proper_nouns = ["Happy Halloween", "Sweet Dreams", "Night Night", "Scary Hours", 
    "Goodnight", "Dreadful Days", "Happy Nightmares", "Dark Days", "Traumatic Times",
    "Silent Night", "An Omen", "Eternal rest", "Everlasting pain", "Everlasting Memories",
    "Overwhelming Chills", "Immense Horror", "Horrifying Times", "Happy Death Day", "Haunted Memories", 
    "Chilling Thoughts", "Restless Nights", "A night full of fright", "A day of dismay", "A scary season"]


# Removes contractions from the inspiring set
def removed_contractions(text):
    expanded_words = []

    for word in text.split():
        expanded_words.append(contractions.fix(word))

    text_without_contractions = " ".join(expanded_words)
    return text_without_contractions


# Generates a non-refined version of one stanza in the poem
def stanza_generator(poem_lines):
    nlp = spacy.load("en_core_web_sm")
    
    for i, line in enumerate(poem_lines):
        
        line = line.split(" ")
        for word in line:
            if word == "up" or word == "a" or word == "an" or word == "Frost" or word == "nose" or word == "being":
                line.remove(word)
        line = ' '.join(line)
        doc = nlp(line)

        updated_line = line

        for token in doc:
            if token.pos_ == 'NOUN':
                if token.text == 'nose':
                    updated_line = updated_line.replace(token.text, '')
                updated_line = updated_line.replace(token.text, random.choice(noun_list), 1)
            if token.pos_ == 'VERB':
                updated_line = updated_line.replace(token.text, random.choice(verb_list_for_preposition))
            if token.pos_ == 'ADJ':
                updated_line = updated_line.replace(token.text, random.choice(general_adjective_list))
            if token.pos_ == 'AUX':
                continue
            if token.pos_ == 'PRON':
                updated_line = updated_line.replace(token.text, "You!") # Replacing pronouns with "You" to make the poem scarier (it will feel like it is talking to you)
            if token.pos_ == 'PROPN':
                if token.text == "Jack":
                    updated_line = updated_line.replace(token.text, random.choice(noun_list))
                if token.text == 'Frost':
                    updated_line = updated_line.replace(token.text, '')
                updated_line = updated_line.replace(token.text, random.choice(general_adjective_list) + " " + random.choice(noun_list) + "!")
            if token.pos_ == 'NUM':
                updated_line = updated_line.replace(token.text, random.choice(noun_list))

            poem_lines[i] = updated_line

    new_poem = '\n'.join(poem_lines)
    return new_poem


# Refines a stanza of the poem (fixes a few grammatical errors and gets rid of extra spaces)
def stanza_refiner(poem):

    tool = language_tool_python.LanguageTool('en-US')
    errors = tool.check(poem)
    
    refined_poem = language_tool_python.utils.correct(poem, errors)
    
    return refined_poem


# Generates the full poem
def poem_generator(poem_lines):

    tripled_poem_lines = poem_lines + poem_lines + poem_lines
    poem = stanza_refiner(stanza_generator(tripled_poem_lines))
    return poem


# Function that adds onomatepia before every 4-line stanza
def add_onomatepia(poem):
    
    lines = poem.split('\n')
    
    for i in range(0, len(lines), 4):
        lines[i] = "\n" + random.choice(onomatepia_list) + "!" + "\n\n" + lines[i]
    
    return '\n'.join(lines)


# Function that evaluates the poem based on it's Horror Level and Quality Level
def evaluation(poem):
    
    # Horror Score from -1 (Very Scary) to 1 (Not Scary) at all
    testimonial = TextBlob(poem)
    print("Horror Score from -1 (Terrifying) to 1 (Not Scary): ")
    print(testimonial.polarity)
    print("\n")

    # Quality Score (out of 100) based on how many times words are repeated
    # Minus 2 when a word is repeated
    counter = {}
    quality_score = 100
    no_newlines = poem.replace("\n", " ")
    no_exclamations = no_newlines.replace("!", " ")
    
    for word in no_exclamations.split(' '):
        if word not in counter:
            counter[word] = 0
        elif word in onomatepia_list and word in counter:
            counter[word] += 1
            quality_score -= 2
        elif word in general_adjective_list and word in counter:
            counter[word] += 1
            quality_score -= 2
        elif word in noun_list and word in counter:
            counter[word] += 1
            quality_score -= 2
        elif word in verb_list_for_nouns and word in counter:
            counter[word] += 1
            quality_score -= 2
        elif word in verb_list_for_preposition and word in counter:
            counter[word] += 1
            quality_score -= 2
        elif word in proper_nouns and word in counter:
            counter[word] += 1
            quality_score -= 2
    print("Quality Score out of 100: ")
    print(quality_score)
    print("\n")


# Function that reads the poem aloud
def say_aloud(poem):
    poem = poem.replace("\n", " ")
    os.system(f"say -v Moira -r 110 {poem}")


# Function that gives user the option to save the poem as a text file
def save_poem(poem):
    response = input("Do you want to save this poem? Enter 'y' (if yes) or 'n' (if no): ")
    if response == 'y':
        filename = input("Enter a title for your poem: ")
        filename = filename + ".txt"
        filename = filename.replace(" ", "_")
        with open(filename, 'w') as file:
            file.write(poem)
            print("Poem saved to file: " + filename + "\n")
    else:
        print("Poem not saved.\n")


# Defining the poem so we can pass it into our website
poem = poem_generator(inspiring_set_lines)
final_poem = add_onomatepia(poem)

app = Flask(__name__)
@app.route("/")

def poem_website():
    return render_template("poem_website.html", final_poem=final_poem.upper())



def main():

    print("\n\n!!!HORROR POEM!!!\n\n")
    print(final_poem.upper())
    print("\n")

    evaluation(final_poem)

    say_aloud(final_poem)

    save_poem(final_poem.upper())

    print("Follow the the 'http:' link below to view the poem on a new webpage: \n")


if __name__ == "__main__":
    main()
    app.run(debug=False)
