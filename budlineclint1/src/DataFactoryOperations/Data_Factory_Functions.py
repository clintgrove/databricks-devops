import logging
import sys
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
sys.path.append('/Workspace/Users/admin@mngenvmcap562520.onmicrosoft.com/')
from Common.Constants import Constants
from azure.identity import ClientSecretCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from time import sleep

constants = Constants()


def run_adf_pipeline(pipeline_name, parameters = None):
    try:
        tenant_id = constants.TENANT_ID
        client_id = constants.CLIENT_ID
        client_secret = constants.CLIENT_SECRET
        subscription_id ='6d0a0c1f-6739-473b-962f-01f793ed5368' #constants.SUBSCRIPTION_ID
        resource_group_name = f"rg-fabric"
        factory_name = f"clintadf1"
        credentials = ClientSecretCredential(tenant_id, client_id, client_secret)
        adf_client = DataFactoryManagementClient(credentials, subscription_id)
        run_response = adf_client.pipelines.create_run(resource_group_name, factory_name, pipeline_name, parameters = parameters)

        # Check the pipeline run status
        run_id = run_response.run_id
        pipeline_status = adf_client.pipeline_runs.get(
            resource_group_name,
            factory_name,
            run_id
        )

        # Poll for the status until the pipeline finishes
        while pipeline_status.status not in ['Succeeded', 'Failed', 'Cancelled']:
            sleep(5)  # Sleep for 5 seconds before checking again
            pipeline_status = adf_client.pipeline_runs.get(
                resource_group_name,
                factory_name,
                run_id
            )

        if pipeline_status.status == 'Succeeded':
            logger.info(f"Pipeline {pipeline_name} Succeeded with run ID: {run_response.run_id}")
        elif pipeline_status.status == 'Cancelled':
            logger.info(f"Pipeline {pipeline_name} Cancelled with run ID: {run_response.run_id}")
        else:
            logger.info(f"Pipeline {pipeline_name} has failed in the Data Factory")

        # return the final status of the pipeline run
        return pipeline_status.status

    except Exception as e:
        logger.error(f"Error running ADF pipeline {pipeline_name}. Exception: {e}")
        raise e

    logger.info(f"Triggered ADF pipeline {pipeline_name} with run ID: {run_response.run_id}")
