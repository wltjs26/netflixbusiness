import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Ensure the graphs directory exists
if not os.path.exists("graphs"):
    os.makedirs("graphs")

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
plt.savefig("graphs/country_content.png", bbox_inches="tight")  # Save image
plt.close()

### 2️⃣ Trends in Movie Releases Over Time ###
movies_per_year = df[df["type"] == "Movie"].groupby("release_year").size()

plt.figure(figsize=(12, 6))
movies_per_year.plot(kind="line", marker="o")
plt.title("Number of Movies Released Per Year")
plt.xlabel("Year")
plt.ylabel("Number of Movies")
plt.grid(True)
plt.savefig("graphs/movies_per_year.png", bbox_inches="tight")
plt.close()

### 3️⃣ Comparison Between TV Shows and Movies ###
type_counts = df["type"].value_counts()

plt.figure(figsize=(6, 6))
type_counts.plot(kind="pie", autopct="%1.1f%%", colors=["skyblue", "lightcoral"])
plt.title("Distribution of Movies and TV Shows on Netflix")
plt.ylabel("")
plt.savefig("graphs/movies_vs_tvshows.png", bbox_inches="tight")
plt.close()

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
plt.savefig("graphs/best_tv_show_month.png", bbox_inches="tight")
plt.close()
