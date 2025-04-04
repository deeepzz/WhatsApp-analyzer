import re
import pandas as pd
def preprocess(data):
    pattern = pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}[\s\u202f]?[AP]M\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    dates = [d.replace("\u202f", " ") for d in dates]
    # Sample input
    df = pd.DataFrame({'user_messages': messages, 'message_date': dates})

    # Apply split and extract the first part for each row
    df['message_date'] = df['message_date'].str.split(" - ").str[0]

    # Optionally, convert it to datetime if needed
    df['message_date'] = pd.to_datetime(df['message_date'], format="mixed", errors='coerce')

    # Rename column
    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for m in df['user_messages']:
        entry = re.split(r'^(.*?):\s*(.*)$', m)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])

    df['user'] = users
    df['messages'] = messages
    df.drop(columns=['user_messages'], inplace=True)
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    period = []
    for h in df['hour']:
        if h == 23:
            period.append(str(h) + "-" + str('00'))
        elif h == 0:
            period.append(str('00') + "-" + str(h + 1))
        else:
            period.append(str(h) + "-" + str(h + 1))

    df['period'] = period
    df = df[~df['user'].str.contains(':', na=False)]
    return df
