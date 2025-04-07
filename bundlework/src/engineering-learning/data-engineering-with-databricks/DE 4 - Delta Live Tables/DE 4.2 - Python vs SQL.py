# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning">
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Delta Live Tables: Python vs SQL
# MAGIC
# MAGIC In this lesson we will be reviewing key differences between the Python and SQL implementations of Delta Live Tables
# MAGIC
# MAGIC By the end of this lesson you will be able to: 
# MAGIC
# MAGIC * Identify key differences between the Python and SQL implementations of Delta Live Tables

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC # Python vs SQL
# MAGIC | Python | SQL | Notes |
# MAGIC |--------|--------|--------|
# MAGIC | Python API | Proprietary SQL API |  |
# MAGIC | No syntax check | Has syntax checks| In Python, if you run a DLT notebook cell on its own it will show in error, whereas in SQL it will check if the command is syntactically valid and tell you. In both cases, individual notebook cells are not supposed to be run for DLT pipelines. |
# MAGIC | A note on imports | None | The dlt module should be explicitly imported into your Python notebook libraries. In SQL, this is not the case. |
# MAGIC | Tables as DataFrames | Tables as query results | The Python DataFrame API allows for multiple transformations of a dataset by stringing multiple API calls together. Compared to SQL, those same transformations must be saved in temporary tables as they are transformed. |
# MAGIC |`@dlt.table()`  | `SELECT` statement | In SQL, the core logic of your query, containing transformations you make to your data, is contained in the `SELECT` statement. In Python, data transformations are specified when you configure options for @dlt.table().  |
# MAGIC | `@dlt.table(comment = `"Python comment",`table_properties = {"quality": "silver"})` | `COMMENT` "SQL comment"       `TBLPROPERTIES ("quality" = "silver")` | This is how you add comments and table properties in Python vs. SQL |
# MAGIC | Python Metaprogramming | N/A | You can use Python inner functions with Delta Live Tables to programmatically create multiple tables to reduce code redundancy.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# MAGIC Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# MAGIC <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# MAGIC <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# MAGIC <a href="https://help.databricks.com/">Support</a>
