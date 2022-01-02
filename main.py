import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
from googlesearch import search
import requests
import numpy as np
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
stop_words = set(stopwords.words('english'))
marks = ['.', ',', ':', ';', '?', "'s"]


def curl(url):
	result = requests.get(url).content
	return result


def remove_tags(html):
	soup = BeautifulSoup(html, "html.parser")
	for data in soup(['style', 'script']):
		data.decompose()
	return ' '.join(soup.stripped_strings)


def clean_text(text):
	# Remove tags
	text = remove_tags(text)
	text.replace('Replacement Chacracter'.upper(), '')
	# Tokenize
	tokens = nltk.word_tokenize(text)
	filtered_words = [w for w in tokens if w in ['a', '.', ',', ':', ';', '?', "'s"] or
	                  (w.isalnum() and len(w) > 1)]
	cleaned_text = " ".join(filtered_words)
	return cleaned_text


def curl_and_clean(url):
	result = curl(url)
	cleaned_text = clean_text(result)
	return cleaned_text


def tokenize_text2search(text):
	le = WordNetLemmatizer()
	tokens = nltk.word_tokenize(text)
	for i in range(len(tokens)):
		tokens[i] = tokens[i].replace('.', '')
	filtered_words = [le.lemmatize(w) for w in tokens if
	                  not w.lower() in stop_words and w.isalpha()]
	for i in range(len(filtered_words)):
		filtered_words[i] = filtered_words[i].replace(".", "")
	cleaned_text = " ".join(filtered_words)
	return cleaned_text


def clean_sentences(list_sentences):
	list_unused_sentences = []
	for i in range(len(list_sentences)):
		list_sentences[i] = list_sentences[i].strip()
	new_sentences = [sentence for sentence in list_sentences if sentence not in list_unused_sentences]
	return new_sentences


def split_into_sentences(text):
	text = text.replace('\n\n', '.')
	text = text.replace('\n', ' ')
	sentences = [sentence.strip() for sentence in text.split('.') if sentence.strip() != '' and len(sentence.split())>2]
	return sentences


def sentences_similarity(sentence1, sentence2):
	words1 = nltk.word_tokenize(sentence1)
	words2 = nltk.word_tokenize(sentence2)
	similar_words = list(np.intersect1d(words1, words2))
	return similar_words


def text_similarity(sentences1, sentences2):
	similarity_matrix = np.zeros((len(sentences1), len(sentences2)), dtype=object)
	for i in range(len(sentences1)):
		for j in range(len(sentences2)):
			similar_words = sentences_similarity(sentences1[i].strip(), sentences2[j].strip())
			if len(similar_words) > len(sentences1[i].strip().split())/2:
				similarity_matrix[i][j] = similar_words
	return similarity_matrix


def texts_similarity(base_text, lst_texts):
	base_sentences = split_into_sentences(base_text)
	similarity_matrix_list = []
	for text in lst_texts:
		sentences = clean_sentences(text.split('.'))
		similarity_matrix = text_similarity(base_sentences, sentences)
		similarity_matrix_list.append(similarity_matrix)
	return similarity_matrix_list


def text_similarity_score(data):
	search_word = tokenize_text2search(data)
	curl_list = []
	url = []
	for search_url in search(search_word, tld="co.in", stop=20, pause=2):
		if search_url[-3:] == 'pdf':
			continue
		clean_curl = curl_and_clean(search_url)
		curl_list.append(clean_curl)
		url.append(search_url)

	matrix_list = texts_similarity(data, curl_list)

	similar_list = []
	iused_url = set({})
	for mi in range(len(matrix_list)):
		rows, columns = matrix_list[mi].shape
		similar = []
		for i in range(rows):
			for j in range(columns):
				if type(matrix_list[mi][i][j]) == list:
					similar.append([(i, j), matrix_list[mi][i][j]])
					iused_url.add(mi)
		similar_list.append(similar)

	used_url = [url[i] for i in iused_url]
	final_lst = []
	data = clean_text(data)
	data_sentences = split_into_sentences(data)
	for i in range(len(data_sentences)):
		lst = []
		for j in range(len(similar_list)):
			for info in similar_list[j]:
				if info[0][0] == i and len(info[1]) >= len(lst):
					lst = info[1]
		if len(lst) > 0:
			final_lst.append([i, lst])
	similar_words = set([word for word_lst in final_lst for word in word_lst[1] if word not in marks])
	data_words = set(word for sentence in data_sentences for word in sentence.split() if word not in marks)
	similarity_score = len(similar_words) / len(data_words)

	return similarity_score, similar_words, data, used_url
