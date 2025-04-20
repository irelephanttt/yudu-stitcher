# yudu-stitcher
A tool to download (some) Yudu ebooks, and save them as a pdf.
-------

## Setup 

Download the `yudu_sticher.py` file in the directory you want the book to be downloaded in.  
Install the dependencies with:
``` shell
pip install requests pillow binascii pycryptodome
```

## Usage

Run the script with
``` shell
python3 yudu_stitcher.py
````
You will be prompted for a url for a book, and a key. 

They key can be found by loading the ebook in a web browser, opening devtools, going to "Network" and checking the response for the "authenticateReader" request:
![image](https://github.com/user-attachments/assets/26c646d8-4724-4360-b03e-44aebbaf54e7)

This is neccessary for the script to work. 

The PDF will then be saved in the directory the script was ran in.
