from datetime import datetime
import sys

def is_saturday(date_string):
    # Parse the date string into a datetime object
    date_object = datetime.strptime(date_string, "%Y-%m-%d")
    
    # Check if the weekday is Saturday (5 represents Saturday)
    return date_object.weekday() == 5

def get_average_time(input_text, cutoff_date):
    # Open a new file for writing output
    with open("averages.txt", "w") as output_file:

        dict = {}
        lines = input_text.splitlines()
        for line in lines:
            parts = line.split(",")
            name = parts[0].strip()  # Remove leading/trailing whitespaces
            date = parts[1].strip()  # Remove leading/trailing whitespaces
            time = int(parts[2].strip())  # Remove leading/trailing whitespaces and convert to integer
            
            if not cutoff_date or cutoff_date < date:
                if is_saturday(date):
                    if name in dict:
                        original_tuple = dict[name]
                        dict[name] = (original_tuple[0], original_tuple[1], original_tuple[2] + time, original_tuple[3] + 1)
                    else:
                        dict[name] = (0, 0, time, 1)
                else:
                    if name in dict:
                        original_tuple = dict[name]
                        dict[name] = (original_tuple[0] + time, original_tuple[1] + 1, original_tuple[2], original_tuple[3])
                    else:
                        dict[name] = (time, 1, 0, 0)

        averages_tuples = []
        for name, tuple in dict.items():
            averages_tuples.append((name, round(tuple[0] / tuple[1] if tuple[1] != 0 else -1, 2), tuple[1], 
                                    round(tuple[2] / tuple[3] if tuple[3] != 0 else -1, 2), tuple[3]))

        sorted_list = sorted(averages_tuples, key=lambda x: x[1])

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


def main(arg1=None):
    # Read the input file
    with open("cleaned_data.txt", "r") as file:
        text = file.read()

    get_average_time(text, arg1)


if __name__ == "__main__":
    # Check if command-line arguments were provided
    if len(sys.argv) >= 2:
        arg1 = sys.argv[1]
        main(arg1)
    else:
        # Call main with default values
        main()