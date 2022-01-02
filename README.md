# Bchecker

Bchecker is a plagiarism checker that check whether the content is plagiarised or not.

# How it works

* Use Google API to search online.
* The matched contents of the resulting URL are compared to the base text.
* Display the similarity score and the matched urls.
* Hightlight overlap words.

# Installation

These instructions presume that you already have Python installed and that you have Python in your Windows environment variables.
* Open command line
* Run the following command:
```bash 
easy_install pip
```
* Then install the required libraries in requirement.txt.

```bash 
pip install [package]
```
# Python scripts

There are 3 main scripts.

* main.py

Main script that gives the result of plagiarism.

* st_app.py

Scripts that using streamlit to open website.

* convert_image_to_text.py

Scripts that support convert digital writing image to plain text.

