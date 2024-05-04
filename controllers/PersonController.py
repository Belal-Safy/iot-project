import os
import uuid
from flask import request
from firebase_admin import db
from services.ResponseHandler import ResponseHandler
from services.face_recognition import FaceRecognition
import time

# ------------------------------------------- Get All People -------------------------------------------
def getAllPeople():
    type = request.args.get('type')
    ref = db.reference('people')
    people = ref.get()

    # add id to person data
    formatted_people = []
    for person_id, person_data in people.items():
        person_data['id'] = person_id
        formatted_people.append(person_data)
        
    people = formatted_people
    
    if type == 'criminal':
        people = [person for person in people if person['case'] == 'criminal']
    elif type == 'missing':
        people = [person for person in people if person['case'] == 'missing']

    return ResponseHandler.success_response(data=people)

# ------------------------------------------- Get Single Person -------------------------------------------
def getPerson(person_id):
    ref = db.reference('people')
    person = ref.child(person_id).get()
    if person:
        return ResponseHandler.success_response(data=person)
    else:
        return ResponseHandler.error_response(error='Person not found', status_code=404)

# ------------------------------------------- Add Person -------------------------------------------
def addPerson():
    person = request.form.to_dict()     
    images = request.files.getlist('images[]')
    
    user_images = []
    
    # Process each image
    allowed_extensions = {'png', 'jpg', 'jpeg'}
    for img in images:
        if not img.filename.lower().endswith(tuple(allowed_extensions)):
            return ResponseHandler.error_response(error='Invalid image format', status_code=400)
        # Generate a random filename
        random_filename = str(uuid.uuid4()) + "." + img.filename.rsplit('.', 1)[1].lower()
        image_path = os.path.join("public/images/people", random_filename)

        # Save the image locally
        img.save(image_path)

        # Get embedding from the saved image
        embedding = FaceRecognition.get_embedding(image_path)
        if embedding is None:
            # Delete the invalid image file
            os.remove(image_path)
            return ResponseHandler.error_response(error='Error generating embedding', status_code=500)
        
        new_img = {
            "img_name": random_filename,
            "embedding": embedding
        }
        
        user_images.append(new_img)
    
    # Add person to database
    person['images'] = user_images
    person['created_at'] = int(time.time())
    person['updated_at'] = int(time.time())
    ()
    ref = db.reference('people')
    new_person_ref = ref.push(person)
    # Return response with person ID
    return ResponseHandler.success_response(msg='Person added successfully', data={'id': new_person_ref.key})

# ------------------------------------------- Update Person -------------------------------------------
def updatePerson(person_id):
    data = request.json
    ref = db.reference('people')
    person_ref = ref.child(person_id)
    if person_ref.get():
        data['updated_at'] = int(time.time())
        person_ref.update(data)
        return ResponseHandler.success_response(msg='Person updated successfully')
    else:
        return ResponseHandler.error_response(error='Person not found', status_code=404)

# ------------------------------------------- Delete Person -------------------------------------------
def deletePerson(person_id):
    ref = db.reference('people')
    person_ref = ref.child(person_id)
    if person_ref.get():
        person_ref.delete()
        return ResponseHandler.success_response(msg='Person deleted successfully')
    else:
        return ResponseHandler.error_response(error='Person not found', status_code=404)
