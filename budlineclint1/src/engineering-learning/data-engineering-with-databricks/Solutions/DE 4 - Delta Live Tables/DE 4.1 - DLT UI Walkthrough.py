# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC <div style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning">
# MAGIC </div>
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC # Using the Delta Live Tables UI
# MAGIC
# MAGIC This demo will explore the DLT UI. By the end of this lesson you will be able to: 
# MAGIC
# MAGIC * Deploy a DLT pipeline
# MAGIC * Explore the resultant DAG
# MAGIC * Execute an update of the pipeline

# COMMAND ----------

# MAGIC %md
# MAGIC ## Classroom Setup
# MAGIC
# MAGIC Run the following cell to configure your working environment for this course.

# COMMAND ----------

# MAGIC %run ./Includes/Classroom-Setup-04.1

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Validate the Pipeline Configuration
# MAGIC
# MAGIC 1. In the Databricks workspace, open the Delta Live Tables (DLT) UI.
# MAGIC
# MAGIC 2. Select your pipeline configuration.
# MAGIC
# MAGIC 3. Review the pipeline configuration settings to ensure they are correctly configured according to the provided instructions.
# MAGIC
# MAGIC 4. **Important:** Remove the maintenance cluster if it is currently part of your pipeline configuration. This is required to successfully validate the pipeline configuration.
# MAGIC
# MAGIC 5. Once you've confirmed that the pipeline configuration is set up correctly and the maintenance cluster has been removed, proceed to the next steps for validating and running the pipeline.
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## Generate Pipeline Configuration
# MAGIC Configuring this pipeline will require parameters unique to a given user.
# MAGIC
# MAGIC In the code cell below, specify which language to use by uncommenting the appropriate line.
# MAGIC
# MAGIC Then, run the cell to print out values you'll use to configure your pipeline in subsequent steps.

# COMMAND ----------

pipeline_language = "SQL"
#pipeline_language = "Python"

DA.print_pipeline_config(pipeline_language)

# COMMAND ----------

# MAGIC %md
# MAGIC In this lesson, we deploy a pipeline with a single notebook, specified as Notebook #1 in the cell output above. 
# MAGIC
# MAGIC <img src="https://files.training.databricks.com/images/icon_hint_24.png"> **HINT:**  You'll want to refer back to the paths above when we add Notebook #2 and #3 to the pipeline in later lessons.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create and Configure a Pipeline
# MAGIC
# MAGIC Let's start by creating a pipeline with a single notebook (Notebook #1).
# MAGIC
# MAGIC Steps:
# MAGIC 1. Click the **Workflows** button on the sidebar, click the **Delta Live Tables** tab, and click **Create Pipeline**. 
# MAGIC 2. Configure the pipeline as specified below. You'll need the values provided in the cell output above for this step.
# MAGIC
# MAGIC | Setting | Instructions |
# MAGIC |--|--|
# MAGIC | Pipeline name | Enter the **Pipeline Name** provided above |
# MAGIC | Product edition | Choose **Advanced** |
# MAGIC | Pipeline mode | Choose **Triggered** |
# MAGIC | Paths | Use the navigator to select or enter the **Notebook # 1 Path** provided above |
# MAGIC | Storage location | Enter the **Storage Location** provided above |
# MAGIC | Target schema | Enter the **Target** database name provided above |
# MAGIC | Cluster policy | Choose the **Policy** provided above |
# MAGIC | Cluster mode | Choose **Fixed size** to disable auto scaling for your cluster |
# MAGIC | Workers | Enter **0** to use a Single Node cluster |
# MAGIC | Photon Acceleration | Check this checkbox to enable |
# MAGIC | Advanced | Click **Add Configuration** to input the **Key** and **Value** for row #1 in the table below,<br>Click **Add Configuration** to input the **Key** and **Value** for row #2 in the table below |
# MAGIC | Channel | Choose **Current** to use the current runtime version |
# MAGIC
# MAGIC | Configuration | Key                 | Value                                      |
# MAGIC | ------------- | ------------------- | ------------------------------------------ |
# MAGIC | #1            | **`spark.master`**  | **`local[*]`**                             |
# MAGIC | #2            | **`source`** | Enter the **source** provided above |
# MAGIC
# MAGIC <br>
# MAGIC
# MAGIC 3. Click the **Create** button.
# MAGIC 4. Verify that the pipeline mode is set to **Development**.

# COMMAND ----------

# This function is provided for students who do not 
# want to work through the exercise of creating the pipeline.
DA.create_pipeline(pipeline_language)

# COMMAND ----------

DA.validate_pipeline_config(pipeline_language)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Additional Notes on Pipeline Configuration
# MAGIC Here are a few notes regarding the pipeline settings above:
# MAGIC
# MAGIC - **Pipeline mode** - This specifies how the pipeline will be run. Choose the mode based on latency and cost requirements.
# MAGIC   - `Triggered` pipelines run once and then shut down until the next manual or scheduled update.
# MAGIC   - `Continuous` pipelines run continuously, ingesting new data as it arrives.
# MAGIC - **Notebook libraries** - Even though this document is a standard Databricks Notebook, the SQL syntax is specialized to DLT table declarations. We will be exploring the syntax in the exercise that follows.
# MAGIC - **Storage location** - This optional field allows the user to specify a location to store logs, tables, and other information related to pipeline execution. If not specified, DLT will automatically generate a directory.
# MAGIC - **Target** - If this optional field is not specified, tables will not be registered to a metastore, but will still be available in the DBFS. See <a href="https://docs.databricks.com/data-engineering/delta-live-tables/delta-live-tables-user-guide.html#publish-tables" target="_blank">documentation</a> for more information on this option.
# MAGIC - **Cluster mode**, **Min Workers**, **Max Workers** - These fields control the worker configuration for the underlying cluster processing the pipeline. Here, we set the number of workers to 0. This works in conjunction with the **spark.master** parameter defined above to configure the cluster as a Single Node cluster.
# MAGIC - **source** - These keys are caps sensitive. Make sure you've got all lower case letters for the word "source"!

# COMMAND ----------

# MAGIC %md
# MAGIC ## Run a Pipeline
# MAGIC
# MAGIC With a pipeline created, you will now run the pipeline.
# MAGIC
# MAGIC 1. Select **Development** to run the pipeline in development mode. Development mode provides for more expeditious iterative development by reusing the cluster (as opposed to creating a new cluster for each run) and disabling retries so that you can readily identify and fix errors. Refer to the <a href="https://docs.databricks.com/data-engineering/delta-live-tables/delta-live-tables-user-guide.html#optimize-execution" target="_blank">documentation</a> for more information on this feature.
# MAGIC 2. Click **Start**.
# MAGIC
# MAGIC The initial run will take several minutes while a cluster is provisioned. Subsequent runs will be appreciably quicker.
# MAGIC
# MAGIC **Note:** If you have created the DLT pipeline manually as described in a previous step, you do not need to run the `DA.start_pipeline()` script. Running this script may not apply to your scenario and could lead to confusion.
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## What is Full Refresh?

# COMMAND ----------

# This function is provided to start the pipeline and  
# block until it has completed, canceled or failed
DA.start_pipeline()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Explore the DAG
# MAGIC
# MAGIC As the pipeline completes, the execution flow is graphed. 
# MAGIC
# MAGIC Selecting the tables reviews the details.
# MAGIC
# MAGIC Select **orders_silver**. Notice the results reported in the **Data Quality** section. 
# MAGIC
# MAGIC With each triggered update, all newly arriving data will be processed through your pipeline. Metrics will always be reported for current run.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Land another batch of data
# MAGIC
# MAGIC Run the cell below to land more data in the source directory, then manually trigger a pipeline update.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Next Steps
# MAGIC
# MAGIC Congratulations on completing the UI walkthrough in section 4.1! Now, here's what to do next:
# MAGIC
# MAGIC 1. **Review Notebook 1:** Navigate to Notebook 1, where you'll find additional exercises and hands-on activities related to the topics covered in the UI walkthrough.
# MAGIC
# MAGIC 2. **Review Notebook 2:** Move on to Notebook 2, which further expands on the concepts learned in the previous notebooks.
# MAGIC
# MAGIC 3. **Troubleshoot in Notebook 3:** If you encounter any issues or want to delve deeper into problem-solving, proceed to Notebook 3 for troubleshooting guidance.
# MAGIC
# MAGIC 4. **Finally, 4.2:** Once you've gone through the previous notebooks, you'll be well-prepared to tackle the content in section 4.2.
# MAGIC
# MAGIC Take your time, and feel free to revisit any section as needed to solidify your understanding. **Happy learning!**

# COMMAND ----------

DA.dlt_data_factory.load()

# COMMAND ----------

# MAGIC %md
# MAGIC As we continue through the course, you can return to this notebook and use the method provided above to land new data.
# MAGIC
# MAGIC Running this entire notebook again will delete the underlying data files for both the source data and your DLT Pipeline. 
# MAGIC
# MAGIC If you get disconnected from your cluster or have some other event where you wish to land more data without deleting things, refer to the <a href="$./DE 4.99 - Land New Data" target="_blank">DE 4.99 - Land New Data</a> notebook.

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# MAGIC Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# MAGIC <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# MAGIC <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# MAGIC <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# MAGIC <a href="https://help.databricks.com/">Support</a>
