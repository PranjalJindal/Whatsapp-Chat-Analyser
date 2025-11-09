import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyser")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    
    df = preprocessor.preprocess(data)
    

    # fetch unique users

    user_list=df['user'].unique().tolist()
    if("group_notification" in user_list):
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        col1, col2, col3, col4 = st.columns(4)

        total_messages,total_words,total_media,total_links=helper.fetch_stats(selected_user,df)

        st.title("Top Statistics")

        with col1:
            st.header("Total messages")
            st.title(total_messages)

        with col2:
            st.header("Total words")
            st.title(total_words)
        with col3:
            st.header("Total Media")
            st.title(total_media)

        with col4:
            st.header("Total Links")
            st.title(total_links)

        st.title("Monthly Timeline")

        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['month'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Daily Timeline")

        daily_time=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_time['only_date'],daily_time['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # activity_map
    
        st.title("Activity Map")

        col1,col2=st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day['day_name'].astype(str), busy_day['message_count'], color='skyblue')
            plt.xticks(rotation=45)
            st.pyplot(fig)



        with col2:

            st.header("Most Busy Month")
            busy_month = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values, color='orange')
            plt.xticks(rotation=45)
            st.pyplot(fig)


        st.title("Weekly Activity Map")

        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)



        if selected_user == "Overall":
            st.title("Most Busy Users")
            x,df_new=helper.fetch_most_busy_users(df)
            fig,ax=plt.subplots()
            
            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(df_new)
        st.title("Word Cloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # most common words

        most_common_df= (helper.most_common_words(selected_user,df))

        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation="vertical")
        st.title("Most Common Words")
        st.pyplot(fig)

        most_common_emoji = helper.emoji_count(selected_user, df)

        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(most_common_emoji)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(
                most_common_emoji['Count'].head(10),
                labels=most_common_emoji['Emoji'].head(10),
                autopct='%1.1f%%',
                startangle=90
            )
            ax.axis('equal')  # makes pie chart circular
            st.pyplot(fig)
        