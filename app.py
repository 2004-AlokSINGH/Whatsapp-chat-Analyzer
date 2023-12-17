import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
from wordcloud import WordCloud


st.sidebar.title("Whatsapp Chat Ananlyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocessor.preprocess(data)

    st.dataframe(df)


    #fetch unique user
    user_list=df['user'].unique().tolist()
    if "group_notification" in user_list:
        user_list.remove("group_notification")
        user_list.sort()
        user_list.insert(0,"Overall")


    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button('Show Analysis'):

        num_message,words,num_media_messages,num_links=helper.fetch_stats(selected_user,df)


        
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_message)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header('Total Media')
            st.title(num_media_messages)

        with col3:
            st.header('Total Links')
            st.title(num_links)
        

        col1,col2=st.columns(2)
        x,new_df=helper.most_busy_users(df)
        if selected_user=='Overall':
            st.title('Most Busy USERS')
            x,new_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # word cloud
        st.title("Word Cloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df=helper.most_common_words(selected_user,df)
        # st.dataframe(most_common_df)
        fig,ax=plt.subplots()
        ax.bar(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("MoST COmmon WordS")
        st.pyplot(fig)

        emojis_df=helper.emoji_helper(selected_user,df)
        st.dataframe()









