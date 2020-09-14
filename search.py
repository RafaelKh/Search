from bs4 import BeautifulSoup
import urllib.request
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="04072003",
  database="links"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE link (link varchar(1000)")


response = urllib.request.urlopen("https://martinfowler.com/")
html = response.read()
soup = BeautifulSoup(html, "html.parser")
links = soup.find_all("a href")

for a in soup.find_all('a', href=True):
    sql = "INSERT INTO links (link) VALUES (%s)"
    val = (a['href'])
    mycursor.execute(sql, val)
