import pytesseract
import pdf2image
import os

base_path = os.path.dirname(__file__)


def pdf2texts(path):
	texts_list = []
	images = pdf2image.convert_from_path(path, poppler_path=base_path + '/poppler-0.68.0/bin')
	for image in images:
		texts_list.append(pytesseract.image_to_string(image))
	text = ''
	for texts in texts_list:
		text += texts + '\n'
	return text


def image2text(path):
	text = pytesseract.image_to_string(path)
	return text


if __name__ == '__main__':
	texts = image2text(r'C:\Users\LENOVO\PycharmProjects\image\Show_proof.png')
	print(*texts)
