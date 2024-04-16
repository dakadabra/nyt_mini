# nyt_mini
Fun little side project to compare scores from our NYT Mini groupchat!
**Running the scripts:**
- First run filter.py
- then run get_metrics.py, which takes an optional argument of the form year-month-day (ex. 2024-01-01), so only data after that date will be processed.

**Files:**
- filter.py filters the raw chat data into cleaned_data.txt
- get_metrics.py processes cleaned_data.txt into different files
- average_placements.txt shows what position people get on average
- averages.txt shows peoples' average times
- first_places.txt shows how often people get first place
    It can be called with an input arg with the format year-month-day, so that only times after that date are analyzed
    - More metrics to come!
