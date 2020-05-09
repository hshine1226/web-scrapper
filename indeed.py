import requests
from bs4 import BeautifulSoup

LIMIT = 50

# https://kr.indeed.com/취업?q=python&limit=50&start=0
URL = f"https://kr.indeed.com/취업?q=python&limit={LIMIT}"


def extract_indeed_pages():
    result = requests.get(URL)

    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find('div', class_='pagination')
    links = pagination.find_all('a')

    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_indeed_jobs(last_page):
    jobs = []
    # for page in range(last_page):
    result = requests.get(f'{URL}&start={0*LIMIT}')
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all('div', class_="jobsearch-SerpJobCard")

    for result in results:
        title = result.find(class_="title").find('a')['title']
        company = result.find('span', class_='company')
        company_anchor = company.find('a')
        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)

        print(title, company, '\n')

    return jobs
