import urllib.parse
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from playwright_stealth import Stealth

def get_dynamic_job_links(skills, level, job_type="Full-time"):
    top_skills = skills[:5] if skills else ["Developer"]
    query_skills = [s.lower().replace(" ", "-").replace("/", "-") for s in top_skills[:2]]
    query = "-".join(query_skills)
    
    base_path = "internships" if job_type == "Internship" else "jobs"
    scrape_url = f"https://internshala.com/{base_path}/keywords-{query}/"
    
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 720}
        )
        page = context.new_page()
        Stealth().apply_stealth_sync(page)
        
        try:
            print(f"Scraping {scrape_url}")
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
                desc = desc_elem.text.strip()[:150] + "..." if desc_elem else f"Matched {job_type} opportunity for your skills."
                
                results.append({
                    "name": "Internshala",
                    "title": title,
                    "company": company,
                    "url": link,
                    "description": desc,
                    "source": "Internshala"
                })
        except Exception as e:
            print(f"Scraping failed: {e}")
        browser.close()
        
    return results

if __name__ == "__main__":
    jobs = get_dynamic_job_links(["Python", "Django", "React", "AWS", "Docker"], "Experienced")
    for job in jobs:
        print(f"{job['title']} at {job['company']} - {job['url']}")
