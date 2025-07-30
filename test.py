import requests
import json

API_key="25dd7cd96ab76fcfd31c67228e42f418"
    
# print("What is the name of your city?")
city='Mumbai'
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
response = requests.get(url)    # Making a get request to the API
res = response.json()       # Converting JSON response to a dictionary
print(res)
if res["cod"] != "404":         # Checking if the city is found. If the value of "cod" is not 404, that means the city is found
        data = res["main"]
        live_temp = data["temp"]
        live_pressure = data["pressure"]
        country=res["sys"]
        cname=country["country"]
        desc = res["weather"]
        weather_desc = desc[0]["description"]
        print("Temperature (in Kelvin scale): " + str(live_temp))
        print("Pressure: " + str(live_pressure))
        print("Description: " + str(weather_desc))
        print("country:"+str(cname))

else:
    print("That is not a valid city")