-- Databricks notebook source
-- MAGIC %md
-- MAGIC
-- MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
-- MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning">
-- MAGIC </div>
-- MAGIC

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC  
-- MAGIC # Cleaning Data
-- MAGIC
-- MAGIC As we inspect and clean our data, we'll need to construct various column expressions and queries to express transformations to apply on our dataset.
-- MAGIC
-- MAGIC Column expressions are constructed from existing columns, operators, and built-in functions. They can be used in **`SELECT`** statements to express transformations that create new columns.
-- MAGIC
-- MAGIC Many standard SQL query commands (e.g. **`DISTINCT`**, **`WHERE`**, **`GROUP BY`**, etc.) are available in Spark SQL to express transformations.
-- MAGIC
-- MAGIC In this notebook, we'll review a few concepts that might differ from other systems you're used to, as well as calling out a few useful functions for common operations.
-- MAGIC
-- MAGIC We'll pay special attention to behaviors around **`NULL`** values, as well as formatting strings and datetime fields.
-- MAGIC
-- MAGIC ## Learning Objectives
-- MAGIC By the end of this lesson, you should be able to:
-- MAGIC - Summarize datasets and describe null behaviors
-- MAGIC - Retrieve and remove duplicates
-- MAGIC - Validate datasets for expected counts, missing values, and duplicate records
-- MAGIC - Apply common transformations to clean and transform data

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC
-- MAGIC ## Run Setup
-- MAGIC
-- MAGIC The setup script will create the data and declare necessary values for the rest of this notebook to execute.

-- COMMAND ----------

-- MAGIC %run ./Includes/Classroom-Setup-02.4

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## Data Overview
-- MAGIC
-- MAGIC We'll work with new users records from the **`users_dirty`** table, which has the following schema:
-- MAGIC
-- MAGIC | field | type | description |
-- MAGIC |---|---|---|
-- MAGIC | user_id | string | unique identifier |
-- MAGIC | user_first_touch_timestamp | long | time at which the user record was created in microseconds since epoch |
-- MAGIC | email | string | most recent email address provided by the user to complete an action |
-- MAGIC | updated | timestamp | time at which this record was last updated |
-- MAGIC
-- MAGIC Let's start by counting values in each field of our data.

-- COMMAND ----------

SELECT count(*), count(user_id), count(user_first_touch_timestamp), count(email), count(updated)
FROM users_dirty

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ## Inspect Missing Data
-- MAGIC
-- MAGIC Based on the counts above, it looks like there are at least a handful of null values in all of our fields.
-- MAGIC
-- MAGIC **NOTE:** Null values behave incorrectly in some math functions, including **`count()`**.
-- MAGIC
-- MAGIC - **`count(col)`** skips **`NULL`** values when counting specific columns or expressions.
-- MAGIC - **`count(*)`** is a special case that counts the total number of rows (including rows that are only **`NULL`** values).
-- MAGIC
-- MAGIC We can count null values in a field by filtering for records where that field is null, using either:  
-- MAGIC **`count_if(col IS NULL)`** or **`count(*)`** with a filter for where **`col IS NULL`**. 
-- MAGIC
-- MAGIC Both statements below correctly count records with missing emails.

-- COMMAND ----------

SELECT count_if(email IS NULL) FROM users_dirty;
SELECT count(*) FROM users_dirty WHERE email IS NULL;

-- COMMAND ----------

-- MAGIC %python 
-- MAGIC from pyspark.sql.functions import col
-- MAGIC usersDF = spark.read.table("users_dirty")
-- MAGIC
-- MAGIC usersDF.selectExpr("count_if(email IS NULL)")
-- MAGIC usersDF.where(col("email").isNull()).count()

-- COMMAND ----------

-- MAGIC %md
-- MAGIC  
-- MAGIC ## Deduplicate Rows
-- MAGIC We can use **`DISTINCT *`** to remove true duplicate records where entire rows contain the same values.

-- COMMAND ----------

SELECT DISTINCT(*) FROM users_dirty

-- COMMAND ----------

-- MAGIC %python
-- MAGIC usersDF.distinct().display()

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC   
-- MAGIC ## Deduplicate Rows Based on Specific Columns
-- MAGIC
-- MAGIC The code below uses **`GROUP BY`** to remove duplicate records based on **`user_id`** and **`user_first_touch_timestamp`** column values. (Recall that these fields are both generated when a given user is first encountered, thus forming unique tuples.)
-- MAGIC
-- MAGIC Here, we are using the aggregate function **`max`** as a hack to:
-- MAGIC - Keep values from the **`email`** and **`updated`** columns in the result of our group by
-- MAGIC - Capture non-null emails when multiple records are present

-- COMMAND ----------

CREATE OR REPLACE TEMP VIEW deduped_users AS 
SELECT user_id, user_first_touch_timestamp, max(email) AS email, max(updated) AS updated
FROM users_dirty
WHERE user_id IS NOT NULL
GROUP BY user_id, user_first_touch_timestamp;

SELECT count(*) FROM deduped_users

-- COMMAND ----------

-- MAGIC %python
-- MAGIC from pyspark.sql.functions import max
-- MAGIC dedupedDF = (usersDF
-- MAGIC     .where(col("user_id").isNotNull())
-- MAGIC     .groupBy("user_id", "user_first_touch_timestamp")
-- MAGIC     .agg(max("email").alias("email"), 
-- MAGIC          max("updated").alias("updated"))
-- MAGIC     )
-- MAGIC
-- MAGIC dedupedDF.count()

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC Let's confirm that we have the expected count of remaining records after deduplicating based on distinct **`user_id`** and **`user_first_touch_timestamp`** values.

-- COMMAND ----------

SELECT COUNT(DISTINCT(user_id, user_first_touch_timestamp))
FROM users_dirty
WHERE user_id IS NOT NULL

-- COMMAND ----------

-- MAGIC %python
-- MAGIC (usersDF
-- MAGIC     .dropDuplicates(["user_id", "user_first_touch_timestamp"])
-- MAGIC     .filter(col("user_id").isNotNull())
-- MAGIC     .count())

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ## Validate Datasets
-- MAGIC Based on our manual review above, we've visually confirmed that our counts are as expected.
-- MAGIC  
-- MAGIC We can also programmatically perform validation using simple filters and **`WHERE`** clauses.
-- MAGIC
-- MAGIC Validate that the **`user_id`** for each row is unique.

-- COMMAND ----------

SELECT max(row_count) <= 1 no_duplicate_ids FROM (
  SELECT user_id, count(*) AS row_count
  FROM deduped_users
  GROUP BY user_id)

-- COMMAND ----------

-- MAGIC %python
-- MAGIC from pyspark.sql.functions import count
-- MAGIC
-- MAGIC display(dedupedDF
-- MAGIC     .groupBy("user_id")
-- MAGIC     .agg(count("*").alias("row_count"))
-- MAGIC     .select((max("row_count") <= 1).alias("no_duplicate_ids")))

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC
-- MAGIC
-- MAGIC Confirm that each email is associated with at most one **`user_id`**.

-- COMMAND ----------

SELECT max(user_id_count) <= 1 at_most_one_id FROM (
  SELECT email, count(user_id) AS user_id_count
  FROM deduped_users
  WHERE email IS NOT NULL
  GROUP BY email)

-- COMMAND ----------

-- MAGIC %python
-- MAGIC
-- MAGIC display(dedupedDF
-- MAGIC     .where(col("email").isNotNull())
-- MAGIC     .groupby("email")
-- MAGIC     .agg(count("user_id").alias("user_id_count"))
-- MAGIC     .select((max("user_id_count") <= 1).alias("at_most_one_id")))

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC  
-- MAGIC ## Date Format and Regex
-- MAGIC Now that we've removed null fields and eliminated duplicates, we may wish to extract further value out of the data.
-- MAGIC
-- MAGIC The code below:
-- MAGIC - Correctly scales and casts the **`user_first_touch_timestamp`** to a valid timestamp
-- MAGIC - Extracts the calendar date and clock time for this timestamp in human readable format
-- MAGIC - Uses **`regexp_extract`** to extract the domains from the email column using regex

-- COMMAND ----------

SELECT *, 
  date_format(first_touch, "MMM d, yyyy") AS first_touch_date,
  date_format(first_touch, "HH:mm:ss") AS first_touch_time,
  regexp_extract(email, "(?<=@).+", 0) AS email_domain
FROM (
  SELECT *,
    CAST(user_first_touch_timestamp / 1e6 AS timestamp) AS first_touch 
  FROM deduped_users
)

-- COMMAND ----------

-- MAGIC %python
-- MAGIC from pyspark.sql.functions import date_format, regexp_extract
-- MAGIC
-- MAGIC display(dedupedDF
-- MAGIC     .withColumn("first_touch", (col("user_first_touch_timestamp") / 1e6).cast("timestamp"))
-- MAGIC     .withColumn("first_touch_date", date_format("first_touch", "MMM d, yyyy"))
-- MAGIC     .withColumn("first_touch_time", date_format("first_touch", "HH:mm:ss"))
-- MAGIC     .withColumn("email_domain", regexp_extract("email", "(?<=@).+", 0))
-- MAGIC )

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC ## Data Profile 
-- MAGIC
-- MAGIC Databricks version 9.1 and newer offer two convenient methods for data profiling within Notebooks: through the cell output UI and via the dbutils library.
-- MAGIC
-- MAGIC When working with data frames or the results of SQL queries in a Databricks Notebook, users have the option to access a dedicated **Data Profile** tab. Clicking on this tab initiates the creation of an extensive data profile, providing not only summary statistics but also histograms that cover the entire dataset, ensuring a comprehensive view of the data, rather than just what is visible.
-- MAGIC
-- MAGIC This data profile encompasses a range of insights, including information about numeric, string, and date columns, making it a powerful tool for data exploration and understanding.
-- MAGIC
-- MAGIC **Using cell output UI:**
-- MAGIC
-- MAGIC 1. In the cell output, you will see a `Table` tab on the right.
-- MAGIC
-- MAGIC 1. Click on the `Table` tab to access the cell output options.
-- MAGIC
-- MAGIC 1. Next to the `Table` tab, you'll find a "Data Profile" tab. Click on it.
-- MAGIC
-- MAGIC 1. Databricks will automatically execute a new command to generate a data profile.
-- MAGIC
-- MAGIC 1. The generated data profile will provide summary statistics for numeric, string, and date columns, along with histograms of value distributions for each column.

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC  
-- MAGIC Run the following cell to delete the tables and files associated with this lesson.

-- COMMAND ----------

-- MAGIC %python
-- MAGIC DA.cleanup()

-- COMMAND ----------

-- MAGIC %md
-- MAGIC
-- MAGIC &copy; 2024 Databricks, Inc. All rights reserved.<br/>
-- MAGIC Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
-- MAGIC <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
-- MAGIC <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
-- MAGIC <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
-- MAGIC <a href="https://help.databricks.com/">Support</a>
