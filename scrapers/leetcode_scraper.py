from playwright.sync_api import sync_playwright
from format_dates import convert_to_utc_formatted, convert_starts_in_to_datetime, calculate_end_time, convert_leetcode_datetime_to_iso
from Add_to_Json.Update_Jsonfiles import append_to_json_file
from processing_logs_functions.add_to_logs import update_processing_logs

from datetime import datetime
import pytz
import json
import os

def scrape_leetcode_contests(page):
    # Initialize logs array
    logs = []
    logs.append(f"Started scraping leetcode contests - {datetime.now()}")
    currentlogs=[]
    
    # Navigate to the LeetCode contests page
    logs.append(f"Navigating to LeetCode contests page... - {datetime.now()}")
    baseUrl = "https://leetcode.com"
    
    try:
        # Wait for the content to load
        page.wait_for_selector(".swiper-slide", timeout=30000)
        logs.append(f"Page loaded successfully - {datetime.now()}")
        
        # Extract all elements with class "swiper-slide"
        contest_elements = page.query_selector_all(".swiper-slide")
        
        # Create an array to store the data
        all_contests = []  # Changed variable name to avoid confusion
        
        # Extract specific information from each swiper-slide
        for index, element in enumerate(contest_elements):
            
            # Initialize data for this slide
            slide_data = {
                "contestLink": "",
                "contestName": "",
                "startTime": "",
                "Status": "",
                "duration": "1:30",
                "Platform": "LeetCode",
                "attempts": 0,
                "youtubeLinks": [],
                "endTime": ""
            }
            
            # Extract all a tags
            a_tags = element.query_selector("a")
            
            href = a_tags.get_attribute("href")
            slide_data["contestLink"] = baseUrl + href
            
            starts_in = element.query_selector("[class*='neIP_']")
            if(starts_in):
                Starts_in_data = starts_in.inner_text()
                exact_time = convert_starts_in_to_datetime(Starts_in_data)
                slide_data["startTime"] = exact_time
            
            # Extract divs with className h-[54px]
            contestFullDetails = element.query_selector("div.h-\\[54px\\]")
            
            text = contestFullDetails.inner_text()
            
            # Split the text to get individual pieces of information
            details_parts = text.split("\n")  # Changed variable name
            
            slide_data["contestName"] = details_parts[0]
            
            if len(details_parts) == 3:
                if details_parts[1] == "Ended":
                    slide_data["Status"] = "Expired"
                    slide_data["startTime"] = details_parts[2]
                    # Convert date-only format to ISO string
                    try:
                        dt = datetime.strptime(details_parts[2], "%b %d, %Y")
                        slide_data["startTime"] = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
                    except ValueError:
                        logs.append(f"Could not parse date: {details_parts[2]} - {datetime.now()}")
            else:
                slide_data["Status"] = "Active"
                
            if(len(slide_data["startTime"]) and len(slide_data["duration"]) and slide_data["Status"] == "Active"):
                end_time = calculate_end_time(slide_data["startTime"], slide_data["duration"])
                slide_data["endTime"] = end_time
            
            # Add to our array
            all_contests.append(slide_data)
            
        elements = page.query_selector_all('div.flex.h-\\[86px\\].items-center')
        
        for index, element in enumerate(elements[:max(3, len(elements))]):
            
            # Initialize data for this slide
            slide_data = {
                "contestLink": "",
                "contestName": "",
                "startTime": "",
                "Status": "Expired",
                "duration": "1:30",
                "Platform": "LeetCode",
                "attempts": 0,
                "youtubeLinks": [],
                "endTime": ""
            }
            a_tag=element.query_selector('a')
            href = a_tag.get_attribute("href")

            slide_data["contestLink"]=baseUrl+href  
            divs_inside_a = a_tag.query_selector_all('div')
        
            # Skip first div, process the second div
            if len(divs_inside_a) >= 2:
                second_div = divs_inside_a[1]
            
                # Get the span (contest name)
                span = second_div.query_selector('span')
                if span:
                    slide_data["contestName"] = span.inner_text()
            
                # Get the div after the span (start time)
                # This assumes the start time div is after the span
                start_time_div = second_div.query_selector('div')
                if start_time_div:
                    date_str = start_time_div.inner_text()
                    slide_data["startTime"] = convert_leetcode_datetime_to_iso(date_str)
            
            if(len(slide_data["startTime"]) and len(slide_data["duration"])):
                end_time = calculate_end_time(slide_data["startTime"], slide_data["duration"])
                slide_data["endTime"] = end_time
                
            all_contests.append(slide_data)
        
        # Print the array length to verify
        logs.append(f"Total contests extracted: {len(all_contests)} - {datetime.now()}")
        logs.append(f"Leetcode contests checking for updation/insertion - {datetime.now()}")
        
        currentlogs=append_to_json_file("contests_data/leetcode_contest_data.json", all_contests, "leetcode")
        logs.append(f"Saved all data to leetcode_contest_data.json - {datetime.now()}")
        logs.append(f"Completed scraping Leetcode ! -{datetime.now()}")
        
    except Exception as e:
        logs.append(f"Error scraping LeetCode contests: {str(e)} - {datetime.now()}")
        logs.append(f"reason-failed - {datetime.now()}")
        update_processing_logs(logs, "scraping leetcode coding platform")

    logs.extend(currentlogs)
    
    # Update the processing logs JSON file
    update_processing_logs(logs, "scraping leetcode coding platform")
    
    return all_contests
