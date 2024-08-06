import json
import webbrowser
from pprint import pprint
import requests
import credentials


def load_json_to_python_format(response):
    try:
        content = response.json()
    except json.decoder.JSONDecodeError:
        print("bad format" , response.text)
    else:
        return content

def get_cats_breeds_description():
    r = requests.get("https://api.thecatapi.com/v1/breeds")
    return load_json_to_python_format(r)

def cats_breeds_id_list(breedsDescription):
    catsBreedsIdList  = [
        line["id"]
        for line in breedsDescription
        ]
    return  catsBreedsIdList

def create_breeds_names_list():
    return [
        BreedName["name"]
        for BreedName in breedsDescription
        ]

def create_cat_breeds_id_dictionary(catsBreedsIdList):
    return {
        number : catsBreedsIdList[number]
        for number in range(len(catsBreedsIdList))
        }
    
def create_cat_breeds_names_dictionary(breedsNamesList):
    return {
    breed : breedsNamesList[breed]
    for breed in range(len(catsBreedsIdList))
    }
  
def show_favorite_cats_assigned_to_sub_id (userId):
    params = {
        "sub_id" : userId
        }
    r = requests.get("https://api.thecatapi.com/v1/favourites/", params=params,
                     headers=credentials.headers)
    return load_json_to_python_format(r)

def draw_random_cat_full_picture():
        r = requests.get("https://api.thecatapi.com/v1/images/search?size=full",
                         headers=credentials.headers)
        return load_json_to_python_format(r)[0]

def draw_random_cat_with_chosen_breed_full_picture(selectedNumber):
    params = {
        "breed_ids" : sequenceCatBreedsIdDictionary[selectedNumber]
        }
    r = requests.get("https://api.thecatapi.com/v1/images/search?size=full",params=params,
                     headers=credentials.headers)
    return load_json_to_python_format(r)[0]

def add_favourite_cat_to_favourites(catId, userId):
    data = {
        "image_id" : catId,
        "sub_id" : userId
        }
    r = requests.post("https://api.thecatapi.com/v1/favourites", json=data,
                      headers=credentials.headers)
    return load_json_to_python_format(r)

def open_new_webbrowser_tab(openUrl, yourCat):
    if openUrl.upper() == ("Y"):
        webbrowser.open_new_tab(yourCat["url"])
    else:
        print("no open")

def remove_cat_from_favourites(userId, favouriteCatId):
   
    r = requests.delete("https://api.thecatapi.com/v1/favourites/"+favouriteCatId,
                      headers=credentials.headers)

    return load_json_to_python_format(r)

def check_result_from_remove_favourite_cat(resultFromRemoveFavouriteCat):
    try:
        if (resultFromRemoveFavouriteCat["message"] == "SUCCESS"):
            print("cat removed")
    except TypeError:
        print("You wrote wrong id")

print("----------------------------------------")    
userId = "einawomaragorp_ąjsap_ąjom"
userName = "uczeń"
    
print("Hello " ,userName, "!")
print("""This game allows you to find best picture of cat you have ever seen!
here you can draw pictures, then added your best choises to your favourites !""")

favouriteCats = show_favorite_cats_assigned_to_sub_id(userId) #ulubione koty 
print(" Here are your favourite cat pictures:")
pprint(favouriteCats)
print(" ----------------------------------------")

breedsDescription = get_cats_breeds_description() # opis ras
catsBreedsIdList = cats_breeds_id_list(breedsDescription)   # lista id ras
breedsNamesList = create_breeds_names_list()                # lista nazw ras

amountOfDrawnCats = int(input("""Draw cats.
Enter here amount of images you want to draw:
min 1: max 5: """))
while (amountOfDrawnCats < 1 or amountOfDrawnCats > 5):    
    amountOfDrawnCats = int(input("min 1: max 5 "))

sequenceCatBreedsIdDictionary = create_cat_breeds_id_dictionary(catsBreedsIdList) # do numerków  przypisuję id rasy
sequenceCatBreedsNamesDictionary = create_cat_breeds_names_dictionary(breedsNamesList)

breedsChose = input(" Would you like to select the cat breed?  Y/N ")
newlyAddedCatInfo = {}
if (breedsChose.upper() == "Y"):
    print("Select breeds --> write number")
    pprint(sequenceCatBreedsNamesDictionary) #słownik by wybrać odpowiedni numer rasy.
    selectedNumber = int(input("Write number "))
    i = 0
    while i < amountOfDrawnCats:
        yourCat = draw_random_cat_with_chosen_breed_full_picture(selectedNumber)
        print("Breed you Chosen:",breedsNamesList[selectedNumber]," ",yourCat["url"]) 
        openUrl = input("Do you want to open url? Y/N ")
        open_new_webbrowser_tab(openUrl, yourCat) 
        favouriteChose = input(" Would you like to add your selected cat to favourites? Y/N ")
        if favouriteChose.upper() == ("Y"):
            resultFromAddingFavouriteCat = add_favourite_cat_to_favourites(yourCat["id"], userId) # otrzymam {'message': 'SUCCESS', 'id': 00000}
            newlyAddedCatInfo = {resultFromAddingFavouriteCat["id"] : yourCat["url"]}   # słownik id : url
        else:
            print("No added")
        i += 1    
else:
    print("Random breed")  
    i = 0
    while i < amountOfDrawnCats:
        yourCat = draw_random_cat_full_picture()
        pprint(yourCat["url"])
        openUrl = input("Do you want to open url? Y/N ") 
        open_new_webbrowser_tab(openUrl, yourCat)  
        favouriteChose = input(" Would you like to add your selected cat to favourites? Y/N ")
        if favouriteChose.upper() == ("Y"):
            resultFromAddingFavouriteCat = add_favourite_cat_to_favourites(yourCat["id"], userId)
            newlyAddedCatInfo = {resultFromAddingFavouriteCat["id"] : yourCat["url"]}
        else:
            print("No added") 
        i += 1
        
print("----------------------------------------")    

            
favouriteCatsById = {
    favouriteCat["id"] : favouriteCat["image"]["url"] 
    for favouriteCat in favouriteCats
    }
newlyAddedCatInfo.update(newlyAddedCatInfo)
pprint(favouriteCatsById)
favouriteCatId = input("Do you want to remove cat from favourites? Write here id: ")
resultFromRemoveFavouriteCat = remove_cat_from_favourites(userId, favouriteCatId) # rezultat usunięcia  SUCCESS lub TypeError
check_result_from_remove_favourite_cat(resultFromRemoveFavouriteCat)

