import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Function to load and clean data (this is a good practice to avoid reloading on every interaction)
@st.cache_data
def load_data():
    df = pd.read_csv('metadata.csv')
    df.dropna(subset=['title', 'abstract'], inplace=True)
    df['journal'].fillna('Unknown Journal', inplace=True)
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['publication_year'] = df['publish_time'].dt.year
    df['abstract_word_count'] = df['abstract'].apply(lambda x: len(str(x).split()))
    return df

# Load the data
df = load_data()

# Set up the app title and description
st.title("CORD-19 Data Explorer 🔬")
st.write("A simple application to explore the CORD-19 research challenge metadata.")

st.markdown("""
---
""")

# --- Display Data Section ---
st.header("Raw Data Sample")
st.write("A small sample of the cleaned dataset:")
st.dataframe(df.sample(n=10))

st.markdown("""
---
""")

# --- Analysis Section ---
st.header("Data Insights and Visualizations")

# Filter data using a slider
year_range = st.slider(
    "Select a publication year range:",
    min_value=int(df['publication_year'].min()),
    max_value=int(df['publication_year'].max()),
    value=(int(df['publication_year'].min()), int(df['publication_year'].max()))
)

# Filter the DataFrame based on the selected year range
filtered_df = df[(df['publication_year'] >= year_range[0]) & (df['publication_year'] <= year_range[1])]

# Display publications over time
st.subheader("Publications Over Time")
papers_by_year = filtered_df['publication_year'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=papers_by_year.index, y=papers_by_year.values, marker='o', ax=ax)
ax.set_title('Number of CORD-19 Publications Over Time')
ax.set_xlabel('Publication Year')
ax.set_ylabel('Number of Papers')
st.pyplot(fig)

st.markdown("""
---
""")

# Display top journals
st.subheader("Top 10 Publishing Journals")
top_journals = filtered_df['journal'].value_counts().head(10)
fig, ax = plt.subplots(figsize=(12, 8))
sns.barplot(x=top_journals.values, y=top_journals.index, palette="viridis", ax=ax)
ax.set_title('Top 10 Journals by Number of Publications')
ax.set_xlabel('Number of Papers')
ax.set_ylabel('Journal Name')
st.pyplot(fig)

st.markdown("""
---
""")

# Display a word cloud
st.subheader("Word Cloud of Paper Titles")
all_titles = ' '.join(title for title in filtered_df['title'].astype(str))
if all_titles:
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
else:
    st.write("No data available for the selected year range to generate a word cloud.")



# Set a style for better-looking plots
sns.set_style("whitegrid")

# Load the metadata.csv file into a DataFrame
try:
    df = pd.read_csv('metadata.csv')
    print("Data loaded successfully!")
except FileNotFoundError:
    print("Error: The file 'metadata.csv' was not found. Please ensure it's in the same directory.")
    exit()

# Display the first 5 rows to get a feel for the data
print("\nFirst 5 rows of the DataFrame:")
print(df.head())

# Check the dimensions (rows and columns) of the DataFrame
print("\nDataFrame dimensions:")
print(f"Number of rows: {df.shape[0]}")
print(f"Number of columns: {df.shape[1]}")

# Get a summary of the DataFrame, including data types and non-null counts
print("\nDataFrame information:")
df.info()

# Check for missing values in each column
print("\nMissing values per column:")
print(df.isnull().sum())

# Drop rows with missing values in 'title' or 'abstract'
cleaned_df = df.dropna(subset=['title', 'abstract'])

# Fill missing values in 'journal' with a placeholder
cleaned_df['journal'].fillna('Unknown Journal', inplace=True)

# Verify the changes
print("\nMissing values after cleaning:")
print(cleaned_df.isnull().sum())

# Convert 'publish_time' to datetime objects
cleaned_df['publish_time'] = pd.to_datetime(cleaned_df['publish_time'], errors='coerce')

# Extract the year from the 'publish_time' and create a new column
cleaned_df['publication_year'] = cleaned_df['publish_time'].dt.year

# Create a new column for abstract word count
cleaned_df['abstract_word_count'] = cleaned_df['abstract'].apply(lambda x: len(str(x).split()))

# Display the updated DataFrame info to confirm the new columns
print("\nDataFrame info after preparation:")
print(cleaned_df.info())

# Count papers by publication year
papers_by_year = cleaned_df['publication_year'].value_counts().sort_index()
print("\nPapers published per year:")
print(papers_by_year)

# Identify the top 10 journals by publication count
top_journals = cleaned_df['journal'].value_counts().head(10)
print("\nTop 10 publishing journals:")
print(top_journals)

# Plot 1: Publications over time
plt.figure(figsize=(10, 6))
sns.lineplot(x=papers_by_year.index, y=papers_by_year.values, marker='o')
plt.title('Number of CORD-19 Publications Over Time')
plt.xlabel('Publication Year')
plt.ylabel('Number of Papers')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot 2: Top publishing journals
plt.figure(figsize=(12, 8))
sns.barplot(x=top_journals.values, y=top_journals.index, palette="viridis")
plt.title('Top 10 Journals by Number of Publications')
plt.xlabel('Number of Papers')
plt.ylabel('Journal Name')
plt.tight_layout()
plt.show()

# Word cloud (requires the wordcloud library: pip install wordcloud)
from wordcloud import WordCloud

# Combine all titles into a single string
all_titles = ' '.join(title for title in cleaned_df['title'].astype(str))

# Create and generate a word cloud image
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)

# Display the generated image
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Paper Titles')
plt.show()
