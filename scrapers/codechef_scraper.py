from playwright.sync_api import sync_playwright
from Add_to_Json.Update_Jsonfiles import append_to_json_file
from datetime import datetime  # Import the datetime class
from processing_logs_functions.add_to_logs import update_processing_logs
import json
import os
from format_dates import convert_to_utc_formatted, convert_starts_in_to_datetime, calculate_end_time

def scrape_codechef_contests(page):
    # Initialize logs array
    logs = []
    currentlogs=[]
    logs.append(f"Started scraping CodeChef contests - {datetime.now()}")
    
    logs.append(f"Navigating to CodeChef contests page... - {datetime.now()}")
    all_contest_data = []

    
    try:
        # Wait for the table body to load
        page.wait_for_selector("tbody", timeout=30000)
        logs.append(f"Page loaded successfully - {datetime.now()}")
        
        # Get all tbody elements
        tbodies = page.query_selector_all("tbody")
        
        
        # Process the first tbody (Active contests)
        if len(tbodies) > 0:
            first_tbody = tbodies[0]
            
            # Get all rows in the first tbody
            rows = first_tbody.query_selector_all("tr")
            
            for i, row in enumerate(rows):
                
                # Extract all tds
                cells = row.query_selector_all("td")
                
                if len(cells) >= 4:
                    try:
                        # Contest Name: first td, second div
                        first_td_divs = cells[0].query_selector_all("div")
                        
                        # Contest Link: second td, second div, a tag href
                        second_td_divs = cells[1].query_selector_all("div")
                        contest_link = ""
                        if len(second_td_divs) >= 2:
                            a_tag = second_td_divs[1].query_selector("a")
                            contest_name = a_tag.inner_text()
                            if a_tag:
                                contest_link = a_tag.get_attribute("href")
                        
                        # Start Time: third td, second div
                        third_td_divs = cells[2].query_selector_all("div")
                        start_time = ""
                        if len(third_td_divs) >= 2:
                            start_time = third_td_divs[1].inner_text().strip()
                            start_time = start_time.replace("\n\n", " ")
                            # Convert to ISO format if possible
                            try:
                                dt = datetime.strptime(start_time, "%d %b %Y %a %H:%M")
                                start_time = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                            except ValueError:
                                logs.append(f"Could not parse date: {start_time} - {datetime.now()}")
                        
                        # Duration: fourth td, second div
                        fourth_td_divs = cells[3].query_selector_all("div")
                        duration = ""
                        if len(fourth_td_divs) >= 2:
                            duration = fourth_td_divs[1].inner_text().strip()
                            duration_list = duration.split(" ")
                            if(len(duration_list) == 4):
                                duration = duration_list[0] + ":" + duration_list[2]
                            else:
                                duration = duration_list[0] + ":" + "00"
                        
                        # Create data object
                        contest_info = {
                            "contestName": contest_name,
                            "contestLink": contest_link,
                            "startTime": start_time,
                            "duration": duration,
                            "Status": "Active",
                            "Platform": "CodeChef",
                            "attempts": 0,
                            "youtubeLinks": []
                        }
                        
                        if(len(contest_info["startTime"]) and len(contest_info["duration"])):
                           end_time = calculate_end_time(contest_info["startTime"], contest_info["duration"])
                           contest_info["endTime"] = end_time
                        
                        all_contest_data.append(contest_info)
                        
                    except Exception as e:
                        logs.append(f"Error processing row {i} from first tbody: {str(e)} - {datetime.now()}")
            
        
        # Process the third tbody (Past contests) - skip the second tbody
        if len(tbodies) > 2:
            third_tbody = tbodies[2]
            
            # Get all rows in the third tbody
            rows = third_tbody.query_selector_all("tr")
            
            # Only process the first four rows
            max_rows = min(4, len(rows))
            for i in range(max_rows):
                row = rows[i]
                
                # Extract all tds
                cells = row.query_selector_all("td")
                
                if len(cells) >= 4:
                    try:
                        # Contest Name: first td, second div
                        first_td_divs = cells[0].query_selector_all("div")
                        
                        # Contest Link: second td, second div, a tag href
                        second_td_divs = cells[1].query_selector_all("div")
                        contest_link = ""
                        if len(second_td_divs) >= 2:
                            a_tag = second_td_divs[1].query_selector("a")
                            if a_tag:
                                contest_name = a_tag.inner_text().split(" ")
                                contest_name = contest_name[0] + contest_name[1]
                                contest_link = a_tag.get_attribute("href")
                        
                        # Start Time: third td, second div
                        third_td_divs = cells[2].query_selector_all("div")
                        start_time = ""
                        if len(third_td_divs) >= 2:
                            start_time = third_td_divs[1].inner_text().strip()
                            start_time = start_time.replace("\n\n", " ")
                            # Convert to ISO format if possible
                            try:
                                dt = datetime.strptime(start_time, "%d %b %Y %a %H:%M")
                                start_time = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                            except ValueError:
                                logs.append(f"Could not parse date: {start_time} - {datetime.now()}")
                        
                        # Duration: fourth td, second div
                        fourth_td_divs = cells[3].query_selector_all("div")
                        duration = ""
                        if len(fourth_td_divs) >= 2:
                            duration = fourth_td_divs[1].inner_text().strip()
                            duration_list = duration.split(" ")
                            if(len(duration_list) == 4):
                                duration = duration_list[0] + ":" + duration_list[2]
                            else:
                                duration = duration_list[0] + ":" + "00"
                        
                        # Create data object
                        contest_info = {
                            "contestName": contest_name,
                            "contestLink": contest_link,
                            "startTime": start_time,
                            "duration": duration,
                            "Status": "Expired",
                            "Platform": "CodeChef",
                            "attempts": 0,
                            "youtubeLinks": []
                        }
                        
                        if(len(contest_info["startTime"]) and len(contest_info["duration"])):
                           end_time = calculate_end_time(contest_info["startTime"], contest_info["duration"])
                           contest_info["endTime"] = end_time
                        
                        all_contest_data.append(contest_info)
                        
                    except Exception as e:
                        logs.append(f"Error processing row {i} from third tbody: {str(e)} - {datetime.now()}")
            
        
        # Print final summary
        logs.append(f"Total contests extracted overall: {len(all_contest_data)} - {datetime.now()}")
        logs.append(f"CodeChef contests checking for updation/insertion - {datetime.now()}")
        
        # Save to file
        currentlogs=append_to_json_file("contests_data/codechef_all_contests.json", all_contest_data, "codechef")
        logs.append(f"Data saved to codechef_all_contests.json - {datetime.now()}")
        logs.append(f"Completed scraping CodeChef! -{datetime.now()}")

        
    except Exception as e:
        logs.append(f"Error scraping CodeChef contests: {str(e)} - {datetime.now()}")
        logs.append(f"reason-failed - {datetime.now()}")
        update_processing_logs(logs, "scraping codechef coding platform")

    logs.extend(currentlogs)
    
    # Update the processing logs JSON file
    update_processing_logs(logs, "scraping codechef coding platform")
    
    return all_contest_data


