from datetime import datetime
import pytz

# Your local timezone, for example 'US/Eastern', 'Asia/Kolkata', etc.
local_timezone = pytz.timezone('US/Eastern')  # Replace with your local timezone

# Example local time (you can replace this with your actual local time)
local_time_str = "2024-12-17 12:27:00"  # Replace with your local time string

# Convert string to datetime object
local_time = datetime.strptime(local_time_str, "%Y-%m-%d %H:%M:%S")

# Localize the datetime to your local timezone
localized_time = local_timezone.localize(local_time)

# Convert to UTC
utc_time = localized_time.astimezone(pytz.utc)

# Print the result
print("Local time:", localized_time)
print("UTC time:", utc_time)
