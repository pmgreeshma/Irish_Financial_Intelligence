# 🇮🇪 Irish Financial Intelligence

> **End-to-end data engineering and business intelligence project analysing Irish economic, financial and consumer indicators using Python, AWS, SQL and Power BI.**

## 📊 Project Overview

**Irish Financial Intelligence** is an end-to-end data analytics and engineering project focused on understanding relationships between monetary policy, borrowing costs, household credit, mortgage arrears, property prices, inflation, unemployment and consumer activity in Ireland.

The project brings together data from Irish and European official statistical sources, processes and validates the datasets using Python, and prepares the resulting data for analysis and visualisation.

The final outputs are designed to demonstrate a complete analytics workflow:

**Data ingestion → Data processing → Data validation → Cloud storage → SQL analysis → Business intelligence**

---

## 🎯 Project Objectives

The project aims to:

* Collect economic and financial data from official Irish and European sources
* Build reusable Python ingestion and processing pipelines
* Clean, transform and validate source datasets
* Create consistent analysis-ready datasets
* Demonstrate cloud data engineering concepts using AWS
* Query processed data using SQL/Athena
* Develop an interactive Power BI dashboard
* Explore relationships between economic conditions, household finances, housing and consumer activity
* Demonstrate an end-to-end portfolio project suitable for data engineering and analytics roles

---

## 🏗️ Architecture

```text
┌──────────────────────────────────────────────┐
│              Official Data Sources           │
│                                              │
│  Central Bank of Ireland                     │
│  Central Statistics Office                   │
│  European Central Bank                      │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
              ┌─────────────────┐
              │     Python      │
              │                 │
              │ API / File      │
              │ Ingestion       │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Data Processing │
              │ & Validation    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    AWS S3       │
              │ Cloud Storage   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    AWS Glue     │
              │ Data Catalog /  │
              │ ETL Concepts    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Amazon Athena   │
              │      SQL        │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Power BI     │
              │ Dashboard &     │
              │ Visual Analysis │
              └─────────────────┘
```

---

## 🗂️ Data Sources

The project works with datasets covering areas including:

| Dataset          | Area                       |
| ---------------- | -------------------------- |
| ECB Policy Rate  | Monetary policy            |
| Household Credit | Household borrowing        |
| Inflation        | Consumer prices            |
| Mortgage Arrears | Household financial stress |
| Mortgage Rates   | Borrowing costs            |
| Property Prices  | Irish housing market       |
| Retail Sales     | Consumer activity          |
| Unemployment     | Labour market              |

The raw source files are intentionally excluded from the public repository. The repository contains the processed datasets used for analysis.

---

## 🔄 Data Pipeline

The project uses Python scripts to ingest and process individual datasets.

Examples include:

```text
src/
├── ingest_cbi_a18.py
├── ingest_cbi_b31.py
├── ingest_cbi_mortgage_arrears.py
├── ingest_cpm20.py
├── ingest_ecb.py
├── ingest_hpm09.py
├── ingest_mum01.py
├── ingest_rsm08.py
└── upload_rsm5_to_s3.py
```

Pipeline orchestration/scripts are maintained separately:

```text
pipelines/
├── pipeline_cbi_a18.py
├── pipeline_cbi_b31.py
├── pipeline_cpm20.py
├── pipeline_ecb_policy_rate.py
├── pipeline_hpm09.py
├── pipeline_mortgage_arrears.py
├── pipeline_mum01.py
└── pipeline_rsm08.py
```

The workflow separates ingestion logic from pipeline execution, making the project easier to maintain and extend.

---

## 🧹 Data Processing & Validation

The processing workflow includes activities such as:

* Loading source data
* Standardising column structures
* Handling date fields
* Cleaning numeric values
* Managing missing values
* Validating dataset structures
* Producing analysis-ready CSV datasets
* Creating validated retail-sales outputs

Processed datasets are stored under:

```text
Data/processed/
```

---

## 📓 Exploratory Data Analysis

The project contains Jupyter notebooks for profiling individual datasets.

```text
Notebooks/
├── 01_profile_rsm08.ipynb
├── 02_profile_cpm20.ipynb
├── 03_profile_mum01.ipynb
├── 04_profile_hpm09.ipynb
├── 05_profile_cbib31.ipynb
├── 06_profile_cbia18.ipynb
├── 07_profile_cbimortgagearrears.ipynb
└── 08_profile_ecbpolicy.ipynb
```

These notebooks are used to inspect source data, understand distributions and structures, and support the data preparation process.

---

## ☁️ Cloud & SQL Components

The project incorporates AWS services as part of the data engineering architecture:

* **Amazon S3** — cloud data storage
* **AWS Glue** — data cataloguing and ETL workflow concepts
* **Amazon Athena** — serverless SQL querying

This demonstrates how locally processed datasets can form part of a cloud-based analytics architecture.

---

## 📈 Power BI Dashboard

The Power BI component brings the processed datasets together into an interactive business intelligence environment.

The dashboard is designed to help explore relationships between:

* Monetary policy
* Mortgage rates
* Household credit
* Mortgage arrears
* Property prices
* Inflation
* Unemployment
* Retail activity

### Dashboard

The Power BI project file is available in:

```text
PowerBi/
└── Irish_Financial_Intelligence.pbix
```

> **Tip:** Add screenshots of your finished dashboard here before submitting the project as a portfolio piece.

For example:

```text
docs/
└── dashboard-overview.png
```

Then embed the image:

```markdown
![Irish Financial Intelligence Dashboard](docs/dashboard-overview.png)
```

---

## 🛠️ Technology Stack

### Programming & Analysis

* Python
* Pandas
* Jupyter Notebook
* REST/API-based ingestion
* Data cleaning and validation

### Cloud

* Amazon S3
* AWS Glue
* Amazon Athena

### Business Intelligence

* Microsoft Power BI
* Data modelling
* Interactive visualisation
* Business-focused analysis

### Database & Querying

* SQL
* Amazon Athena

### Version Control

* Git
* GitHub

---

## 📁 Repository Structure

```text
Irish_Financial_Intelligence/
│
├── Data/
│   └── processed/
│       ├── ecb_policy_rate.csv
│       ├── household_credit.csv
│       ├── inflation.csv
│       ├── mortgage_arrears.csv
│       ├── mortgage_rates.csv
│       ├── property_prices.csv
│       ├── rsm08_retail_monthly.csv
│       ├── rsm08_retail_validated.csv
│       └── unemployment.csv
│
├── Notebooks/
│   ├── 01_profile_rsm08.ipynb
│   ├── 02_profile_cpm20.ipynb
│   ├── 03_profile_mum01.ipynb
│   ├── 04_profile_hpm09.ipynb
│   ├── 05_profile_cbib31.ipynb
│   ├── 06_profile_cbia18.ipynb
│   ├── 07_profile_cbimortgagearrears.ipynb
│   └── 08_profile_ecbpolicy.ipynb
│
├── PowerBi/
│   └── Irish_Financial_Intelligence.pbix
│
├── pipelines/
│   ├── pipeline_cbi_a18.py
│   ├── pipeline_cbi_b31.py
│   ├── pipeline_cpm20.py
│   ├── pipeline_ecb_policy_rate.py
│   ├── pipeline_hpm09.py
│   ├── pipeline_mortgage_arrears.py
│   ├── pipeline_mum01.py
│   └── pipeline_rsm08.py
│
├── src/
│   ├── ingest_cbi_a18.py
│   ├── ingest_cbi_b31.py
│   ├── ingest_cbi_mortgage_arrears.py
│   ├── ingest_cpm20.py
│   ├── ingest_ecb.py
│   ├── ingest_hpm09.py
│   ├── ingest_mum01.py
│   ├── ingest_rsm08.py
│   └── upload_rsm5_to_s3.py
│
├── .gitignore
└── README.md
```

---

## 🔐 Data & Security

The repository intentionally excludes:

```text
.venv/
Data/Raw/
.env
AWS credentials
private keys
```

Sensitive configuration and credentials should never be committed to source control.

The `.gitignore` file contains rules to prevent common environment files, credentials and local development artefacts from being committed.

---

## 💡 Key Skills Demonstrated

This project demonstrates practical experience with:

**Data Engineering**

* Data ingestion
* ETL/ELT concepts
* Data cleaning
* Data validation
* Pipeline development
* Cloud storage

**Data Analytics**

* Exploratory data analysis
* Time-series data
* Economic indicators
* Data quality analysis
* Cross-dataset analysis

**Cloud & SQL**

* AWS S3
* AWS Glue
* Amazon Athena
* SQL querying

**Business Intelligence**

* Power BI
* Data modelling
* Dashboard development
* Business-focused visualisation

**Software Engineering**

* Python scripting
* Modular project structure
* Git
* GitHub
* Reproducible workflows

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/pmgreeshma/Irish_Financial_Intelligence.git
cd Irish_Financial_Intelligence
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

If a `requirements.txt` file is added to the project:

```bash
pip install -r requirements.txt
```

### 4. Explore the notebooks

Open the notebooks in:

```text
Notebooks/
```

### 5. Open the Power BI dashboard

Open:

```text
PowerBi/Irish_Financial_Intelligence.pbix
```

in Microsoft Power BI Desktop.

---

## 📌 Project Status

**Current status:** Portfolio project — data ingestion, processing, notebooks, pipelines and Power BI dashboard developed.

Future improvements may include:

* Automated pipeline scheduling
* Expanded data-quality checks
* Infrastructure-as-code
* Additional economic indicators
* Automated dashboard refresh
* CI/CD integration
* Expanded documentation and data lineage

---

## 👩‍💻 Author

**PM Greeshma**

Data Engineering | Data Analytics | Business Intelligence

This project was developed as a practical demonstration of building an end-to-end data pipeline and analytics solution using Irish economic and financial data.

---

## 📄 Licence

Add an appropriate open-source licence if you intend to explicitly license the code for reuse.
