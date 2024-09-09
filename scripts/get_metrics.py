from datetime import datetime
from faker import Faker
import sys

# from plot_data import plot_data

# Check if a day is a saturday
def is_saturday(date_string):
    # Parse the date string into a datetime object
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    
    # Check if the weekday is Saturday (5 represents Saturday)
    return date_object.weekday() == 5

# sorts the scores acheieved by date
def process_scores(input_text, cutoff_date):
    lines = input_text.splitlines()
    scores_struct = []
    for line in lines:
        parts = line.split(",")
        name = parts[0].strip()  # Remove leading/trailing whitespaces
        date = parts[1].strip()  # Remove leading/trailing whitespaces
        time = int(parts[2].strip())  # Remove leading/trailing whitespaces and convert to integer
        if cutoff_date <= date: # filter by cutoff date input argument, 
            if time <= 1200: # remove times that are over 20 minutes
                scores_struct.append((name, date, time))

    sorted_list = sorted(scores_struct, key=lambda x: x[1])
    return sorted_list

def anonymize_names(sorted_list):
    Faker.seed(1)
    faker = Faker()
    dict_names = {name: faker.name() for name, _, _ in sorted_list}
    #NOTE: Could hardcode names here if we wanted to
    anonymized_sorted_list = [(dict_names[name], date, time) for name, date, time in sorted_list]
    return anonymized_sorted_list

# calculate each person's average non-saturday and saturday time
def get_average_time(scores, cutoff_date):
    # Open a new file for writing output
    with open("../text_files/averages.txt", "w") as output_file:
        dict = {}
        for score in scores:
            name, date, time = score
            
            if is_saturday(date):
                # third and forth list spots are for saturdays
                if name in dict:
                    original_tuple = dict[name]
                    dict[name] = (original_tuple[0], original_tuple[1], original_tuple[2] + time, original_tuple[3] + 1)
                else:
                    dict[name] = (0, 0, time, 1)
            else:
                # first and second list spots are for non-saturdays
                if name in dict:
                    original_tuple = dict[name]
                    dict[name] = (original_tuple[0] + time, original_tuple[1] + 1, original_tuple[2], original_tuple[3])
                else:
                    dict[name] = (time, 1, 0, 0)

        averages_tuples = []
        for name, tuple in dict.items():
            # get average times for saturdays and non-saturdays, ensuring we don't divide by zero
            averages_tuples.append((name, round(tuple[0] / tuple[1] if tuple[1] != 0 else -1, 2), tuple[1], 
                                    round(tuple[2] / tuple[3] if tuple[3] != 0 else -1, 2), tuple[3]))

        sorted_list = sorted(averages_tuples, key=lambda x: x[1])

        # headers
        if cutoff_date:
            output_file.write("Cutoff day: " + cutoff_date + "\n")
        output_file.write("Name, Average Time, Number of Times\n")

        for score in sorted_list:
            output_file.write(f"{score[0]}, {score[1]}, {score[2]}\n")

        output_file.write("\nSaturdays:\n")

        # Sort Saturdays
        sorted_list = sorted(averages_tuples, key=lambda x: x[3])

        for score in sorted_list:
            output_file.write(f"{score[0]}, {score[3]}, {score[4]}\n")

# calculate each person's average position compared to others' times
def find_average_place(individualsDict):
    with open("../text_files/average_placements.txt", "w") as output_file:
        output_file.write("Average placements per person:")
        personAveragesList = []

        # get each person's average
        for person, placesList in individualsDict.items():
            average = round(sum(placesList) / len(placesList), 2)
            personAveragesList.append((person, average))

        # sort the averages
        sorted_list = sorted(personAveragesList, key=lambda x: x[1])
        for person, average in sorted_list:
            output_file.write(f"\n{person}, {average}")

# find the number of times a person has come first for that day
def find_number_of_firsts(individualsDict):
    with open("../text_files/first_places.txt", "w") as output_file:
        output_file.write("Number of first place finishes per person:")
        firstPlacesList = []
        # count each person's number of times being first
        for person, placesList in individualsDict.items():
            firstPlaces = placesList.count(1)
            firstPlacesList.append((person, firstPlaces))
        
        # sort the number of times someone got first, most at the top
        sorted_list = reversed(sorted(firstPlacesList, key=lambda x: x[1]))
        for person, firstPlaces in sorted_list:
            output_file.write(f"\n{person}, {firstPlaces}")

# processes peoples' placement for each day to make other calculations easier
def analyze_placement_info(scores, cutoff_date):
    individualsDict = {} # key is name, value is list of placements
    dayScoresList = []
    currentDate = cutoff_date

    for idx, score in enumerate(scores):
        name, date, time = score

        # add to current day which is being analyzed
        if date == currentDate and idx != len(scores)-1:
            dayScoresList.append((name, time))
        # we have gone through all the stats for today
        else:
            sorted_list = sorted(dayScoresList, key=lambda x: x[1])
            for place, tuple in enumerate(sorted_list):
                nameInTuple, score = tuple
                
                # if was a twin
                while place > 0 and score == sorted_list[place - 1][1]: # loop cause more than two people could've tied
                    # then give them the same placement as their twin, that just happened to be sorted first
                    place -= 1
                
                if nameInTuple in individualsDict:
                    individualsDict[nameInTuple].append(place+1)
                else:
                    individualsDict[nameInTuple] = [place+1]

            currentDate = date
            dayScoresList = [(name, time)]

    find_average_place(individualsDict)
    find_number_of_firsts(individualsDict)

def count_times_occurences(sorted_scores, cutoff_date):
    time_occurences_dict = {}
    for score in sorted_scores:
        time = score[2]
        if time in time_occurences_dict:
            time_occurences_dict[time] += 1
        else:
            time_occurences_dict[time] = 1
    with open("../text_files/time_occurences.txt", "w") as output_file:
        output_file.write("Number of occurences for each time (cutoff date is "+ cutoff_date + "):\n")
        for time in dict(sorted(time_occurences_dict.items())):
            output_file.write("Time: " + str(time) + "   Occurence: " + str(time_occurences_dict[time]) + "\n")
    with open("../text_files/most_common_times.txt", "w") as output_file:
        output_file.write("Times sorted by which is most common (cutoff date is "+ cutoff_date + "):\n")
        for time in dict(sorted(time_occurences_dict.items(), key=lambda item: (item[1], item[0]), reverse=True)):
            output_file.write("Occurence: " + str(time_occurences_dict[time]) + "    Time: " + str(time) +  "\n")

def main(cutoff_date = "2023-02-21"):
    # Read the input file
    with open("../text_files/cleaned_data.txt", "r") as file:
        text = file.read()

    sorted_scores = process_scores(text, cutoff_date) # format is [[name, date, time], ...]
    anon_sorted_scores = anonymize_names(sorted_scores)
    get_average_time(anon_sorted_scores, cutoff_date)
    analyze_placement_info(anon_sorted_scores, cutoff_date)
    count_times_occurences(anon_sorted_scores, cutoff_date)
    # plot_data(anon_sorted_scores)


if __name__ == "__main__":
    # Check if command-line arguments were provided
    if len(sys.argv) >= 2:
        arg1 = sys.argv[1]
        main(arg1)
    else:
        # Call main with default values
        main()