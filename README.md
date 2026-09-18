# 🇮🇪 Irish Financial Intelligence

### Understanding how monetary policy, borrowing, households, housing and consumer activity connect across the Irish economy

Irish Financial Intelligence is an end-to-end data engineering, analytics and business intelligence project built around one central question:

> **How do changes in monetary policy and financial conditions relate to borrowing costs, household credit, mortgage stress, property prices and consumer activity in Ireland?**

Rather than analysing one economic indicator in isolation, this project brings together **eight official datasets** from the Central Statistics Office (CSO), Central Bank of Ireland (CBI) and European Central Bank (ECB).

The goal was not simply to collect eight datasets.

The goal was to build a small financial intelligence system where different parts of the Irish economy can be viewed together.

---

# 📖 The Story Behind the Project

Economic conditions rarely move through an economy as a single number.

A change in monetary policy can affect the cost of borrowing.

Changes in borrowing costs can influence household borrowing conditions.

Household borrowing conditions can matter for mortgage affordability and financial stress.

Housing conditions can influence household balance sheets and economic activity.

At the same time, inflation changes the purchasing power of households, while unemployment provides another important indicator of labour-market conditions.

Consumer spending gives another view of how households are behaving.

This led to the central idea behind this project:

```text
                 ECB MONETARY POLICY
                         │
                         ▼
                  BORROWING COSTS
                         │
                         ▼
                  HOUSEHOLD CREDIT
                         │
                         ▼
                  MORTGAGE STRESS
                         │
                         ▼
                   PROPERTY MARKET
                         │
                         ▼
                   CONSUMER ACTIVITY

          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
      INFLATION                    UNEMPLOYMENT
          │                             │
          └──────── MACROECONOMIC ──────┘
                    CONTEXT
```

This is **not presented as a claim that one variable causes another**.

Instead, the project creates an analytical framework for investigating how these indicators move over time and whether meaningful relationships, patterns or periods of financial stress can be identified.

That distinction is important.

The project is designed to ask better questions rather than manufacture causal conclusions.

---

# 🎯 Why These 8 Datasets?

The eight datasets were selected because each represents a different part of the financial and economic story.

| Dataset                       | Source                  | What it represents                | Frequency   |
| ----------------------------- | ----------------------- | --------------------------------- | ----------- |
| **RSM08 — Retail Sales**      | CSO                     | Consumer activity                 | Monthly     |
| **CPM20 — Inflation**         | CSO                     | Consumer price conditions         | Monthly     |
| **MUM01 — Unemployment**      | CSO                     | Labour-market conditions          | Monthly     |
| **HPM09 — Property Prices**   | CSO                     | Irish residential property market | Monthly     |
| **B.3.1 — Mortgage Rates**    | Central Bank of Ireland | Mortgage borrowing costs          | Quarterly   |
| **A.18 — Household Credit**   | Central Bank of Ireland | Household borrowing/credit        | Quarterly   |
| **Mortgage Arrears**          | Central Bank of Ireland | Mortgage financial stress         | Quarterly   |
| **ECB Deposit Facility Rate** | European Central Bank   | Monetary policy conditions        | Event-based |

Together, these datasets allow the project to look at Ireland from several perspectives:

### The macroeconomic environment

* Inflation
* Unemployment
* Retail activity

### The monetary environment

* ECB policy rate
* Mortgage rates

### Household financial conditions

* Household credit
* Mortgage arrears

### The housing market

* Residential property prices

The result is a connected financial dataset rather than eight unrelated charts.

---

# 🔎 What Questions Is This Project Actually Trying to Answer?

The project is built around a series of analytical questions.

### Monetary policy

* How have ECB policy rates changed over time?
* How do Irish mortgage rates move alongside the broader interest-rate environment?
* Are changes in mortgage rates visible in periods of changing household credit conditions?

### Household finances

* How has household credit changed over time?
* Do periods of changing borrowing costs coincide with changes in mortgage arrears?
* What periods show increased signs of mortgage financial stress?

### Housing

* How have Irish residential property prices changed over time?
* How do property-price trends compare with mortgage rates and household credit?
* Are major changes in the housing market occurring during different borrowing-cost environments?

### Consumer activity

* How has retail activity changed through different inflationary environments?
* What happens to consumer activity during periods of changing unemployment?
* Do periods of higher inflation coincide with noticeable changes in retail activity?

### The bigger picture

Ultimately, the project asks:

> **When monetary, household, housing and consumer indicators are viewed together, what does the combined data tell us about changing financial conditions in Ireland?**

---

# 🧩 Why Eight Datasets Instead of One?

A single economic dataset can answer a narrow question.

For example:

```text
Inflation
   ↓
"What happened to consumer prices?"
```

But financial intelligence requires more context.

Adding unemployment gives us:

```text
Inflation + Unemployment
   ↓
"What was happening to prices and the labour market?"
```

Adding retail sales gives us:

```text
Inflation + Unemployment + Retail Sales
   ↓
"What were households experiencing and how was
consumer activity changing?"
```

Then housing and credit add another layer:

```text
Property Prices
Mortgage Rates
Household Credit
Mortgage Arrears
```

Finally, the ECB policy rate provides a monetary-policy context.

The eight datasets therefore create a broader analytical picture:

```text
                         ECB POLICY
                             │
                             ▼
                      MORTGAGE RATES
                             │
                             ▼
                     HOUSEHOLD CREDIT
                             │
                             ▼
                     MORTGAGE ARREARS
                             │
                             ▼
                      HOUSING MARKET
                             │
                             ▼
                      CONSUMER ACTIVITY
                             ▲
                             │
                ┌────────────┴────────────┐
                │                         │
            INFLATION                UNEMPLOYMENT
```

Again, this represents the **analytical relationships being investigated**, not predetermined causal relationships.

---

# 🌐 The Data Was Not Delivered in One Convenient Format

One of the most important engineering lessons from this project was that official economic data does not necessarily arrive in one standard format.

The eight datasets required different ingestion approaches.

The project worked with combinations of:

```text
REST APIs
   ↓
CSV
   ↓
JSON
   ↓
XLS
   ↓
XLSX
   ↓
Event-based observations
```

This meant the challenge was not simply:

> "Download eight CSV files."

Instead, each source had to be understood before it could become part of the analytical model.

For example:

* CSO datasets could be accessed through API-based data sources.
* Central Bank datasets included API/JSON and spreadsheet-based sources.
* Some historical financial datasets were delivered through XLS/XLSX files.
* The ECB policy-rate dataset followed an event-based structure because policy rates change on specific dates rather than arriving as regular monthly observations.

This made the project much closer to a real-world data engineering problem.

---

# 🔄 From Raw Source to Analytical Dataset

The overall workflow was:

```text
Official Data Sources
        │
        ▼
Python Ingestion
        │
        ▼
Raw Source Data
        │
        ▼
Inspection & Profiling
        │
        ▼
Series Selection
        │
        ▼
Cleaning & Transformation
        │
        ▼
Validation
        │
        ▼
Processed Analytical Dataset
```

The purpose of the processing stage was not simply to make the files look cleaner.

The goal was to make them **safe and consistent enough to analyse together**.

---

# 🐍 Python Ingestion & Processing

Python was used as the main ingestion and preparation layer.

Separate ingestion scripts were created for the different sources.

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

Pipeline scripts were maintained separately:

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

This separation keeps ingestion logic and pipeline execution easier to understand and maintain.

---

# 🔬 Data Profiling and Validation

Before combining the datasets, the source data was profiled and validated.

The project checked things such as:

* row counts
* date ranges
* missing values
* duplicate dates
* numeric ranges
* selected statistical series
* frequency
* data types
* source structure
* historical coverage

Eight profiling notebooks were created:

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

This was particularly important because official datasets often contain more series and dimensions than are required for a specific analytical question.

The project therefore required identifying the appropriate series rather than blindly importing everything.

---

# 🧹 From Official Data to Analysis-Ready Data

The processed datasets were standardised into cleaner analytical tables.

The repository currently contains processed outputs such as:

```text
Data/processed/
├── ecb_policy_rate.csv
├── household_credit.csv
├── inflation.csv
├── mortgage_arrears.csv
├── mortgage_rates.csv
├── property_prices.csv
├── rsm08_retail_monthly.csv
├── rsm08_retail_validated.csv
└── unemployment.csv
```

The processing stage included tasks such as:

* standardising column names
* handling dates
* converting numeric fields
* selecting the required series
* handling missing values
* validating observations
* deriving analytical measures where appropriate
* producing consistent processed outputs

---

# 🕒 Different Frequencies Required Different Thinking

The eight datasets do not all have the same frequency.

Some are monthly:

```text
Retail Sales
Inflation
Unemployment
Property Prices
```

Others are quarterly:

```text
Mortgage Rates
Household Credit
Mortgage Arrears
```

And the ECB policy rate is event-based:

```text
Policy-rate change
       ↓
New effective rate
       ↓
Next policy-rate change
       ↓
New effective rate
```

This creates an important data-engineering problem.

A quarterly mortgage observation cannot simply be joined to a monthly observation using an exact date.

Likewise, an ECB policy rate should not be treated as though the rate changes every month.

The project therefore uses the concept of **observation availability / as-of logic** when building the combined analytical layer.

In other words:

> For each analytical month, the model should use the latest valid observation available at that point in time rather than forcing unrelated datasets to share identical dates.

This makes the combined dataset more realistic and preserves the historical timing of the information.

---

# 🔄 Keeping the Data Current

Another important part of the project was dealing with source data that continues to be updated.

The project was not built around a single static historical download.

Where official APIs or updated source files were available, the ingestion process was designed to retrieve the latest available observations and transform them into the project's standard analytical structure.

This means the project demonstrates an important real-world principle:

```text
Official Source
      ↓
Latest available data
      ↓
Ingestion
      ↓
Validation
      ↓
Processed dataset
      ↓
Cloud analytical layer
      ↓
Dashboard
```

This is better described as **current/fresh data ingestion** rather than claiming the dashboard is already real-time.

Full scheduled automation using AWS Lambda + EventBridge is deliberately kept as a future enhancement.

---

# ☁️ Moving From Local Data to AWS

Once the datasets had been ingested, cleaned and validated locally, the project moved into the cloud layer.

The architecture is:

```text
CSO / CBI / ECB
       │
       ▼
Python ingestion
       │
       ▼
Raw / processed data
       │
       ▼
AWS S3
       │
       ▼
AWS Glue Data Catalog
       │
       ▼
Amazon Athena
       │
       ▼
Analytical SQL layer
       │
       ▼
Power BI
```

---

# 🪣 Amazon S3

S3 provides the cloud storage layer for the project.

The data is organised into logical areas such as:

```text
raw/
processed/
```

This creates a simple data-lake-style structure and separates source data from analytical outputs.

---

# 🧾 AWS Glue

AWS Glue was used to catalogue the datasets and make them queryable through Athena.

A Glue database was created:

```text
irish_financial_intelligence_gdb
```

The project also involved resolving schema issues such as:

```text
date
  ↓
date

numeric fields
  ↓
double / bigint where appropriate
```

This demonstrated an important practical lesson:

> Cloud analytics is not just about uploading files. The schema needs to represent the data correctly before SQL analysis becomes reliable.

---

# 🔎 Amazon Athena

Athena provides the SQL analysis layer over the cloud data.

All eight datasets were successfully queried through Athena.

A monthly analytical foundation was also created combining:

* inflation
* unemployment
* retail sales
* property prices

The next analytical stage extends this foundation with the quarterly and event-based financial datasets using appropriate as-of logic.

---

# 📊 Power BI

Power BI provides the business intelligence layer.

The dashboard is intended to move the project from:

```text
Raw numbers
     ↓
Clean datasets
     ↓
SQL analysis
     ↓
Business questions
     ↓
Interactive visualisation
```

The current project includes the Power BI file:

```text
PowerBi/
└── Irish_Financial_Intelligence.pbix
```

Additional dashboard pages will continue to be added as the analytical model develops.

---

# 🖼️ Project Screenshots

Screenshots documenting the development process are available under:

```text
Screenshots/
```

These include examples of:

* API ingestion
* data profiling
* pipeline processing
* AWS Glue
* Athena SQL
* Athena query results
* DAX measures
* Power BI dashboard development

The screenshots are included to show not only the final dashboard but also the engineering process behind it.

---

# 🏗️ Current Architecture

```text
                    OFFICIAL DATA SOURCES
              ┌────────────────────────────┐
              │                            │
              │ CSO   Central Bank   ECB   │
              │                            │
              └─────────────┬──────────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ Python Ingestion  │
                  │                   │
                  │ API / CSV / JSON  │
                  │ XLS / XLSX        │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ Profiling &       │
                  │ Validation        │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ Processed Data    │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │     AWS S3        │
                  │  Cloud Storage    │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │    AWS Glue       │
                  │   Data Catalog    │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │  Amazon Athena    │
                  │       SQL         │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │    Power BI       │
                  │ Dashboard / BI    │
                  └───────────────────┘
```

---

# 🧠 What This Project Demonstrates

This project is intentionally broader than a Power BI dashboard.

It demonstrates:

### Data Engineering

* API ingestion
* File-based ingestion
* Data cleaning
* Data transformation
* Data validation
* Pipeline development
* Handling different source structures
* Working with different data frequencies
* Historical/as-of data alignment

### Cloud

* Amazon S3
* AWS Glue
* Amazon Athena
* Cloud-based analytical storage
* Data cataloguing

### Analytics

* Python
* Pandas
* Jupyter
* Time-series analysis
* Economic indicators
* Cross-dataset analysis
* SQL

### Business Intelligence

* Power BI
* DAX
* Data modelling
* Interactive dashboards
* Financial/economic storytelling

### Development

* VS Code
* Git
* GitHub
* Modular Python scripts
* Reproducible workflows

---

# 🚧 What Is Deliberately Not Finished Yet?

The project is intentionally being built in stages.

The current core architecture is working:

```text
Ingestion
    ✓

Cleaning
    ✓

Validation
    ✓

S3
    ✓

Glue
    ✓

Athena
    ✓

Monthly analytical foundation
    ✓

Power BI
    ✓
```

The next stage is to strengthen the combined financial model and expand the Power BI dashboard.

---

# 🔮 Future Architecture

Automation with AWS Lambda and EventBridge has been explored as a potential future enhancement.

The eventual architecture could become:

```text
             EventBridge
                  │
                  ▼
               Lambda
                  │
                  ▼
       Official APIs / Sources
                  │
                  ▼
                 S3
                  │
                  ▼
              Glue
                  │
                  ▼
              Athena
                  │
                  ▼
              Power BI
```

CloudWatch could also be introduced for monitoring and failure visibility.

However, **Lambda and EventBridge are currently paused rather than being presented as completed components**.

The priority is to make the core data model, analytical layer and dashboard robust before adding automation.

---

# 📌 The Financial Intelligence Question

At its core, this project is asking:

> **How do changes in monetary policy and financial conditions relate to borrowing costs, household credit, mortgage stress, property prices and consumer activity in Ireland?**

The eight datasets provide different pieces of the answer.

```text
ECB Policy Rate
       │
       ▼
Mortgage Rates
       │
       ▼
Household Credit
       │
       ▼
Mortgage Arrears
       │
       ▼
Property Prices
       │
       ▼
Retail Activity

Inflation ───────────────┐
                         ├── Macroeconomic Context
Unemployment ────────────┘
```

The purpose is not to say:

> "Interest rates caused X."

Instead, the purpose is to investigate:

> **"When these indicators are viewed together, what patterns and relationships appear in Ireland's financial and economic data?"**

That is the central idea behind Irish Financial Intelligence.

---

# 📁 Repository Structure

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
├── Screenshots/
│   ├── aws athena query results.png
│   ├── aws athena sql query 1.png
│   ├── aws glue snippet.png
│   ├── dashboard 1 overview.png
│   ├── dax query latest inflation and list of measures.png
│   ├── ingestion of rsm08 API data.png
│   ├── pipeline the rsm.png
│   └── profiling rsm.png
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

# 🔐 Data & Security

Raw source files and local development artefacts are intentionally excluded from the public repository.

The `.gitignore` protects items such as:

```text
.venv/
Data/Raw/
.env
.env.*
*.pem
*.key
```

AWS credentials and secrets should never be committed to GitHub.

The public repository focuses on the reproducible processing logic, processed analytical datasets, notebooks, pipelines, dashboard and documentation.

---

# 🚀 Project Status

### Core data engineering

* [x] Identify eight official datasets
* [x] Build ingestion scripts
* [x] Process different source formats
* [x] Profile datasets
* [x] Validate datasets
* [x] Produce processed analytical files
* [x] Upload data to S3
* [x] Create Glue database and tables
* [x] Resolve schema issues
* [x] Query datasets with Athena
* [x] Build monthly analytical foundation

### Analytics & BI

* [x] Build Power BI model/dashboard
* [x] Create DAX measures
* [x] Document analytical workflow
* [ ] Complete additional dashboard pages
* [ ] Extend master financial view
* [ ] Perform deeper cross-dataset analysis

### Future engineering improvements

* [ ] Lambda-based ingestion
* [ ] EventBridge scheduling
* [ ] CloudWatch monitoring
* [ ] Automated refresh
* [ ] Additional data-quality checks
* [ ] Infrastructure as code

---

# 👩‍💻 Author

**PM Greeshma**

Data Engineering | Data Analytics | Business Intelligence

This project was built as a practical demonstration of taking heterogeneous official economic and financial data, turning it into validated analytical datasets, moving it through a cloud data architecture, querying it with SQL, and communicating the resulting financial story through Power BI.

