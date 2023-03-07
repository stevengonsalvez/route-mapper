import os
import csv
from maps import get_optimal_route
from maps import get_distance
from maps import classify_postcodes_ew

# Replace YOUR_API_KEY with your actual API key
API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

# Replace ORIGIN_POSTCODE with the postcode you want to start from
ORIGIN_POSTCODE = os.environ.get("ORIGIN_POSTCODE")

# # Initialize empty lists for postcodes above and below 2 miles
# postcodes_above_2_miles = []
# postcodes_below_2_miles = []
#
# # Open the CSV file containing postcodes
# # Open the CSV file containing postcodes
# with open("postcodes.csv", "r") as f:
#     reader = csv.reader(f)
#     next(reader)  # Skip the header row
#     destinations = [row[0] for row in reader]
#
# # Get the distances between the origin and destination postcodes
# distances = get_distance(ORIGIN_POSTCODE, destinations, API_KEY)
#
# # Add the postcodes to the appropriate list based on the distance
# for postcode, distance in distances.items():
#     if distance > 2:
#         postcodes_above_2_miles.append(postcode)
#     else:
#         postcodes_below_2_miles.append(postcode)
#
# print (postcodes_above_2_miles)
# print (postcodes_below_2_miles)

test_postcodes = ['UB32AX', 'SL38BH', 'UB70LH', 'UB40HU', 'UB40BS', 'UB56RU', 'UB109DU', 'NW98DN', 'HA63AN', 'UB32AU', 'SL38LW']


result = classify_postcodes_ew(test_postcodes, ORIGIN_POSTCODE, API_KEY)
east_postcodes = result[0]
west_postcodes = result[1]

print("East postcodes:", east_postcodes)
print("West postcodes:", west_postcodes)

