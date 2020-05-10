import requests
from bs4 import BeautifulSoup

# https://stackoverflow.com/jobs?q=python
# https://stackoverflow.com/jobs?q=python&pg=2
URL = f"https://stackoverflow.com/jobs?q=python"


def get_last_page():
    result = requests.get(URL)

    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find('div', class_='s-pagination')
    links = pagination.find_all('a', class_='s-pagination--item')
    span = []
    for link in links:
        span.append(link.find('span').string)
    pages = span[:-2]
    max_page = int(pages[-1])
    return max_page


def extract_job(html):
    title = html.find('a', class_='s-link')['title']
    company, location = html.find('h3').find_all('span')

    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = int(html['data-jobid'])

    # https://stackoverflow.com/jobs?id=377499&pg=2&q=python
    # https://stackoverflow.com/jobs/167366

    return {
        'title': title,
        'company': company,
        'location': location,
        'apply_link': f'https://stackoverflow.com/jobs/{job_id}'
    }


def get_jobs(last_page):
    jobs = []

    for page in range(last_page):
        print(f"Scrapping SO Page: {page}")
        result = requests.get(f'{URL}&pg={page+1}')
        soup = BeautifulSoup(result.text, "html.parser")
        # # job card를 받아온 변수
        results = soup.find_all('div', class_='-job')
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_so_jobs():
    last_page = get_last_page()
    jobs = get_jobs(last_page)

    return jobs
