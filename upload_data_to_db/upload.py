import json
import os
from utils.db_connection import get_db
from datetime import datetime
from processing_logs_functions.add_to_logs import update_processing_logs



def upload_contests_from_json():
    logs=[]
    try:
        # Connect to the database
        db = get_db()
        logs.append(f"Connected to db! - {datetime.now()}")

        
        # Connect to the Contests collection
        contests_collection = db["Contests"]
        logs.append(f"Connected to collection Contests! - {datetime.now()} ")

        
        # Path to the upload file
        upload_file_path = "updates/need_upload.json"
        
        # Check if file exists
        if not os.path.exists(upload_file_path):
            print(f"Upload file not found: {upload_file_path}")
            logs.append(f"Update file not found: {update_file_path} - {datetime.now()} ")

            return
        upload_data=[]
        
        # Read data from the JSON file
        with open(upload_file_path, 'r', encoding='utf-8') as file:
            upload_data = json.load(file)
        
        # Check if there are items to upload
        if not upload_data or len(upload_data) == 0:
            print("No uploads found in the file.")
            logs.append(f"No updates Required - {datetime.now()} ")

            return
        
        # Insert all documents in the collection at once
        result = contests_collection.insert_many(upload_data)
        
        print(f"Successfully uploaded {len(result.inserted_ids)} contests from updates/need_upload.json")
        logs.append(f"Successfully uploaded {len(result.inserted_ids)} contests from updates/need_upload.json - {datetime.now()}")
        
        # Clear the file after successful upload
        with open(upload_file_path, 'w', encoding='utf-8') as file:
            json.dump([], file)
        print("Upload file cleared for next run")
        logs.append(f"Upload file cleared for next run")

            
    except Exception as e:
        print(f"Error uploading contests: {str(e)}")
        logs.append(f"Error uploading contests: {str(e)} - {datetime.now()}")
    update_processing_logs(logs,"Updating Documents...")



