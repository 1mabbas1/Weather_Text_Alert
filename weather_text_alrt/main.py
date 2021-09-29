import requests
from twilio.rest import Client
import os
from twilio.http.http_client import TwilioHttpClient

"""This program sends you a text message when the weather is forecast to be rainy"""

#enter your latitude and longitude
params = {'lat': 1,
          'lon':1,

          'units': 'metric',
          'exclude':'current,minutely,daily',
          'appid': '72747834d0216600c234702e12a62886'
          }

#enter your twilio account details
account_sid = 'Your Twilio account SID'
auth_token = 'Your Twilio Auth_token'


#get weather info from open weather map api
response = requests.get('https://api.openweathermap.org/data/2.5/onecall', params = params)
response.raise_for_status()
weather = response.json()
slice =  weather['hourly'][:12]

#determine if there will be rain
willrain = False
for hourdata in slice:
    code = (hourdata['weather'][0]['id'])
    if int(code)<700:
        willrain = True
#semd a text message to your phone number if rain is forecast.
if willrain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)

    message = client.messages \
        .create(
        body="It's forecast to rain, take an umbrella.",
        from_='your twilio phone number',
        to='your phone number'
    )

    print(message.status)




