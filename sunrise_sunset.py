import requests
import datetime as dt
from datetime import timezone
import smtplib
import time

my_email = "palatkarabhi@gmail.com"
password = "Zxcvbnm12$"

to_email = ["apalatkar@marvell.com", "abhijeetpalatkar12@gmail.com"]

MY_LAT = 37.392727185
MY_LONG = -121.9486459
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0
}
DELAY = 60
while True:
    time.sleep(DELAY)
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    # print(response.raise_for_status())
    data = response.json()
    # print(data)
    sunrise = data['results']['sunrise'].split("T")[1].split(":")[0]
    sunset = data['results']['sunset'].split("T")[1].split(":")[0]
    # print("Current Loc:\nSunrise_hour:{},\nSunset_hour:{}".format(sunrise,sunset))

    curr_time = dt.datetime.now().astimezone(tz=timezone.utc)
    curr_hour = str(curr_time).split(" ")[1].split(":")[0]
    # print(sunset , curr_hour , sunrise)
    if int(sunset) <= int(curr_hour) <= int(sunrise):
        print("It' Dark")
        response = requests.get(url="http://api.open-notify.org/iss-now.json")
        ISS_lat = response.json()["iss_position"]["latitude"]
        ISS_lng = response.json()["iss_position"]["longitude"]
        print("ISS LAT:{}, LNG{}".format(round(float(ISS_lat),4), round(float(ISS_lng),4)))
        iss_lat = round(float(ISS_lat))
        iss_lng = round(float(ISS_lng))

        if round(MY_LAT)-3 <= iss_lat <= round(MY_LAT)+3 and round(MY_LONG)-3 <= iss_lng <= round(MY_LONG)+3:
            with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
                connection.login(user=my_email, password=password)
                mymsg = "Subject: ISS ABOVE YOU\n\n{} Lat: {},Lng: {}".format("LOOK UP",
                                                                          round(float(ISS_lat),4),
                                                                          round(float(ISS_lng),4))
                for receiver in to_email:
                    connection.sendmail(from_addr=my_email, to_addrs=receiver, msg=mymsg)
        iss_lat=0.0
        iss_lng=0.0
