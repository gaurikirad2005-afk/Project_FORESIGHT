# PROJECT FORESIGHT

### Retail Sales Analytics Dashboard

An end-to-end retail analytics project that transforms retail transaction data into an interactive Streamlit dashboard.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-purple)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-orange)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-orange)
![License](https://img.shields.io/badge/License-MIT-green)

**[Live Demo](https://project-foresight-uk4v.onrender.com)** · **[GitHub Repository](https://github.com/gaurikirad2005-afk/Project_FORESIGHT)**

---

## Live Demo

**https://project-foresight-uk4v.onrender.com**

> ⚠️ The application is hosted on Render's free tier. If the app has been inactive, the first load may take some time while the service starts.

---

## What this is

**Project FORESIGHT** analyzes retail transaction data through a series of Jupyter notebooks covering:

- Data cleaning
- Exploratory data analysis
- Feature engineering
- Customer segmentation
- Demand forecasting
- Inventory recommendation
- Dashboard preparation

The processed outputs are then connected to a **Streamlit executive dashboard** for interactive analysis of retail sales, revenue, products, customers, countries, analytics, and business insights.

---

## Repository Structure

```text
Project_FORESIGHT/
│
├── app/
│   └── app.py                         # Streamlit dashboard entry point
│
├── data/
│   ├── raw/
│   │   └── online_retail_II.xlsx      # Raw retail dataset
│   │
│   └── processed/
│       ├── cleaned_step1.csv
│       ├── feature_engineered.csv
│       ├── customer_segments.csv
│       ├── inventory_recommendation.csv
│       ├── dashboard_monthly.csv
│       ├── dashboard_customers.csv
│       ├── dashboard_products.csv
│       └── dashboard_country.csv
│
├── models/                             # Model-related directory
│
├── notebooks/
│   ├── 01_Data_Cleaning.ipynb
│   ├── 02_EDA.ipynb
│   ├── 03_Feature_Engineering.ipynb
│   ├── 04_Customer_Segmentation.ipynb
│   ├── 05_Demand_Forecasting.ipynb
│   ├── 06_Inventory_Recommendation.ipynb
│   └── 07_Dashboard_Preparation.ipynb
│
├── reports/                            # Generated reports
│
├── screenshots/
│   ├── dashboard.png
│   ├── analytics.png
│   ├── insights.png
│   └── map.png
│
├── src/                                # Source-code directory
│
├── requirements.txt
├── .gitignore
└── README.md
