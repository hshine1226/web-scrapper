import requests
from bs4 import BeautifulSoup

LIMIT = 50

# https://kr.indeed.com/취업?q=python&limit=50&start=0
URL = f"https://kr.indeed.com/취업?q=python&limit={LIMIT}"


def get_last_page():
    result = requests.get(URL)

    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find('div', class_='pagination')
    links = pagination.find_all('a')

    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(html):
    title = html.find(class_="title").find('a')['title']

    company = html.find('span', class_='company')
    company_anchor = company.find('a')

    location = html.find(class_='location').string

    job_id = html['data-jk']

    # https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit=50&start=0&vjk=c6bf8184940d37c3

    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)

    company = company.strip()

    return {
        'title': title,
        'company': company,
        'location': location,
        'apply_link': f'{URL}&start=0&vjk={job_id}'
    }


def get_jobs(last_page):
    jobs = []

    for page in range(last_page):
        print(f'Scrapping page {page}')
        result = requests.get(f'{URL}&start={page*LIMIT}')
        soup = BeautifulSoup(result.text, "html.parser")
        # job card를 받아온 변수
        results = soup.find_all('div', class_="jobsearch-SerpJobCard")

        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs


def get_indeed_jobs():
    last_page = get_last_page()
    jobs = get_jobs(last_page)

    return jobs