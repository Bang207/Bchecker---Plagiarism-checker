import streamlit as st
import os
from PIL import Image
from convert_image_to_text import pdf2texts
from convert_image_to_text import image2text
import main
from load_css import local_css


def load_image(image_file):
	img = Image.open(image_file)
	return img


marks = ['.', ',', ':', ';', '?', "'s"]
icon = load_image('Bchecker.ico')
st.set_page_config(
	page_title='Bchecker',
	page_icon=icon
)
local_css("style.css")
st.markdown("<h><span class = 'header bold'>Bchecker - A Plagiarism Checker</span></h>", unsafe_allow_html=True)

menu = st.sidebar.selectbox('Menu', ('Home', 'Image', 'Text'))
text = ''
if menu == 'Home':
	st.markdown("<h><span class = 'header bold'>Welcome to my website</span></h>", unsafe_allow_html=True)
	st.subheader('Here are the guide lines:')
	st.write("* On the left, there is a select box for you to choose.")
	st.write('* Choose "Image" if you want to upload your image file.')
	st.write('* Choose "Text" if you want to copy and paste your text.')
elif menu == 'Image':
	file = st.file_uploader('')
	if file is not None:
		file_details = {'File_Name': file.name, 'File_Type': file.type}
		# Saving file
		with open(file.name, 'wb') as f:
			f.write(file.getbuffer())
		if file.type[:5] == 'image':
			# Convert image to text
			text = image2text(file.name)
		elif file.type[-3:] == 'pdf':
			# Convert image to text
			text = pdf2texts(file.name)

		else:
			st.write('This is not an image file!')

		if os.path.exists(file.name):
			os.remove(file.name)
		else:
			pass
elif menu == 'Text':
	text = st.text_area('Copy and Paste your document here')
if text != '':
	score, sim_words, clean_text, urls = main.text_similarity_score(text)
	data_words = clean_text.split()
	colored_text = '<h>'
	for i in range(len(data_words)):
		if data_words[i] in sim_words:
			data_words[i] = "<span class='bold highlight' >" + data_words[i] + "</span>"
		if data_words[i] in marks or i == 1:
			colored_text += data_words[i]
		else:
			colored_text += ' ' + data_words[i]
	colored_text += '</h>'
	st.markdown(colored_text, unsafe_allow_html=True)
	st.markdown(f'<h><span class = "bold">Rate: </span>{round(score, 4)*100}%</h>', unsafe_allow_html=True)
	st.markdown(f'<h><span class = "bold">List of plagiarized url:</span></h>', unsafe_allow_html=True)
	for url in urls:
		st.write(url)
