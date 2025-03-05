import json
import webbrowser
import requests
import os
from pprint import pprint

# Importowanie lub tworzenie pliku credentials
if not os.path.exists("credentials.py"):
    api_key = input("Podaj swój API Key: ")
    with open("credentials.py", "w") as f:
        f.write(f'API_KEY = "{api_key}"\n')
        f.write('headers = {"x-api-key": API_KEY}\n')

import credentials

def load_json_to_python_format(response):
    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        print("Bad format:", response.text)
        return None

def get_cats_breeds_description():
    r = requests.get("https://api.thecatapi.com/v1/breeds", headers=credentials.headers)
    return load_json_to_python_format(r)

def cats_breeds_id_list(breeds_description):
    return [breed["id"] for breed in breeds_description]

def create_breeds_names_list(breeds_description):
    return [breed["name"] for breed in breeds_description]

def create_cat_breeds_id_dictionary(cats_breeds_id_list):
    return {i: cats_breeds_id_list[i] for i in range(len(cats_breeds_id_list))}

def create_cat_breeds_names_dictionary(breeds_names_list):
    return {i: breeds_names_list[i] for i in range(len(breeds_names_list))}

def show_favorite_cats(user_id):
    r = requests.get("https://api.thecatapi.com/v1/favourites", 
                     params={"sub_id": user_id}, headers=credentials.headers)
    return load_json_to_python_format(r)

def draw_random_cat():
    r = requests.get("https://api.thecatapi.com/v1/images/search?size=full", headers=credentials.headers)
    return load_json_to_python_format(r)[0]

def draw_random_cat_by_breed(selected_number, breeds_dict):
    params = {"breed_ids": breeds_dict[selected_number]}
    r = requests.get("https://api.thecatapi.com/v1/images/search?size=full", params=params, headers=credentials.headers)
    return load_json_to_python_format(r)[0]

def add_favourite_cat(cat_id, user_id):
    data = {"image_id": cat_id, "sub_id": user_id}
    r = requests.post("https://api.thecatapi.com/v1/favourites", json=data, headers=credentials.headers)
    return load_json_to_python_format(r)

def remove_cat_from_favourites(favourite_cat_id):
    r = requests.delete(f"https://api.thecatapi.com/v1/favourites/{favourite_cat_id}", headers=credentials.headers)
    return load_json_to_python_format(r)

def open_webbrowser_tab(open_url, cat):
    if open_url.upper() == "Y":
        webbrowser.open_new_tab(cat["url"])

def main():
    print("----------------------------------------")
    user_id = "einawomaragorp_ąjsap_ąjom"
    user_name = "uczeń"
    print(f"Hello {user_name}!")
    print("This game allows you to find the best cat picture you've ever seen!")

    favourite_cats = show_favorite_cats(user_id)
    print("Here are your favorite cat pictures:")
    pprint(favourite_cats)
    print("----------------------------------------")

    breeds_description = get_cats_breeds_description()
    if not breeds_description:
        print("Error loading breeds.")
        return
    
    cats_breeds_id_list = cats_breeds_id_list(breeds_description)
    breeds_names_list = create_breeds_names_list(breeds_description)
    breeds_id_dict = create_cat_breeds_id_dictionary(cats_breeds_id_list)
    breeds_names_dict = create_cat_breeds_names_dictionary(breeds_names_list)

    amount_of_drawn_cats = int(input("Draw cats. Enter amount (1-5): "))
    while amount_of_drawn_cats < 1 or amount_of_drawn_cats > 5:
        amount_of_drawn_cats = int(input("Enter a valid number (1-5): "))
    
    breed_choice = input("Would you like to select the cat breed? Y/N ")
    
    if breed_choice.upper() == "Y":
        pprint(breeds_names_dict)
        selected_number = int(input("Write number: "))
        for _ in range(amount_of_drawn_cats):
            cat = draw_random_cat_by_breed(selected_number, breeds_id_dict)
            print(f"Breed: {breeds_names_list[selected_number]} {cat['url']}")
            open_webbrowser_tab(input("Open in browser? Y/N: "), cat)
            if input("Add to favourites? Y/N: ").upper() == "Y":
                add_favourite_cat(cat["id"], user_id)
    else:
        for _ in range(amount_of_drawn_cats):
            cat = draw_random_cat()
            print(cat["url"])
            open_webbrowser_tab(input("Open in browser? Y/N: "), cat)
            if input("Add to favourites? Y/N: ").upper() == "Y":
                add_favourite_cat(cat["id"], user_id)

if __name__ == "__main__":
    main()
