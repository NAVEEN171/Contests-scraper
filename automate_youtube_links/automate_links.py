import json
import os
from utils.db_connection import get_db
from datetime import datetime, timedelta
import pytz
from automate_youtube_links.generate_youtube_data import find_high_view_videos
from processing_logs_functions.add_to_logs import update_processing_logs


def update_endtimes_and_get_eligible():
    logs = []
    try:
        # Connect to the database
        db = get_db()
        
        # Connect to the Contests collection
        contests_collection = db["Contests"]
        
        # Current time for comparisons
        current_time = datetime.now(pytz.UTC)
        day_ago = current_time - timedelta(days=1)
        day_ago_iso = day_ago.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Find eligible contests using aggregation
        eligible_contests = list(contests_collection.aggregate([
            {
                "$addFields": {
                    "effectiveEndTime": {
                        "$cond": {
                            "if": {"$or": [
                                {"$eq": ["$endTime", ""]}, 
                                {"$eq": ["$endTime", None]}
                            ]},
                            "then": "$startTime",
                            "else": "$endTime"
                        }
                    }
                }
            },
            {
                "$match": {
                    "Status": "Expired",
                    "attempts": {"$lte": 1},
                    "effectiveEndTime": {"$lt": day_ago_iso}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "contestName": 1,
                    "Platform": 1,
                    "startTime": 1,
                    "endTime": 1,
                    "effectiveEndTime": 1,
                    "contestLink": 1,
                    "attempts": 1,
                    "youtubeLinks": 1
                }
            },
            {
                "$sort": {"effectiveEndTime": -1}
            }
        ]))
        
        print(f"Found {len(eligible_contests)} contests eligible for video search")
        logs.append(f"Found {len(eligible_contests)} contests eligible for video search - {datetime.now()}")
        
        # Output the eligible contests
        if eligible_contests:
            print("\nEligible contests:")
            logs.append(f"\nEligible contests: - {datetime.now()}")
            for contest in eligible_contests:
                # For display purposes, calculate how many days ago
                end_time_str = contest["effectiveEndTime"]
                
                # Parse the ISO string to datetime for comparison
                end_time = datetime.fromisoformat(end_time_str.replace("Z", "+00:00"))
                days_ago = (current_time - end_time).days
                
                contest_info = f"- {contest['contestName']} ({contest['Platform']}) - Ended {days_ago} days ago, Attempts: {contest.get('attempts', 0)}"
                print(contest_info)
                logs.append(f"{contest_info} - {datetime.now()}")
        
        # Ensure directory exists
        os.makedirs(os.path.dirname("automate_youtube_links/eligible_candidates.json"), exist_ok=True)
        
        # Save eligible contests to the specified file
        with open("automate_youtube_links/eligible_candidates.json", "w", encoding="utf-8") as f:
            json.dump(eligible_contests, f, indent=2)
        print("Saved eligible contests to automate_youtube_links/eligible_candidates.json")
        logs.append(f"Saved eligible contests to automate_youtube_links/eligible_candidates.json - {datetime.now()}")
        
        # If we have eligible candidates, pass them to the processing function
        if len(eligible_contests) > 0:
            process_eligible_candidates(eligible_contests)
        
        # Save logs to file
        update_processing_logs(logs,"Retrieving the Expired Contest");        
                
        return eligible_contests
        
    except Exception as e:
        error_msg = f"Error in update_endtimes_and_get_eligible: {str(e)}"
        print(error_msg)
        logs.append(f"{error_msg} - {datetime.now()}")
        
        # Save logs even if there's an error
       
                
        return []

def process_eligible_candidates(eligible_candidates):
    logs = []
    try:
        # Connect to the database
        db = get_db()
        contests_collection = db["Contests"]
        
        updates_needed = []
        
        for contest in eligible_candidates:
            contest_name = contest["contestName"]
            platform = contest["Platform"]
            current_attempts = contest.get("attempts", 0)
            
            print(f"Processing {contest_name} ({platform})...")
            logs.append(f"Processing {contest_name} ({platform})... - {datetime.now()}")
            
            # Call the function to find high view videos
            youtube_results = find_high_view_videos(contest_name, platform)
            
            if youtube_results:
                print(f"Found {len(youtube_results)} videos for {contest_name}")
                logs.append(f"Found {len(youtube_results)} videos for {contest_name} - {datetime.now()}")
                
                # Create update document
                update_doc = {
                    "attempts": current_attempts + 1,
                    "youtubeLinks": youtube_results,
                    "update": [{
                        "attempts": current_attempts + 1,
                        "youtubeLinks": youtube_results
                    }]
                }
                
                # Add to updates array
                updates_needed.append({
                    "contestName": contest_name,
                    "Platform": platform,
                    "attempts": current_attempts + 1,
                    "youtubeLinks": youtube_results,
                    "update": [{
                        "attempts": current_attempts + 1,
                        "youtubeLinks": youtube_results
                    }]
                })
            else:
                print(f"No videos found for {contest_name}")
                logs.append(f"No videos found for {contest_name} - {datetime.now()}")
                
                # Still increment the attempt count
                updates_needed.append({
                    "contestName": contest_name,
                    "Platform": platform,
                    "attempts": current_attempts + 1,
                    "update": [{
                        "attempts": current_attempts + 1
                    }]
                })
        
        # Save all updates to need_update.json
        if updates_needed:
            # Ensure directory exists
            os.makedirs(os.path.dirname("updates/need_update.json"), exist_ok=True)
            
            # Write updates to the specified path
            with open("updates/need_update.json", "w", encoding="utf-8") as f:
                json.dump(updates_needed, f, indent=2)
            print(f"Saved {len(updates_needed)} updates to updates/need_update.json")
            logs.append(f"Saved {len(updates_needed)} updates to updates/need_update.json - {datetime.now()}")
        
        
        
        update_processing_logs(logs,"Updating youtube solutions");        
     
        return updates_needed
    
    except Exception as e:
        error_msg = f"Error in process_eligible_candidates: {str(e)}"
        print(error_msg)
        logs.append(f"{error_msg} - {datetime.now()}")
        
      
                
        return []