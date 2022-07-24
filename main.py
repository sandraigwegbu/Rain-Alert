import requests
import smtplib
import os

# Defining constants
API_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
API_KEY = os.environ.get("OWM_API_KEY")
LAT = os.environ.get("MY_LAT")
LONG = os.environ.get("MY_LONG")

ALERT_PERIOD = 12  # hours of notice

MY_EMAIL = os.environ.get("MY_EMAIL")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL")

# Request weather data at specified location
parameters = {
	"lat": LAT,
	"lon": LONG,
	"appid": API_KEY,
	"exclude": "current,minutely,daily,alerts"
}

response = requests.get(API_ENDPOINT, params=parameters)
response.raise_for_status()
weather_data = response.json()

# Determine hourly weather condition codes on a given day
weather_id = []
for hour in weather_data["hourly"]:
	condition_code = hour["weather"][0]["id"]
	weather_id.append(condition_code)
# print(weather_id[:ALERT_PERIOD])  # testing code to determine whether there's a code <700 in the list

# Determine whether it is due to rain within the set ALERT_PERIOD
will_rain = False
for num in weather_id[:ALERT_PERIOD]:
	if num < 700:
		will_rain = True

# if it is due to rain, send email
if will_rain:
	with smtplib.SMTP("smtp.gmail.com") as connection:
		connection.starttls()
		connection.login(user=MY_EMAIL, password=EMAIL_PASSWORD)
		connection.sendmail(from_addr=MY_EMAIL, to_addrs=RECIPIENT_EMAIL,
		                    msg="Subject:Weather Alert\n\nIt's going to rain today! Remember to bring an umbrella!")
