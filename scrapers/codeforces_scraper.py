from playwright.sync_api import sync_playwright

import json
import os
from processing_logs_functions.add_to_logs import update_processing_logs


from format_dates import convert_to_utc_formatted,convert_starts_in_to_datetime,calculate_end_time
from Add_to_Json.Update_Jsonfiles import append_to_json_file
from datetime import datetime



def scrape_codeforces_contests(page):
    # Initialize logs array
    logs = []
    logs.append(f"Started scraping CodeForces contests - {datetime.now()}")
    currentlogs=[]
    
    logs.append(f"Navigating to Codeforces contests page... - {datetime.now()}")
    baseUrl = "https://codeforces.com"
    
    try:
        # Wait for the table body to load
        page.wait_for_selector("tbody", timeout=30000)
        logs.append(f"Page loaded successfully - {datetime.now()}")
        
        # Get all tbody elements
        tbodies = page.query_selector_all("tbody")
        
        all_contest_data = []
        
        # Work with the first tbody (future contests)
        if len(tbodies) > 0:
            first_tbody = tbodies[0]
            
            # Get all rows in the first tbody
            rows = first_tbody.query_selector_all("tr")
            
            # Skip the header row
            first_tbody_contests = []
            
            # Start from index 1 to skip the header row
            for i in range(1, len(rows)):
                row = rows[i]
                
                # Get all cells in the row
                cells = row.query_selector_all("td")
                
                if len(cells) >= 6:
                    # Extract contest name (1st td)
                    contest_name = cells[0].inner_text().strip()
                    
                    # Extract start time (3rd td)
                    start_time = cells[2].inner_text().strip()
                    start_time = convert_to_utc_formatted(start_time)
                    
                    # Extract duration (4th td)
                    duration = cells[3].inner_text().strip()
                    
                    # Extract registration link (6th td)
                    registration_td = cells[5]
                    registration_link = "unspecified"
                    
                    # Check if there's an 'a' tag for registration
                    register_link_element = registration_td.query_selector("a")
                    if register_link_element:
                        registration_link = register_link_element.get_attribute("href")
                        last_num_array=registration_link.split("/")
                        if(len(last_num_array)>0):
                            last_num=last_num_array[-1]
                            contest_name=contest_name+" "+last_num

                    elif "before registration" in registration_td.inner_text().lower():
                        registration_link = "unspecified"
                    else:
                        registration_link = registration_td.inner_text().strip()
                    
                    
                    # Create a data object for this contest
                    contest_info = {
                        "contestName": contest_name,
                        "startTime": start_time,
                        "duration": duration,
                        "contestLink": registration_link,
                        "Status": "Active",
                        "Platform": "CodeForces",
                        "attempts": 0,
                        "youtubeLinks": []
                    }
                    if(registration_link == "unspecified"):
                        contest_info["Status"] = "Upcoming"
                    else:
                        contest_info["contestLink"] = baseUrl + contest_info["contestLink"]
                    
                    first_tbody_contests.append(contest_info)
                    
                    if(len(contest_info["startTime"]) and len(contest_info["duration"])):
                        end_time = calculate_end_time(contest_info["startTime"], contest_info["duration"])
                        contest_info["endTime"] = end_time
                    
            
            # Add first tbody contests to the overall data
            all_contest_data.extend(first_tbody_contests)
        
        # Work with the second tbody (past contests)
        if len(tbodies) > 1:
            second_tbody = tbodies[1]
            
            # Get all rows in the second tbody
            rows = second_tbody.query_selector_all("tr")
            
            # Skip the header row
            second_tbody_contests = []
            
            # Start from index 1 to skip the header row, and take only two rows
            for i in range(1, min(3, len(rows))):  # Get only five rows from the past contests
                row = rows[i]
                
                # Get all cells in the row
                cells = row.query_selector_all("td")
                
                if len(cells) >= 4:
                    # Extract contest name (1st td)
                    contest_name = cells[0].inner_text().strip()
                    if "enter" in contest_name.lower():
                        contest_name = contest_name.split("\n")[0]
                    
                    # Extract registration link (1st td, second a tag)
                    a_tags = cells[0].query_selector_all("a")
                    registration_link = ""
                    if len(a_tags) >= 2:
                        registration_link = a_tags[1].get_attribute("href")
                    
                    # Extract start time (3rd td)
                    start_time = cells[2].inner_text().strip()
                    start_time = convert_to_utc_formatted(start_time)
                    
                    # Extract duration (4th td)
                    duration = cells[3].inner_text().strip()
                    
                    # Create a data object for this contest
                    contest_info = {
                        "contestName": contest_name,
                        "startTime": start_time,
                        "duration": duration,
                        "contestLink": registration_link,
                        "Status": "Expired",
                        "Platform": "CodeForces",
                        "attempts": 0,
                        "youtubeLinks": []
                    }
                    
                    contest_info["contestLink"] = baseUrl + contest_info["contestLink"]
                    if(len(contest_info["startTime"]) and len(contest_info["duration"])):
                        end_time = calculate_end_time(contest_info["startTime"], contest_info["duration"])
                        contest_info["endTime"] = end_time
                    
                    second_tbody_contests.append(contest_info)
            
            # Add second tbody contests to the overall data
            all_contest_data.extend(second_tbody_contests)
        
        # Print summary
        logs.append(f"Total contests extracted (both tbodies): {len(all_contest_data)} - {datetime.now()}")
        logs.append(f"CodeForces contests checking for updation/insertion - {datetime.now()}")
        
        # Save to file
        currentlogs=append_to_json_file("contests_data/codeforces_all_contests.json", all_contest_data, "codeforces")
        logs.append(f"Data saved to codeforces_all_contests.json - {datetime.now()}")
        logs.append(f"Completed scraping CodeForces ! -{datetime.now()}")

        
    except Exception as e:
        logs.append(f"Error scraping CodeForces contests: {str(e)} - {datetime.now()}")
        logs.append(f"reason-failed - {datetime.now()}")
        update_processing_logs(logs, "scraping leetcode coding platform")

    
    # Update the processing logs JSON file
    logs.extend(currentlogs)


    update_processing_logs(logs, "scraping codeforces coding platform")
    
    return all_contest_data

