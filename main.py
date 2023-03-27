from bs4 import BeautifulSoup
import requests, openpyxl
excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = "Movies_List"
sheet.append(["Rank","Movie Name","Year","Ratings"])
try:
    response = requests.get("https://www.imdb.com/chart/top/")
    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup)
    movies = soup.find("tbody", class_="lister-list").find_all("tr")
    for movie in movies:
        rank = movie.find("td",class_="titleColumn").get_text(strip=True).split(".")[0]
        name = movie.find("td", class_="titleColumn").a.text
        year = movie.find("td",class_="titleColumn").span.text.replace("(","")
        year = year.replace(")","")
        rate = movie.find("td",class_="ratingColumn").strong.text

        sheet.append([rank,name,year,rate])
except Exception as e:
    print(e)
excel.save("Top Movies.xlsx")
