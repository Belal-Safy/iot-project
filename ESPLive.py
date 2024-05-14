import requests
import os
import random
import string
from services.face_recognition import FaceRecognition
from controllers.PersonController import getAllPeople
    

# ----------------------- Get Current Frame From ESP32 Cam -----------------------
# 
#
def download_image(url, save_directory="static/images/detected"):
    # Make HTTP request to get the image
    response = requests.get(url)
    if response.status_code == 200:
        # Generate a random filename
        random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        # Get the file extension from the URL
        file_extension = "jpg"
        # Concatenate the random filename with the file extension
        filename = f"{random_filename}.{file_extension}"
        # Define the full path to save the image
        save_path = os.path.join(save_directory, filename)
        
        # Save the image to the specified directory
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Image downloaded and saved as {save_path}")
        return save_path
    else:
        print("Failed to download image")
        return None

# ---------------------------- Handel Found Person ----------------------------
# 
#
def takeAction(found_person):
    print("Found person: ", found_person['name'])



################################# Main Loop #################################
ESP_URL = "http://192.168.246.116/capture" 
while True:
    people = getAllPeople()["data"]
    frame_path = download_image(ESP_URL)
    if(frame_path):
        found_person = FaceRecognition.search_faces_in_frame(frame_path, people) 
        if(found_person):
            takeAction(found_person)
