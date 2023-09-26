import datetime
import json
import base64
import requests
from authKey import SECRET_KEY
from dbConnection import mycursor, connection


IMAGE_PATH = 'second.jpg'
#IMAGE_PATH = 'first1.jpg'


with open(IMAGE_PATH, 'rb') as image_file:
    img_base64 = base64.b64encode(image_file.read())

url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
r = requests.post(url, data = img_base64)

num_plate=(json.dumps(r.json(), indent=2))
info=(list(num_plate.split("candidates")))
print(info)
plate=info[1]
print("plate : ", plate)
plate=plate.split(',')[0:3]
p=plate[1]
print("p : ", p)
p1= p.split(":")
print("p1 : ", p1)
number=p1[1]
print("number : ", number)
number=number.replace('"','')
number=number.lstrip()
print(number)


getnumber = "SELECT * FROM users WHERE number_plate = '{}'".format(number)
mycursor.execute(getnumber)
templist = list(mycursor)
#print(len(templist))
#print(templist)
if len(templist) == 0:
    temp_time = datetime.datetime.now()
    entered_time = temp_time.strftime("%Y %m %d %H %M %S")
    print("entered time ", entered_time)
    mycursor.execute("INSERT INTO users VALUES ('{}', '{}')".format(number, entered_time))
    connection.commit()
else:
    for temp in templist:
        #print(temp)
        if number == temp[0]:
            print(temp[1])
            #result = datetime.datetime.now() - temp[1]
            current_time = datetime.datetime.now()
            arrival_time_temp = temp[1].split('.')
            print("arrival time temp ", arrival_time_temp[0])
            arrival_time_temp[0] = str(arrival_time_temp[0])
            arrival_time = datetime.datetime.strptime(arrival_time_temp[0], "%Y %m %d %H %M %S")
            result = current_time - arrival_time
            print("result = ", result)
            days = result.days
            hours = result.seconds/3600
            print("hours : ", hours, "days : ", days)
            fare = (days * 24 + hours) * 20
            if hours < 6:
                fare = 20

            query = "DELETE FROM users WHERE number_plate = '{}'".format(temp[0])
            mycursor.execute(query)
            connection.commit()
            print("deleted")
            print(temp[0], fare)



