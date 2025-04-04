import streamlit as st
import preprocessing
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessing.preprocess(data)



    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove("group notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show Analysis wrt",user_list)
    if st.sidebar.button("Show Analysis"):
        st.header("Top Statistics")
        num_messages,words,num_media_messages,link=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(link)

        #monthly_timeline
        st.title("Monthly Timeline")

        # Get the timeline DataFrame
        timeline = helper.monthly_timeline(selected_user, df)

        # Create a smaller figure
        fig, ax = plt.subplots(figsize=(7,3))  # Adjust size

        # Plot the data
        ax.plot(timeline["time"], timeline["messages"], color="lime", marker="o", linestyle="-")  # Lime for contrast

        # Rotate x-axis labels to 45 degrees
        plt.xticks(rotation=45, color="white")  # White text

        # Set dark background
        fig.patch.set_facecolor("#0D0F12")  # Dark blue (almost black)
        ax.set_facecolor("#0D0F12")  # Background for plot

        # Set axis labels and ticks to white
        ax.spines["bottom"].set_color("white")
        ax.spines["left"].set_color("white")
        ax.spines["top"].set_color("white")
        ax.spines["right"].set_color("white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.tick_params(axis="x", colors="white")
        ax.tick_params(axis="y", colors="white")

        # Display in Streamlit
        st.pyplot(fig)

        #daily_timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(7, 3))  # Adjust size

        # Plot the data
        ax.plot(daily_timeline["only_date"], daily_timeline["messages"], color="lime", linestyle="-")
        plt.xticks(rotation=45, color="white")  # White text

        # Set dark background
        fig.patch.set_facecolor("#0D0F12")  # Dark blue (almost black)
        ax.set_facecolor("#0D0F12")  # Background for plot

        # Set axis labels and ticks to white
        ax.spines["bottom"].set_color("white")
        ax.spines["left"].set_color("white")
        ax.spines["top"].set_color("white")
        ax.spines["right"].set_color("white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.tick_params(axis="x", colors="white")
        ax.tick_params(axis="y", colors="white")

        # Display in Streamlit
        st.pyplot(fig)

        #activity_map
        st.title('Activity Map')
        col1,col2=st.columns(2)

        with col1:
            st.header("Most Busy Days")
            fig=helper.week_activity_map(selected_user, df)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.header("Most Busy Months")
            fig2= helper.monthly_activity_map(selected_user, df)
            st.plotly_chart(fig2, use_container_width=True)





        #finding the busiest user
        if selected_user=='Overall':
            st.title("Most Active Users")
            col1,col2=st.columns(2)
            fig,nd= helper.most_busy_users(df)
            with col1:
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.dataframe(nd)


        st.title('WordCloud')
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

        st.title("Most Commonly Used Words")

        most_common_df=helper.most_common_words(selected_user, df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation=45)

        st.pyplot(fig)

        st.header("Emoji Analysis")
        emoji_df=helper.emoji_helper(selected_user,df)
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            explode = [0.1] * len(emoji_df[1].head())
            fig.patch.set_facecolor('#0D0F12')
            # Create the pie chart with explode and shadow for a 3D-like effect
            ax.pie(
                emoji_df[1].head(),
                labels=emoji_df[0].head(),
                autopct="%0.2f",
                explode=explode,  # Add explode effect
                shadow=True,  # Add shadow for a 3D-like look
                startangle=90  # Rotate the chart to start at the top
            )
            st.pyplot(fig)

        st.header("weekly Activity Map")
        user_heatmap=helper.activity_heatmap(selected_user, df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)
