# Databricks notebook source
# INSTALL_LIBRARIES
version = "v3.0.70"
if not version.startswith("v"): library_url = f"git+https://github.com/databricks-academy/dbacademy@{version}"
else: library_url = f"https://github.com/databricks-academy/dbacademy/releases/download/{version}/dbacademy-{version[1:]}-py3-none-any.whl"
pip_command = f"install --quiet --disable-pip-version-check {library_url}"

# COMMAND ----------

# MAGIC %pip $pip_command

# COMMAND ----------

# MAGIC %run ./_dataset_index

# COMMAND ----------

import pyspark.sql.functions as F
from dbacademy import dbgems
from dbacademy.dbhelper import DBAcademyHelper, Paths, CourseConfig, LessonConfig

# The following attributes are externalized to make them easy
# for content developers to update with every new course.

course_config = CourseConfig(course_code = "dewd",
                             course_name = "data-engineering-with-databricks",
                             data_source_name = "data-engineer-learning-path",
                             data_source_version = "v04",
                             install_min_time = "2 min",
                             install_max_time = "10 min",
                             remote_files = remote_files,
                            #  supported_dbrs = ["11.3.x-scala2.12", "11.3.x-photon-scala2.12", "11.3.x-cpu-ml-scala2.12"],
                             supported_dbrs = ["13.3.x-scala2.12", "13.3.x-photon-scala2.12", "13.3.x-cpu-ml-scala2.12"],
                             expected_dbrs = "{{supported_dbrs}}")

# Defined here for the majority of lessons, 
# and later modified on a per-lesson basis.
lesson_config = LessonConfig(name = None,
                             create_schema = True,
                             create_catalog = False,
                             requires_uc = False,
                             installing_datasets = True,
                             enable_streaming_support = False,
                             enable_ml_support = False)

@DBAcademyHelper.monkey_patch
def clone_source_table(self, table_name, source_path=None, source_name=None):
    start = dbgems.clock_start()

    if source_path is None: source_path = self.paths.datasets
    if source_name is None: source_name = table_name

    print(f"Cloning the \"{table_name}\" table from \"{source_path}/{source_name}\".", end="...")
    
    spark.sql(f"""
        CREATE OR REPLACE TABLE {table_name}
        SHALLOW CLONE delta.`{source_path}/{source_name}`
        """)
    
    print(dbgems.clock_stopped(start))
    

@DBAcademyHelper.monkey_patch
def display_config_values(self, config_values):
    """
    Displays list of key-value pairs as rows of HTML text and textboxes
    :param config_values: list of (key, value) tuples
    """
    html = """<table style="width:100%">"""
    for name, value in config_values:
        html += f"""
        <tr>
            <td style="white-space:nowrap; width:1em">{name}:</td>
            <td><input type="text" value="{value}" style="width: 100%"></td></tr>"""
    html += "</table>"
    displayHTML(html)        


ANALYSTS_ROLE_NAME = "analysts"

None
