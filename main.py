import requests
import json
import datetime as dt
import smtplib
import ssl
import time

GMAIL_USERNAME = '@gmail.com'
GMAIL_PASSWORD = 'p'
SHEETLY_PASSWORD ="== "
SHEETLY_ROUTE = 'htt1'
KIWI_API_KEY = 'LqQDF'
KIWI_PATH = "https:ch"

URL = SHEETLY_ROUTE
header = {"Authorization": SHEETLY_PASSWORD}
response_sheetly = requests.get(url=URL,headers=header)
# print(response_sheetly.text)

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

  def check_flights(self, fly_from='airport:EWR', fly_to='airport:AMS', date_from="09/09/2022", time_frame=170,
                      max_stopovers=0):
        self.fly_from = fly_from
        self.fly_to = fly_to
        self.date_from = date_from
        date_to = dt.datetime.strptime(date_from, "%d/%m/%Y") + dt.timedelta(days=time_frame)
        self.date_to = date_to.strftime("%d/%m/%Y")
        self.max_stopovers = max_stopovers

        header = {'Content_Type': "application/json",
                   "Content_Encoding": "gzip",
                   "apikey": KIWI_API_KEY
                   }
        path = KIWI_PATH
        fly_from = "airport:EWR"  # "city:DUS"  #airport:DUS
        fly_to = "airport:BRU"
        date_from = "09/09/2022"
        date_to = "31/12/2022"

        query = {'fly_from': self.fly_from,
                      'fly_to': self.fly_to,
                      "date_to": self.date_to,
                      "date_from": self.date_from,
                      "max_stopovers": self.max_stopovers}

        response = requests.get(path, params=query, headers=header)
        response = json.loads(response.text)
        #print(response.get('search_params'))
        #print(response)
        self.price = response.get('data')[0].get('price')  # price for flight
        self.bags_price = response.get('data')[0].get('bags_price')# sometimes more than one baggage rated different
        self.bag_limit = response.get('data')[0].get('bag_limit')
        self.availability = response.get('data')[0].get('availability')
        self.route = response.get('data')[0].get('route')
        self.local_departure = response.get('data')[0].get('local_departure')
        self.local_arrival = response.get('data')[0].get('local_arrival')
        self.currency = response.get('currency')
  def datechanger(self,tarih):
  # changes string datetime 
  # "%Y-%m-%d" ==>> "%d/%m/%Y"
    return dt.datetime.strftime(dt.datetime.strptime(tarih,"%Y-%m-%d"),"%d/%m/%Y")

class Mail:

    def __init__(self):
        self.port = 465
        self.smtp_server_domain_name = "smtp.gmail.com"
        self.sender_mail = GMAIL_USERNAME
        self.password = GMAIL_PASSWORD
        print('Mail Sender V 1.0 created......')
        time.sleep(1)
       
    def send(self, email, subject, content):
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(self.smtp_server_domain_name, self.port, context=ssl_context)
        service.login(self.sender_mail, self.password)
        print('Login Successfull')
        time.sleep(1)
        print(f"Sending to: {email}")
        time.sleep(1)
        result = service.sendmail(self.sender_mail, email, f"Subject: {subject}\n{content}")
        service.quit()
        print('All job done. Quitting')
        time.sleep(1)
        
        
        mail_server = Mail()
for i in json.loads(response_sheetly.text)['sheet1']:
  if i.get('user') != '' and i.get('user') is not None:
    # print(i)
    flight = FlightSearch()
    fly_from = i.get('flyFrom')
    fly_to = i.get('flyTo')
    date_from = flight.datechanger(i.get('dateFrom'))
    time_frame = i.get('timeFrame')
    max_stopovers = i.get('maxStopovers')
    price_threshold = i.get('lowestPrice')
    name= i.get('name')
    recipient = i.get('user') #mail to
    
    flight.check_flights(fly_from=fly_from,fly_to=fly_to,date_from=date_from,time_frame=time_frame,max_stopovers=max_stopovers)

    if flight.price < price_threshold:
      
      content =[]
      subject = f"We found a cheaper flight from {flight.fly_from} to {flight.fly_to} which is {flight.price} {flight.currency} \nFlight details are below\n------------------------"
      #print(flight.route[i])
      for i in range(len(flight.route)):
        content.append(f"From {flight.route[i].get('flyFrom')} to {flight.route[i].get('flyTo')} with flight number {flight.route[i].get('airline')} {flight.route[i].get('flight_no')} at {flight.route[i].get('local_departure')}\n")
      email_string = f'''Subject: {subject}
To: {recipient} 
{''.join(content)}'''
      print(email_string)


    else:
      content =[]
      subject = f"The cheapest flight we found from {flight.fly_from} to {flight.fly_to} is {flight.price} {flight.currency} \nFlight details are below\n------------------------"
      for i in range(len(flight.route)):
        #print(flight.route[i])
        content.append(f"From {flight.route[i].get('flyFrom')} to {flight.route[i].get('flyTo')} with flight number {flight.route[i].get('airline')} {flight.route[i].get('flight_no')} at {flight.route[i].get('local_departure')}(Local Time)")
      email_string = f'''Subject: {subject}
To: {recipient} 
{''.join(content)}'''

      
    mail_server.send(email=recipient,subject=subject,content=email_string)

  else:
    pass
    
    
