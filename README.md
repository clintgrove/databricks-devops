# How to promote or push your notebooks and python files to a Databricks workspace using CI/CD or devops
We are running pipelines from Azure Devops and GitHub Actions to demonstrate how you can use the Databricks CLI capabilities like `databricks workspace` from the command line to copy files from your local or from your git repository to the Databricks workspace to any location you specify. You can set `--overwrite` to make sure that you overwrite any existing files there. 

# Prerequisites
- 2 Databricks workspaces. As I have set this up to mimic a Dev to Prod type promotion
- The Databricks workspaces need to have Unity Catalog
- You need access to the Account Dashboard

## Setting this up for Azure Devops 
From this site https://medium.com/@akshaybagal/mastering-ci-cd-for-azure-databricks-notebooks-using-azure-devops-pipeline-a-comprehensive-guide-cfe7538e4944

Currently the Azure Devops is going through my clintgrove organisation. It is deploying to Databricks on Microsoft Non-production. 

## Idea for Github actions from 
Thanks to https://endjin.com/blog/2019/09/import-and-export-notebooks-in-databricks

 It is deploying to Databricks on Microsoft Non-production. 

 ## Asset Bundles
 These are pointing to my Contoso tenant.
