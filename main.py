import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

movies_data = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/Dataset%20for%20Practice/movies.csv")
movies_data = movies_data.dropna()

# tạo sidebar
st.sidebar.title('Lọc dữ liệu')

# khoang diem
st.sidebar.write('Select a range on the slider (it represents movie score) to view the total number of movies in a genre that falls within that range')
score_range = st.sidebar.slider(
    "Chọn khoảng điểm",
    min_value=1.0, max_value=10.0, value=(3.0, 4.0)
)

# the loai
genres = st.sidebar.multiselect(
    "Chọn thể loại",
    options=movies_data['genre'].unique(),
    #default=['Animation','Horror', 'Fantasy','Romance']
    default=list(movies_data['genre'].unique())
)

# nam
years = sorted(movies_data['year'].unique())
selected_year = st.sidebar.selectbox(
    "Chọn năm",
    options=years
)

# lọc dữ liệu
filtered_data = movies_data[
    (movies_data['score'] >= score_range[0]) &
    (movies_data['score'] <= score_range[1]) &
    (movies_data['genre'].isin(genres)) &
    (movies_data['year'] == selected_year)
]

# display:flex
col1, col2 = st.columns(2)

with col1:
    st.header('Lists of movies filtered by year and Genre')
    st.dataframe(filtered_data[['name', 'genre', 'year']])

with col2:
    st.header('User score of movies and their genre')
    genre_score = movies_data.groupby('genre')['score'].sum().reset_index()
    st.line_chart(genre_score.set_index('genre'))


# hiển thị biểu đồ
st.subheader("Biểu đồ ngân sách trung bình theo thể loại")
avg_budget = movies_data.groupby('genre')['budget'].mean().round()
avg_budget = avg_budget.reset_index()

# vẽ
fig = plt.figure(figsize=(10, 5))
plt.bar(avg_budget['genre'], avg_budget['budget'], color='lightblue')
plt.xlabel('Thể loại')
plt.ylabel('Ngân sách trung bình')
plt.title('Trung bình ngân sách theo thể loại')
plt.xticks(rotation=45)
st.pyplot(fig)
