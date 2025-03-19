from datetime import datetime
import os
import json
def update_processing_logs(new_logs, title):
    """Update the processing_logs.json file with new logs"""
    log_file_path = "updates/processing_logs.json"
    
    # Create log entry with source
    log_entry = {
        "title": title,
        "timestamp": datetime.now().isoformat(),
        "logs": new_logs
    }
    
    try:
        # Check if file exists and has content
        if os.path.exists(log_file_path) and os.path.getsize(log_file_path) > 0:
            with open(log_file_path, 'r') as file:
                try:
                    log_data = json.load(file)
                    
                    # If it's not in the expected format, initialize properly
                    if not isinstance(log_data, list):
                        log_data = [{"logs": []}]
                        
                    # If the list exists but is empty, add the first entry
                    if len(log_data) == 0:
                        log_data.append({"logs": []})
                    
                    # If logs key exists in the first item and is a list, append to it
                    if "logs" in log_data[0] and isinstance(log_data[0]["logs"], list):
                        log_data[0]["logs"].append(log_entry)
                    else:
                        # Otherwise create the logs array
                        log_data[0]["logs"] = [log_entry]
                        
                except json.JSONDecodeError:
                    # If file is not valid JSON, initialize with new structure
                    log_data = [{"logs": [log_entry]}]
        else:
            # Create new file with initial structure
            log_data = [{"logs": [log_entry]}]
        
        # Write updated logs back to file
        with open(log_file_path, 'w') as file:
            json.dump(log_data, file, indent=2)
            
    except Exception as e:
        print(f"Error updating processing logs: {str(e)}")
