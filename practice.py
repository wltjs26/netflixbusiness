import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = r"D:\다운로드\datasets\datasets\netflix_data.csv"  # Update as needed
df = pd.read_csv(file_path)

# Convert date_added to datetime format
df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

# Extract year and month from date_added
df["month_added"] = df["date_added"].dt.month
df["year_added"] = df["date_added"].dt.year

# Convert release_year to numeric
df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")

# Extract main genre from listed_in
df["main_genre"] = df["listed_in"].apply(lambda x: x.split(",")[0] if isinstance(x, str) else x)

# Ensure ratings are strings
df["rating"] = df["rating"].astype(str)

### 1️⃣ Netflix Content Distribution by Country ###
content_by_country = df.groupby(["country", "type"]).size().unstack().fillna(0)
content_by_country.sort_values(by="Movie", ascending=False, inplace=True)

plt.figure(figsize=(12, 6))
content_by_country.head(10).plot(kind="bar", stacked=True)
plt.title("Top 10 Countries by Content Type on Netflix")
plt.xlabel("Country")
plt.ylabel("Number of Titles")
plt.legend(title="Type")
plt.xticks(rotation=45)
plt.show()

### 2️⃣ Trends in Movie Releases Over Time ###
movies_per_year = df[df["type"] == "Movie"].groupby("release_year").size()

plt.figure(figsize=(12, 6))
movies_per_year.plot(kind="line", marker="o")
plt.title("Number of Movies Released Per Year")
plt.xlabel("Year")
plt.ylabel("Number of Movies")
plt.grid(True)
plt.show()

### 3️⃣ Comparison Between TV Shows and Movies ###
type_counts = df["type"].value_counts()

plt.figure(figsize=(6, 6))
type_counts.plot(kind="pie", autopct="%1.1f%%", colors=["skyblue", "lightcoral"])
plt.title("Distribution of Movies and TV Shows on Netflix")
plt.ylabel("")
plt.show()

### 4️⃣ Best Time to Launch a TV Show (Based on Release Month) ###
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
plt.show()

### 5️⃣ Most Featured Actors & Directors ###
df["cast"] = df["cast"].fillna("").apply(lambda x: x.strip())
df["director"] = df["director"].fillna("").apply(lambda x: x.strip())

# Split actors and explode the list
actor_counts = df["cast"].str.split(", ").explode().value_counts()
actor_counts = actor_counts[actor_counts.index.str.strip() != ""]  # Remove empty actor names

# Top 10 Actors
top_actors = actor_counts.head(10)

plt.figure(figsize=(12, 6))
top_actors.plot(kind="bar", color="teal")
plt.title("Top 10 Most Featured Actors on Netflix")
plt.xlabel("Actor")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.show()

# Split directors and explode the list
director_counts = df["director"].str.split(", ").explode().value_counts()
director_counts = director_counts[director_counts.index.str.strip() != ""]  # Remove empty director names

# Top 10 Directors
top_directors = director_counts.head(10)

plt.figure(figsize=(12, 6))
top_directors.plot(kind="bar", color="orange")
plt.title("Top 10 Most Featured Directors on Netflix")
plt.xlabel("Director")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.show()

### 6️⃣ Netflix's Focus: Movies vs. TV Shows Over Time ###
recent_trend = df[df["release_year"] >= 2000].groupby(["release_year", "type"]).size().unstack().fillna(0)

plt.figure(figsize=(12, 6))
recent_trend.plot(kind="line", marker="o")
plt.title("Trend of Movies vs. TV Shows Released Each Year")
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.legend(title="Type")
plt.grid(True)
plt.show()

### 7️⃣ Content Ratings by Genre ###
rating_genre = df.groupby(["rating", "main_genre"]).size().unstack(fill_value=0)
top_ratings = rating_genre.sum(axis=1).nlargest(10).index  # Top 10 ratings
rating_genre_filtered = rating_genre.loc[top_ratings]

plt.figure(figsize=(12, 6))
rating_genre_filtered.plot(kind="bar", stacked=True, alpha=0.8)
plt.title("Content Ratings by Genre")
plt.xlabel("Rating Category")
plt.ylabel("Number of Titles")
plt.legend(title="Genre", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.xticks(rotation=45)
plt.show()

### 8️⃣ Seasonal Trends in Content Release ###
seasonal_trends = df.groupby("month_added").size()

# Ensure all months (1-12) are included
seasonal_trends = all_months.add(seasonal_trends, fill_value=0)

plt.figure(figsize=(12, 6))
seasonal_trends.plot(kind="bar", color="purple", alpha=0.8)
plt.title("Seasonal Trends in Content Release")
plt.xlabel("Month")
plt.ylabel("Number of Titles Added")
plt.xticks(range(12), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=45)
plt.show()

### 9️⃣ Top 10 Countries by Total Netflix Content ###
top_countries = df["country"].value_counts().head(10)

plt.figure(figsize=(12, 6))
top_countries.plot(kind="bar", color="green", alpha=0.8)
plt.title("Top 10 Countries by Number of Titles on Netflix")
plt.xlabel("Country")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.show()
