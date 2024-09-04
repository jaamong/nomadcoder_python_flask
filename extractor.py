from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def scrape_job(keyword):

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    target_url = f"https://www.wanted.co.kr/search?query={keyword}&tab=position"

    p = sync_playwright().start()
    browser = p.chromium.launch(headless=True)  # initialize the browser
    page = browser.new_page(extra_http_headers={  # create new tap(page)
        "User-Agent": user_agent
    })

    page.goto(target_url)
    content = page.content()  # get the full html page

    p.stop()

    soup = BeautifulSoup(content, "html.parser")
    jobs = soup.find_all(
        "div", class_="JobCard_container__REty8 JobCard_container--variant-card__gaJS_")

    jobs_db = []
    for job in jobs:  # job : each one of jobs(soup element)
        link = f"https://www.wanted.co.kr{job.find('a')['href']}"
        title = job.find("strong", class_="JobCard_title__HBpZf").text
        company_name = job.find(
            "span", class_="JobCard_companyName__N1YrF").text
        reward = job.find("span", class_="JobCard_reward__cNlG5").text

        job = {
            "title": title,
            "company": company_name,
            "reward": reward,
            "link": link,
        }
        jobs_db.append(job)

    return jobs_db
