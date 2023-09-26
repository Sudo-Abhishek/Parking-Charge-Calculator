from tkinter import *
import tkinter
import customtkinter
from PIL import ImageTk, Image
from tkinter import filedialog
import cv2
import time
import json
import base64
import requests
import datetime
from authKey import SECRET_KEY
from dbConnection import mycursor, connection
import datetime
import json
import base64
import requests



root = Tk()



root.attributes('-fullscreen', True)
root.title("Parking Charge Calculator")
bg = PhotoImage(file ="car background1.png")
background_image_label = Label(root, image=bg)
background_image_label.place(x=0, y=0, relwidth=1, relheight=1)

global fare_text
fare_text = "Nothing to Show"

def show_fare():
    fare_label = Label(root, text=fare_text, bg="grey", font=("Helvetica", 15), fg="white", width=30, height=3 , borderwidth=5, relief="solid").place(relx=0.17, rely=0.83)

def exit_command():
    root.quit()

def select_from_camera():
    cam = cv2.VideoCapture(0)
    while True:

        _, img = cam.read()
        key = cv2.waitKey(1) & 0xff
        cv2.imshow("Capture License Number", img)
        if (key == ord('q')):
            cv2.destroyAllWindows()
            print("Captured...")
            cv2.imwrite("first1.jpg", img)
            # time.sleep(5)
            IMAGE_PATH1 = "first1.jpg"
            my_image1 = ImageTk.PhotoImage(Image.open(IMAGE_PATH1))
            my_image_label = Label(root, image=my_image1, width=650, height=300)
            my_image_label.image = my_image1
            my_image_label.place(relx=0.03, rely=0.4)



            with open(IMAGE_PATH1, 'rb') as image_file:
                img_base64 = base64.b64encode(image_file.read())

            url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (
                SECRET_KEY)
            r = requests.post(url, data=img_base64)

            num_plate = (json.dumps(r.json(), indent=2))
            info = (list(num_plate.split("candidates")))
            print(info)
            plate = info[1]
            plate = plate.split(',')[0:3]
            p = plate[1]
            p1 = p.split(":")
            number = p1[1]
            number = number.replace('"', '')
            number = number.lstrip()
            print(number)

            getnumber = "SELECT * FROM users WHERE number_plate = '{}'".format(number)
            mycursor.execute(getnumber)
            templist = list(mycursor)
            # print(len(templist))
            # print(templist)
            if len(templist) == 0:
                temp_time = datetime.datetime.now()
                entered_time = temp_time.strftime("%Y %m %d %H %M %S")
                print("entered time ", entered_time)
                mycursor.execute("INSERT INTO users VALUES ('{}', '{}')".format(number, entered_time))
                list_of_globals = globals()
                list_of_globals['fare_text'] = "Vehicle details has been\n entered into the database"
                show_fare()
                connection.commit()
            else:
                for temp in templist:
                    # print(temp)
                    if number == temp[0]:
                        print(temp[1])
                        # result = datetime.datetime.now() - temp[1]
                        current_time = datetime.datetime.now()
                        arrival_time_temp = temp[1].split('.')
                        print("arrival time temp ", arrival_time_temp[0])
                        arrival_time_temp[0] = str(arrival_time_temp[0])
                        arrival_time = datetime.datetime.strptime(arrival_time_temp[0], "%Y %m %d %H %M %S")
                        result = current_time - arrival_time
                        print("result = ", result)
                        days = result.days
                        hours = result.seconds / 3600
                        print("hours : ", hours, "days : ", days)
                        fare = (days * 24 + hours) * 20
                        if hours < 6:
                            fare = 20

                        query = "DELETE FROM users WHERE number_plate = '{}'".format(temp[0])
                        mycursor.execute(query)
                        connection.commit()
                        list_of_globals = globals()
                        list_of_globals['fare_text'] = "Vehicle Number : {} \n Parking Charge : {}".format(temp[0], fare)
                        show_fare()
                        print("deleted")
                        print(temp[0], fare)
            break


        elif (key == ord('w')):
            break

    cam.release()
    cv2.destroyAllWindows()

def select_from_file():
    global my_image
    root.filename = filedialog.askopenfilename(initialdir="E:/Python machine learning projects/ParkingChargeCalc_ML",
                                               title="Select A File",
                                               filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
    print(root.filename)
    IMAGE_PATH = root.filename
    my_image = ImageTk.PhotoImage(Image.open(root.filename))
    my_image_label = Label(root, image=my_image, width=650, height=300).place(relx=0.03, rely=0.4)


    # IMAGE_PATH = 'first1.jpg'

    with open(IMAGE_PATH, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())

    url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
    r = requests.post(url, data=img_base64)

    num_plate = (json.dumps(r.json(), indent=2))
    info = (list(num_plate.split("candidates")))
    print(info)
    plate = info[1]
    print("plate : ", plate)
    plate = plate.split(',')[0:3]
    p = plate[1]
    print("p : ", p)
    p1 = p.split(":")
    print("p1 : ", p1)
    number = p1[1]
    print("number : ", number)
    number = number.replace('"', '')
    number = number.lstrip()
    print(number)

    getnumber = "SELECT * FROM users WHERE number_plate = '{}'".format(number)
    mycursor.execute(getnumber)
    templist = list(mycursor)
    # print(len(templist))
    # print(templist)
    if len(templist) == 0:
        temp_time = datetime.datetime.now()
        entered_time = temp_time.strftime("%Y %m %d %H %M %S")
        print("entered time ", entered_time)
        mycursor.execute("INSERT INTO users VALUES ('{}', '{}')".format(number, entered_time))
        list_of_globals = globals()
        list_of_globals['fare_text'] = "Vehicle details has been\nentered into the database"
        show_fare()
        connection.commit()
    else:
        for temp in templist:
            # print(temp)
            if number == temp[0]:
                print(temp[1])
                # result = datetime.datetime.now() - temp[1]
                current_time = datetime.datetime.now()
                arrival_time_temp = temp[1].split('.')
                print("arrival time temp ", arrival_time_temp[0])
                arrival_time_temp[0] = str(arrival_time_temp[0])
                arrival_time = datetime.datetime.strptime(arrival_time_temp[0], "%Y %m %d %H %M %S")
                result = current_time - arrival_time
                print("result = ", result)
                days = result.days
                hours = result.seconds / 3600
                print("hours : ", hours, "days : ", days)
                fare = (days * 24 + hours) * 20
                if hours < 6:
                    fare = 20

                query = "DELETE FROM users WHERE number_plate = '{}'".format(temp[0])
                mycursor.execute(query)
                connection.commit()
                list_of_globals = globals()
                list_of_globals['fare_text'] = "Vehicle Number : {} \n Parking Charge : {}".format(temp[0], fare)
                show_fare()
                print("deleted")
                print(temp[0], fare)


heading_label = Label(root, text="PARKING CHARGE CALCULATOR", bg="light blue", font=("Helvetica", 30), fg="blue", bd=4, padx=2, pady=4)
exit_button = Button(root, text="EXIT", command=exit_command, bg="brown", font=("Helvetica", 15), fg="white", bd=4, padx=2, pady=4)
image_from_file_button = Button(root, text="Select Image From File System",bg="yellow", font=("Helvetica", 15), fg="green", bd=4, padx=2, pady=4, command=select_from_file)
image_from_camera_button = Button(root, text="Capture Image From Camera", bg="yellow", font=("Helvetica", 15), fg="green", bd=4, padx=2, pady=4, command=select_from_camera)
button_fare = Button(root, text="Show Parking Charge", command=show_fare, bg="orange", font=("Helvetica", 15), fg="purple", padx=2, pady=4, bd=4)


heading_label.place(relx=0.05, rely=0.05)
image_from_file_button.place(relx=0.05, rely=0.2)
image_from_camera_button.place(relx=0.3, rely=0.2)
exit_button.place(relx=0.6, rely=0.9)
button_fare.place(relx=0.2, rely=0.3)


root.mainloop()