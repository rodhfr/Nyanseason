#import typer
#import inquirer
from yaspin import yaspin
from nyaa_tools import get_nyaa_updates


#get_nyaa_updates()



from tabulate import tabulate

# Sample dictionary
data = {
    "Name": "Alice",
    "Age": 28,
    "Country": "Wonderland",
    "Occupation": "Explorer"
}

# Convert dictionary to a list of lists
table_data = [[key, value] for key, value in data.items()]

# Display the table
print(tabulate(table_data, headers=["Key", "Value"], tablefmt="grid"))