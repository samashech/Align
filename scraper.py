import urllib.parse
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from playwright_stealth import stealth
import time
import random

# Top 10 Legitimate Sites Categorized
LEGIT_SITES = {
    "Full-time": [
        {"name": "LinkedIn", "base": "https://www.linkedin.com/jobs/search/?keywords={query}"},
        {"name": "Indeed", "base": "https://in.indeed.com/jobs?q={query}"},
        {"name": "Glassdoor", "base": "https://www.glassdoor.com/Job/jobs.htm?sc.keyword={query}"},
        {"name": "Wellfound", "base": "https://wellfound.com/role/l/{dash_query}"},
        {"name": "Naukri", "base": "https://www.naukri.com/{dash_query}-jobs"},
        {"name": "ZipRecruiter", "base": "https://www.ziprecruiter.in/jobs/search?q={query}"},
        {"name": "Monster", "base": "https://www.foundit.in/srp/results?query={query}"},
        {"name": "SimplyHired", "base": "https://www.simplyhired.co.in/search?q={query}"},
        {"name": "Dice", "base": "https://www.dice.com/jobs?q={query}"},
        {"name": "CareerBuilder", "base": "https://www.careerbuilder.com/jobs?keywords={query}"}
    ],
    "Part-time": [
        {"name": "LinkedIn Part-Time", "base": "https://www.linkedin.com/jobs/search/?keywords={query}%20Part%20Time"},
        {"name": "Indeed Part-Time", "base": "https://in.indeed.com/jobs?q={query}+part+time"},
        {"name": "FlexJobs", "base": "https://www.flexjobs.com/search?search={query}&schedule=Part-Time"},
        {"name": "Glassdoor Part-Time", "base": "https://www.glassdoor.com/Job/jobs.htm?sc.keyword={query}%20part%20time"},
        {"name": "Snagajob", "base": "https://www.snagajob.com/search?q={query}"},
        {"name": "SimplyHired", "base": "https://www.simplyhired.co.in/search?q={query}+part+time"},
        {"name": "ZipRecruiter", "base": "https://www.ziprecruiter.in/jobs/search?q={query}+part+time"},
        {"name": "Wellfound", "base": "https://wellfound.com/role/l/{dash_query}-part-time"},
        {"name": "Upwork (Hourly)", "base": "https://www.upwork.com/nx/search/jobs/?q={query}"},
        {"name": "Fiverr", "base": "https://www.fiverr.com/search/gigs?query={query}"}
    ],
    "Internship": [
        {"name": "Internshala", "base": "https://internshala.com/internships/keywords-{dash_query}/"},
        {"name": "LinkedIn Internships", "base": "https://www.linkedin.com/jobs/search/?keywords={query}%20Internship"},
        {"name": "WayUp", "base": "https://www.wayup.com/s/internships/{dash_query}/"},
        {"name": "Glassdoor Interns", "base": "https://www.glassdoor.com/Job/jobs.htm?sc.keyword={query}%20internship"},
        {"name": "Indeed Interns", "base": "https://in.indeed.com/jobs?q={query}+internship"},
        {"name": "Chegg Internships", "base": "https://www.internships.com/search?q={query}"},
        {"name": "Handshake", "base": "https://app.joinhandshake.com/stu/postings?query={query}"},
        {"name": "LetsIntern", "base": "https://www.letsintern.com/internships?q={query}"},
        {"name": "Wellfound Interns", "base": "https://wellfound.com/role/l/{dash_query}-internship"},
        {"name": "Naukri Interns", "base": "https://www.naukri.com/{dash_query}-internship-jobs"}
    ],
    "Freelance": [
        {"name": "Upwork", "base": "https://www.upwork.com/nx/search/jobs/?q={query}"},
        {"name": "Freelancer", "base": "https://www.freelancer.com/jobs/?keyword={query}"},
        {"name": "Fiverr", "base": "https://www.fiverr.com/search/gigs?query={query}"},
        {"name": "Toptal", "base": "https://www.toptal.com/talent/apply"},
        {"name": "Guru", "base": "https://www.guru.com/d/jobs/q/{query}/"},
        {"name": "PeoplePerHour", "base": "https://www.peopleperhour.com/freelance-jobs?q={query}"},
        {"name": "FlexJobs", "base": "https://www.flexjobs.com/search?search={query}&jobType=Freelance"},
        {"name": "SolidGigs", "base": "https://solidgigs.com/"},
        {"name": "WeWorkRemotely", "base": "https://weworkremotely.com/remote-jobs/search?term={query}"},
        {"name": "Hubstaff Talent", "base": "https://talent.hubstaff.com/search/jobs?search={query}"}
    ]
    }
from playwright_stealth import Stealth

def get_dynamic_job_links(skills, level, job_type="Full-time"):
    """
    Uses Playwright stealth and BeautifulSoup to dynamically scrape actual job postings.
    Falls back to generating search URLs if scraping fails.
    """
    top_skills = skills[:5] if skills else ["Developer"]
    query_skills = [s.lower().replace(" ", "-").replace("/", "-") for s in top_skills[:2]]
    query = "-".join(query_skills)

    results = []

    # Try Dynamic Scraping First (Internshala handles both jobs and internships)
    try:
        base_path = "internships" if job_type == "Internship" else "jobs"
        scrape_url = f"https://internshala.com/{base_path}/keywords-{query}/"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={'width': 1280, 'height': 720}
            )
            page = context.new_page()
            Stealth().apply_stealth_sync(page)

            page.goto(scrape_url, wait_until="domcontentloaded", timeout=20000)
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            cards = soup.find_all("div", class_="internship_meta")

            for card in cards:
                if len(results) >= 10:
                    break

                title_a = card.find("a", class_="job-title-href")
                if not title_a:
                    continue
                title = title_a.text.strip()
                link = "https://internshala.com" + title_a.get("href", "")

                company_elem = card.find("p", class_="company-name")
                company = company_elem.text.strip() if company_elem else "Unknown Company"

                desc_elem = card.find("div", class_="text")
                desc = desc_elem.text.strip()[:150] + "..." if desc_elem else f"Matched {job_type} opportunity for your skills: {', '.join(top_skills)}."

                results.append({
                    "name": "Internshala",
                    "title": title,
                    "company": company,
                    "url": link,
                    "description": desc,
                    "source": "Internshala"
                })
            browser.close()
    except Exception as e:
        print(f"Scraping failed: {e}")

    # Fallback to static URLs if scraping didn't yield enough results
    if len(results) < 5:
        fallback_query = " ".join(top_skills)
        encoded_query = urllib.parse.quote(fallback_query)
        dash_query = fallback_query.replace(' ', '-').replace('/', '-')

        category_sites = LEGIT_SITES.get(job_type, LEGIT_SITES["Full-time"])

        for site in category_sites:
            if len(results) >= 10:
                break
            url = site["base"].format(query=encoded_query, dash_query=dash_query)
            # Avoid adding the same company if it was somehow scraped
            if not any(r["name"] == site["name"] for r in results):
                results.append({
                    "name": site["name"],
                    "title": f"{job_type} Role - {site['name']}",
                    "company": "Various Companies",
                    "url": url,
                    "description": f"Matched {job_type} opportunities for your top 5 skills: {', '.join(top_skills)}."
                })

    return results
