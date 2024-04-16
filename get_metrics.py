from datetime import datetime
import sys

# Check if a day is a saturday
def is_saturday(date_string):
    # Parse the date string into a datetime object
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    
    # Check if the weekday is Saturday (5 represents Saturday)
    return date_object.weekday() == 5

def get_average_time(input_text, cutoff_date):
    # Open a new file for writing output
    with open("text_files/averages.txt", "w") as output_file:

        dict = {}
        lines = input_text.splitlines()
        for line in lines:
            parts = line.split(",")
            name = parts[0].strip()  # Remove leading/trailing whitespaces
            date = parts[1].strip()  # Remove leading/trailing whitespaces
            time = int(parts[2].strip())  # Remove leading/trailing whitespaces and convert to integer
            
            if cutoff_date <= date: # filter by cutoff date input argument
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

def find_average_place(individualsDict):
    with open("text_files/average_placements.txt", "w") as output_file:
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

def find_number_of_firsts(individualsDict):
    with open("text_files/first_places.txt", "w") as output_file:
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

def analyze_placement_info(input_text, cutoff_date):
    individualsDict = {} # key is name, value is list of placements
    dayScoresList = []
    lines = input_text.splitlines()
    currentDate = cutoff_date
    for line in lines:
        parts = line.split(",")
        name = parts[0].strip()  # Remove leading/trailing whitespaces
        date = parts[1].strip()  # Remove leading/trailing whitespaces
        time = int(parts[2].strip())  # Remove leading/trailing whitespaces and convert to integer
        
        # add to current day which is being analyzed
        if date == currentDate:
            dayScoresList.append((name, time))
        # we have gone through all the stats for today
        else: # TODO: This assumes all the results are in chronological order
            sorted_list = sorted(dayScoresList, key=lambda x: x[1]) # TODO: fix ties so that both get the same placement
            for place, tuple in enumerate(sorted_list):
                name = tuple[0]
                if name in individualsDict:
                    individualsDict[name].append(place)
                else:
                    individualsDict[name] = [place]

            currentDate = date
            dayScoresList = []
        
        find_average_place(individualsDict)
        find_number_of_firsts(individualsDict)

def main(cutoff_date = "2023-02-21"):
    # Read the input file
    with open("text_files/cleaned_data.txt", "r") as file:
        text = file.read()

    get_average_time(text, cutoff_date)
    analyze_placement_info(text, cutoff_date)


if __name__ == "__main__":
    # Check if command-line arguments were provided
    if len(sys.argv) >= 2:
        arg1 = sys.argv[1]
        main(arg1)
    else:
        # Call main with default values
        main()