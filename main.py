from scipy import stats
from datetime import timedelta
import pandas as pd

#Create and Concat the H1 and H2 dataframes
df1 = pd.read_csv('H1.csv')
df2 = pd.read_csv('H2.csv')
df = pd.concat([df1,df2])
# print(df)
#Verify the Columns are in the correct type


print(df.info())

#Combine the dates into one column
    #convert the string Months to integers
month_to_day_conversion = {
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
    'December': 12,
}
df['ArrivalDateMonth'] = df['ArrivalDateMonth'].replace(month_to_day_conversion)
    #zip the year,month,day into one column and then change to a datetime object
df['ArrivalDate'] = ["{}/{}/{}".format(x,y,z) for x,y,z in zip(df['ArrivalDateYear'], df['ArrivalDateMonth'], df['ArrivalDateDayOfMonth'])]
df['ArrivalDate'] = pd.to_datetime(df['ArrivalDate'], yearfirst=True, format='%Y/%m/%d').dt.date
    #Remove the year, month, and day columns. place the new column closer to the front of the df
df.drop(['ArrivalDateYear', 'ArrivalDateMonth', 'ArrivalDateDayOfMonth'], axis=1, inplace=True)
temp_column = df.pop('ArrivalDate')
df.insert(2, 'ArrivalDate', temp_column)

#Determine Reservation Date
    #subtract leadtime from the arrivaldate
df['ReservationDate'] = [x - timedelta(y) for x,y in zip(df['ArrivalDate'], df['LeadTime'])]
    #Place the new column closer to the front
temp_column = df.pop('ReservationDate')
df.insert(2, 'ReservationDate', temp_column)

#Hypothesis test whether having at least 1 child increases the chances of cancelling
    #Fill the nan cells with 0 and convert column to int64
df['Children'] = df['Children'].fillna(0)
df['Children'] = df['Children'].astype('int64')
    #ttest
t, p = stats.ttest_ind(df['IsCanceled'][df['Children'] == 0],
                      df['IsCanceled'][df['Children'] > 0])
print('Null Hypothesis: The amount of children a person has does not make them more or less likely to cancel their hotel\np_value = {}\np_value is greater than 0.05'.format(round(p, 3)))
x = 5

