from deepface import DeepFace
import numpy as np
from scipy.spatial.distance import cosine
import os
import pandas as pd

class FaceRecognition:
    @staticmethod
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

    @staticmethod
    def search_faces_in_frame(frame_path, people):
        # get real time image embedding
        frame_embedding = FaceRecognition.get_embedding(frame_path)

        # Compare between current frame with all people images  
        is_match = False
        found_person = None
        
        # loop over the list of people
        for person in people:
            # loop over the list of current person images
            for image in person["images"]:
                # compare frame embedding with person image embedding
                is_match, similarity_score = FaceRecognition.compare_embeddings(frame_embedding, image['embedding'])
                
                # if match found check similarity score
                if is_match:
                    # if similarity score is more than 0.5 return person id
                    if similarity_score > 0.5:
                        found_person = person['id']
                        break

            if(found_person):
                break

        return found_person
    
    @staticmethod
    def compare_embeddings(embedding1, embedding2, threshold=0.6):
        try:
            # Calculate cosine similarity between the two embeddings
            similarity_score = 1 - cosine(embedding1, embedding2)

            # Check if the similarity score exceeds the threshold
            if similarity_score >= threshold:
                return True, similarity_score
            else:
                return False, similarity_score

        except Exception as e:
            print(f"Error: {e}")
            return False, None
        
    # @staticmethod
    # def compare_embedding_with_df(single_embedding, embeddings_df, threshold=0.9):
    #     try:
    #         # Flatten the single embedding vector
    #         single_embedding_flat = np.array(single_embedding).flatten()

    #         # Initialize a list to store similarity scores
    #         similarity_scores = []

    #         # Iterate over each row in the embeddings DataFrame
    #         for index, row in embeddings_df.iterrows():
    #             # Get the embedding from the DataFrame and flatten it
    #             df_embedding_flat = np.array(row['Embedding']).flatten()

    #             # Calculate the cosine similarity between the single embedding and the embedding from the DataFrame
    #             similarity_score = 1 - cosine(single_embedding_flat, df_embedding_flat)
    #             similarity_scores.append(similarity_score)

    #         # Convert similarity_scores to numpy array
    #         similarity_scores = np.array(similarity_scores)

    #         # Check if any similarity score exceeds the threshold
    #         if np.any(similarity_scores >= threshold):
    #             # Get the index of the image with the highest similarity score
    #             max_index = np.argmax(similarity_scores)
    #             # Return True and the name of the image
    #             return True, embeddings_df.loc[max_index, 'Image_Name']

    #         # If no matching embedding is found, return False and None
    #         return False, None

    #     except Exception as e:
    #         # print(f"Error: {e}")
    #         return False, None

# example of the 3 functions 
# single_embedding = FaceRecognition.get_embedding("images/JtiGPl0ReaRPr9VY.jpg")
# folder_embeddings_df = generate_embeddings_for_folder("people")
# is_match, image_name = FaceRecognition.compare_embedding_with_df(single_embedding, folder_embeddings_df)
# print(f"Is match: {is_match}, Image name: {image_name}")
