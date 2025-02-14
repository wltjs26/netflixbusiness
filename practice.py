import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure the graphs directory exists
if not os.path.exists("graphs"):
    os.makedirs("graphs")

# Load dataset
file_path = "D:/다운로드/datasets/datasets/netflix_data.csv"
df = pd.read_csv(file_path)

### 1️⃣ Data Preprocessing (결측값 처리 및 기초 통계 분석) ###

# Check for missing values
missing_values = df.isnull().sum().sort_values(ascending=False)
missing_values = missing_values[missing_values > 0]  # Only show columns with missing values

# Save missing values plot
plt.figure(figsize=(10, 5))
missing_values.plot(kind="bar", color="red", alpha=0.8)
plt.title("Missing Values per Column")
plt.xlabel("Columns")
plt.ylabel("Count of Missing Values")
plt.xticks(rotation=45)
plt.savefig("graphs/missing_values.png", bbox_inches="tight")
plt.close()

# Fill missing values with appropriate defaults
df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
df["date_added"].fillna(pd.Timestamp("2000-01-01"), inplace=True)

df = df.assign(
    rating=df["rating"].fillna("Unknown"),
    country=df["country"].fillna("Unknown"),
    cast=df["cast"].fillna(""),
    director=df["director"].fillna(""),
    listed_in=df["listed_in"].fillna("")
)

# Extract year and month from date_added
df["month_added"] = df["date_added"].dt.month
df["year_added"] = df["date_added"].dt.year

# Convert release_year to numeric
df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")

# Summary statistics for numerical columns
numeric_summary = df.describe()
numeric_summary.to_csv("graphs/numeric_summary.csv")

# Save numeric summary visualization
plt.figure(figsize=(10, 5))
sns.boxplot(data=df[["release_year"]].dropna())
plt.title("Distribution of Release Years")
plt.savefig("graphs/numeric_summary.png", bbox_inches="tight")
plt.close()

# Extract main genre from listed_in
df["main_genre"] = df["listed_in"].apply(lambda x: x.split(",")[0] if isinstance(x, str) else x)

### 2️⃣ Netflix Content Distribution by Country ###
content_by_country = df.groupby(["country", "type"]).size().unstack().fillna(0)
content_by_country.sort_values(by="Movie", ascending=False, inplace=True)

plt.figure(figsize=(12, 6))
content_by_country.head(10).plot(kind="bar", stacked=True)
plt.title("Top 10 Countries by Content Type on Netflix")
plt.xlabel("Country")
plt.ylabel("Number of Titles")
plt.legend(title="Type")
plt.xticks(rotation=45)
plt.savefig("graphs/country_content.png", bbox_inches="tight")  
plt.close()

### 3️⃣ Trends in Movie Releases Over Time ###
movies_per_year = df[df["type"] == "Movie"].groupby("release_year").size()

plt.figure(figsize=(12, 6))
movies_per_year.plot(kind="line", marker="o")
plt.title("Number of Movies Released Per Year")
plt.xlabel("Year")
plt.ylabel("Number of Movies")
plt.grid(True)
plt.savefig("graphs/movies_per_year.png", bbox_inches="tight")
plt.close()

### 4️⃣ Comparison Between TV Shows and Movies ###
type_counts = df["type"].value_counts()

plt.figure(figsize=(6, 6))
type_counts.plot(kind="pie", autopct="%1.1f%%", colors=["skyblue", "lightcoral"])
plt.title("Distribution of Movies and TV Shows on Netflix")
plt.ylabel("")
plt.savefig("graphs/movies_vs_tvshows.png", bbox_inches="tight")
plt.close()

### 5️⃣ Best Time to Launch a TV Show (Based on Release Month) ###
tv_shows_monthly = df[df["type"] == "TV Show"].groupby("month_added").size()

# Ensure all months (1-12) are represented
all_months = pd.Series(index=range(1, 13), data=0)
tv_shows_monthly = all_months.add(tv_shows_monthly, fill_value=0)

plt.figure(figsize=(12, 6))
tv_shows_monthly.plot(kind="bar", color="purple", alpha=0.8)
plt.title("Best Time to Launch a TV Show (Monthly Analysis)")
plt.xlabel("Month")
plt.ylabel("Number of TV Shows Added")
plt.xticks(range(12), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=45)
plt.savefig("graphs/best_tv_show_month.png", bbox_inches="tight")
plt.close()

### 6️⃣ Most Featured Actors (Filtered) ###
actor_counts = df["cast"].str.split(", ").explode().value_counts()

# Remove extreme values (actors appearing in more than 100 titles)
actor_counts = actor_counts[actor_counts.between(1, 100)]

top_actors = actor_counts.head(10)

plt.figure(figsize=(12, 6))
top_actors.plot(kind="bar", color="teal")
plt.title("Top 10 Most Featured Actors on Netflix (Filtered)")
plt.xlabel("Actor")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.savefig("graphs/top_actors_filtered.png", bbox_inches="tight")
plt.close()

### 7️⃣ Most Featured Directors (Filtered) ###
director_counts = df["director"].str.split(", ").explode().value_counts()

# Remove extreme values (directors appearing in more than 100 titles)
director_counts = director_counts[director_counts.between(1, 100)]

top_directors = director_counts.head(10)

plt.figure(figsize=(12, 6))
top_directors.plot(kind="bar", color="orange")
plt.title("Top 10 Most Featured Directors on Netflix (Filtered)")
plt.xlabel("Director")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.savefig("graphs/top_directors_filtered.png", bbox_inches="tight")
plt.close()

### 8️⃣ Seasonal Trends in Content Release ###
seasonal_trends = df.groupby("month_added").size()

plt.figure(figsize=(12, 6))
seasonal_trends.plot(kind="bar", color="purple", alpha=0.8)
plt.title("Seasonal Trends in Content Release")
plt.xlabel("Month")
plt.ylabel("Number of Titles Added")
plt.xticks(rotation=45)
plt.savefig("graphs/seasonal_trends.png", bbox_inches="tight")
plt.close()

### 🔟 Top 10 Countries by Total Netflix Content ###
top_countries = df["country"].value_counts().head(10)

plt.figure(figsize=(12, 6))
top_countries.plot(kind="bar", color="green", alpha=0.8)
plt.title("Top 10 Countries by Number of Titles on Netflix")
plt.xlabel("Country")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.savefig("graphs/top_countries.png", bbox_inches="tight")
plt.close()
