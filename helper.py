from urlextract import URLExtract
import matplotlib.pyplot as plt
import seaborn as sns
from  wordcloud import WordCloud
import plotly.graph_objects as go
import pandas as pd
from collections import Counter
import emoji
import nltk
from nltk.corpus import stopwords

# Télécharger les stopwords (à faire une seule fois)
nltk.download('stopwords')

# Fusionner les stopwords français et anglais
stop_words = set(stopwords.words('french')) | set(stopwords.words('english'))

extractor = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    link = []
    for message in df['messages']:
        link.extend(extractor.find_urls(message))

    for message in df['messages']:
        words.extend(message.split())
    num_media_messages = df[df['messages'] == '<Media omitted>'].shape[0]
    return num_messages, len(words), num_media_messages, len(link)

def most_busy_users(df):
    X = df['user'].value_counts().head()
    names = X.index
    counts = X.values

    fig = go.Figure(data=[go.Bar(
        x=names,
        y=counts,
        marker=dict(color=counts, colorscale="Blues", line=dict(width=2)),
        width=0.4
    )])

    fig.update_layout(
        title="Interactive 3D-like Bar Chart",
        xaxis_title="Names",
        yaxis_title="Count",
        template="plotly_dark",
        width=600,
        height=500,
        plot_bgcolor="#0D0F12",
        paper_bgcolor="#0D0F12",
        font=dict(color="white")
    )
    nd = round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(
        columns={'user': 'Names', 'count': 'percent'})

    return fig, nd

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group notification']
    temp = temp[temp['messages'] != '<Media omitted>']

    def remove_stopwords(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['messages'] = temp['messages'].apply(remove_stopwords)
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group notification']
    temp = temp[temp['messages'] != '<Media omitted>']

    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    ndf = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return ndf

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    X = df['day_name'].value_counts()

    names = X.index
    counts = X.values

    fig = go.Figure(data=[go.Bar(
        x=names,
        y=counts,
        marker=dict(color=counts, colorscale="Blues", line=dict(width=2)),
        width=0.5
    )])

    fig.update_layout(
        title="Most Busy Days",
        xaxis_title="Days",
        template="plotly_dark",
        width=700,
        height=500,
        plot_bgcolor="#0D0F12",
        paper_bgcolor="#0D0F12",
        font=dict(color="white")
    )

    return fig

def monthly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    X = df['month'].value_counts()
    names = X.index
    counts = X.values

    fig = go.Figure(data=[go.Bar(
        x=names,
        y=counts,
        marker=dict(color=counts, colorscale="Blues", line=dict(width=2)),
        width=0.5
    )])

    fig.update_layout(
        title="Most Busy Months",
        xaxis_title="Days",
        template="plotly_dark",
        width=700,
        height=500,
        plot_bgcolor="#0D0F12",
        paper_bgcolor="#0D0F12",
        font=dict(color="white")
    )

    return fig

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    fig3 = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return fig3
