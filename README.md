# nyt_mini
Fun little side project to compare scores from our NYT Mini groupchat!

Files:
- filter.py filters the raw chat data into cleaned_data.txt
- get_metrics.py processes cleaned_data.txt into averages.txt
    It can be called with an input arg with the format year-month-day, so that only times after that date are analyzed
    - More metrics to come!