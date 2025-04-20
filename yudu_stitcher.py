import requests
import json
import os
import base64
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from PIL import Image



yudu_book_url = input("[1] Enter the book's url: ")
yudu_key_hex = input("[2] Enter the book's key (as hex): ")

yudu_key = binascii.unhexlify(yudu_key_hex)

yudu_info_json_url = yudu_book_url[0:yudu_book_url.find("index.html")] + "yuduBook.json"

yudu_json_request = requests.get(yudu_info_json_url)

yudu_info_dict = json.loads(yudu_json_request.text)

if yudu_json_request.status_code == 200:   
    
    print("Book " + yudu_info_dict["yuduBook"]["settings"]["name"] + " (id: " + str(yudu_info_dict["yuduBook"]["settings"]["id"]) + ") fetched with response code " +  str(yudu_json_request.status_code))
else:
    print("Request Failed with code " + str(yudu_json_request.status_code))
    quit()


yudu_tiles = []

def fetch_tiles():
    yudu_tile_folders = []
    
    for page_number, folder in enumerate(yudu_info_dict["yuduBook"]["pages"]):
        yudu_folder_iv = binascii.unhexlify(folder["iv"])
        yudu_folder_ciphertext = base64.b64decode(folder["data"])
        cipher = AES.new(yudu_key, AES.MODE_CBC, yudu_folder_iv)
        yudu_folder_plaintext = json.loads(unpad(cipher.decrypt(yudu_folder_ciphertext), AES.block_size).decode("utf-8"))["folder"]
        print("Page " + str(page_number) + "'s folder is " + yudu_folder_plaintext)
        yudu_tile_folders.append(yudu_folder_plaintext)
    
    page_images = []
    for folder_number, folder in enumerate(yudu_tile_folders):
        base_tile_url = yudu_book_url[0:yudu_book_url.find("index.html")] + "tiles/"
        try:
            tile1 = Image.open(urlopen(base_tile_url + folder + "/tile-0-0-0.jpg"))
            tile2 = Image.open(urlopen(base_tile_url + folder + "/tile-0-1-0.jpg"))
            tile3 = Image.open(urlopen(base_tile_url + folder + "/tile-0-0-1.jpg"))
            tile4 = Image.open(urlopen(base_tile_url + folder + "/tile-0-1-1.jpg"))
            tile5 = Image.open(urlopen(base_tile_url + folder + "/tile-0-0-2.jpg"))
            tile6 = Image.open(urlopen(base_tile_url + folder + "/tile-0-1-2.jpg"))

        except HTTPError as e:
            if e.code == 404:
                print("Error fetching one or more tile, tile not found")
            elif e.code == 403:
                print("Error fetching one or more tile, unauthorised (403)")
            else:
                print("Something went wrong with fetching one or more tile.\nCode:\t" + str(e.code) + "\nReason:\t" + e.reason)
        except URLError as e:
            print("Something went wrong with fetching one or more tile.\n" + e.reason)
        

        
        print("All tiles on page " + str(folder_number) + " fetched successfully.") 
        
        page_width = tile1.size[0] + tile2.size[0]
        page_height = tile1.size[1] + tile3.size[1] + tile5.size[1]

        page_image = Image.new("RGBA", (page_width, page_height))


        page_image.paste(tile1)
        page_image.paste(tile2, (tile1.size[0], 0))
        page_image.paste(tile3, (0, tile1.size[1]))
        page_image.paste(tile4, (tile3.size[0], tile2.size[1]))
        page_image.paste(tile5, (0, tile3.size[1] * 2))
        page_image.paste(tile6, (tile5.size[0], tile4.size[1] * 2))
        """
        page_image.show()
        go_prompt = input("Continue? (y/n): ")
        if go_prompt == "y":
            continue
        elif go_prompt == "n":
            print("Stopping.")
            quit()
        else:
            print("Unrecognised input.\nAbort.")
            quit()
        
        
        """
        page_images.append(page_image)

    return page_images

        


page_images_for_pdf = fetch_tiles()

page_images_for_pdf[0].save(yudu_info_dict["yuduBook"]["settings"]["name"] + "." + str(yudu_info_dict["yuduBook"]["settings"]["id"]) + "_ebook.pdf" , "PDF", resolution=100.0, save_all=True, append_images=page_images_for_pdf[1:])


print("Book Successfully saved as PDF.")
