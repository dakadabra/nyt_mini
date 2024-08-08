import pandas as pd
import matplotlib.pyplot as plt

def plot_data(data):

    # Convert data to a Pandas DataFrame
    df = pd.DataFrame(data, columns=['Name', 'Date', 'Times'])

    # Convert Date and Time columns to datetime objects
    df['Date'] = pd.to_datetime(df['Date'])
    df['Times'] = pd.to_datetime(df['Times'])

    # Plot the data
    plt.figure(figsize=(10, 6))

    # Group data by Name and plot each group as a separate line
    for name, group in df.groupby('Name'):
        plt.plot(group['Date'], group['Times'], label=name)

    # Add labels and legend
    plt.xlabel('Date')
    plt.ylabel('Times')
    plt.title('Times vs Date for Each Person')
    plt.legend()

    # Show plot
    plt.show()
