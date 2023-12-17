from collections import Counter
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
extract=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=  df[df['user']==selected_user]
    
    num_messages= df.shape[0]
    words=[]
    for message in df['msgs']:
        words.extend(message.split())

    

# fetch no of media
    num_media_messages=0
    num_media_messages=df[df['msgs']=='<Media omitted>'].shape[0]
    
    
# urls
    links=[]
    for m in df['msgs']:
        links.extend(extract.find_urls(m))
    num_links=len(links)
    
    return num_messages,len(words),num_media_messages,num_links

def most_busy_users(df):
    x=df['user'].value_counts().head()
    dfx=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':
                                                                                    'percent'})
    return x,dfx

# wordcloud
def create_wordcloud(selected_user,df):
    
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    temp=df[df['user']!='group_notification']
    temp=temp[temp['msgs']!='<Media omitted>']

    stop_words=['hai','hmm','haan','acha','media','omitted','<Media omitted>']
    def remove_stop_word(message):    
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
#  can remove stopwords here Also like bwlow
        
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['msgs']=temp['msgs'].apply(remove_stop_word)
    df_wc=wc.generate(temp['msgs'].str.cat(sep=' '))
    return df_wc






# most common user
def most_common_words(selected_user,df):
    temp=df[df['user']!='group_notification']
    temp=temp[temp['msgs']!='<Media omitted>']
    
    if selected_user!='Overall':
        temp=temp[temp['user']==selected_user]
    

    
    # return temp
    wordss=[]
    for msg in temp['msgs']:
        m=msg.lower()
        for word in m.split():

            # manullay handling media omitted
            if len(word)>=3 and word!='<media' and word!='omitted>':
                wordss.append(word)
    from collections import Counter
    most_common_df=pd.DataFrame(Counter(wordss).most_common(20)) 
    return most_common_df


import emoji
import pandas as pd
from collections import Counter

def extract_emojis(text):
    return ''.join(c for c in text if c in emoji.EMOJI_DATA)


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['msgs']:
        # Use extract_emojis function to filter out non-emoji characters
        emojis.extend(extract_emojis(message))

    emojis_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emojis_df
