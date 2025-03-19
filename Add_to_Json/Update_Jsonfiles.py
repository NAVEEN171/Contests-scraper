import os
import json
from datetime import datetime

def append_to_json_file(filename, new_data, platform):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    currentlogs=[]
    
    # Initialize existing data
    existing_data = []
    
    # Check if file exists and read existing data
    if os.path.exists(filename):
        currentlogs.append(f"{filename} exists - {datetime.now()}")

        try:
            with open(filename, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            # If file exists but isn't valid JSON (e.g., empty file)
            print(f"Warning: {filename} exists but contains invalid JSON. Starting fresh.")
            currentlogs.append(f"Warning: {filename} exists but contains invalid JSON. Starting fresh. -{datetime.now()}")

            existing_data = []
    
    data_to_append = []
    data_to_replace = []
    currentlogs.append(f"Checking for Updating and Inserting new Contests in {platform}. -{datetime.now()}")

    
    # if len(new_data) > 0:
    #     new_data[0]["Status"] = "Expired"
    #     new_data[0]["startTime"]="2025-03-12T20:00:00Z"

    
    if len(new_data):
        for ele in new_data:
            matched_content = None
            for existing_contest in existing_data:
                if ele["contestName"] == existing_contest["contestName"]:
                    # print(True)
                    matched_content = existing_contest 
                    matched_content["update"] = []

                    if ele["Status"] != existing_contest["Status"]:
                        matched_content["Status"] = ele["Status"]
                        matched_content["update"].append({"Status": ele["Status"]})
                        if ele["startTime"] != matched_content["startTime"]:
                           matched_content["startTime"] = ele["startTime"]
                           matched_content["update"].append({"startTime": ele["startTime"]})
                        if ele["contestLink"]!= matched_content["contestLink"]:
                            matched_content["startTime"]=ele["contestLink"]
                            matched_content["update"].append({"contestLink":ele["contestLink"]})
                        data_to_replace.append(matched_content)
                        

                    break
            if not matched_content:
                data_to_append.append(ele)

    # Only process uploads if there are items to append
    

    if len(data_to_append) > 0:
        Uploadpath = "updates/need_upload.json"
        existingUploadData = []
        totalData = []
        
        # Create directory if it doesn't exist
        
        if os.path.exists(Uploadpath):
            try:
                with open(Uploadpath, "r", encoding="utf-8") as f:
                    existingUploadData = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: {Uploadpath} exists but contains invalid JSON. Starting fresh.")
                existingUploadData = []
        
        if isinstance(existingUploadData, list):
            totalData = existingUploadData + data_to_append
        else:
            totalData = [existingUploadData, data_to_append]
        
        with open(Uploadpath, "w", encoding="utf-8") as f:
            json.dump(totalData, f, indent=2)
        print(f"Added {len(data_to_append)} items to need_upload.json")
        currentlogs.append(f"Added {len(data_to_append)} Contests to need_upload.json -{datetime.now()}")

    else:
        currentlogs.append(f"No Contests need to be Added -{datetime.now()}")


    # Only process updates if there are items to replace
    if len(data_to_replace) > 0:
        Updatepath = "updates/need_update.json"
        existingUpdateData = []
        totalUpdateData = []
        
        # Create directory if it doesn't exist
        
        if os.path.exists(Updatepath):
            try:
                with open(Updatepath, "r", encoding="utf-8") as f:
                    existingUpdateData = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: {Updatepath} exists but contains invalid JSON. Starting fresh.")
                existingUpdateData = []
        
        if isinstance(existingUpdateData, list):
            totalUpdateData = existingUpdateData + data_to_replace
        else:
            totalUpdateData = [existingUpdateData, data_to_replace]
        
        with open(Updatepath, "w", encoding="utf-8") as f:
            json.dump(totalUpdateData, f, indent=2)
        print(f"Added {len(data_to_replace)} items to need_update.json")
        currentlogs.append(f"Added {len(data_to_replace)} Contests to need_update.json -{datetime.now()}")
    else:
        currentlogs.append(f"No Contests need to be updated -{datetime.now()}")


    

    
    # Append new data
    combined_data = []
    if isinstance(existing_data, list):
        combined_data = existing_data + data_to_append
    else:
        # If for some reason existing_data isn't a list, make a new list with both
        combined_data = [existing_data, data_to_append]
    
    # Write combined data back to file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(combined_data, f, indent=2)
    
    return currentlogs