AutoCheck Car Listings - Data Extraction and Analytics
=====================================================

Project Overview
-------------------
The Car Crawler project aims to design and implement a web scraping application that extracts comprehensive car listing information from https://www.jiji.ng, a popular online marketplace in Nigeria.

Objectives
------------
  - Develop a scalable web crawler using Beautiful Soup and Pandas to extract car listing data
  - Implement data cleaning, formatting, and storage in an MSSQL database
  - Ensure data freshness through daily incremental ETL runs
  - Monitor and log application performance using Prometheus
  - Provide a structured dataset for future data analytics and visualization
    
Project Scope
----------------
  - Data Extraction
  - 50-100 pages (expandable)
  - Data elements:
      + Manufacturer
      + Model
      + Year
      + Color
      + Transmission type
      + Condition (used/foreign used)
      + Location (area, state)
      + Price
  - Technical Requirements
      + Data storage: MSSQL database
      + ETL schedule: Daily incremental runs
   
Deliverables
--------------
  - A fully functional web crawler application
  - A well-structured MSSQL database containing extracted car listing data
  - A Prometheus monitoring dashboard
  - Documentation outlining project architecture, usage, and maintenance
    
Benefits
----------
  - Provides valuable insights into Nigerian car market trends
  - Enables data-driven decision-making for car buyers and sellers
  - Facilitates market research and analysis

Technologies Used
--------------------
+ Beautiful Soup
+ Pandas
+ SQL Alchemy
+ MSSQL
+ Prometheus
