from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3


try:
    response = requests.get("https://www.imdb.com/chart/top/")
    soup = BeautifulSoup(response.text, 'html.parser')

    movies = soup.find("tbody", class_="lister-list").find_all("tr")
    movie_list = {"Movie Rank": [], "Movie Name": [], "Movie Year":[], "Movie Rate": []};
    for movie in movies:
        rank = movie.find("td",class_="titleColumn").get_text(strip=True).split(".")[0]
        name = movie.find("td", class_="titleColumn").a.text
        year = movie.find("td",class_="titleColumn").span.text.replace("(","")
        year = year.replace(")","")
        rate = movie.find("td",class_="ratingColumn").strong.text

        movie_list["Movie Rank"].append(rank)
        movie_list["Movie Name"].append(name)
        movie_list["Movie Year"].append(year)
        movie_list["Movie Rate"].append(rate)

except Exception as e:
    print(e)

df = pd.DataFrame(data=movie_list)
print(df.head())

connection = sqlite3.connect("test.db")
cursor = connection.cursor()
qry = "CREATE TABLE IF NOT EXISTS movies(Movie Rank, Movie_Name, Movie_Year, Movie_Rate)"
cursor.execute(qry)

for i in range(len(df)):
    cursor.execute("insert into movies values (?,?,?,?)",df.iloc[i])

connection.commit()
connection.close()
