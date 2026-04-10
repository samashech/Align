import urllib.parse
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from playwright_stealth import Stealth
import time

def get_dynamic_job_links(skills, level, job_type="Full-time"):
    """
    Uses Playwright stealth and BeautifulSoup to scrape actual specific latest job postings
    based on the top 5 skills. Returns the top 10 matched job listings.
    """
    # The system matches the current user's top 5 skills
    top_skills = skills[:5] if skills else ["Developer"]
    
    # We construct a search query using the top 2-3 skills to avoid zero results
    query_skills = top_skills[:3]
    query = " ".join(query_skills)
    encoded_query = urllib.parse.quote(query)
    
    results = []
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            Stealth().apply_stealth_sync(page)
            
            # Scrape WeWorkRemotely for remote jobs
            # WWR allows querying without aggressive blocking
            scrape_url = f"https://weworkremotely.com/remote-jobs/search?term={encoded_query}"
            print(f"Scraping {scrape_url}")
            page.goto(scrape_url, timeout=30000, wait_until="domcontentloaded")
            time.sleep(2) 
            html = page.content()
            soup = BeautifulSoup(html, "html.parser")
            
            # WWR job cards
            job_cards = soup.find_all("li", class_="feature")
            for card in job_cards:
                if len(results) >= 10:
                    break
                
                title_elem = card.find("span", class_="title")
                company_elem = card.find("span", class_="company")
                link_elem = card.find("a")
                
                if title_elem and link_elem:
                    # Make sure it's an actual job link
                    href = link_elem.get("href", "")
                    if "remote-jobs" in href:
                        title = title_elem.text.strip()
                        company = company_elem.text.strip() if company_elem else "Unknown Company"
                        link = "https://weworkremotely.com" + href
                        
                        results.append({
                            "name": "WeWorkRemotely",
                            "title": title,
                            "company": company,
                            "url": link,
                            "description": f"Actual {job_type} posting scraped for your top skills: {', '.join(top_skills)}."
                        })

            # If we don't have 10, try another query with broader terms
            if len(results) < 10 and len(top_skills) > 0:
                broad_query = urllib.parse.quote(top_skills[0])
                broad_url = f"https://weworkremotely.com/remote-jobs/search?term={broad_query}"
                print(f"Scraping broader {broad_url}")
                page.goto(broad_url, timeout=30000, wait_until="domcontentloaded")
                time.sleep(2)
                html2 = page.content()
                soup2 = BeautifulSoup(html2, "html.parser")
                job_cards2 = soup2.find_all("li", class_="feature")
                for card in job_cards2:
                    if len(results) >= 10:
                        break
                    title_elem = card.find("span", class_="title")
                    company_elem = card.find("span", class_="company")
                    link_elem = card.find("a")
                    if title_elem and link_elem:
                        href = link_elem.get("href", "")
                        # avoid duplicates
                        if "remote-jobs" in href and not any(r["url"].endswith(href) for r in results):
                            title = title_elem.text.strip()
                            company = company_elem.text.strip() if company_elem else "Unknown Company"
                            link = "https://weworkremotely.com" + href
                            results.append({
                                "name": "WeWorkRemotely",
                                "title": title,
                                "company": company,
                                "url": link,
                                "description": f"Broad {job_type} posting scraped for: {top_skills[0]}."
                            })

            browser.close()
    except Exception as e:
        print(f"Playwright scraping failed: {e}")
        
    # If stealth scraping totally failed, return a fallback so UI still works
    if not results:
        results.append({
            "name": "Fallback Scraper",
            "title": f"Senior {top_skills[0] if top_skills else 'Software'} Developer",
            "company": "Tech Innovations Inc.",
            "url": "#",
            "description": f"Fallback result for {job_type} role matching skills: {', '.join(top_skills)}."
        })
        
    return results

if __name__ == "__main__":
    jobs = get_dynamic_job_links(["Python", "Django", "React", "AWS", "Docker", "SQL", "Git"], "Experienced")
    for job in jobs:
        print(f"{job['title']} at {job['company']}")
