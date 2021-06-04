import streamlit as st
import matplotlib.pyplot as plt
import random

import spacy
from spacy.lang.en.stop_words import STOP_WORDS

from string import punctuation

from heapq import nlargest

import pyautogui

stopwords = list(STOP_WORDS)
nlp = spacy.load('en_core_web_sm')
punctuation = punctuation + '\n'


def word_frequency(doc):
	print("In word_frequency")

	tokens = [token.text for token in doc]

	word_frequencies = {}
	for word in doc:
		if word.text.lower() not in stopwords:
			if word.text.lower() not in punctuation:
				if word.text not in word_frequencies.keys():
					word_frequencies[word.text] = 1
				else:
					word_frequencies[word.text] += 1
	
	max_frequency = max(word_frequencies.values())
	for word in word_frequencies.keys():
		word_frequencies[word] = word_frequencies[word]/max_frequency

	return word_frequencies


def sentence_score(word_frequencies, doc):
	print("In sentence_score")

	sentence_tokens = [sent for sent in doc.sents]

	sentence_scores = {}

	for sent in sentence_tokens:
		for word in sent:
			if word.text.lower() in word_frequencies.keys():
				if sent not in sentence_scores.keys():
					sentence_scores[sent] = word_frequencies[word.text.lower()]
				else:
					sentence_scores[sent] += word_frequencies[word.text.lower()]
	return sentence_scores,sentence_tokens



def get_summary(sentence_scores,sentence_tokens):
	print("In get_summary")

	select_length = int(len(sentence_tokens)*0.3)
	
	summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)

	final_summary = [word.text for word in summary]
	summary = ' '.join(final_summary)


	return summary

def summarize_text(text):
	
	doc = nlp(text)

	word_frequencies= word_frequency(doc)
	print("word_frequencies: ",word_frequencies)

	sentence_scores, sentence_tokens= sentence_score(word_frequencies, doc)
	print("sentence_scores: ",sentence_scores)

	summary =  get_summary(sentence_scores, sentence_tokens)
	print("summary: ",summary)

	return summary 





def random_colors(number_of_colors):
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                 for i in range(number_of_colors)]
    return color


        
def plot(wf_key,wf_value):
    
    y_pos =[i+1 for i in range(len(wf_key))]
    plt.barh(y_pos, wf_value, color = random_colors(len(wf_value)))

    plt.yticks(y_pos, wf_key)
    plt.tick_params(
		axis='x',
		which='both', 
		bottom=False,
		top=False,
		labelbottom=False)
    return plt

def plot_wf(word_frequencies):
    
    st.set_option('deprecation.showPyplotGlobalUse', False)
    wf_key, wf_value = [],[]
    for key,value in word_frequencies.items():
        wf_key.append(key)
        wf_value.append(value)

    n = len(wf_key)
    while n > 20:
            st.pyplot(plot(wf_key[:20],wf_value[:20]).show())
            n = n-20
            wf_key = wf_key[20:]
            wf_value = wf_value[20:]
    wf_key =  [""]*(20-n) + wf_key
    wf_value =[0]*(20-n) + wf_value
    st.pyplot(plot(wf_key[:20],wf_value[:20]))








def main():

	st.title("Text Summarizer using NLP")

	text_placeholder = st.empty()
	button_placeholder = st.empty()

	text = text_placeholder.text_input("Enter text to be summarized","")
	if button_placeholder.button("Get Summary"):

		if len(text):
			doc = nlp(text)

			word_frequencies= word_frequency(doc)
			print("word_frequencies: ",word_frequencies)

			sentence_scores, sentence_tokens= sentence_score(word_frequencies, doc)
			print("sentence_scores: ",sentence_scores)

			summary =  get_summary(sentence_scores, sentence_tokens)
			print("summary: ",summary)

			
			text_placeholder.empty()
			button_placeholder.empty()
			st.subheader("Original Text")
			st.info(text)
			st.subheader("Summary")
			st.info(summary)


			st.markdown("<p style='text-align: center;'>Insights</p>", unsafe_allow_html=True)

			st.text("Length of Origional text: "+str(len(text)))
			st.text("Length of Summary: "+str(len(summary)))

			st.text("Frequency of each word")
			plot_wf(word_frequencies)

			if st.button("Try again"):
				pyautogui.hotkey('f5')

		else:
			st.warning("Please Enter some text")

if __name__ == "__main__":
	main()