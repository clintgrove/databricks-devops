# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning">
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC # Getting Started with the Databricks Platform
# MAGIC
# MAGIC This notebook provides a hands-on review of some of the basic functionality of the Databricks Data Science and Engineering Workspace.
# MAGIC
# MAGIC ## Learning Objectives
# MAGIC By the end of this lab, you should be able to:
# MAGIC - Rename a notebook and change the default language
# MAGIC - Attach a cluster
# MAGIC - Use the **`%run`** magic command
# MAGIC - Run Python and SQL cells
# MAGIC - Create a Markdown cell

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Renaming a Notebook
# MAGIC
# MAGIC Changing the name of a notebook is easy. Click on the name at the top of this page, then make changes to the name. To make it easier to navigate back to this notebook later in case you need to, append a short test string to the end of the existing name.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Attaching a cluster
# MAGIC
# MAGIC Executing cells in a notebook requires computing resources, which is provided by clusters. The first time you execute a cell in a notebook, you will be prompted to attach to a cluster if one is not already attached.
# MAGIC
# MAGIC Attach a cluster to this notebook now by clicking the dropdown near the top-right corner of this page. Select the cluster you created previously. This will clear the execution state of the notebook and connect the notebook to the selected cluster.
# MAGIC
# MAGIC Note that the dropdown menu provides the option of starting or restarting the cluster as needed. You can also detach and re-attach to a cluster in a single operation. This is useful for clearing the execution state when needed.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Using %run
# MAGIC
# MAGIC Complex projects of any type can benefit from the ability to break them down into simpler, reusable components.
# MAGIC
# MAGIC In the context of Databricks notebooks, this facility is provided through the **`%run`** magic command.
# MAGIC
# MAGIC When used this way, variables, functions and code blocks become part of the current programming context.
# MAGIC
# MAGIC Consider this example:
# MAGIC
# MAGIC **`Notebook_A`** has four commands:
# MAGIC   1. **`name = "John"`**
# MAGIC   2. **`print(f"Hello {name}")`**
# MAGIC   3. **`%run ./Notebook_B`**
# MAGIC   4. **`print(f"Welcome back {full_name}`**
# MAGIC
# MAGIC **`Notebook_B`** has only one commands:
# MAGIC   1. **`full_name = f"{name} Doe"`**
# MAGIC
# MAGIC If we run **`Notebook_B`** it will fail to execute because the variable **`name`** is not defined in **`Notebook_B`**
# MAGIC
# MAGIC Likewise, one might think that **`Notebook_A`** would fail becase it uses the variable **`full_name`** which is likewise not defined in **`Notebook_A`**, but it doesn't!
# MAGIC
# MAGIC What actually happens is that the two notebooks are merged together as we see below and **then** executed:
# MAGIC 1. **`name = "John"`**
# MAGIC 2. **`print(f"Hello {name}")`**
# MAGIC 3. **`full_name = f"{name} Doe"`**
# MAGIC 4. **`print(f"Welcome back {full_name}")`**
# MAGIC
# MAGIC And thus providing the expected behavior:
# MAGIC * **`Hello John`**
# MAGIC * **`Welcome back John Doe`**

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC The folder that contains this notebook contains a subfolder named **`ExampleSetupFolder`**, which in turn contains a notebook called **`example-setup`**.
# MAGIC
# MAGIC This simple notebook does the following:
# MAGIC   - Declares the variable **`my_name`** and sets it to **`None`**
# MAGIC   - Creates the DataFrame **`example_df`**, as well as the table **`nyc_taxi`** (we'll use these later)
# MAGIC
# MAGIC Run the following cell to execute this notebook.
# MAGIC
# MAGIC Then, open the **`example-setup`** notebook and change the **`my_name`** variable from **`None`** to your name (or anyone's name) enclosed in quotes. If done correctly, the following two cells should execute without throwing an **`AssertionError`**.
# MAGIC
# MAGIC <img src="https://files.training.databricks.com/images/icon_note_24.png"> You will see additional references **`_utility-methods`** and **`DBAcademyHelper`** which are used to this configure  courseware and should be ignored for this exercise.

# COMMAND ----------

# MAGIC %run ./ExampleSetupFolder/example-setup

# COMMAND ----------

assert my_name is not None, "Name is still None"
print(my_name)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Run a Python cell
# MAGIC
# MAGIC Run the following cell to verify that the **`example-setup`** notebook was executed by displaying the **`example_df`** DataFrame. This table consists of 16 rows of increasing values.

# COMMAND ----------

display(example_df)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC
# MAGIC ## Change Language
# MAGIC
# MAGIC Notice that the default language for this notebook is set to Python. Change this by clicking the **Python** button to the right of the notebook name. Change the default language to SQL.
# MAGIC
# MAGIC Notice that the Python cells are automatically prepended with a <strong><code>&#37;python</code></strong> magic command to maintain validity of those cells. 
# MAGIC
# MAGIC Note that this operation also clears the execution state. After changing the default language for this notebook, make sure to re-run the example setup script above to proceed.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Create a Markdown Cell
# MAGIC
# MAGIC Add a new cell below this one. Populate with some Markdown that includes at least the following elements:
# MAGIC * A header
# MAGIC * Bullet points
# MAGIC * A link (using your choice of HTML or Markdown conventions)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Run a SQL cell
# MAGIC
# MAGIC Run the following cell to query a Delta table using SQL. This executes a simple query against a table is backed by a Databricks-provided example dataset included in all DBFS installations.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM nyc_taxi

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC Execute the following cell to view the underlying files backing this table.

# COMMAND ----------

files = dbutils.fs.ls(f"{DA.paths.datasets}/nyctaxi-with-zipcodes/data")
display(files)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Clearing notebook state
# MAGIC
# MAGIC Sometimes it is useful to clear all variables defined in the notebook and start from the beginning.  This can be useful when you want to test cells in isolation, or you simply want to reset the execution state.
# MAGIC
# MAGIC Visit the **Run** menu and select the **Clear state and outputs**.
# MAGIC
# MAGIC Now try running the cell below and notice the variables defined earlier are no longer defined, until you rerun the example-setup.

# COMMAND ----------

# MAGIC %run ./ExampleSetupFolder/example-setup

# COMMAND ----------

print(my_name)

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Wrapping Up
# MAGIC
# MAGIC By completing this lab, you should now feel comfortable manipulating notebooks, creating new cells, and running notebooks within notebooks.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# MAGIC Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# MAGIC <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# MAGIC <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# MAGIC <a href="https://help.databricks.com/">Support</a>
