from datetime import datetime, timedelta
import pytz

def convert_starts_in_to_datetime(starts_in_text):
    """Convert 'Starts in Xd Yh Zm' format to ISO 8601 datetime string."""
    # Handle empty or None input
    if not starts_in_text:
        return ""
        
    # Extract the time components
    time_parts = starts_in_text.replace("Starts in ", "").split()
    
    # Initialize timedelta components
    days, hours, minutes, seconds = 0, 0, 0, 0
    
    # Parse each part
    for part in time_parts:
        if part.endswith('d'):
            days = int(part[:-1])
        elif part.endswith('h'):
            hours = int(part[:-1])
        elif part.endswith('m'):
            minutes = int(part[:-1])
        elif part.endswith('s'):
            seconds = int(part[:-1])
    
    # Calculate the future time
    current_time = datetime.now(pytz.UTC)
    future_time = current_time + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    
    # Format the result as ISO 8601 string
    iso_date = future_time.isoformat().replace("+00:00", "Z")
    
    return iso_date



def convert_leetcode_datetime_to_iso(date_str):
    """
    Convert LeetCode datetime format (e.g., 'Mar 2, 2025 8:00 AM GMT+5:30') to ISO format
    Returns the date in format: '2025-03-02T02:30:00Z'
    """
    try:
        # Handle empty strings
        if not date_str or len(date_str.strip()) == 0:
            return ""
            
        # Check if the string contains timezone info
        if "GMT" in date_str:
            # Split into date part and timezone part
            date_parts = date_str.split("GMT")
            date_part = date_parts[0].strip()
            tz_part = date_parts[1] if len(date_parts) > 1 else "+0000"
            
            # Parse the date without timezone
            dt = datetime.strptime(date_part, "%b %d, %Y %I:%M %p")
            
            # Handle timezone with colon (like +5:30)
            if ':' in tz_part:
                sign = -1 if tz_part.startswith('-') else 1
                hour_part, minute_part = tz_part[1:].split(':')
                tz_hours = int(hour_part) * sign
                tz_minutes = int(minute_part) * sign
            else:
                # Handle format without colon
                if tz_part.startswith('-'):
                    tz_hours = -int(tz_part[1:3]) if len(tz_part) >= 3 else 0
                    tz_minutes = 0
                else:
                    tz_hours = int(tz_part[1:3]) if len(tz_part) >= 3 else 0
                    tz_minutes = 0
            
            # Calculate total minutes offset for pytz
            total_minutes = tz_hours * 60 + tz_minutes
            
            # Create a fixed timezone with the calculated offset
            tz = pytz.FixedOffset(total_minutes)
            dt = dt.replace(tzinfo=tz)
            
            # Convert to UTC
            dt_utc = dt.astimezone(pytz.UTC)
            
            # Format as ISO string
            return dt_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
        else:
            # Handle date-only format
            dt = datetime.strptime(date_str, "%b %d, %Y")
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception as e:
        print(f"Error converting date '{date_str}': {str(e)}")
        return date_str  # Return original if parsing fails


def convert_to_utc_formatted(date_string):
    """Convert 'Apr/05/2025 20:05UTC+5.5' format to ISO 8601 UTC datetime string."""
    # Handle empty input
    if not date_string:
        return ""
        
    # Split the date and timezone parts
    parts = date_string.split("UTC")
    if len(parts) != 2:
        return ""
        
    date_part, timezone_part = parts
    
    # Parse the date part
    try:
        parsed_date = datetime.strptime(date_part.strip(), "%b/%d/%Y %H:%M")
    except ValueError:
        return ""
    
    # Create a timezone-aware datetime based on the offset
    try:
        if "+" in timezone_part:
            hours, minutes = timezone_part.replace("+", "").split(".")
            offset_hours = int(hours)
            offset_minutes = int(float("0." + minutes) * 60)
        else:
            hours, minutes = timezone_part.replace("-", "").split(".")
            offset_hours = -int(hours)
            offset_minutes = -int(float("0." + minutes) * 60)
            
        # Create the timezone
        from_zone = pytz.FixedOffset(offset_hours * 60 + offset_minutes)
        
        # Make the datetime timezone-aware
        parsed_date = parsed_date.replace(tzinfo=from_zone)
        
        # Convert to UTC
        utc_date = parsed_date.astimezone(pytz.UTC)
        
        # Format as ISO 8601 string
        iso_date = utc_date.isoformat().replace("+00:00", "Z")
        
        return iso_date
    except Exception:
        return ""

def calculate_end_time(start_time_str, duration_str):
    """Calculate end time from start time and duration, returning ISO 8601 format."""
    # Handle empty input
    if not start_time_str:
        return ""
    
    try:
        # Try standard format with time
        start_time = datetime.strptime(start_time_str, "%d %b %Y %a %H:%M")
    except ValueError:
        try:
            # Try ISO format
            start_time = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
        except ValueError:
            try:
                # Try alternative format (May 1, 2022)
                start_time = datetime.strptime(start_time_str, "%b %d, %Y")
                # Set to midnight
                start_time = start_time.replace(hour=0, minute=0)
            except ValueError:
                # If all parsing attempts fail
                return ""
    
    # Parse duration
    try:
        hours, minutes = map(int, duration_str.split(':'))
        duration = timedelta(hours=hours, minutes=minutes)
    except (ValueError, AttributeError):
        # Default to 0 duration if parsing fails
        duration = timedelta(hours=0, minutes=0)
    
    # Calculate end time
    end_time = start_time + duration
    
    # Convert to UTC if it's not timezone-aware
    if not end_time.tzinfo:
        end_time = pytz.UTC.localize(end_time)
    
    # Format as ISO 8601 string
    iso_date = end_time.isoformat().replace("+00:00", "Z")
    
    return iso_date