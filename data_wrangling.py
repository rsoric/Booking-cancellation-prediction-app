import matplotlib
import matplotlib.pyplot
import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from datetime import date
from sklearn.preprocessing import StandardScaler
pd.set_option('display.max_columns', 500)


hotel= pd.read_csv("hotel_bookings.csv")
hotel_full = hotel

#hotel.stays_in_week_nights.plot(kind='box')
#plt.show()

#hotel.adults.plot(kind='box')
#plt.show()

###2.2.1 Prazni unosi
hotel=hotel.drop(['agent','company'],axis=1)
hotel = hotel.dropna(axis = 0)
#print(hotel.isnull().sum())

###2.2.2. Unosi bez gostiju
#print(hotel.shape)
filter = (hotel.children == 0) & (hotel.adults == 0) & (hotel.babies == 0)
hotel = hotel[~filter]
#print(hotel.shape)

###2.2.3. Outlieri dana
#print(hotel.shape)
filter = (hotel.stays_in_weekend_nights > 8) | (hotel.stays_in_week_nights > 10)
hotel = hotel[~filter]
#print(hotel.shape)

###2.2.4. Nedefinirani obroci
#hotel['meal'].hist(bins=30)
#plt.show()
hotel.loc[hotel.meal == 'Undefined', 'meal'] = "SC"
#hotel['meal'].hist(bins=30)
#plt.show()

###2.2.5. Binariziranje
#hotel
hotel.loc[hotel.hotel == 'Resort Hotel', 'hotel'] = 0
hotel.loc[hotel.hotel == 'City Hotel', 'hotel'] = 1
#hotel['hotel'].hist(bins=30)
#plt.show()

#room type
def room_check(row):
        if row['reserved_room_type']==row['assigned_room_type']:
                return 1
        return 0

hotel['wanted_room_available'] = hotel.apply(lambda row: room_check(row), axis=1)
#hotel['wanted_room_available'].hist(bins=10)
#plt.show()
hotel=hotel.drop(['reserved_room_type','assigned_room_type'],axis=1)

#waiting list
def wait_check(row):
        if row['days_in_waiting_list']>0:
                return 1
        return 0

hotel['is_on_waiting_list'] = hotel.apply(lambda row: wait_check(row), axis=1)
#hotel['is_on_waiting_list'].hist(bins=10)
#plt.show()
hotel=hotel.drop(['days_in_waiting_list'],axis=1)

#prev cancel
def cancel_check(row):
        if row['previous_cancellations']==0:
                return 0
        return 1
hotel['previous_cancellation'] = hotel.apply(lambda row: cancel_check(row), axis=1)
#hotel['previous_cancellation'].hist(bins=10)
#plt.show()
hotel=hotel.drop(['previous_cancellations'],axis=1)

###2.2.6. Market segment
def market_segment_check(row):
        if row['market_segment']=="Online TA":
                return "TravelAgency"
        if row['market_segment']=="Offline TA/TO":
                return "TravelAgency"
        if row['market_segment']=="Groups":
                return "Group"
        if row['market_segment']=="Direct":
                return "Direct"
        if row['market_segment']=="Corporate":
                return "Corporate"
        if row['market_segment']=="Complementary":
                return "Other"
        if row['market_segment']=="Aviation":
                return "Other"
        return 0
hotel['market_segment'] = hotel.apply(lambda row: market_segment_check(row), axis=1)
oneHotEncodedMarketSegment = pd.get_dummies(hotel.market_segment, prefix='bookingType')
hotel = pd.concat([hotel, oneHotEncodedMarketSegment], axis=1)
#print(hotel.head())
hotel=hotel.drop(['market_segment','distribution_channel'],axis=1)

###########DEPOSIT
def deposit_check(row):
        if row['deposit_type'] == "No Deposit":
                return 0
        if row['deposit_type'] == "Refundable":
                return 1
        return 1
hotel['deposit'] = hotel.apply(lambda row: deposit_check(row), axis=1)
hotel=hotel.drop('deposit_type',axis=1)
######################

###2.2.7. Datumi
#day of week
def monthToNum(monthString):
    return {
            'January': 1,
            'February': 2,
            'March': 3,
            'April': 4,
            'May': 5,
            'June': 6,
            'July': 7,
            'August': 8,
            'September': 9,
            'October': 10,
            'November': 11,
            'December': 12
    }[monthString]
hotel['day_of_week'] = hotel.apply(lambda row: date(row.arrival_date_year, monthToNum(row.arrival_date_month), row.arrival_date_day_of_month).weekday(), axis=1)
oneHotEncodedDays = pd.get_dummies(hotel.day_of_week, prefix='day_of_week')
hotel = pd.concat([hotel, oneHotEncodedDays], axis=1)
hotel=hotel.drop(['day_of_week'],axis=1)
#print(hotel.head())

#month and date
hotel['month_int'] = hotel.apply(lambda row: monthToNum(row.arrival_date_month), axis=1)
hotel['month_sin'] = np.sin(2 * np.pi * (hotel['month_int']-1)/12)
hotel['month_cos'] = np.cos(2 * np.pi * (hotel['month_int']-1)/12)
#plt.scatter(hotel['month_sin'],hotel['month_cos'])
#plt.show()
hotel=hotel.drop(['arrival_date_month', 'month_int'],axis=1)

hotel['day_sin'] = np.sin(2 * np.pi * (hotel['arrival_date_day_of_month']-1)/31)
hotel['day_cos'] = np.cos(2 * np.pi * (hotel['arrival_date_day_of_month']-1)/31)
#plt.scatter(hotel['day_sin'],hotel['day_cos'])
#plt.show()
hotel=hotel.drop(['arrival_date_day_of_month'],axis=1)

###2.2.8. Final brisanje
hotel=hotel.drop(['arrival_date_year','arrival_date_week_number','previous_bookings_not_canceled','booking_changes','customer_type','adr','reservation_status','reservation_status_date'],axis=1)
print(hotel.head())

###DEPOSIT


#hotel.country.value_counts().plot(kind='pie')
#print(hotel['total_of_special_requests'].describe())
#hotel['total_of_special_requests'].hist(bins=30)
#hotel.stays_in_weekend_nights.plot(kind='box')
#plt.show()
#print(hotel['country'].nunique())

#hotel.boxplot(column="adults")
#plt.show()
# df = hotel
#
# df['distribution_channel']=df['distribution_channel'].astype('category').cat.codes
# df['market_segment']=df['market_segment'].astype('category').cat.codes
# print(df.corr())
#
# hotel=hotel.drop(['agent','company','reservation_status','reservation_status_date'],axis=1)
# hotel = hotel.dropna(axis = 0)
#
# filter = (hotel.children == 0) & (hotel.adults == 0) & (hotel.babies == 0)
# hotel = hotel[~filter]
#
#
#
#
# hotel['day_of_week'] = hotel.apply(lambda row: date(row.arrival_date_year, monthToNum(row.arrival_date_month), row.arrival_date_day_of_month).weekday(), axis=1)
#

# randoms = [1234, 4445, 15000, 35421, 91235]
#
# for x in randoms:
#         print(x)
#         print(hotel.iloc[x]['arrival_date_year'])
#         print(hotel.iloc[x]['arrival_date_month'])
#         print(hotel.iloc[x]['arrival_date_day_of_month'])
#         print(hotel.iloc[x]['day_of_week'])
#         print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

# oneHotEncodedDays = pd.get_dummies(hotel.day_of_week, prefix='day')
# hotel = pd.concat([hotel, oneHotEncodedDays], axis=1)
#
# hotel['month_int'] = hotel.apply(lambda row: monthToNum(row.arrival_date_month), axis=1)
#
# hotel['month_sin'] = np.sin(2 * np.pi * (hotel['month_int']-1)/12)
# hotel['month_cos'] = np.cos(2 * np.pi * (hotel['month_int']-1)/12)
#
# hotel['day_sin'] = np.sin(2 * np.pi * (hotel['arrival_date_day_of_month']-1)/31)
# hotel['day_cos'] = np.cos(2 * np.pi * (hotel['arrival_date_day_of_month']-1)/31)



#hotel=hotel.drop(['day_of_week','month_int','arrival_date_month','arrival_date_year','arrival_date_week_number','arrival_date_day_of_month'],axis=1)
hotel.to_csv('hotel_dataset_rsoric.csv', index=False)
