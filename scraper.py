def get_dynamic_job_links(skills, level):
    query = f"{'Junior' if level == 'Fresher' else ''} {skills[0]}".strip()
    # List of top sites
    sites = [
        {"name": "Indeed", "url": f"https://in.indeed.com/jobs?q={query}"},
        {"name": "LinkedIn", "url": f"https://www.linkedin.com/jobs/search/?keywords={query}"},
        {"name": "Glassdoor", "url": f"https://www.glassdoor.co.in/Job/index.htm?keyword={query}"},
        {"name": "Wellfound", "url": f"https://wellfound.com/role/l/{query.replace(' ', '-')}"},
        {"name": "Naukri", "url": f"https://www.naukri.com/{query.replace(' ', '-')}-jobs"}
    ]
    return sites
