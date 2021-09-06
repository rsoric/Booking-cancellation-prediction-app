import tkinter
import urllib.request
from tkinter import *
from tkcalendar import *
import json
from datetime import datetime, date
import datetime as dt
import numpy as np
import copy
import matplotlib as mpl
import re

def popupmsg(msg):
    popup = tkinter.Tk()
    popup.wm_title("Error")
    label = tkinter.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=20,padx=20)
    B1 = tkinter.Button(popup, text="Okay", command = popup.destroy)
    B1.pack(side="bottom",pady=10,padx=20)
    popup.mainloop()

dataTemplate =  {

        "Inputs": {

                "input1":
                {
                    "ColumnNames": ["hotel", "lead_time", "stays_in_weekend_nights", "stays_in_week_nights", "adults", "children", "babies", "meal", "is_repeated_guest", "required_car_parking_spaces", "total_of_special_requests", "wanted_room_available", "is_on_waiting_list", "previous_cancellation", "bookingType_Corporate", "bookingType_Direct", "bookingType_Group", "bookingType_Other", "bookingType_TravelAgency", "deposit", "day_of_week_0", "day_of_week_1", "day_of_week_2", "day_of_week_3", "day_of_week_4", "day_of_week_5", "day_of_week_6", "month_sin", "month_cos", "day_sin", "day_cos"],
                    "Values": [[ "0", "0", "0", "0", "0", "0", "0", "value", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0" ]]
                },        },
            "GlobalParameters": {
}
    }

def colorFader(c1,c2,mix=0):
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

c1='#91C499' #green
c2='#FF928B' #red

def makeAPIRequest():

    data = copy.copy(dataTemplate)

    # hotel

    selectHotelValue = select_hotel_label.get()

    if selectHotelValue == "Resort hotel":
        data["Inputs"]["input1"]["Values"][0][0] = "0"
    elif selectHotelValue == "City hotel":
        data["Inputs"]["input1"]["Values"][0][0] = "1"
    elif selectHotelValue == "Select hotel":
        popupmsg("Please select a hotel")
        return None

    # adults

    try:
        adultsValue = int(numOfAdults.get())
    except ValueError:
        popupmsg("Number of adults should be an integer")
        return None

    if adultsValue == 0:
        popupmsg("Your booking should contain at least 1 adult")
        return None
    elif adultsValue < 0:
        popupmsg("Number of adults can't be negative")
        return None
    else:
        data["Inputs"]["input1"]["Values"][0][4] = str(adultsValue)

    # children

    try:
        childrenValue = int(numOfChildren.get())
    except ValueError:
        popupmsg("Number of children should be an integer")
        return None

    if childrenValue < 0:
        popupmsg("Number of children can't be negative")
        return None
    else:
        data["Inputs"]["input1"]["Values"][0][5] = str(childrenValue)

    # babies

    try:
        babiesValue = int(numOfBabies.get())
    except ValueError:
        popupmsg("Number of babies should be an integer")
        return None

    if babiesValue < 0:
        popupmsg("Number of babies can't be negative")
        return None
    else:
        data["Inputs"]["input1"]["Values"][0][6] = str(babiesValue)

    # parking

    try:
        parkingValue = int(numOfParkingSpaces.get())
    except ValueError:
        popupmsg("Number of parking spaces should be an integer")
        return None

    if parkingValue < 0:
        popupmsg("Number of parking spaces can't be negative")
        return None
    else:
        data["Inputs"]["input1"]["Values"][0][9] = str(parkingValue)

    # special requests

    try:
        specialRequestsValue = int(numOfSpecialRequests.get())
    except ValueError:
        popupmsg("Number of special requests should be an integer")
        return None

    if specialRequestsValue < 0:
        popupmsg("Number of special requests can't be negative")
        return None
    else:
        data["Inputs"]["input1"]["Values"][0][10] = str(specialRequestsValue)

    # meal

    mealValue = meal_label.get()
    # print(mealValue)

    if mealValue == "Breakfast only":
        data["Inputs"]["input1"]["Values"][0][7] = "BB"
    elif mealValue == "Breakfast and dinner":
        data["Inputs"]["input1"]["Values"][0][7] = "HB"
    elif mealValue == "Breakfast, Lunch, Dinner":
        data["Inputs"]["input1"]["Values"][0][7] = "FB"
    elif mealValue == "No meal":
        data["Inputs"]["input1"]["Values"][0][7] = "SC"
    elif mealValue == "Meal type":
        popupmsg("Please select a meal type")
        return None

    # booking type

    bookingTypeValue = booking_label.get()

    if bookingTypeValue == "Direct":
        data["Inputs"]["input1"]["Values"][0][15] = "1"
        data["Inputs"]["input1"]["Values"][0][18] = "0"
        data["Inputs"]["input1"]["Values"][0][14] = "0"
        data["Inputs"]["input1"]["Values"][0][16] = "0"
        data["Inputs"]["input1"]["Values"][0][17] = "0"
    elif bookingTypeValue == "Travel agency":
        data["Inputs"]["input1"]["Values"][0][18] = "1"
        data["Inputs"]["input1"]["Values"][0][15] = "0"
        data["Inputs"]["input1"]["Values"][0][14] = "0"
        data["Inputs"]["input1"]["Values"][0][16] = "0"
        data["Inputs"]["input1"]["Values"][0][17] = "0"
    elif bookingTypeValue == "Corporate":
        data["Inputs"]["input1"]["Values"][0][14] = "1"
        data["Inputs"]["input1"]["Values"][0][18] = "0"
        data["Inputs"]["input1"]["Values"][0][15] = "0"
        data["Inputs"]["input1"]["Values"][0][16] = "0"
        data["Inputs"]["input1"]["Values"][0][17] = "0"
    elif bookingTypeValue == "Group":
        data["Inputs"]["input1"]["Values"][0][16] = "1"
        data["Inputs"]["input1"]["Values"][0][18] = "0"
        data["Inputs"]["input1"]["Values"][0][14] = "0"
        data["Inputs"]["input1"]["Values"][0][15] = "0"
        data["Inputs"]["input1"]["Values"][0][17] = "0"
    elif bookingTypeValue == "Other":
        data["Inputs"]["input1"]["Values"][0][17] = "1"
        data["Inputs"]["input1"]["Values"][0][18] = "0"
        data["Inputs"]["input1"]["Values"][0][14] = "0"
        data["Inputs"]["input1"]["Values"][0][16] = "0"
        data["Inputs"]["input1"]["Values"][0][15] = "0"

    # repeat guest

    repeatGuestValue = isRepeatedGuest.get()
    data["Inputs"]["input1"]["Values"][0][8] = str(repeatGuestValue)

    # Previous cancel

    prevCancelValue = isPreviousCancellation.get()
    data["Inputs"]["input1"]["Values"][0][13] = str(prevCancelValue)

    # Desired room

    desiredRoomValue = isDesiredRoom.get()
    data["Inputs"]["input1"]["Values"][0][11] = str(desiredRoomValue)

    # Waiting list

    waitingListValue = isWaitingList.get()
    data["Inputs"]["input1"]["Values"][0][12] = str(waitingListValue)

    # Deposit

    depositValue = isDeposit.get()
    data["Inputs"]["input1"]["Values"][0][19] = str(depositValue)

    # Calendar
    bookingStartDateValue = datetime.strptime(calendarBookingStart.get_date(), "%m/%d/%y")
    todayDateValue = datetime.strptime(calendarTodayDate.get_date(), "%m/%d/%y")
    bookingEndDateValue = datetime.strptime(calendarBookingEnd.get_date(), "%m/%d/%y")
    if (bookingStartDateValue < todayDateValue):
        popupmsg("Booking cannot start before today's date")
        return None
    if (bookingEndDateValue < todayDateValue):
        popupmsg("Booking cannot end before today's date")
        return None
    if (bookingEndDateValue < bookingStartDateValue):
        popupmsg("Booking cannot start before the booking end date")
        return None
    if (bookingEndDateValue == bookingStartDateValue):
        popupmsg("Booking cannot start and end on the same day")
        return None

    bookingStartDayOfWeek = bookingStartDateValue.weekday()
    if bookingStartDayOfWeek == 0:
        data["Inputs"]["input1"]["Values"][0][20] = "1"
        data["Inputs"]["input1"]["Values"][0][21] = "0"
        data["Inputs"]["input1"]["Values"][0][22] = "0"
        data["Inputs"]["input1"]["Values"][0][23] = "0"
        data["Inputs"]["input1"]["Values"][0][24] = "0"
        data["Inputs"]["input1"]["Values"][0][25] = "0"
        data["Inputs"]["input1"]["Values"][0][26] = "0"
    elif bookingStartDayOfWeek == 1:
        data["Inputs"]["input1"]["Values"][0][20] = "0"
        data["Inputs"]["input1"]["Values"][0][21] = "1"
        data["Inputs"]["input1"]["Values"][0][22] = "0"
        data["Inputs"]["input1"]["Values"][0][23] = "0"
        data["Inputs"]["input1"]["Values"][0][24] = "0"
        data["Inputs"]["input1"]["Values"][0][25] = "0"
        data["Inputs"]["input1"]["Values"][0][26] = "0"
    elif bookingStartDayOfWeek == 2:
        data["Inputs"]["input1"]["Values"][0][20] = "0"
        data["Inputs"]["input1"]["Values"][0][21] = "0"
        data["Inputs"]["input1"]["Values"][0][22] = "1"
        data["Inputs"]["input1"]["Values"][0][23] = "0"
        data["Inputs"]["input1"]["Values"][0][24] = "0"
        data["Inputs"]["input1"]["Values"][0][25] = "0"
        data["Inputs"]["input1"]["Values"][0][26] = "0"
    elif bookingStartDayOfWeek == 3:
        data["Inputs"]["input1"]["Values"][0][20] = "0"
        data["Inputs"]["input1"]["Values"][0][21] = "0"
        data["Inputs"]["input1"]["Values"][0][22] = "0"
        data["Inputs"]["input1"]["Values"][0][23] = "1"
        data["Inputs"]["input1"]["Values"][0][24] = "0"
        data["Inputs"]["input1"]["Values"][0][25] = "0"
        data["Inputs"]["input1"]["Values"][0][26] = "0"
    elif bookingStartDayOfWeek == 4:
        data["Inputs"]["input1"]["Values"][0][20] = "0"
        data["Inputs"]["input1"]["Values"][0][21] = "0"
        data["Inputs"]["input1"]["Values"][0][22] = "0"
        data["Inputs"]["input1"]["Values"][0][23] = "0"
        data["Inputs"]["input1"]["Values"][0][24] = "1"
        data["Inputs"]["input1"]["Values"][0][25] = "0"
        data["Inputs"]["input1"]["Values"][0][26] = "0"
    elif bookingStartDayOfWeek == 5:
        data["Inputs"]["input1"]["Values"][0][20] = "0"
        data["Inputs"]["input1"]["Values"][0][21] = "0"
        data["Inputs"]["input1"]["Values"][0][22] = "0"
        data["Inputs"]["input1"]["Values"][0][23] = "0"
        data["Inputs"]["input1"]["Values"][0][24] = "0"
        data["Inputs"]["input1"]["Values"][0][25] = "1"
        data["Inputs"]["input1"]["Values"][0][26] = "0"
    elif bookingStartDayOfWeek == 6:
        data["Inputs"]["input1"]["Values"][0][20] = "0"
        data["Inputs"]["input1"]["Values"][0][21] = "0"
        data["Inputs"]["input1"]["Values"][0][22] = "0"
        data["Inputs"]["input1"]["Values"][0][23] = "0"
        data["Inputs"]["input1"]["Values"][0][24] = "0"
        data["Inputs"]["input1"]["Values"][0][25] = "0"
        data["Inputs"]["input1"]["Values"][0][26] = "1"

    bookingStartMonth = bookingStartDateValue.month
    bookingStartDay = bookingStartDateValue.day

    bookingMonthSin = np.sin(2 * np.pi * (bookingStartMonth - 1) / 12)
    bookingMonthCos = np.cos(2 * np.pi * (bookingStartMonth - 1) / 12)

    bookingDaySin = np.sin(2 * np.pi * (bookingStartDay - 1) / 31)
    bookingDayCos = np.cos(2 * np.pi * (bookingStartDay - 1) / 31)

    data["Inputs"]["input1"]["Values"][0][27] = str(bookingMonthSin)
    data["Inputs"]["input1"]["Values"][0][28] = str(bookingMonthCos)
    data["Inputs"]["input1"]["Values"][0][29] = str(bookingDaySin)
    data["Inputs"]["input1"]["Values"][0][30] = str(bookingDayCos)

    leadTime = bookingStartDateValue.date() - todayDateValue.date()
    leadTimeValue = str(leadTime.days)
    data["Inputs"]["input1"]["Values"][0][1] = leadTimeValue

    numOfWeekdays = np.busday_count(bookingStartDateValue.date(), bookingEndDateValue.date(), weekmask='1111100')
    numOfWeekendDays = np.busday_count(bookingStartDateValue.date(), bookingEndDateValue.date(), weekmask='0000011')

    data["Inputs"]["input1"]["Values"][0][2] = str(numOfWeekendDays)
    data["Inputs"]["input1"]["Values"][0][3] = str(numOfWeekdays)

    # print(data)
    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/5c373ed9903b4b54915e3e5c30790ae0/services/ee21656adb9341f2b55df3af1f60197a/execute?api-version=2.0&details=true'
    api_key = 'abc123'  # Replace this with the API key for the web service
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}
    req = urllib.request.Request(url, body, headers)
    response = urllib.request.urlopen(req)
    result = response.read()
    print(result)

    resultVars = re.findall('"([^"]*)"', str(result))
    resultChance = float(resultVars[-1])

    resultString = str(resultChance * 100)[0:4] + "%"

    resultsFrame.config(background=colorFader(c1, c2, resultChance))

    resultLabel.config(text=resultString, background=colorFader(c1, c2, resultChance))
    resultLabel.place(relx=.5, rely=.47, anchor="c")

    if resultLabelDisplayed == False:
        resultLabelText = Label(resultsFrame, text="chance of cancellation",background=colorFader(c1, c2, resultChance))
        resultLabelText.place(relx=.5, rely=.53, anchor="c")
        resultLabelDisplayed == True



def check_num(newval):
    return re.match('^[0-9]*$', newval) is not None and len(newval) <= 5

hotels_list = ["Resort hotel", "City hotel"]
meals_list = ["Breakfast only", "Breakfast and dinner", "Breakfast, Lunch, Dinner", "No meal"]
booking_list = ["Direct","Travel agency","Corporate","Group","Other"]

window = Tk()
window.title("Booking Cancellation Prediction")

today = date.today()
tomorrow = today + dt.timedelta(days=1)

check_num_wrapper = (window.register(check_num), '%P')

calendarTodayDate = Label(window, text="Today's date")
calendarTodayDate.grid(row=0, column=0, padx=10,pady=10)
calendarTodayDate = Calendar(window, selectmode = 'day',
               year = today.year, month = today.month,
               day = today.day)
calendarTodayDate.grid(row=1, column=0,padx=10,pady=10)

calendarBookingStartLabel = Label(window, text='Booking start date')
calendarBookingStartLabel.grid(row=0, column=1)
calendarBookingStart = Calendar(window, selectmode = 'day',
               year = today.year, month = today.month,
               day = today.day)
calendarBookingStart.grid(row=1, column=1,padx=10,pady=10)

calendarBookingEndLabel = Label(window, text="Booking end date")
calendarBookingEndLabel.grid(row=0, column=2, padx=10,pady=10)
calendarBookingEnd = Calendar(window, selectmode = 'day',
               year = tomorrow.year, month = tomorrow.month,
               day = tomorrow.day)
calendarBookingEnd.grid(row=1, column=2,padx=10,pady=10)

tkinter.Label(window, text="Hotel").grid(row=2,column=0)
select_hotel_label = tkinter.StringVar(window)
select_hotel_label.set(hotels_list[0])
selectHotel = tkinter.OptionMenu(window, select_hotel_label, *hotels_list)
selectHotel.grid(row=2,padx=10,pady=10, column=1)

tkinter.Label(window, text="Adults").grid(row=3,column=0)
numOfAdults = tkinter.Entry(window)
numOfAdults.insert(END, 2)
numOfAdults.grid(row=3,column=1,padx=10,pady=10)

tkinter.Label(window, text="Children").grid(row=4,column=0)
numOfChildren = tkinter.Entry(window)
numOfChildren.insert(END,0)
numOfChildren.grid(row=4,column=1,padx=10,pady=10)

tkinter.Label(window, text="Babies").grid(row=5,column=0)
numOfBabies = tkinter.Entry(window)
numOfBabies.insert(END,0)
numOfBabies.grid(row=5,column=1,padx=10,pady=10)

tkinter.Label(window, text="Required parking spaces").grid(row=6,column=0)
numOfParkingSpaces = tkinter.Entry(window)
numOfParkingSpaces.insert(END,0)
numOfParkingSpaces.grid(row=6,column=1,padx=10,pady=10)

tkinter.Label(window, text="Number of special requests").grid(row=7,column=0)
numOfSpecialRequests = tkinter.Entry(window)
numOfSpecialRequests.insert(END,0)
numOfSpecialRequests.grid(row=7,column=1,padx=10,pady=10)

tkinter.Label(window, text="Meal type").grid(row=8,column=0)
meal_label = StringVar(window)
meal_label.set(meals_list[0])
mealType = OptionMenu(window, meal_label, *meals_list)
mealType.grid(row=8, column=1,padx=10,pady=10)

tkinter.Label(window, text="Booking type").grid(row=9,column=0)
booking_label = StringVar(window)
booking_label.set(booking_list[0])
bookingType = OptionMenu(window, booking_label, *booking_list)
bookingType.grid(row=9, column=1,padx=10,pady=10)

tkinter.Label(window, text="Repeat guest").grid(row=10,column=0)
isRepeatedGuest = IntVar()
Checkbutton(window, text="", variable=isRepeatedGuest).grid(row=10, column=1,padx=10,pady=10)

tkinter.Label(window, text="Guest with previous cancellation").grid(row=11,column=0,padx=10,pady=10)
isPreviousCancellation = IntVar()
Checkbutton(window, text="", variable=isPreviousCancellation).grid(row=11, column=1,padx=10,pady=10)

tkinter.Label(window, text="Desired room available").grid(row=12,column=0,padx=10,pady=10)
isDesiredRoom = IntVar()
Checkbutton(window, text="", variable=isDesiredRoom).grid(row=12, column=1,padx=10,pady=10)

tkinter.Label(window, text="Booking on waiting list").grid(row=13,column=0,padx=10,pady=10)
isWaitingList = IntVar()
Checkbutton(window, text="", variable=isWaitingList).grid(row=13, column=1,padx=10,pady=10)

tkinter.Label(window, text="Deposit").grid(row=14,column=0,padx=10,pady=10)
isDeposit = IntVar()
Checkbutton(window, text="", variable=isDeposit).grid(row=14, column=1,padx=10,pady=10)

checkButton = tkinter.Button(text ="Check chance of cancellation", command=makeAPIRequest).grid(row=15,columnspan =2,padx=10,pady=10)

resultsFrame = LabelFrame(window, text="Result")
resultsFrame.grid(row=2, column=2,padx=10,pady=10,rowspan=13,sticky=N+S+E+W)

resultLabel = Label(resultsFrame,text="",font=("Arial", 25))
resultLabel.pack()

resultLabelDisplayed = False

window.mainloop()
