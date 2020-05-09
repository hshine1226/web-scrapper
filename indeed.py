import requests
from bs4 import BeautifulSoup

INDEED_URL = "https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit=50&radius=25"

def extract_indeed_pages():
    result = requests.get(INDEED_URL)
    soup = BeautifulSoup(result.text, "html.parser")


    pagination = soup.find('div', class_= 'pagination')


    links = pagination.find_all('a')

    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


