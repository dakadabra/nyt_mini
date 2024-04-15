import re

# Regular expression to match timestamps
timestamp_regex = r"\[(\d{4}-\d{2}-\d{2}, \d{1,2}:\d{2}:\d{2} (?:AM|PM))\]"

# Regular expression to get info from URLs
url_search_regex = r"\[\d{4}-\d{2}-\d{2}, \d{1,2}:\d{2}:\d{2} (?:AM|PM)\] ~?\s*([^\s:]+(?: [^\s:]+)*)?:.*?d=(\d{4}-\d{2}-\d{2}).*?t=(\d+)&"

# Regular expression to match solved crossword time
crossword_time_regex = r"\[\d{4}-\d{2}-\d{2}, \d{1,2}:\d{2}:\d{2} (?:AM|PM)\] ~?\s*([^\s:]+(?: [^\s:]+)*)?:.*?I solved the (\d{1,2}/\d{1,2}/\d{4}) New York Times Mini Crossword in (\d+:\d{2})!"

# Regular expressions for different formats to match
custom_formats = {
    "URL": r".*https://www\.nytimes\.com/badges.*",
    "Crossword": r".*I solved the (\d{1,2}/\d{1,2}/\d{4}) New York Times Mini Crossword in (\d+:\d{2})!.*",
    # Add more custom formats if needed
}
    
def time_to_seconds(time_str):
    # Split the time string into minutes and seconds
    minutes, seconds = map(int, time_str.split(':'))
    
    # Calculate total seconds
    total_seconds = minutes * 60 + seconds
    
    return total_seconds

def find_solve_time(text):
    # Find all lines matching the solved crossword time format
    match = re.search(crossword_time_regex, text)
    name = match[1]
    date = match[2].replace("/", "-")
    solve_time = match[3]
    return name, date, solve_time

# Function to check if a piece of text matches a given format
def check_format(text, format_regex):
    return re.match(format_regex, text) is not None

# Read the input file
with open("input_file.txt", "r") as file:
    text = file.read()

# Find all timestamps
timestamps = re.findall(timestamp_regex, text)

# Open a new file for writing output
with open("output_file.txt", "w") as output_file:
    for i in range(len(timestamps)-1):
        # Get the text between two timestamps
        start_index = text.find(timestamps[i]) - 1
        end_index = text.find(timestamps[i+1]) - 1
        text_between_timestamps_newlines = text[start_index:end_index].strip()
        text_between_timestamps = text_between_timestamps_newlines.replace("\n", " ")

        # Check if the text matches any custom format
        for format_name, format_regex in custom_formats.items():
            if check_format(text_between_timestamps, format_regex):
                # If a match is found, print out different things based on the format
                if format_name == "URL":
                    match = re.search(url_search_regex, text_between_timestamps)
                    if match:
                        name, date, number = match.groups()
                        output_file.write(f"{name}, {date}, {number}\n")
                elif format_name == "Crossword":
                    # print("---"+text_between_timestamps+"---")
                    name, date, solve_time = find_solve_time(text_between_timestamps)
                    solve_time_in_seconds = time_to_seconds(solve_time)
                    output_file.write(f"{name}: {date}, {solve_time_in_seconds}\n")
                elif format_name == "CustomFormat1":
                    output_file.write(f"Custom format 1 matched between timestamps {timestamps[i]} and {timestamps[i+1]}: {text_between_timestamps}\n")
                # Add more conditions for other formats as needed
                break  # Break the loop after the first match
        # else:
        #     # If no match is found, print a default message
        #     output_file.write(f"No matching format found between timestamps {timestamps[i]} and {timestamps[i+1]}\n")
