import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
import re
import string
#from pyvi import ViTokenizer
import pickle
nltk.download('punkt')
nltk.download('brown')
from nltk.corpus import brown
from nltk.corpus import words
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.stem.porter import PorterStemmer 
from nltk.tokenize import word_tokenize 
from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import word_tokenize 
import inflect 
p = inflect.engine()
lemmatizer = WordNetLemmatizer() 
stemmer = PorterStemmer() 

class DocClassification:
	def __init__(self, text):
		self.text = text
		self.vectorizer = pickle.load(open('domain1_app/models_classification/vectorizer.pickle', 'rb'))
		self.tfidf = pickle.load(open('domain1_app/models_classification/tfidf.pickle', 'rb'))
		self.le = pickle.load(open('domain1_app/models_classification/le.pickle', 'rb'))
		self.model = pickle.load(open('domain1_app/models_classification/LG/model_lg.pkl', 'rb'))

	def text_lowercase(self, text): 
		return text.lower() 
  
	def remove_numbers(self, text): 
	    result = re.sub(r'\d+', '', text) 
	    return result 
	 
	  
	# convert number into words 
	def convert_number(self, text): 
	    # split string into list of words 
	    temp_str = text.split() 
	    # initialise empty list 
	    new_string = [] 
	  
	    for word in temp_str: 
	        # if word is a digit, convert the digit 
	        # to numbers and append into the new_string list 
	        if word.isdigit(): 
	            temp = p.number_to_words(word) 
	            new_string.append(temp) 
	  
	        # append the word as it is 
	        else: 
	            new_string.append(word) 
	  
	    # join the words of new_string to form a string 
	    temp_str = ' '.join(new_string) 
	    return temp_str 
	  
	# remove punctuation 
	def remove_punctuation(self, text): 
	    translator = str.maketrans('', '', string.punctuation) 
	    return text.translate(translator) 
	  
	# remove whitespace from text 
	def remove_whitespace(self, text): 
	    return  " ".join(text.split()) 
	  
	# remove stopwords function 
	def remove_stopwords(self, text): 
	    stop_words = set(stopwords.words("english")) 
	    word_tokens = word_tokenize(text) 
	    filtered_text = [word for word in word_tokens if word not in stop_words] 
	    return " ".join(filtered_text)
	  
	  
	# stem words in the list of tokenised words 
	def stem_words(self, text): 
	    word_tokens = word_tokenize(text) 
	    stems = [stemmer.stem(word) for word in word_tokens] 
	    return stems 
	  
	# lemmatize string 
	def lemmatize_word(self, text): 
	    word_tokens = word_tokenize(text) 
	    # provide context i.e. part-of-speech 
	    lemmas = [lemmatizer.lemmatize(word, pos ='v') for word in word_tokens] 
	    return " ".join(lemmas) 

	def remove_tag_NNP(self, words_tokenize):
	  wordtags = nltk.pos_tag(words_tokenize)
	  words_result = []
	  for wt in wordtags:
	    if wt[1] != 'NNP':
	      words_result.append(wt[0].lower())
	  return " ".join(words_result)

	def clean_text(self, document):
		doc_remove_tag_NNP = self.remove_tag_NNP(word_tokenize(document))
		doc_lower = self.text_lowercase(doc_remove_tag_NNP)
		doc_convertNumber = self.convert_number(doc_lower)
		doc_remove_punctuation = self.remove_punctuation(doc_convertNumber)
		doc_remove_whitespace = self.remove_whitespace(doc_remove_punctuation)
		doc_remove_stopwords = self.remove_stopwords(doc_remove_whitespace)
		doc_lematize = self.lemmatize_word(doc_remove_stopwords)
		return doc_lematize

	def predict(self):
		dict_category = {
			'sport' : 'SPORTS',
			'politics' : 'POLITIC',
			'technology' : 'TECHNOLOGY',
			'entertainment' : 'ENTERTAINMENT',
			'business' : 'BUSINESS'
		} 

		processing_text = [self.clean_text(self.text)]
		x = self.tfidf.transform(self.vectorizer.transform(processing_text)).toarray()
		y_pred = self.model.predict(x)
		return dict_category[self.le.inverse_transform(y_pred.tolist())[0]]
# text = """
# President Biden misspoke in a speech Thursday offering updates on an update on vaccination progress in the U.S., referring to his vice president as "President Harris." 

# "When President Harris and I took ..." Biden said, before momentarily pausing, "a virtual tour of a vaccination site in Arizona not long ago, one of the nurses on that tour injecting people, giving vax each shot, was like administering a dose of hope." 

# At the same time, the president announced the administration would achieve its goal of 100 million vaccines administered in 100 days on Friday, the 58th day of the new administration. At this point, Biden said, 65% of people aged 65 and older have received at least one dose of a Covid-19 vaccine.
# """
# clf = DocClassification(text)
# print(clf.predict())

# INSERT INTO public."DB2_CATEGORY"(
# 	id, "nameCategory")
# 	VALUES (1, 'SPORTS');
	
# INSERT INTO public."DB2_CATEGORY"(
# 	id, "nameCategory")
# 	VALUES (2, 'POLITIC');

# INSERT INTO public."DB2_CATEGORY"(
# 	id, "nameCategory")
# 	VALUES (3, 'TECHNOLOGY');

# INSERT INTO public."DB2_CATEGORY"(
# 	id, "nameCategory")
# 	VALUES (4, 'ENTERTAINMENT');

# INSERT INTO public."DB2_CATEGORY"(
# 	id, "nameCategory")
# 	VALUES (5, 'BUSINESS');
# INSERT INTO public."DB2_CATEGORY"(
# 	id, "nameCategory")
# 	VALUES (6, 'UNKNOWN');



