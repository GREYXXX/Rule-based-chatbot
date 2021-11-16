#This python file is for chatbot implementation from task 1 to 4
#Includes the lingusitic patterns for date, location, budget and numer of people
#Run by "python3 project1_bot.py"
#@Author: XI RAP
#@Student number :22435044 



from numpy import random
import spacy
import re
from spacy.matcher import Matcher
from telegram.ext import Updater, MessageHandler, Filters

nlp = spacy.load('en_core_web_sm')

"""
1st pattern for DST and ORG
First pattern : ADP+PROPN for dst and org.  (E.g. from...to.... or to...from...)
Second Pattern : VERB+PROPN     (E.g. visit Neverland)
"""

locs = []
l_pattern1 = [{"TEXT": "to"}, {"POS": "PROPN"}]
l_pattern2 = [{"TEXT": "from"}, {"POS": "PROPN"}]
l_pattern3 = [{"POS": "VERB"}, {"POS": "PROPN"}]

def loc_pattern1(sent):
    matcher = Matcher(nlp.vocab)
    matcher.add("ADP+PROPN && VERB+PROPN", [l_pattern1, l_pattern2])
    matches = matcher(sent, as_spans=True)
    app = {}
    for i in matches:
        if str(i[0]) == 'to':
            app['dst'] = str(i[1:])
        elif str(i[0]) == 'from':
            app['org'] = str(i[1:])
    return app

def loc_pattern2(sent):
    matcher = Matcher(nlp.vocab)
    matcher.add("VERB+PROPN", [l_pattern3])
    matches = matcher(sent, as_spans=True)
    app = {}
    for i in matches:
        app['dst'] = str(i[1:])
        print(i)
    return app


"""
2nd pattern for how many people 
NUM + NOUN (E.g. 5 adults)
NOUN + AUX + NUM (E.g. Our kids are 12)
NOUN + AUX + VERB + NUM (E.G Our number of kids would be 12)
"""

n_pattern1 = [{"POS": "NUM"}, {"POS": "NOUN"}]
n_pattern2 = [{"POS": "NOUN"}, {"POS": "AUX"}, {"POS": "NUM"}]
n_pattern3 = [{"POS": "NOUN"}, {"POS": "AUX"}, {"POS": "VERB"}, {"POS": "NUM"}]


def num_pattern(sent, pattern):
    keys = [list(i.values()) for i in pattern]
    label = '+'.join([x for xs in keys for x in xs])
    matcher = Matcher(nlp.vocab)
    matcher.add(label, [pattern])
    matches = matcher(sent, as_spans=True)
    return matches

def num_pattern1(sent):
    return num_pattern(sent, n_pattern1)

def num_pattern2(sent):
    return num_pattern(sent, n_pattern2)

def num_pattern3(sent):
    return num_pattern(sent, n_pattern3)


"""
6 patterns for dates
1. PROPN + NUM                 e.g August 13
2. NUM + PROPN                 e.g. 13 August
3. NOUN + ADP +PROPN           e.g. 13th of August
4. NOUN/ADJ + PROPN                e.g. 13th August
5. PROPN + NOUN                e.g. August 13th
# 6. PROPN + NUM + PROPN + NUM   e.g. Monday, 12 Jan, 2016
"""

d_pattern1 = [{"POS": "PROPN"}, {"POS": "NUM"}]  
d_pattern2 = [{"POS": "NUM"}, {"POS": "PROPN"}]
d_pattern3 = [{"POS": "NOUN"}, {"POS": "ADP"}, {"POS": "PROPN"}]
d_pattern4 = [{"POS": "ADJ"}, {"POS": "PROPN"}]
d_pattern5 = [{"POS": "PROPN"}, {"POS": "NOUN"}]
# d_pattern6 = [{"POS": "PROPN"}, {"POS": "NUM"}, {"POS": "PROPN"}, {"POS": "NUM"}]

def date_pattern(sent, pattern):
    keys = [list(i.values()) for i in pattern]
    label = '+'.join([x for xs in keys for x in xs])
    matcher = Matcher(nlp.vocab)
    matcher.add(label, [pattern])
    matches = matcher(sent, as_spans=True)
    return matches

def date_pattern1(sent):  
    return date_pattern(sent, d_pattern1)
    
def date_pattern2(sent):
    return date_pattern(sent, d_pattern2)

def date_pattern3(sent):
    return date_pattern(sent, d_pattern3)
    
def date_pattern4(sent):
    return date_pattern(sent, d_pattern4)

def date_pattern5(sent):
    return date_pattern(sent, d_pattern5)

# def date_pattern6(sent):
#     return date_pattern(sent, d_pattern6)




"""
patterns for budget
1. SYM + NUM e.g. $2400
2. VERB + NUM e.g. would be 2400
3. AUX + NUM  e.g. My budget ois 2400
4. between+NUM+and+NUM" e.g. My budget is between 2400 and 3000
"""

b_pattern1 = [{"POS": "SYM"}, {"POS": "NUM"}]
b_pattern2 = [{"POS" : "VERB"}, {"POS" : "NUM"}]
b_pattern3 = [{"POS" : "AUX"}, {"POS" : "NUM"}]
b_pattern4 = [{"TEXT" : "between"}, {"POS" : "NUM"}, {"TEXT": "and"}, {"POS" : "NUM"}]
    
def budget_pattern(sent, pattern):
    keys = [list(i.values()) for i in pattern]
    label = '+'.join([x for xs in keys for x in xs])
    matcher = Matcher(nlp.vocab)
    matcher.add(label, [pattern])
    matches = matcher(sent, as_spans=True)
    return matches

def budget_pattern1(sent):  
    return budget_pattern(sent, b_pattern1)

def budget_pattern2(sent):
    return budget_pattern(sent, b_pattern2)

def budget_pattern3(sent):
    return budget_pattern(sent, b_pattern3)

def budget_pattern4(sent):
    return budget_pattern(sent, b_pattern4)




##########
###Bot####
##########


#Token that I used for my chatbot
TOKEN = '1948586502:AAFMfGr8VYJnm4sUM9FHlVpmCHeEl7fjSrs'
random_lists = ['Sorry, I dont understand you', 'Please rephrase your request. Be as specific as possible!', 
'I am a robot for assistanting your trip requests, please identify at least one of the following intents: budget, locations, date, nunmber of person'
]
def utterance(update, context):
    msg = update.message.text
    doc = nlp(msg)
    ents = [(e.label_) for e in doc.ents]

    #If no expected intents, randomly reply
    if ("GPE" not in ents) and ("CARDINAL" not in ents) and ("MONEY" not in ents) and ("DATE" not in ents): 
        random.shuffle(random_lists)
        update.message.reply_text(random_lists[0])
        return
    
    if "GPE" in ents:
        get = loc_pattern1(doc), loc_pattern2(doc) 
        print(get)
        if 'dst' in get[0] and 'org' in get[0]:
            update.message.reply_text('destination city is {} and original city is {}'.format(get[0]['dst'], get[0]['org']))
        elif 'dst' in get[0] and 'org' not in get[0]:
            update.message.reply_text('destination city is {}'.format(get[0]['dst']))
        elif 'org' in get[0] and 'dst' not in get[0]:
            update.message.reply_text('original city is {}'.format(get[0]['org']))       
        if 'dst' in get[1]:
            update.message.reply_text('destination city is {}'.format(get[1]['dst']))
    if ("MONEY" in ents) or ("CARDINAL") in ents:
        get = budget_pattern1(doc), budget_pattern2(doc), budget_pattern3(doc), budget_pattern4(doc)
        print(get)
        if len(get[0]) != 0:
            update.message.reply_text('Your budget is {}'.format(get[0][0]))
        if len(get[1]) != 0:
            numbers = re.findall('[0-9]+', str(get[1][0]))
            if int(numbers[0]) > 100:        #set 100 as threshold, if < 100, don't identify as budget.
                update.message.reply_text('Your budget is {}'.format(numbers[0]))
        if len(get[2]) != 0:
            numbers = re.findall('[0-9]+', str(get[2][0]))
            if int(numbers[0]) > 100:        #set 100 as threshold, if < 100, don't identify as budget.
                update.message.reply_text('Your budget is {}'.format(numbers[0]))
        if len(get[3]) != 0:
            numbers = re.findall('[0-9]+', str(get[3][0]))
            if int(numbers[0]) > 100 and  int(numbers[1])  > 100:
                update.message.reply_text('So, your minimum budget is {} and your maximum budget is {}'.format(numbers[0], numbers[1]))
        if len(get[0]) == 0 and len(get[1]) == 0 and len(get[2]) == 0 and len(get[3]) == 0:
            update.message.reply_text('Sorry, you did not specify any validate budget, or I am so struggle to get it (sob..). \
            Please use these following pattern to identify your date if you have one:' + '\n' +' 1. SYM + NUM e.g. $2400' + "\n" +\
            '2. VERB + NUM                  e.g. My budget would be 2400' +  "\n" + \
            '3. AUX + NUM                   e.g. My budget is 2400' +  "\n" + \
            '4.between+NUM+and+NUM"         e.g. My budget is between 2400 and 3000'  + "\n"
            )
    
    if "DATE" in ents:
        get = date_pattern1(doc), date_pattern2(doc), date_pattern3(doc), date_pattern4(doc), date_pattern5(doc)
        print(get)
        if len(get[0]) != 0:
            # date = max(get[0], key=len)         #reply with longest match
            update.message.reply_text('Your date is {}'.format(get[0][0]))
        elif len(get[1]) != 0:
            update.message.reply_text('Your date is {}'.format(get[1][0]))
        elif len(get[2]) != 0:
            update.message.reply_text('Your date is {}'.format(get[2][0]))
        elif len(get[3]) != 0:
            update.message.reply_text('Your date is {}'.format(get[3][0]))
        elif len(get[4]) != 0:
            update.message.reply_text('Your date is {}'.format(get[4][0]))
        # elif len(get[5]) != 0:
        #     update.message.reply_text('Your date is {}'.format(get[5][0]))
        else:
            update.message.reply_text('Sorry, you did not specify any validate dates, or I am so struggle to get it (sob..). \
            Please use these following pattern to identify your date if you have one:' + '\n' +' 1. PROPN + NUM  e.g August 13' + "\n" +\
            '2. NUM + PROPN                 e.g. 13 August' +  "\n" + \
            '3. NOUN + ADP +PROPN           e.g. 13th of August' +  "\n" + \
            '4. NOUN + PROPN                e.g. 13th August'  + "\n" + \
            '5. PROPN + NOUN                e.g. August 13th'  + "\n"  +\
            '6. PROPN + NUM + PROPN + NUM   e.g. Monday, 12 Jan, 2016' +"\n"
            )
    if "CARDINAL" in ents:
        get = num_pattern1(doc), num_pattern2(doc), num_pattern3(doc)
        print(get)
        if len(get[0]) != 0:
            li = [str(i) for i in get[0]]
            update.message.reply_text('Your number of persions are {}'.format(','.join(li)))
        elif len(get[1]) != 0:
            li = [str(i) for i in get[1]]
            update.message.reply_text('Your {}'.format(','.join(li)))
        elif len(get[2]) != 0:
            li = [str(i) for i in get[2]]
            update.message.reply_text('Your {}'.format(','.join(li)))
        else:
            update.message.reply_text('Sorry, you did not specify any validate number of persons, or I am so struggle to get it (sob..). \
            Please use these following pattern to identify your date if you have one:' + '\n' + \
            '1. NUM + NOUN                  e.g. 5 adults)' + "\n" +\
            '2. NOUN + AUX + NUM            e.g. Our kids are 12)' +  "\n" + \
            '3. NOUN + AUX + VERB + NUM     e.g Our number of kids would be 12)' +  "\n"
        )
    
        


#the code responsible for interactions with Telegram
updater = Updater(TOKEN, use_context=True)
updater.dispatcher.add_handler(MessageHandler(Filters.text, utterance))
updater.start_polling()
updater.idle()