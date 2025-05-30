"""
1) Executa o scraper
2) Executa o processador
"""
from src.linkedin_scraper import main as run_scraper
from src.process_jobs import main as run_processor

def main():
    print("Iniciando pipeline")
    run_scraper()     # coleta vagas e salva arquivo raw
    run_processor()   # cria arquivo processado
    print("Pipeline finalizado com sucesso!")

if __name__ == "__main__":
    main()
