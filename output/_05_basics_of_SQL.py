#!/usr/bin/env python
# coding: utf-8

# # Basics of SQL
# 
# Structured Query Language (SQL) is a domain-specific programming language designed for managing and querying data in relational database systems. Relational databases organize data into tables, which consist of rows (records) and columns (attributes). SQL is the standard language used for interacting with these databases, and it plays a fundamental role in finance and data analysis, particularly when working with large datasets.
# 
# This lesson provides a brief introduction to SQL concepts that are helpful for understanding the scripts used in the homework, such as `pull_CRSP_stock.py`, `pull_CRSP_Compustat.py`, and `pull_SP500_constituents.py`. The focus will be on the basic SQL commands needed to query and extract data from databases such as the CRSP and Compustat datasets available through the WRDS platform.
# 
# 
# ## Introduction 
# 
# ### What is SQL?
# 
# SQL is used to perform the following operations on relational databases:
# - **Querying data**: Extract specific information using the `SELECT` statement.
# - **Filtering data**: Use `WHERE` conditions to retrieve only relevant records.
# - **Joining tables**: Combine data from multiple tables using `JOIN`.
# - **Sorting and aggregating data**: Use functions such as `ORDER BY`, `GROUP BY`, and aggregate functions (e.g., `SUM`, `AVG`).
# 
# Relational databases are ubiquitous in the finance industry due to their ability to handle structured data efficiently. SQL is widely used because of its simplicity, flexibility, and ability to process complex queries across large datasets.
# 
# ### Why is SQL so useful?
# 
# SQL is incredibly useful because it provides a powerful, standardized language for efficiently querying, managing, and analyzing structured data stored in relational databases. It allows users to retrieve specific information, filter records, join tables, and perform complex aggregations with minimal effort. 
# 
# ### Why are relational databases so popular?
# 
# Relational databases are popular because they organize data into tables with defined relationships, ensuring consistency, integrity, and scalability. They also support features like indexing for fast access, concurrency for multi-user operations, and robust security mechanisms. These capabilities make relational databases and SQL indispensable for industries that rely on large, structured datasets, such as finance, healthcare, and e-commerce.
# 
# Furthermore, large companies use databases because they efficiently handle large-scale, complex, and sensitive data. Databases enable fast querying, filtering, and joining of data, which is critical for managing and analyzing structured datasets. They ensure data integrity through constraints and transactions, support multiple concurrent users, and provide robust security features like encryption and access control. Databases also automate backups, ensure data redundancy, and comply with regulatory requirements through logging and retention policies. Unlike plain files, databases are scalable, reliable, and integrate seamlessly with analytics tools, making them essential for modern enterprises.
# 
# As an example, the acronym "ACID" is commonly used to describe the properties of a database system. An "ACID database" refers to a database that adheres to the ACID properties, which stand for "Atomicity, Consistency, Isolation, and Durability" - essentially meaning that any transaction within the database will be completed fully and reliably, ensuring data integrity even in the face of errors or system failures; it's a standard for ensuring data consistency in database operations, particularly important for applications requiring high reliability like financial systems. 

# ## Basic SQL Syntax
# 
# To understand the SQL queries used in the provided scripts, it is important to review the following basic concepts.

# In[ ]:


import pandas as pd
import wrds

from settings import config
WRDS_USERNAME = config("WRDS_USERNAME")

db = wrds.Connection(wrds_username=WRDS_USERNAME)


# ### 1. **Selecting Data**
# The `SELECT` statement retrieves specific columns from a table.
# 
# ```sql
# SELECT column1, column2
# FROM table_name;
# ```
# 
# Example:
# 
# This query retrieves the `date`, `permno` (unique stock identifier), and `ret` (return) columns from the `crsp.msf` table. Note that the `LIMIT` clause is used to limit the number of rows returned to 10.

# In[ ]:


db.raw_sql("""
SELECT date, permno, ret
FROM crsp.msf
LIMIT 10;
;
""")


# ### 2. **Filtering Data**
# The `WHERE` clause is used to filter rows that meet specific conditions.
# 
# ```sql
# SELECT column1, column2
# FROM table_name
# WHERE condition;
# ```
# 
# Example:
# 
# This query retrieves data for stocks within the specified date range.
# 

# In[ ]:


db.raw_sql("""
SELECT date, permno, ret
FROM crsp.msf
WHERE date BETWEEN '2023-01-01' AND '2023-12-31'
LIMIT 10;
""")


# ### 3. **Joining Tables**
# The `JOIN` clause combines data from multiple tables based on a common column.
# 
# ```sql
# SELECT t1.column1, t2.column2
# FROM table1 AS t1
# JOIN table2 AS t2
# ON t1.common_column = t2.common_column;
# ```
# 
# Example:
# 

# In[ ]:


db.raw_sql("""
SELECT msf.date, msf.permno, msf.ret, msenames.comnam
FROM crsp.msf AS msf
    LEFT JOIN 
        crsp.msenames as msenames
    ON 
        msf.permno = msenames.permno AND
        msenames.namedt <= msf.date AND
        msf.date <= msenames.nameendt
LIMIT 10;
""")


# 
# This query demonstrates a common pattern in financial data analysis - joining historical stock returns with company names. Let's break it down:
# 
# - The Main Table (crsp.msf):
#     - msf is the CRSP Monthly Stock File containing stock returns
#     - We alias it as `msf` for cleaner syntax
#     - Contains columns like `date`, `permno` (stock identifier), and `ret` (returns)
# - The Name History Table (crsp.msenames):
#     - Contains historical company names
#     - We alias it as `msenames`
#     - Has columns like `permno`, `comnam` (company name), `namedt` (start date), and `nameendt` (end date)
# - The JOIN Conditions:
# 
# ```sql
# ON 
#     msf.permno = msenames.permno AND 
#     msenames.namedt <= msf.date AND 
#     msf.date <= msenames.nameendt
# ```
# This is a complex join with three conditions: 
#  - Match the stock identifier (permno) 
#  - Ensure the stock date is after the name's start date (namedt) 
#  - Ensure the stock date is before the name's end date (nameendt){note} 
#  
# Example:
# 
# If a company changed its name from "Old Corp" to "New Corp" on 2020-01-01:
#  - Returns before 2020-01-01 will match with "Old Corp"
#  - Returns after 2020-01-01 will match with "New Corp"4. 
#  
# **Why LEFT JOIN?** 
#  - LEFT JOIN keeps all rows from msf even if there's no matching name 
#  - This prevents losing return data just because we can't find a company nameThis query structure is common in financial databases where entities (like company names) change over time and we need to match historical data correctly.

# ### 4. **Aggregating Data**
# Aggregate functions summarize data (e.g., calculate totals, averages).
# 
# ```sql
# SELECT column, aggregate_function(column)
# FROM table_name
# GROUP BY column;
# ```
# 
# Example:
# 
# This query calculates the average return for each date in the `crsp.msf` table.
# 

# In[ ]:


db.raw_sql("""
SELECT date, AVG(ret) AS avg_return
FROM crsp.msf
GROUP BY date
LIMIT 10;
""")


# ---
# 
# ## Example Queries in the Repository
# 
# ### 1. **Query from `pull_CRSP_stock.py`**
# 
# The `pull_CRSP_monthly_file` function includes an SQL query to pull CRSP monthly stock data. Here is an excerpt of the query:
# 
# ```sql
# SELECT 
#     date,
#     msf.permno, msf.permco, shrcd, exchcd, comnam, shrcls, 
#     ret, retx, dlret, dlretx, dlstcd,
#     prc, altprc, vol, shrout, cfacshr, cfacpr,
#     naics, siccd
# FROM crsp.msf AS msf
# LEFT JOIN crsp.msenames AS msenames
# ON msf.permno = msenames.permno
# WHERE 
#     msf.date BETWEEN '{start_date}' AND '{end_date}' AND 
#     msenames.shrcd IN (10, 11, 20, 21, 40, 41, 70, 71, 73);
# ```
# 
# This query pulls monthly stock data from CRSP (Center for Research in Security Prices) with several specific purposes:
# 
# 1. Core Stock Data Selection:
# 
# ```sql
# SELECT 
#     date,
#     msf.permno, msf.permco,  -- Stock identifiers
#     ret, retx,               -- Returns (with/without distributions)
#     prc, altprc, vol,       -- Price and volume data
#     shrout, cfacshr, cfacpr -- Share data and adjustment factors
# ```
# 
# These fields are essential for calculating stock returns and market capitalizations.
# 
# 2. Company Information Linking:
# ```sql
# FROM crsp.msf AS msf
# LEFT JOIN crsp.msenames as msenames
# ON msf.permno = msenames.permno AND
#     msenames.namedt <= msf.date AND
#     msf.date <= msenames.nameendt
# ```
# 
# This join handles company name changes over time by:
# - Matching stock identifiers (permno)
# - Ensuring the date falls within the valid period for each company name
# 
# 3. Delisting Information:
# ```sql
# LEFT JOIN crsp.msedelist as msedelist
# ON msf.permno = msedelist.permno AND
#     date_trunc('month', msf.date)::date =
#     date_trunc('month', msedelist.dlstdt)::date
# ```
# 
# This join captures when companies are delisted from exchanges, which is crucial for:
# - Accurate return calculations
# - Avoiding survivorship bias in the data
# 
# 4. Data Filtering:
# ```sql
# WHERE 
#     msf.date BETWEEN '{start_date}' AND '{end_date}' AND 
#     msenames.shrcd IN (10, 11, 20, 21, 40, 41, 70, 71, 73);
# ```
# This filters:
# - Specific date range
# - Specific share codes (e.g., 10-11 for ordinary common shares)
# 
# - **Key Concepts**:
#   - `LEFT JOIN` ensures all rows from the `crsp.msf` table are returned, even if there is no match in the `crsp.msenames` table.
#   - The `WHERE` clause filters data for specific date ranges and share codes (`shrcd`).
# 
# 
# 

# 
# ### 2. **Query from `pull_CRSP_Compustat.py`**
# 
# The `pull_CRSP_Comp_Link_Table` function extracts the link table between CRSP and Compustat:
# 
# ```sql
# SELECT 
#     gvkey, lpermno AS permno, linktype, linkprim, linkdt, linkenddt
# FROM 
#     crsp.ccmxpf_linktable
# WHERE 
#     substr(linktype,1,1)='L' AND 
#     (linkprim ='C' OR linkprim='P');
# ```
# 
# - **Key Concepts**:
#   - The `substr(linktype,1,1)='L'` condition ensures only "Link" records are retrieved.
#   - The `linkprim` condition ensures that only primary or secondary links are included.
# 
# 

# 
# ### 3. **Query from `pull_SP500_constituents.py`**
# 
# The `pull_constituents` function extracts S&P 500 constituent data:
# 
# ```sql
# SELECT *  
# FROM crsp_m_indexes.dsp500list_v2;
# ```
# 
# - **Key Concepts**:
#   - The `SELECT *` retrieves all columns from the `dsp500list_v2` table.

# ## Appendix: Why are databases so important?
# 
# Large companies store data in databases rather than in plain files for several key reasons related to **data organization, scalability, security, efficiency, and reliability**. Below is a detailed breakdown of why databases are preferred in enterprise settings:
# 
# 
# ### 1. **Efficient Data Management and Querying**
# Databases use structured query languages (e.g., SQL) to efficiently retrieve, filter, and manipulate data. This is not practical with plain files.
# 
# - **Indexed Searching**: Databases use indexes to locate data quickly, which is much faster than searching through plain files line-by-line.
# - **Complex Queries**: Relational databases allow users to run complex queries (e.g., `JOIN`, `GROUP BY`) to extract insights from large datasets, whereas with plain files, this would require extensive custom programming.
# 
# **Example**: A financial institution analyzing stock returns for a portfolio over multiple years can use a database query to join data across tables in seconds, while processing plain files might take significantly longer.
# 
# 
# ### 2. **Data Integrity**
# Databases ensure data consistency and accuracy through mechanisms such as:
# - **Constraints**: Enforce rules, such as ensuring no duplicate stock identifiers (`permno`), or that all transactions have valid dates.
# - **Transactions**: Ensure multiple operations (e.g., updating stock prices and their related indices) are performed reliably using the ACID (Atomicity, Consistency, Isolation, Durability) principles. Plain files lack this reliability.
# 
# **Example**: If an update fails halfway through in a plain file, the file could become corrupted, but databases can roll back the transaction to maintain integrity.
# 
# 
# 
# ### 3. **Scalability**
# Databases are designed to handle large-scale data storage and access needs, which are common in large companies.
# 
# - **Horizontal and Vertical Scaling**: Modern databases can scale to store terabytes or even petabytes of data and handle thousands of concurrent users.
# - **Efficient Storage**: Databases store data efficiently using techniques such as compression and normalization (eliminating redundant data).
# 
# In contrast, plain files become unwieldy as data grows, leading to performance bottlenecks and significant manual effort to manage.
# 
# 
# 
# ### 4. **Concurrency and Multi-User Access**
# Databases allow multiple users to access and modify data simultaneously without conflicts.
# 
# - **Locking Mechanisms**: Databases manage concurrent access using row- or table-level locks, ensuring that no two users overwrite the same data.
# - **Version Control**: Some databases support versioning, allowing users to work on data without overwriting others' changes.
# 
# Plain files lack these features and often require manual handling, such as creating multiple copies of files to allow simultaneous use, which is inefficient and error-prone.
# 
# 
# 
# ### 5. **Data Security**
# Databases provide robust security measures to protect sensitive data.
# 
# - **Authentication and Access Control**: Databases allow companies to define user roles and permissions, ensuring only authorized personnel can access or modify specific datasets.
# - **Encryption**: Many databases encrypt data at rest and in transit to prevent unauthorized access.
# - **Audit Trails**: Databases log all user activity, making it easier to track who accessed or modified data.
# 
# Plain files are much harder to secure and track, especially when shared across teams or stored on distributed systems.
# 
# 
# 
# ### 6. **Data Redundancy and Backup**
# Databases offer built-in mechanisms to manage redundancy and automate backups, ensuring data availability and recovery.
# 
# - **Replication**: Databases can maintain multiple synchronized copies of data in real-time, ensuring redundancy for high availability.
# - **Automated Backups**: Many databases support scheduled backups, including incremental backups for efficiency.
# - **Disaster Recovery**: Advanced databases provide tools for disaster recovery, allowing businesses to quickly recover from hardware failures or data corruption.
# 
# Plain files often require manual duplication, which increases the risk of errors and slows recovery in case of data loss.
# 
# 
# 
# ### 7. **Data Relationships and Complex Structures**
# Relational databases store and manage relationships between datasets using primary and foreign keys.
# 
# - **Normalization**: Breaks down data into smaller, logically connected tables to avoid duplication and ensure consistency.
# - **Joins**: Databases can efficiently combine data across multiple tables to answer complex questions.
# 
# In plain files, maintaining relationships between datasets requires significant manual effort, such as creating multiple files and writing custom code to merge them.
# 
# 
# 
# ### 8. **Scalable Data Analytics**
# Databases integrate with analytics and reporting tools, enabling companies to derive insights from their data.
# 
# - **Business Intelligence (BI) Tools**: Databases can directly feed data into tools like Tableau, Power BI, or Python-based analytics pipelines.
# - **SQL for Analytics**: Companies can use SQL to aggregate, filter, and transform data for advanced analytics without needing to write additional scripts.
# 
# Plain files require additional preprocessing to prepare data for analysis, slowing down workflows.
# 
# 
# 
# ### 9. **Data Consistency Across Applications**
# Large companies often have multiple systems (e.g., finance, HR, marketing) that need to share data. Databases serve as a **centralized repository** for this data, ensuring consistency across applications.
# 
# - **Integration**: Databases can be accessed through APIs and middleware, enabling seamless integration with software systems.
# - **Real-Time Updates**: Changes made in a database are immediately reflected in all connected systems, which is not possible with plain files.
# 
# 
# 
# ### 10. **Regulatory Compliance**
# Many industries, such as finance and healthcare, are subject to strict regulations regarding data storage, access, and reporting.
# 
# - **Auditability**: Databases maintain detailed logs of data access and changes, enabling compliance with laws like GDPR and SOX.
# - **Retention Policies**: Databases can enforce retention policies to archive or delete data as required by law.
# 
# Plain files lack built-in logging and retention features, making them unsuitable for compliance purposes.
# 
# 
# 
# ### Summary Table: Database vs. Plain Files
# 
# | Feature                     | Database                        | Plain Files                     |
# |-----------------------------|----------------------------------|----------------------------------|
# | Querying and Searching      | Optimized (e.g., indexing)      | Inefficient (line-by-line)      |
# | Data Integrity              | High (ACID compliance)          | Manual error handling           |
# | Scalability                 | Handles terabytes/petabytes     | Limited to small datasets       |
# | Security                    | Authentication, encryption      | Basic file permissions          |
# | Backup and Recovery         | Automated backups, replication  | Manual backups                  |
# | Multi-User Access           | Supported with concurrency      | Limited or unsupported          |
# | Data Relationships          | Built-in support (joins)        | Manual handling required        |
# | Regulatory Compliance       | Built-in logging and policies   | Lacks built-in compliance       |
# 
# 
# In summary, databases are far superior to plain files for managing large, complex, and sensitive datasets. They offer efficiency, security, scalability, and the ability to handle concurrent users, making them indispensable for large companies, especially in data-intensive industries like finance.

# In[ ]:


db.close()

