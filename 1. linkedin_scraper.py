import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

def coletar_job_ids(keyword, location, limit=50):
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    job_ids = []
    start = 0

    while len(job_ids) < limit:
        parametros_busca = {"keywords":keyword, "location":location, "start": start}
        try:
            response = requests.get(base_url, params=parametros_busca, timeout=10)
            print(f"URL da requisição: {response.url}")

            soup = BeautifulSoup(response.text, "html.parser")
            jobs_list = soup.find_all("li")
            if not jobs_list:
                print("Fim da busca de vagas!")
                break

            for job_found in jobs_list:
                job_id = job_found.find("div", {"class": "base-card"}).get("data-entity-urn", "").split(":")[-1]
                
                if job_id:
                    job_ids.append(job_id)
            start += 25  # Avança para a próxima página
            time.sleep(1)  # Evita bloqueio

        except Exception as e:
            print(f"Erro na requisição: {e}")
            break

    return job_ids[:limit]


def coletar_job_detalhes(job_id):
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")


        job_details = {
            "title": soup.find("h2", class_="top-card-layout__title").get_text(strip=True) 
                    if soup.find("h2", class_="top-card-layout__title") else "N/A",
            "company": soup.find("a", class_="topcard__org-name-link").get_text(strip=True) 
                    if soup.find("a", class_="topcard__org-name-link") else "N/A",
            "location": soup.find("span", class_="topcard__flavor--bullet").get_text(strip=True) 
                    if soup.find("span", class_="topcard__flavor--bullet") else "N/A",
            "posted": soup.find("span", class_="posted-time-ago__text").get_text(strip=True) 
                    if soup.find("span", class_="posted-time-ago__text") else "N/A",
            "description": soup.find("div", class_="description__text").get_text(strip=True)
                    if soup.find("div", class_="description__text") else "N/A",
            "applicants": soup.find("span", class_="num-applicants__figure").get_text(strip=True) 
                    if soup.find("span", class_="num-applicants__figure") else "N/A",
            "work_mode": "Remote" if "remote" in soup.get_text().lower() else "On-site/Hybrid",
            "link": url
        }
        return job_details

    except Exception as e:
        print(f"Erro ao processar vaga {job_id}: {e}")
        return None

def main():
    print("Iniciando scraping...")
    job_ids = coletar_job_ids("Cientista de Dados", "São Paulo", limit=50)

    jobs = []
    for i, job_id in enumerate(job_ids):
        job = coletar_job_detalhes(job_id)
        if job:
            jobs.append(job)
        print(f"{i+1}/{len(job_ids)} vagas coletadas.")
        time.sleep(1)

    df = pd.DataFrame(jobs)
    df.to_csv("linkedin_datascience_jobs.csv", index=False, encoding="utf-8-sig")
    print("Arquivo salvo como linkedin_datascience_jobs.csv")

if __name__ == "__main__":
    main()
