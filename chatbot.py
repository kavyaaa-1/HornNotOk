
import nltk 
import numpy as np
import random
import string
import re

import warnings
warnings.filterwarnings = False 

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

f = open("DataSet.txt", "r")
corpus_text = f.read()
     

corpus_text = corpus_text.lower()
     

corpus_text = re.sub(r'\s+', ' ', corpus_text)
     


#converting text into sentences and words
corpus_sentences=nltk.sent_tokenize(corpus_text)
corpus_words=nltk.word_tokenize(corpus_text)

greeting_inputs=["hey","hello","hi","heyaa","evening","evenings","greetings","sup","hola"]
greeting_response=["Hey","How can I help you?","**nods**","Hello","Hi there mate","Hola!"]

greeting_input2 = ["you?" , "day?"]
greeting_response2 = ["I am fine, thankyou" , "Good, thanks", "Not bad"]
     

def greet_someone(greeting):
  for x in greeting.split():
      if x.lower() in greeting_inputs:
          return (random.choice(greeting_response))
     

def greet_someone2(greeting):
  for x in greeting.split():
      if x.lower() in greeting_input2:
          return (random.choice(greeting_response2))
     

wn_lemmatizer = nltk.stem.WordNetLemmatizer()

def lemmatize_data(tokens):
    return [wn_lemmatizer.lemmatize(token) for token in tokens]

punct_remover=dict((ord(punctuation),None) for punctuation in string.punctuation)
     

def get_processed_data(data):
    return lemmatize_data(nltk.word_tokenize(data.lower().translate(punct_remover)))
     

def respond(input):
  bot_response=''
  corpus_sentences.append(input)

  word_vectorizer=TfidfVectorizer(tokenizer=get_processed_data,stop_words='english')
  corpus_word_vectors=word_vectorizer.fit_transform(corpus_sentences)
  cos_sin_vectors=cosine_similarity(corpus_word_vectors[-1],corpus_word_vectors)
  similar_response_idx=cos_sin_vectors.argsort()[0][-2]

  matched_vector = cos_sin_vectors.flatten()
  matched_vector.sort()
  vector_matched = matched_vector[-2]

  if vector_matched==0:
    bot_response=bot_response+"I am sorry I could not get that"
  else:
    bot_response=bot_response+corpus_sentences[similar_response_idx]
    return bot_response
     

chat = True
print("Bot : Heloo!")
print("Bot : What would you like to ask?")
while(chat == True):
  user_query = input("Me : ")
  user_query = user_query.lower()
  if (user_query == "quit" or user_query == "bye" ):
    chat = False
    print("Bot : Bye, Have a nice day")

  elif (user_query != "quit" or user_query != "bye"):
    
    if(user_query == "thanks" or user_query == "thankyou" or user_query == "thank you"):
      chat = False
      print("Bot : You are welcome!")
    else:
      if greet_someone(user_query) != None:
        print("Bot : " + greet_someone(user_query))
      elif greet_someone2(user_query) != None:
        print("Bot : " + greet_someone2(user_query))
      else:
        print("Bot : ", end = "")
        print(respond(user_query))
        corpus_sentences.remove(user_query)

     



     