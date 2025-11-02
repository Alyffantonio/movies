#  MovieProject (Projeto Filmes)

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.1.1-success?logo=django)
![Celery](https://img.shields.io/badge/Celery-5.4.0-green?logo=celery)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)
![License](https://img.shields.io/badge/License-MIT-yellow?logo=open-source-initiative)

---

## Sumário

- [ Sobre o Projeto](#-sobre-o-projeto)
- [ Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [ Como Rodar com Docker](#-como-rodar-com-docker)
- [ Configuração Local (Sem Docker)](#️-configuração-local-sem-docker)
- [ Endpoints / Rotas Principais](#-endpoints--rotas-principais)
- [ Variáveis de Ambiente](#-variáveis-de-ambiente)
- [ Estrutura de Pastas](#-estrutura-de-pastas)
- [ Como Usar a Aplicação](#-como-usar-a-aplicação)
- [ Testes](#-testes)
- [ Autor](#-autor)
- [ Licença](#-licença)

---

##  Sobre o Projeto

**MovieProject** é uma aplicação web desenvolvida em **Django** que automatiza a coleta de informações sobre filmes.

O usuário envia uma planilha `.xlsx` com títulos de filmes, e o sistema:
- Processa o arquivo em **background (Celery + RabbitMQ)**.
- Busca dados na **API OMDb**.
- Faz **web scraping** (Rotten Tomatoes e Metacritic).
- Gera uma nova planilha consolidada com os dados e notas de cada filme.

**Status:** 🏁 Finalizado.

---

##  Tecnologias Utilizadas

| Categoria | Ferramentas |
|------------|-------------|
| **Backend** | Python 3.12, Django 5.1.1, Celery 5.4.0, Gunicorn |
| **Banco de Dados** | PostgreSQL |
| **Frontend** | TailwindCSS, JavaScript, Toastr.js |
| **Scraping & Dados** | Pandas, openpyxl, Selenium, BeautifulSoup4, Requests |
| **DevOps** | Docker, Docker Compose, RabbitMQ |
| **Testes** | Pytest, Pytest-Django |

---

##  Como Rodar com Docker

A forma mais simples de executar o projeto é utilizando o **Docker Compose**, que gerencia todos os serviços necessários.

###  Configurar Variáveis de Ambiente

1. Crie um arquivo `.env` na raiz do projeto.  
2. Preencha-o com base no modelo [aqui](#-variáveis-de-ambiente).  
3. Obtenha uma chave de API em [OMDb API](https://www.omdbapi.com/apikey.aspx).

---

### Iniciar os Containers

```bash
docker-compose up --build
```

Após os containers subirem, siga os passos abaixo para finalizar a configuração:

1. Acesse o container **django_movies** (ou o nome equivalente do seu container Django).

   * No **Docker Desktop**, vá até a aba **Containers**, clique em **django_movies** e depois em **Exec**.

2. Dentro do terminal do container, execute os seguintes comandos:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

   Isso garante que:

   * Todas as **migrações do banco de dados** sejam aplicadas corretamente.
   * Todos os **arquivos estáticos** sejam coletados e disponibilizados no ambiente Docker.

---


###  Acessar a Aplicação

A aplicação estará disponível em:  
 [http://localhost:8000](http://localhost:8000)

**Containers iniciados:**

| Serviço | Descrição |
|----------|------------|
| `web` | Aplicação Django |
| `db` | Banco de dados PostgreSQL |
| `rabbitmq` | Message Broker para o Celery |
| `celery_worker` | Worker que processa as tarefas assíncronas |

---


##  Endpoints / Rotas Principais

| Método | Rota | Descrição |
|:--------|:------|:-----------|
| `GET` | `/` | Página principal (lista relatórios gerados). |
| `GET` | `/admin/` | Painel administrativo do Django. |
| `POST` | `/api/upload/` | Envia o título e arquivo `.xlsx` para processamento. |
| `GET` | `/api/delete/<id>` | Exclui um registro e o relatório associado. |

---

##  Variáveis de Ambiente

```env
DJANGO_SECRET_KEY='django-insecure-seu-segredo-aqui'
DJANGO_DEBUG=True

POSTGRES_DB=filmes_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//
CELERY_RESULT_BACKEND='django-db'

OMDB_API_KEY=SUA_CHAVE_OMDB_AQUI

SELENIUM_HEADLESS=True
SELENIUM_DRIVER_PATH=/usr/bin/chromedriver
```

---

##  Estrutura de Pastas

```
/movie_project (root)
 ├── media/              # Arquivos de upload e relatórios gerados
 ├── movie_project/      # Configurações do projeto Django
 │    ├── settings.py    # Arquivo principal de configurações
 │    ├── urls.py        # URLs globais (ex: /admin)
 │    └── celery.py      # Configuração do App Celery
 ├── movies/             # App principal "movies"
 │    ├── controller.py   # Endpoints da API (upload, delete)
 │    ├── models.py       # Modelos (Upload, Movie, Report)
 │    ├── tasks.py        # Lógica do Celery (processamento do arquivo)
 │    ├── views.py        # Views da página principal (listar relatórios)
 │    ├── urls.py         # URLs do app (/, /api/upload, /api/delete)
 │    ├── omdb_client.py  # Cliente da OMDb API
 │    └── selenium_scraper.py # Web scrapers (Rotten Tomatoes, Metacritic)
 ├── templates/          # Templates HTML
 ├── static/             # Arquivos estáticos (JS, CSS)
 ├── .env                # Arquivo de variáveis de ambiente (local)
 ├── docker-compose.yml  # Orquestração dos containers
 ├── Dockerfile          # Definição do container da aplicação web
 ├── manage.py           # Utilitário de linha de comando do Django
 └── requirements.txt    # Dependências Python

```

---

##  Como Usar a Aplicação

1. Acesse a aplicação: [http://localhost:8000](http://localhost:8000)  
2. No formulário **"Enviar Lista de Filmes"**, preencha o campo **"Título do relatório"**.  
3. Clique em **"Escolher arquivo"** e envie uma planilha `.xlsx` ou `.csv` contendo uma coluna com os títulos dos filmes.  
4. Clique em **"Enviar e Processar"**.  
5. Uma notificação de sucesso será exibida via Toastr.  
   O processamento ocorre em **segundo plano** (Celery + RabbitMQ).  
6. A página será recarregada automaticamente após o envio.  
7. Quando concluído, o relatório aparecerá em **“Relatórios Gerados”**.  
8. Clique no ícone de ** download** para baixar o relatório  
   ou no ícone de ** lixeira** para excluí-lo.

---

##  Testes

O projeto utiliza **pytest** com integração Django.

### Executar Testes

Dentro do container `web`:
```bash
docker-compose exec web pytest
```

---

## Autor

**Alyff Antonio**  
 [alyffantonio@gmail.com](mailto:alyffantonio@gmail.com)  
 [LinkedIn](https://www.linkedin.com/in/alyff-antonio/)  
 [GitHub](https://github.com/Alyffantonio)

---

