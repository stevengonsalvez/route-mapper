import requests
import json

def classify_postcodes_ew(postcodes, origin, API_KEY):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
    origin_params = {
        "address": origin,
        "key": API_KEY,
    }
    origin_response = requests.get(base_url, params=origin_params)
    origin_data = json.loads(origin_response.text)
    if origin_data["status"] == "OK":
        origin_latlng = origin_data["results"][0]["geometry"]["location"]
    else:
        raise ValueError("Invalid origin postcode")
    east_postcodes = []
    west_postcodes = []
    for postcode in postcodes:
        postcode_params = {
            "address": postcode,
            "key": API_KEY,
        }
        postcode_response = requests.get(base_url, params=postcode_params)
        postcode_data = json.loads(postcode_response.text)
        if postcode_data["status"] == "OK":
            postcode_latlng = postcode_data["results"][0]["geometry"]["location"]
            if postcode_latlng["lng"] > origin_latlng["lng"]:
                east_postcodes.append(postcode)
            else:
                west_postcodes.append(postcode)
        else:
            raise ValueError(f"Invalid postcode: {postcode}")
    return east_postcodes, west_postcodes

def get_distance(origin, destinations, API_KEY):
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
    destinations_str = "|".join(destinations)
    params = {
        "origins": origin,
        "destinations": destinations_str,
        "mode": "driving",
        "units": "imperial",
        "key": API_KEY,
    }
    response = requests.get(base_url, params=params)
    data = json.loads(response.text)
    distances = {}
    for i, destination in enumerate(destinations):
        if data["rows"][0]["elements"][i]["status"] == "OK":
            distance = data["rows"][0]["elements"][i]["distance"]["value"] * 0.000621371 # Convert meters to miles
            distances[destination] = distance
    return distances

def get_optimal_route(postcodes, origin, API_KEY):
    base_url = "https://maps.googleapis.com/maps/api/directions/json?"
    origin_destinations = [origin] + postcodes + [origin]
    waypoints_str = "|".join(origin_destinations)
    params = {
        "origin": origin,
        "destination": origin,
        "waypoints": f"optimize:true|{waypoints_str}",
        "mode": "driving",
        "key": API_KEY,
    }
    response = requests.get(base_url, params=params)
    data = json.loads(response.text)
    path = "color:0xff0000ff|weight:5"
    for leg in data["routes"][0]["legs"]:
        for step in leg["steps"]:
            path += f"|{step['start_location']['lat']},{step['start_location']['lng']}"
            path += f"|{step['end_location']['lat']},{step['end_location']['lng']}"
    map_url = f"https://www.google.com/maps/dir/?api=1&travelmode=driving&waypoints={waypoints_str}&path={path}"
    return map_url