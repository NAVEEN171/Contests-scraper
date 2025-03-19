import json
import os
from utils.db_connection import get_db
from datetime import datetime

def upload_processing_logs():
    try:
        # Connect to the database
        db = get_db()
        
        # Connect to the Processing_logs collection
        logs_collection = db["Processing_logs"]
        
        # Path to the processing logs file
        logs_file_path = "updates/processing_logs.json"
        
        # Check if file exists
        if not os.path.exists(logs_file_path):
            print(f"Processing logs file not found: {logs_file_path}")
            return
        
        # Read logs from the JSON file
        with open(logs_file_path, 'r', encoding='utf-8') as file:
            file_logs = json.load(file)
        
        # Check if there are logs to insert
        if not file_logs or len(file_logs) == 0:
            print("No logs to process.")
            return
        
        # Insert logs to database
        result = logs_collection.insert_many(file_logs)
        print(f"Successfully inserted {len(result.inserted_ids)} log entries into database")
        
        # Clear the file after successful insertion by initializing with empty array
        with open(logs_file_path, 'w', encoding='utf-8') as file:
            json.dump([], file)
        print("Processing logs file cleared")
        
    except Exception as e:
        print(f"Error processing logs: {str(e)}")