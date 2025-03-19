import json
import os
from utils.db_connection import get_db
from datetime import datetime
from processing_logs_functions.add_to_logs import update_processing_logs


def update_contests_from_json():
    logs=[]
    try:
        # Connect to the database
        db = get_db()
        logs.append(f"Connected to db! - {datetime.now()}")
        
        # Connect to the Contests collection
        contests_collection = db["Contests"]
        logs.append(f"Connected to collection Contests! - {datetime.now()} ")
        
        # Path to the update file
        update_file_path = "updates/need_update.json"
        
        # Check if file exists
        if not os.path.exists(update_file_path):
            print(f"Update file not found: {update_file_path}")
            logs.append(f"Update file not found: {update_file_path} - {datetime.now()} ")

            return
        
        # Read data from the JSON file
        with open(update_file_path, 'r', encoding='utf-8') as file:
            update_data = json.load(file)
        
        # Check if there are items to update
        if not update_data or len(update_data) == 0:
            print("No updates found in the file.")
            logs.append(f"No updates Required - {datetime.now()} ")

            return
        
        update_count = 0
        for contest in update_data:
            contest_name = contest.get("contestName")
            if not contest_name:
                print(f"Skipping update - missing contestName")
                logs.append(f"Skipping update  - missing contestName - {datetime.now()} ")

                continue
            
            # Check if the update field exists and is an array
            if "update" not in contest or not isinstance(contest["update"], list):
                print(f"Skipping contest {contest_name} - invalid or missing update field - {datetime.now()}")
                continue
            
            # Create update document using only the fields in the update array
            update_doc = {}
            for update_item in contest["update"]:
                # Each item in update array should be a dictionary with one key-value pair
                for field, value in update_item.items():
                    update_doc[field] = value
            
            # Update the document in the collection with only the specified fields
            if update_doc:
                result = contests_collection.update_one(
                    {"contestName": contest_name},
                    {"$set": update_doc}
                )
                
                if result.matched_count > 0:
                    update_count += 1
                    print(f"Updated contest: {contest_name} with fields: {list(update_doc.keys())}")
                    logs.append(f"Updated contest: {contest_name} with fields: {list(update_doc.keys())} - {datetime.now()} ")

                else:
                    print(f"Contest not found for update: {contest_name}")
                    logs.append(f"Contest not found for update: {contest_name}")

        
        print(f"Successfully updated {update_count} contests from updates/need_update.json")
        logs.append(f"Successfully updated {update_count} contests from updates/need_update.json - {datetime.now()}")

        
        # Clear the file after successful update
        with open(update_file_path, 'w', encoding='utf-8') as file:
            json.dump([], file)
        print("Update file cleared for next run")
        logs.append(f"Update file cleared for next run - {datetime.now()}")

            
    except Exception as e:
        print(f"Error updating contests: {str(e)}")
        logs.append(f"Error updating contests Reason: {str(e)} - {datetime.now()}")
    
    update_processing_logs(logs,"Updating Documents...")



