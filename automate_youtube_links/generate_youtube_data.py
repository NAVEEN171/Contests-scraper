from googleapiclient.discovery import build
import json
from dotenv import load_dotenv
import os
import re

load_dotenv()

# YouTube API setup
API_KEY = os.environ.get("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=API_KEY)

def find_high_view_videos(contest_name,platform_name):
    # Search for videos about the specific contest
    query = f"{platform_name} {contest_name} solutions"
    search_response = youtube.search().list(
        q=query,
        part="id,snippet",
        maxResults=10,  # Increased to get more candidates
        type="video"
    ).execute()
    
    video_ids = [item["id"]["videoId"] for item in search_response["items"]]
    
    # Get video statistics to sort by view count
    videos_response = youtube.videos().list(
        part="statistics,snippet",
        id=",".join(video_ids)
    ).execute()
    
    results = []
    for video in videos_response["items"]:
        title = video["snippet"]["title"]
        
        # Get thumbnails - YouTube provides different sizes
        thumbnails = video["snippet"]["thumbnails"]
        # Choose the highest quality available, falling back to smaller ones if needed
        thumbnail_url = (
            thumbnails.get("maxres", {}).get("url") or
            thumbnails.get("high", {}).get("url") or
            thumbnails.get("medium", {}).get("url") or
            thumbnails.get("default", {}).get("url")
        )
        
        # Calculate how closely the title matches our query
        query_terms = set(query.lower().split())
        title_terms = set(title.lower().split())
        match_score = len(query_terms.intersection(title_terms)) / len(query_terms)
        
        # Check if both "LeetCode" and the contest name appear in the title
        contains_platform = platform_name.lower() in title.lower()
        contains_contest = contest_name.lower() in title.lower()

        if(match_score>0):
            results.append({
            "title": title,
            "url": f"https://youtube.com/watch?v={video['id']}",
            "thumbnail": thumbnail_url,
            "views": int(video["statistics"]["viewCount"]),
            "channel": video["snippet"]["channelTitle"],
            "match_score": match_score,
            "exact_match": contains_platform and contains_contest
            })
    
    # Sort by views (highest first)
    results = sorted(results, key=lambda x: x["views"], reverse=True)
    
    # Filter for exact matches first, then high view counts
    exact_matches = [v for v in results if v["exact_match"]]
    if exact_matches:
        results = exact_matches
    
    return results

# Example usage
# contest = "Biweekly Contest 85"
# high_view_videos = find_high_view_videos(contest)
# print(json.dumps(high_view_videos, indent=2))