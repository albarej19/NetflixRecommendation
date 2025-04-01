import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ✅ Load Merged Dataset
df = pd.read_csv("movies.csv")

# Ensure Premiere is numeric
df["Premiere"] = pd.to_numeric(df["Premiere"], errors='coerce')

df["Watchtime in Million"] = df["Watchtime in Million"].str.replace("M", "").astype(float)

# 🎬 App Title
st.title("🎥 Netflix Movie Recommendation System")

# 👉 Sidebar for User Inputs
# 👉 Sidebar for User Inputs
st.sidebar.header("🔍 Filter Options")
movie_type = st.sidebar.selectbox("🎞️ Select Type:", ["Movie", "TV Show"])
genre = st.sidebar.selectbox("🎭 Select Genre:", df["Genre"].unique())

# 📅 Replace Slider with Start and End Year Dropdowns
start_year, end_year = st.sidebar.selectbox(
    "📅 Select Start Year:", list(range(2000, 2024)), index=10
), st.sidebar.selectbox(
    "📅 Select End Year:", list(range(2000, 2024)), index=20
)

view_option = st.sidebar.radio("📈 Select Viewing Preference:", ["Most Viewed", "Least Viewed"])
analysis_option = st.sidebar.selectbox("📊 Select Analysis Type:", [
    "Netflix Insights",
    "Movie Purchase Recommendation",
    "Customer Complaints & Suggestions"
])

# 📚 Filter dataset using selected year range
filtered_data = df[
    (df["Type"] == movie_type)
    & (df["Genre"].str.contains(genre, na=False))
    & (df["Premiere"].between(start_year, end_year))
]


# 🧩 Sort based on selected viewing preference
if view_option == "Most Viewed":
    filtered_data = filtered_data.sort_values(by="Watchtime in Million", ascending=False)
else:
    filtered_data = filtered_data.sort_values(by="Watchtime in Million", ascending=True)

# 🎁 Show Key Metrics
st.subheader("📊 Key Insights at a Glance")
col1, col2, col3 = st.columns(3)

col1.metric("🎥 Total Movies/Shows", len(filtered_data))
col2.metric("🔥 Avg. Watchtime (M)", f"{filtered_data['Watchtime in Million'].mean():.2f}M")
col3.metric("📅 Latest Year Available", int(filtered_data["Premiere"].max()))

# 📊 Plot Top 5 Titles Based on Watchtime
st.subheader("📈 Top 5 Titles Based on Watchtime")
if not filtered_data.empty:
    top_5_data = filtered_data.head(5)
    fig, ax = plt.subplots()
    ax.bar(top_5_data["Title"], top_5_data["Watchtime in Million"], color='skyblue')
    plt.xticks(rotation=45, ha='right')
    plt.ylabel("Watchtime in Million")
    plt.title("Top 5 Most/Least Viewed Titles")
    st.pyplot(fig)
else:
    st.write("⚠️ No data available for the selected filters.")

# 🎥 Show Filtered Data in Styled Format
st.subheader("🎞️ Filtered Results (Top 10)")
if not filtered_data.empty:
    for idx, row in filtered_data.head(10).iterrows():
        st.markdown(f"""
        <div style="border:1px solid #ccc; padding:10px; border-radius:10px; margin-bottom:10px;">
        <h4>{row['Title']} ({int(row['Premiere'])})</h4>
        <p>🎭 Genre: {row['Genre']} | 🔥 Watchtime: {row['Watchtime in Million']}M</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.write("⚠️ No matching records found.")

# 📊 Perform Analysis Based on User Selection
st.subheader("📚 Analysis & Insights")
if analysis_option == "Netflix Insights":
    st.write("""
    ### 5 Key Insights Netflix Can Use:
    - Find the most popular genre in different regions.
    - Analyze trends in movie watchtime over the years.
    - Identify underperforming movies and genres.
    - Recommend suitable movie categories for different seasons.
    - Analyze audience preference for new vs. old movies.
    """)

elif analysis_option == "Movie Purchase Recommendation":
    if not filtered_data.empty:
        top_movie = filtered_data.iloc[0]
        st.success(f"🎯 **Recommendation:** Purchase movies similar to '{top_movie['Title']}' as it has high watchtime in its category.")
    else:
        st.warning("⚠️ No suitable recommendation found based on the current filters.")

elif analysis_option == "Customer Complaints & Suggestions":
    st.write("""
    ### Customer Complaints & Suggestions:
    - More diversity in content with different genres.
    - Adding more classic movies based on audience interest.
    - Increasing availability of highly watched but discontinued shows.
    - Better regional content selection based on viewing trends.
    - More frequent updates on trending movie lists.
    """)

# 🎉 Footer
st.markdown("---")
st.caption("📽️ Built with ❤️ by Albarej19")
