import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage to scrape
url = "https://services.planningcenteronline.com/plans/62713651/public"

# Make a request to the webpage
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Initialize empty list to store the extracted data
agenda_items = []
durations = []
remaining_time = []

# Initialize a variable to store the total duration of the broadcast
total_duration = 58*60 + 58

# Find all elements with the class "PlanSong" or "PlanItem"
for element in soup.find_all(class_=["PlanSong","PlanItem"]):
    # Extract the title and duration of the agenda item
    title = element.find("span", class_="title").get_text()
    duration_string = element.find("span", class_="length").get_text()
    duration = int(duration_string.split(':')[0])*60 + int(duration_string.split(':')[1])
    # check if the duration is less than 40 minutes
    if duration < 40*60:
        agenda_items.append(title)
        durations.append(duration)
        remaining_time.append(total_duration)
        total_duration -= duration

# Create a dataframe from the extracted data
data = {"Agenda Item": agenda_items, "Duration": durations, "Remaining Time": remaining_time}
df = pd.DataFrame(data)


# Convert seconds to minutes and seconds in the "Duration" and "Remaining Time" columns
df["Duration"] = df["Duration"].apply(lambda x: divmod(x, 60))
df["Duration"] = df["Duration"].apply(lambda x: f"{x[0]}:{x[1]:02d}")
df["Remaining Time"] = df["Remaining Time"].apply(lambda x: divmod(x, 60))
df["Remaining Time"] = df["Remaining Time"].apply(lambda x: f"{x[0]}:{x[1]:02d}")

# Output the dataframe to a .csv file
df.to_csv("broadcast_schedule.csv", index=False)
