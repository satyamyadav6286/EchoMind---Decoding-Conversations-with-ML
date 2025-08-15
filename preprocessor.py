import re
import pandas as pd

def preprocess(data):
    # Robust WhatsApp date pattern: matches e.g. 12/05/2023, 10:15 - or 5/12/23, 10:15 AM - or 12-05-2023, 10:15 pm -
    pattern = r'((?:\d{1,2}[\/\-]){2}\d{2,4}),?\s\d{1,2}:\d{2}(?:\s?[APMapm]{2})?\s-\s'

    messages = re.split(pattern, data)[1:]
    # The split will alternate: [date, message, date, message, ...]
    dates = messages[::2]
    messages = messages[1::2]

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_date type
    df['message_date'] = df['message_date'].astype(str).str.strip()
    # Try multiple common WhatsApp date formats
    def try_parse_date(s):
        for fmt in [
            '%d/%m/%Y, %H:%M', '%d/%m/%y, %H:%M', '%d-%m-%Y, %H:%M', '%d-%m-%y, %H:%M',
            '%d/%m/%Y, %I:%M %p', '%d/%m/%y, %I:%M %p', '%d-%m-%Y, %I:%M %p', '%d-%m-%y, %I:%M %p',
            '%m/%d/%Y, %H:%M', '%m/%d/%y, %H:%M', '%m-%d-%Y, %H:%M', '%m-%d-%y, %H:%M',
            '%m/%d/%Y, %I:%M %p', '%m/%d/%y, %I:%M %p', '%m-%d-%Y, %I:%M %p', '%m-%d-%y, %I:%M %p',
        ]:
            try:
                return pd.to_datetime(s, format=fmt)
            except Exception:
                continue
        # Fallback to dateutil parser
        try:
            return pd.to_datetime(s, errors='coerce')
        except Exception:
            return pd.NaT
    df['message_date'] = df['message_date'].apply(try_parse_date)

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df