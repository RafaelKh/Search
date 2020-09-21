import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from config import DATABASE, SITE_NAME, SITE_PROTOCOL
from model import create_connection, create_table, select_all_links
from sql import sql_create_links_table
import os

directory = SITE_NAME

parent_dir = "/home/rafael/Desktop/Python_projects/python_parser"

path = os.path.join(parent_dir, directory)
# os.mkdir(path)


def get_content(url):
    data = requests.get(url)
    # Ստուգումներ անել ստատուս կոդ և այլն...
    soup = BeautifulSoup(data.text, 'html.parser')
    return soup

def get_html(url):
    data = requests.get(url)
    return data.text


def get_page_links(soup):
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        o = urlparse(href)
        
        if o.path:
            flag = False
            if o.netloc == SITE_NAME or not o.netloc:
                flag = True
                if len(links) > 0:
                    # այս մասում տունը մտածել այլ տարբերակ
                    for data in links:
                        if data.get('path') == o.path:
                            flag = False
            
            if flag:
                links.append({'protocol': o.scheme, 'domain': o.netloc, 'path': o.path})

    return links


def all_html(list_links):
    for i in range(len(list_links)):
        text = get_html(SITE_PROTOCOL + SITE_NAME + list_links[i][1])
        name = str(list_links[i][0]) + ".html"
        f = open(SITE_NAME + '/' + name, "w")
        f.write(text)
        f.close()


def main():
    conn = create_connection(DATABASE)

    if conn is not None:
        create_table(conn, sql_create_links_table)

        links = select_all_links(conn)
        all_html(links)


if __name__ == "__main__":
    main()