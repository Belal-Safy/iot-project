# !pip install deepface

from deepface import DeepFace
import cv2
import numpy as np
import os
import pandas as pd


#function takes an img path return the embedings

def get_embedding(image_path):
    try:
        # Get embedding using DeepFace library
        embedding_objs = DeepFace.represent(img_path=image_path)

        # Check if the result is a list
        if isinstance(embedding_objs, list):
            # Extract embedding from the first item in the list
            embedding = embedding_objs[0]["embedding"]
            return embedding
        else:
            # print("Error: Unexpected result format from DeepFace.represent()")
            return None
    except Exception as e:
        # print(f"Error: {e}")
        return None



#function takes a folder path return imgs names and the embedings in df

def generate_embeddings_for_folder(folder_path):
    try:
        # Initialize an empty list to store embeddings and image names
        embeddings = []
        img_names = []

        # Iterate over each file in the folder
        for file_name in os.listdir(folder_path):
            # Check if the file is an image
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Construct the full path to the image file
                image_path = os.path.join(folder_path, file_name)

                # Get embedding using DeepFace library
                embedding_objs = DeepFace.represent(img_path=image_path)

                # Extract embedding and image name
                embedding = embedding_objs[0]["embedding"]

                # Append embedding and image name to the respective lists
                embeddings.append(embedding)
                img_names.append(file_name)

        # Create DataFrame from embeddings and image names
        embeddings_df = pd.DataFrame({'Image_Name': img_names, 'Embedding': embeddings})

        return embeddings_df

    except Exception as e:
        # print(f"Error: {e}")
        return None


# function takes an img path and folder path to check if this person exist or not 

def compare_embedding_with_df(single_embedding, embeddings_df, threshold=0.9):
    dfs = DeepFace.find(img_path = single_embedding, db_path = "people")
    return dfs
    try:
        # Flatten the single embedding vector
        single_embedding_flat = np.array(single_embedding).flatten()

        # Initialize a list to store similarity scores
        similarity_scores = []

        # Iterate over each row in the embeddings DataFrame
        for index, row in embeddings_df.iterrows():
            # Get the embedding from the DataFrame and flatten it
            df_embedding_flat = np.array(row['Embedding']).flatten()

            # Calculate the cosine similarity between the single embedding and the embedding from the DataFrame
            similarity_score = 1 - cosine(single_embedding_flat, df_embedding_flat)
            similarity_scores.append(similarity_score)

        # Convert similarity_scores to numpy array
        similarity_scores = np.array(similarity_scores)

        # Check if any similarity score exceeds the threshold
        if np.any(similarity_scores >= threshold):
            # Get the index of the image with the highest similarity score
            max_index = np.argmax(similarity_scores)
            # Return True and the name of the image
            return True, embeddings_df.loc[max_index, 'Image_Name']

        # If no matching embedding is found, return False and None
        return False, None

    except Exception as e:
        # print(f"Error: {e}")
        return False, None



# example of the 3 functions 

# single_embedding = get_embedding("images/JtiGPl0ReaRPr9VY.jpg")
# folder_embeddings_df = generate_embeddings_for_folder("people")
# is_match, image_name = compare_embedding_with_df(single_embedding, folder_embeddings_df)
# print(f"Is match: {is_match}, Image name: {image_name}")


dfs = DeepFace.find(img_path = "images/JtiGPl0ReaRPr9VY.jpg", db_path = "people")
print(dfs)