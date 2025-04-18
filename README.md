
Sure! Here's a structured **README** for your project:

---

# Competitive Programming Contest Tracker

A Python-based scraper that extracts contest data from **LeetCode**, **CodeChef**, and **Codeforces**, handles dynamic content, and integrates with MongoDB and the YouTube Data API. This tool helps track upcoming and expired contests, attach video solutions, and keep data synchronized with minimal updates.

## Features

- **Dynamic Scraping**: 
  - Scrapes data from **LeetCode**, **CodeChef**, and **Codeforces** using **Playwright** to handle JavaScript-heavy content.
  
- **Contest Metadata**: 
  - Collects detailed information such as:
    - **Start Time**
    - **End Time**
    - **Duration**
    - **Expiration Status**
    - **Registration/Virtual Links**
  
- **Data Sync**:
  - Detects new or updated contests, organizes them, and syncs only necessary data to **MongoDB**, avoiding redundant writes.
  
- **YouTube Video Integration**:
  - Uses the **YouTube Data API** to fetch and link relevant video solutions to **expired contests**, with retry logic (up to 2 attempts per contest).

- **Logging**:
  - Implements step-wise logging for debugging, monitoring, and future scaling.

- **Local Execution**:
  - Built for local execution but easily integrates with automated schedulers like **cron jobs** or can be deployed to **cloud functions**.

## Technologies Used

- **Python**
- **Playwright** (for dynamic web scraping)
- **MongoDB** (for data storage)
- **YouTube Data API** (for fetching video solutions)
- **JSON files** (for local data tracking and comparison)
- **Logging** (for debugging and monitoring)

## How It Works

1. **Scraping**:
   - The scraper uses **Playwright** to handle the JavaScript rendering of dynamic pages and scrape contest details from **LeetCode**, **CodeChef**, and **Codeforces**.
   
2. **Data Comparison**:
   - The scraper compares the current scraped data with existing local records (stored in JSON files) to detect any new or updated contests.
   
3. **Data Sync to MongoDB**:
   - Once new or updated contests are identified, only the necessary changes are synced to the **MongoDB database**.

4. **YouTube Video Solutions**:
   - For contests that are expired, the scraper checks if relevant video solutions exist on YouTube using the **YouTube Data API**, and if they don’t, it attempts to fetch the video up to 2 times.
   
5. **Logging**:
   - Step-wise logging is implemented at each stage to track the scraping, comparison, update, and syncing processes.

## Installation

### Prerequisites

- **Python 3.x**
- **Playwright** (with installed browser binaries)
- **MongoDB** (or a MongoDB instance)
- **YouTube Data API Key** (for video solution fetching)

### Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/competitive-programming-contest-tracker.git
   cd competitive-programming-contest-tracker
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your **YouTube Data API** key in the script:

   ```python
   youtube_api_key = 'YOUR_YOUTUBE_API_KEY'
   ```

4. Configure your **MongoDB connection** if necessary, or ensure you have MongoDB running locally.

5. Run the scraper:

   ```bash
   python scraper.py
   ```

## Usage

1. The scraper will automatically start scraping contests from the specified platforms.
2. It will check for any new contests or updates, and sync the necessary data to MongoDB.
3. Expired contests will have video solutions fetched via the YouTube Data API, and retry logic will be applied if the video isn’t available on the first attempt.

## Future Enhancements

- **Automated Scheduling**: Implement scheduling using cron jobs or cloud functions to automate periodic scraping.
- **Data Visualization**: Add a dashboard to visualize contest data and trends.
- **More Platforms**: Extend scraping to other competitive programming platforms.

## Contributing

Feel free to fork the repository, create an issue, or submit a pull request for any enhancements, fixes, or new features. Contributions are always welcome!

---

Let me know if you need any adjustments or additional sections!
