import matplotlib.pyplot as plt
import streamlit as st
import preprocessor,helper
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocessor.preprocess(data)
    # st.dataframe(df)

    # fetch unqiue users
    user_list = df['user'].unique().tolist()

    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis WRT", user_list)

    if st.sidebar.button("Show Analysis"):
        st.title('Top Statistics')

        num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user, df)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Total Media Messages")
            st.title(num_media_messages)
        with col4:
            st.header("Total links shared")
            st.title(links)

        # timeline
        st.title('Monthly timeline')
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header('Most busy day')
            busy_day = helper.weakly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header('Most busy month')
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # heat MAP
        st.title("Weakly activity heatmap")
        user_activity_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_activity_heatmap)
        st.pyplot(fig)



        # most busy user
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_user(df)
            fig, ax = plt.subplots()
            ax.bar(x.index, x.values)
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        plt.imshow(df_wc)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most Common Words ')
        st.pyplot(fig)
        # st.dataframe(most_common_df)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title('Most Emoji Used')
        st.dataframe(emoji_df)

