import pandas as pd
from pymongo import MongoClient

# Load dataset
csv_file = "imdb_top_1000.csv"  # Replace with your actual CSV file path
df = pd.read_csv(csv_file)

# Connect to MongoDB
client = MongoClient("mongodb+srv://chintan:chintan123@cluster0.i5cai.mongodb.net")  # Update if using a remote DB
db = client["moviemate"]  # Your database name
collection = db["movies"]  # Your collection name

# Convert dataset fields to match MongoDB schema
movies = []

for _, row in df.iterrows():
    movie = {
        "name": row["Series_Title"],
        "pic_url": row["Poster_Link"],
        "description": row["Overview"],
        "trailer_url": "",  # No trailer in dataset, keep empty or use an API to fetch
        "release_date": row["Released_Year"],  # Convert to int or keep as string
        "average_rating": row["IMDB_Rating"],
        "genre": row["Genre"].split(", "),  # Convert string to list
        "cast": [row["Star1"], row["Star2"], row["Star3"], row["Star4"]],  # List of actors
        "directors": [row["Director"]],
        "runtime": row["Runtime"],  # Optional, not in original schema
        "meta_score": row["Meta_score"] if not pd.isna(row["Meta_score"]) else None,
        "certificate": row["Certificate"] if not pd.isna(row["Certificate"]) else None,
        "votes": row["No_of_Votes"],
        "gross": row["Gross"] if not pd.isna(row["Gross"]) else None,
    }
    movies.append(movie)

# Insert into MongoDB
if movies:
    collection.insert_many(movies)
    print(f"Inserted {len(movies)} movies into MongoDB.")
else:
    print("No movies to insert.")
