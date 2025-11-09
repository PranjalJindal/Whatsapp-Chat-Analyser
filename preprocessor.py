import re
import pandas as pd

def preprocess(data):
    """
    Preprocess WhatsApp chat text and return a clean DataFrame.
    """
    # Pattern to match date and time at the start of each message
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2})\s-\s'
    
    # Split messages and extract dates
    messages = re.split(pattern, data)[1:]  # Split keeps dates and messages together
    dates = messages[0::2]  # Dates are every even index
    texts = messages[1::2]  # Messages are every odd index

    # Convert dates to datetime
    df = pd.DataFrame({'date': pd.to_datetime(dates, format='%d/%m/%y, %H:%M', errors='coerce'),
                       'user_message': texts})

    # Extract users and messages
    users = []
    messages_list = []

    for message in df['user_message']:
        # Split by first occurrence of "name: message"
        entry = re.split(r'([\w\W]+?):\s', message, maxsplit=1)
        if len(entry) == 3:
            users.append(entry[1])
            messages_list.append(entry[2])
        else:
            users.append('group_notification')
            messages_list.append(entry[0])

    df['user'] = users
    df['message'] = messages_list
    df.drop(columns=['user_message'], inplace=True)

    # Add additional time-related columns
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num']=df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['only_date']=df['date'].dt.date
    df['day_name']=df['date'].dt.day_name()


    period=[]

    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour==0:
            period.append(str('00') + "-" + str(hour + 1))

        else :
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] =period

    # Drop rows with invalid date parsing
    df = df.dropna(subset=['date'])

    return df
