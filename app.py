import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df, region_df)
# df = pd.read_csv(r'E:\FYP\My Project Data\ODA\ReactNative\CleanedDataSet\CleanedCsvFile.csv')

st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis','Athlete wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)


    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("No. of Events over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'), annot=True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt, annot=True)
    st.pyplot(fig)

    st.title("Top 10 athletes of " + selected_country)
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top10_df)




if user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=800, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)
    # Corrected sns.scatterplot call with x and y as keyword arguments
    fig, ax = plt.subplots()
    sns.scatterplot(x='Weight', y='Height', hue='Medal', style='Sex', data=temp_df, s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=800, height=600)
    st.plotly_chart(fig)












































# 1
# import pandas as pd
# import preprocessor
# df = pd.read_csv('athlete_events.csv')
# region_df = pd.read_csv('noc_regions.csv')
# df = preprocessor.preprocess(df,region_df)
# preprocessor.save_to_json(df, r'E:\finalfile.json')



# 2
# import pandas as pd
# import preprocessor
# df = pd.read_csv('athlete_events.csv')
# region_df = pd.read_csv('noc_regions.csv')
# df = preprocessor.preprocess(df,region_df)
# preprocessor.save_to_csv(df, r'E:\filefinal.csv')


# 3
# import streamlit as st
# import pandas as pd
# loaded_df = pd.read_csv(r'E:\filefinal.csv')
# st.title('Olympics Data Analysis')
# st.write("Loaded Data from CSV:")
# st.dataframe(loaded_df)




# 4
# import streamlit as st
# import pandas as pd
# # Streamlit app title
# st.title('Cleaned Olympics Data')
#
# # File load karein
# df = pd.read_csv('E:/filefinal.csv')
#
# # Duplicates drop karein
# df_cleaned = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
#
# # Cleaned data ko save karein
# df_cleaned.to_csv('E:/cleandata/filefinal.csv', index=False)
#
# # Dataframe display karein
# st.write("Here is the cleaned data:")
# st.dataframe(df_cleaned)



# 5
# import streamlit as st
# import pandas as pd
# # Streamlit app title
# st.title('Cleaned Olympics Data')
#
# # File load karein
# df = pd.read_csv('E:/filefinal.csv')
#
# # Duplicates drop karein
# df_cleaned = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
#
# # Cleaned data ko JSON format mein save karein
# df_cleaned.to_json('E:/cleandata/finalfile.json', orient='records', lines=True)
#
# # Dataframe display karein
# st.write("Here is the cleaned data:")
# st.dataframe(df_cleaned)





# 6 clean karne ky baad save ki hoe 1 file ko test ky liye attach aur upar 2 files ko remove
# import streamlit as st
# import pandas as pd
# import helper
# df = pd.read_csv(r'E:\filefinal.csv')



# 7
# import streamlit as st
# import pandas as pd
# # Streamlit app title
# st.title('Cleaned Olympics Data')
#
# # File load karein
# df = pd.read_csv(r'E:/filefinal.csv')
#
# # Duplicates drop karein
# df_cleaned = df.drop_duplicates(subset=['Name' ,'Sex', 'Age', 'Height', 'Weight', 'Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal', 'region', 'notes', 'Bronze', 'Gold', 'Silver'])
#
# # Cleaned data ko save karein
# df_cleaned.to_csv(r'E:/filefinalTest.csv', index=False)
#
# # Dataframe display karein
# st.write("Here is the cleaned data:")
# st.dataframe(df_cleaned)



# 8
# import streamlit as st
# import pandas as pd
# # Streamlit app title
# st.title('Cleaned Olympics Data')
#
# # File load karein
# df = pd.read_csv(r'E:/filefinal.csv')
#
# # Duplicates drop karein
# df_cleaned = df.drop_duplicates(subset=['Name' ,'Sex', 'Age', 'Height', 'Weight', 'Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal', 'region', 'notes', 'Bronze', 'Gold', 'Silver'])
#
# # Cleaned data ko save karein
# df_cleaned.to_json(r'E:/finalfileTest.json', index=False)
#
# # Dataframe display karein
# st.write("Here is the cleaned data:")
# st.dataframe(df_cleaned)


#9 jason-array
# import streamlit as st
# import pandas as pd
#
# # Streamlit app title
# st.title('Cleaned Olympics Data')
#
# # File load karein
# df = pd.read_csv(r'E:\7S\FYP\My Project Data\ODA 120 years data set and project complete code\CleanedDataSet\filefinal.csv')
#
# # Duplicates drop karein
# df_cleaned = df.drop_duplicates(subset=['Name', 'Sex', 'Age', 'Height', 'Weight', 'Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal', 'region', 'notes', 'Bronze', 'Gold', 'Silver'])
#
# # Cleaned data ko JSON array format me save karein
# json_data = df_cleaned.to_json(orient='records', lines=False)
#
# with open(r'E:/filefinalTest.json', 'w') as file:
#     file.write(json_data)
#
# # Dataframe display karein
# st.write("Here is the cleaned data:")
# st.dataframe(df_cleaned)
#
# st.write("JSON data saved successfully.")


#9 jason-array with set
# import streamlit as st
# import pandas as pd
#
# # Streamlit app title
# st.title('Cleaned Olympics Data')
#
# # File load karein
# df = pd.read_csv(r'E:\7S\FYP\My Project Data\ODA 120 years data set and project complete code\CleanedDataSet\filefinal.csv')
#
# # Duplicates drop karein
# df_cleaned = df.drop_duplicates(subset=['Name', 'Sex', 'Age', 'Height', 'Weight', 'Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal', 'region', 'notes', 'Bronze', 'Gold', 'Silver'])
#
# # Cleaned data ko JSON array format me save karein, har record alag line par
# json_data = df_cleaned.to_json(orient='records', lines=True)
#
# with open(r'E:/filefinalTest3.json', 'w') as file:
#     file.write('[' + ',\n    '.join(json_data.splitlines()) + ']')
#
# # Dataframe display karein
# st.write("Here is the cleaned data:")
# st.dataframe(df_cleaned)
#
# st.write("JSON data saved successfully.")






# 10 module 1 specific drop.duplicates, sort and reset index
# import streamlit as st
# import pandas as pd
#
# # Streamlit app title
# st.title('Cleaned Olympics Data')
#
# # File load karein
# df = pd.read_csv(r'E:\7S\FYP\CopyDataSet\CleanedCsvFile.csv')
#
# # Duplicates drop karein
# df_cleaned = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
#
# # Sort dataframe by Gold medals in descending order and then reset the index
# df_sorted = df_cleaned.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
#
# # Cleaned and sorted data ko JSON array format me save karein, har record alag line par
# json_data = df_sorted.to_json(orient='records', lines=True)
#
# with open(r'E:\module3file.json', 'w') as file:
#     file.write('[' + ',\n    '.join(json_data.splitlines()) + ']')
#
# # Dataframe display karein
# st.write("Here is the cleaned and sorted data:")
# st.dataframe(df_sorted)
#
# st.write("JSON data saved successfully.")





























# Waseem-SpamData
# import streamlit as st
# import pandas as pd
# # Streamlit app title
# st.title('Cleaned Spam Data')
#
# # File load karein
# df = pd.read_csv(r'E:\WaseemSpamDataSet\spam.csv')
#
# # Duplicates drop karein
# df_cleaned = df.drop_duplicates(subset=['v1' ,'v2'])
#
# # Cleaned data ko save karein
# df_cleaned.to_csv(r'E:\WaseemSpamDataSet\cleanedspam.csv', index=False)
#
# # Dataframe display karein
# st.write("Here is the cleaned data...")
# st.dataframe(df_cleaned)

#for CSV
# import streamlit as st
# import pandas as pd
#
# def load_data(file_path, encoding='utf-8'):
#     try:
#         return pd.read_csv(file_path, encoding=encoding)
#     except UnicodeDecodeError:
#         return pd.read_csv(file_path, encoding='ISO-8859-1')
#
# def clean_data(df):
#     df_cleaned = df.drop_duplicates(inplace=True)
#     return df_cleaned
#
# def save_data(df, file_path):
#     df.to_csv(file_path, index=False)
#
# # Streamlit app title
# st.title('Cleaned Spam Data')
#
# # File load karein
# file_path = r'E:\WaseemSpamDataSet\spam.csv'
# df = load_data(file_path)
#
# # Duplicates drop karein
# df_cleaned = clean_data(df)
#
# # Cleaned data ko save karein
# output_file_path = r'E:\WaseemSpamDataSet\cleanedspamTest.csv'
# save_data(df_cleaned, output_file_path)
#
# # Dataframe display karein
# st.write("Here is the cleaned data:")
# st.dataframe(df_cleaned)

# for json
# import streamlit as st
# import pandas as pd
#
# def load_data(file_path, encoding='utf-8'):
#     try:
#         return pd.read_csv(file_path, encoding=encoding)
#     except UnicodeDecodeError:
#         return pd.read_csv(file_path, encoding='ISO-8859-1')
#
# def clean_data(df):
#     df.drop_duplicates(inplace=True)
#     return df
#
# def save_data(df, file_path, format='csv'):
#     if format == 'csv':
#         df.to_csv(file_path, index=False)
#     elif format == 'json':
#         df.to_json(file_path, orient='records', lines=True)
#
# # Streamlit app title
# st.title('Cleaned Spam Data')
#
# # File load karein
# file_path = r'E:\WaseemSpamDataSet\spam.csv'
# df = load_data(file_path)
#
# # Duplicates drop karein
# df_cleaned = clean_data(df)
#
# # Cleaned data ko JSON format mein save karein
# output_file_path = r'E:\WaseemSpamDataSet\cleanedspamTest.json'
# save_data(df_cleaned, output_file_path, format='json')
#
# # Dataframe display karein
# st.write("Here is the cleaned data:")
# st.dataframe(df_cleaned)
