\# Job Market Analytics Platform



A full-stack platform that collects real job market data, analyzes hiring trends, predicts salaries with machine learning, and answers natural-language questions through an LLM-powered assistant.



\*\*Live demo:\*\* \_(add link after deployment)\_



\## Features



\- \*\*Real job market data\*\* — pulled from the Adzuna API across India, US, UK, and Australia, plus realistic synthetic data for volume

\- \*\*Interactive analytics dashboard\*\* — top in-demand skills and top hiring locations, visualized with live charts

\- \*\*ML salary prediction\*\* — a trained RandomForest regressor predicts salary from title, location, skills, and years of experience

\- \*\*ML job category classification\*\* — a TF-IDF + Logistic Regression model classifies postings into roles (Data Science, Backend, Frontend, DevOps, Product)

\- \*\*AI chatbot\*\* — ask natural-language questions about the job market, answered from live database statistics using Groq's Llama 3.3

\- \*\*AI career report generator\*\* — a multi-step LLM reasoning pipeline (summarize → analyze → write) produces a structured markdown career report per category, downloadable as a file

\- \*\*Skills gap checker\*\* — compares a user's skills against the most in-demand skills for a chosen category



\## Tech Stack



\*\*Backend:\*\* Python, FastAPI, SQLAlchemy, PostgreSQL (Neon)

\*\*Frontend:\*\* React, Vite, Recharts, Axios

\*\*ML:\*\* scikit-learn (RandomForestRegressor, TF-IDF + LogisticRegression)

\*\*LLM:\*\* Groq API (Llama 3.3 70B)

\*\*Data collection:\*\* Adzuna API, custom skill-extraction and currency-normalization pipeline



\## Architecture



job-market-analytics/

├── backend/

│ ├── app/

│ │ ├── main.py # FastAPI app entrypoint

│ │ ├── models.py, schemas.py # DB models \& API schemas

│ │ ├── routers/ # jobs, analytics, chatbot endpoints

│ │ └── services/

│ │ ├── data\_collection/ # Adzuna API client, scraper

│ │ ├── ml/ # training, prediction, feature engineering

│ │ └── llm/ # chatbot + career report generation

│ ├── seed\_data.py # generates realistic synthetic postings

│ ├── fetch\_real\_data.py # pulls real postings from Adzuna

│ └── normalize\_currency.py # converts multi-country salaries to USD

└── frontend/

└── src/

├── components/ # dashboard, charts, chatbot, report generator

└── api.js # backend API client





\## Key Engineering Decisions



\- \*\*Multi-currency normalization\*\*: Adzuna returns salaries in local currency (INR, GBP, AUD, USD). All salaries are normalized to USD before training or display, so comparisons across countries are meaningful.

\- \*\*Realistic model evaluation\*\*: skill overlap was deliberately introduced across categories during data generation so category classification is a genuine ML problem (\~76-93% accuracy) rather than trivial keyword matching (which produced a meaningless 100%).

\- \*\*years\_experience as a real feature\*\*: seniority is decoupled from job title text and stored as a numeric field, so the salary model responds correctly to experience level regardless of how a title is phrased.

\- \*\*Multi-step LLM reasoning\*\*: the career report generator uses three sequential LLM calls (data summarizer → market analyst → report writer) rather than one prompt, producing more structured, grounded output.

\- \*\*Resilient DB connections\*\*: configured with `pool\_pre\_ping` and `pool\_recycle` to handle Neon's serverless auto-suspend behavior gracefully.



\## Local Setup



\### Backend

```bash

cd backend

pip install -r requirements.txt

cp .env.example .env   # fill in your DATABASE\_URL, ADZUNA\_APP\_ID, ADZUNA\_APP\_KEY, GROQ\_API\_KEY

python -m app.services.ml.train

python -m uvicorn app.main:app --reload

```



\### Frontend

```bash

cd frontend

npm install

npm run dev

```



\## Environment Variables



| Variable | Description |

|---|---|

| `DATABASE\_URL` | PostgreSQL connection string (e.g. from \[Neon](https://neon.tech), free tier) |

| `ADZUNA\_APP\_ID` / `ADZUNA\_APP\_KEY` | Free API credentials from \[Adzuna](https://developer.adzuna.com/) |

| `GROQ\_API\_KEY` | Free API key from \[Groq](https://console.groq.com/) |



\## Model Performance



| Model | Metric | Score |

|---|---|---|

| Salary prediction | R² (holdout) | \~0.74 |

| Category classification | Accuracy (holdout) | \~76-93% (varies by data mix) |



\## Author



Built by \[Your Name] as a full-stack ML/LLM portfolio project.

