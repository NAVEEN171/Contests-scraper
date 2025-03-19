# Coding Contests Frontend Documentation

This document provides information about the frontend implementation of the Coding Contests application, which uses MUI components for the UI and Redux for state management.

## Folder Structure

```
src/
├── assets/            # Static assets like images, icons, etc.
├── components/        # Reusable UI components
│   ├── ContestListing/  # Components for displaying contest listings
│   ├── Filters/         # Filter components for the filtering system
│   ├── Loaders/         # Loading components and animations
│   └── UI/              # Generic UI components
├── pages/             # Page components for different routes
├── store/             # Redux store configuration
│   └── Substores/      # Redux slices for different features
├── App.css            # Main application styles
├── App.jsx            # Main application component
├── index.css          # Global styles
└── main.jsx           # Entry point for the application
```





## Filtering System

The application implements a comprehensive filtering system that uses search parameters synced with filter states:

1. **Contest Status**: Filter contests by their status
   - Available options: Active, Upcoming, Expired
   - Maps to the `Status` query parameter

2. **Platform Filter**: Filter contests by platform
   - Available options: CodeChef, CodeForces, LeetCode
   - Maps to the `Platform` query parameter

3. **Active Contests Toggle**: Show only currently active contests
   - Maps to the `Active` query parameter (Boolean)

4. **Solutions Toggle**: Show only contests with available solutions
   - Maps to the `Solutions` query parameter (Boolean)

5. **Date Range Filter**: Find contests within specific dates
   - Maps to the `ContestPeriod` query parameter
   - Format: "YYYY-MM-DD,YYYY-MM-DD"

6. **Duration Filter**: Filter contests by their length
   - Maps to the `duration` query parameter
   - Unit: hours (e.g., 3 hours)

7. **Latest First Sorting**: Sort contests by start time
   - Maps to the `Latest` query parameter (Boolean)
   - Enabled by default
  

#### Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| Page | Number | Page number for pagination (default: 1) |
| Solutions | Boolean | When true, returns only contests with available solutions |
| Active | Boolean | When true, returns only active contests |
| Status | String | Comma-separated list of contest statuses to filter by (Active, Upcoming, Expired) |
| Platform | String | Comma-separated list of platforms to filter by (CodeChef, CodeForces, LeetCode) |
| ContestPeriod | String | Date range in format "YYYY-MM-DD,YYYY-MM-DD" |
| duration | Number | Filter contests by duration (in hours) |
| Latest | Boolean | When true, sorts contests by start time in descending order |


