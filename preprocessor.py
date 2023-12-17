

def preprocess(data):
    p='\d{1,2}\/\d{1,2}\/\d{2}, \d{1,2}:\d{2}\u202f[APM]+\s-\s'
    pattern = r'\u202f'
    import re
    msg=re.split(p,data)
    msg=msg[4:]
    dates=re.findall(p,data)
    org_strings = dates
# Initialize an empty list to store the modified strings
    date=[]

# Use re.sub to replace the pattern in each string and append the result to mod_strings
    for org_string in org_strings:
        mod_string = re.sub(pattern, ' ', org_string)
        date.append(mod_string)
    date=date[3:]

    import pandas as pd
    df=pd.DataFrame({"user_msg":msg,"msg-date":date})
    df['msg-date']=pd.to_datetime(df['msg-date'], format='%m/%d/%y, %I:%M %p - '
    )
    df.rename(columns={'msg-date':'date'},inplace=True)
    df.head()
    
    users=[]
    msgs=[]
    for m in df['user_msg']:
        e=re.split('([\w\W]+?):\s',m)
        if e[1:]:
            users.append(e[1])
            msgs.append(e[2])
        else:
            users.append('group_notification')
            msgs.append(e[0])
    # mm=[]
    # for i in msgs:
    #     mm.append(i[:-2])


    df['user']=users
    df['msgs']=msgs
    df.drop(columns=['user_msg'],inplace=True)

    # users=[]
    # msgs=[]
    # for m in df['user_msg']:
    #     e=re.split('([\w\W]+?):\s',m)
    #     if e[1:]:
    #         users.append(e[1])
    #         msgs.append(e[2])
    #     else:
    #         users.append('group_notification')
    #         msgs.append(e[0])

    # df['user']=users
    # df['msgs']=msgs
    # df.drop(columns=['user_msg'],inplace=True)

    df['year']=df['date'].dt.year
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['hour']=df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    return df

   