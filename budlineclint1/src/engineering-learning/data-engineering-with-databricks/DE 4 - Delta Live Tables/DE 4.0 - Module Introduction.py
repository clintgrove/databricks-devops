# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning">
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Build Data Pipelines with Delta Live Tables
# MAGIC This module is part of the Data Engineer Learning Path by Databricks Academy.
# MAGIC
# MAGIC #### DLT UI
# MAGIC
# MAGIC Lecture: The Medallion Architecture <br>
# MAGIC Lecture: Introduction to Delta Live Tables <br>
# MAGIC [DE 4.1 - DLT UI Walkthrough]($./DE 4.1 - DLT UI Walkthrough) <br>
# MAGIC
# MAGIC #### DLT Syntax
# MAGIC DE 4.1.1 - Orders Pipeline: [SQL]($./DE 4.1A - SQL Pipelines/DE 4.1.1 - Orders Pipeline) or [Python]($./DE 4.1B - Python Pipelines/DE 4.1.1 - Orders Pipeline)<br>
# MAGIC DE 4.1.2 - Customers Pipeline: [SQL]($./DE 4.1A - SQL Pipelines/DE 4.1.2 - Customers Pipeline) or [Python]($./DE 4.1B - Python Pipelines/DE 4.1.2 - Customers Pipeline) <br>
# MAGIC [DE 4.2 - Python vs SQL]($./DE 4.2 - Python vs SQL) <br>
# MAGIC
# MAGIC #### Pipeline Results, Monitoring, and Troubleshooting
# MAGIC [DE 4.3 - Pipeline Results]($./DE 4.3 - Pipeline Results) <br>
# MAGIC [DE 4.4 - Pipeline Event Logs]($./DE 4.4 - Pipeline Event Logs) <br>
# MAGIC DE 4.1.3 - Status Pipeline: [SQL]($./DE 4.1A - SQL Pipelines/DE 4.1.3L - Status Pipeline Lab) or [Python]($./DE 4.1B - Python Pipelines/DE 4.1.3L - Status Pipeline Lab) <br>
# MAGIC [DE 4.99 - Land New Data]($./DE 4.99 - Land New Data) <br>
# MAGIC
# MAGIC #### Prerequisites
# MAGIC
# MAGIC * Beginner familiarity with cloud computing concepts (virtual machines, object storage, etc.)
# MAGIC * Ability to perform basic code development tasks using the Databricks Data Engineering & Data Science workspace (create clusters, run code in notebooks, use basic notebook operations, import repos from Git, etc)
# MAGIC * Beginning programming experience with Delta Lake
# MAGIC * Use Delta Lake DDL to create tables, compact files, restore previous table versions, and perform garbage collection of tables in the Lakehouse
# MAGIC   * Use CTAS to store data derived from a query in a Delta Lake table
# MAGIC   * Use SQL to perform complete and incremental updates to existing tables
# MAGIC * Beginning programming experience with Spark SQL or PySpark
# MAGIC   * Extract data from a variety of file formats and data sources
# MAGIC   * Apply a number of common transformations to clean data
# MAGIC   * Reshape and manipulate complex data using advanced built-in functions
# MAGIC * Production experience working with data warehouses and data lakes
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# MAGIC Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# MAGIC <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# MAGIC <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# MAGIC <a href="https://help.databricks.com/">Support</a>
