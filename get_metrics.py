def get_average_time(input_text):
    dict = {}
    lines = input_text.splitlines()
    for line in lines:
        parts = line.split(",")
        name = parts[0].strip()  # Remove leading/trailing whitespaces
        date = parts[1].strip()  # Remove leading/trailing whitespaces
        time = int(parts[2].strip())  # Remove leading/trailing whitespaces and convert to integer
        
        if name in dict:
            original_tuple = dict[name]
            dict[name] = (original_tuple[0] + time, original_tuple[1] + 1)
        else:
            dict[name] = (time, 1)
    averages_tuples = []
    for name, tuple in dict.items():
        averages_tuples.append((name, round(tuple[0] / tuple[1], 2)))

    sorted_list = sorted(averages_tuples, key=lambda x: x[1])

    for score in sorted_list:
        output_file.write(f"{score[0]}, {score[1]}\n")



# Read the input file
with open("cleaned_data.txt", "r") as file:
    text = file.read()

# Open a new file for writing output
with open("averages.txt", "w") as output_file:
    get_average_time(text)