import re

# Regular expression to match timestamps and names
timestamp_name_regex = r"\[(\d{4}-\d{2}-\d{2}, \d{1,2}:\d{2}:\d{2} (?:AM|PM))\] (.+?):"

# Regular expression to match URLs
url_regex = r"(http[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)"

# Regular expression to match solved crossword time
crossword_time_regex = r"I solved the (\d{1,2}/\d{1,2}/\d{4}) New York Times Mini Crossword in (\d+:\d{2})!"

# Function to find the next URL after a given index in the text
def find_next_url(text, start_index):
    match = re.search(url_regex, text[start_index:])
    if match:
        return match.group(0)
    else:
        return None
    
def extract_date_and_number(url):
    # Regular expression pattern to match the date
    date_pattern = r'd=(\d{4}-\d{2}-\d{2})'

    # Regular expression pattern to match the number after '&'
    number_pattern = r'&t=(\d+)'

    # Find the date
    date_match = re.search(date_pattern, url)
    date = date_match.group(1) if date_match else None

    # Find the number after '&'
    number_match = re.search(number_pattern, url)
    number = number_match.group(1) if number_match else None

    return date, number

def time_to_seconds(time_str):
    # Split the time string into minutes and seconds
    minutes, seconds = map(int, time_str.split(':'))
    
    # Calculate total seconds
    total_seconds = minutes * 60 + seconds
    
    return total_seconds

def find_solve_time(text, start_index):
    # Find all lines matching the solved crossword time format
    match = re.search(crossword_time_regex, text[start_index:])
    date = match[1]
    solve_time = match[2]
    return date, solve_time
    # Write date and time to output file
    # output_file.write(f"Solved New York Times Mini Crossword on {date} in {time}\n")



# Read the input file
with open("test_in.txt", "r") as file:
    text = file.read()

# Open a new file for writing output
with open("output_file.txt", "w") as output_file:
    # Find all lines matching the timestamp and name format
    matches = re.findall(timestamp_name_regex, text)
    for match in matches:
        timestamp = match[0]
        name = match[1]
        # Find the next URL after the line
        next_url = find_next_url(text, text.find(match[1]) + len(match[1]))

        # if the next URL fits this format, check for the match with just text
        if next_url == "https://www.nytimes.com/crosswords/game/mini":
            date, solve_time = find_solve_time(text, text.find(match[1]) + len(match[1]))
            solve_time_in_seconds = time_to_seconds(solve_time)
            output_file.write(f"{name}: {date}, {solve_time_in_seconds}\n")
        elif next_url:
            date, solve_time = extract_date_and_number(next_url)
            # Write name and URL to output file
            output_file.write(f"{name}: {date}, {solve_time}\n")
        else:
            # If no URL found after the name, write a placeholder
            output_file.write(f"{name}: No URL found\n")
    

