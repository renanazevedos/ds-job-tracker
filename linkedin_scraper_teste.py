import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def coletar_job_ids(keyword, location, limit=50):
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    job_ids = []
    start = 0

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    }

    while len(job_ids) < limit:
        parametros_busca = {"keywords": keyword, "location": location, "start": start}
        tentativa = 0
        sucesso = False

        while tentativa < 5 and not sucesso:
            try:
                response = requests.get(base_url, params=parametros_busca, headers=headers, timeout=10)
                print(f"URL da requisição: {response.url}")

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    jobs_list = soup.find_all("li")
                    if not jobs_list:
                        print("Fim da busca de vagas!")
                        return job_ids[:limit]

                    for job_found in jobs_list:
                        base_card = job_found.find("div", {"class": "base-card"})
                        if base_card:
                            job_id = base_card.get("data-entity-urn", "").split(":")[-1]
                            if job_id and job_id not in job_ids:
                                job_ids.append(job_id)

                    start += 25
                    sucesso = True
                    time.sleep(1)
                else:
                    print(f"⚠️ Código {response.status_code} recebido. Tentando novamente...")
                    tentativa += 1
                    time.sleep(2 ** tentativa)

            except Exception as e:
                print(f"Erro na requisição: {e}. Tentando novamente...")
                tentativa += 1
                time.sleep(2 ** tentativa)

        if not sucesso:
            print("Falha repetida. Abortando busca.")
            break

    return job_ids[:limit]

def coletar_job_detalhes(job_id):
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    }

    tentativa = 0
    sucesso = False

    while tentativa < 5 and not sucesso:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
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
                sucesso = True
                return job_details
            else:
                print(f"⚠️ Código {response.status_code} recebido no detalhe. Tentando novamente...")
                tentativa += 1
                time.sleep(2 ** tentativa)

        except Exception as e:
            print(f"Erro ao processar vaga {job_id}: {e}. Tentando novamente...")
            tentativa += 1
            time.sleep(2 ** tentativa)

    print(f"Falha ao coletar detalhes da vaga {job_id}.")
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
