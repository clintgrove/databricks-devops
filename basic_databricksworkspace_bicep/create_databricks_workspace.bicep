@description('The name of the Azure Databricks workspace.')
param workspaceName string = 'cgroove2dbx'

@description('The location of the Azure Databricks workspace.')
param location string = resourceGroup().location

@description('The pricing tier of the Azure Databricks workspace.')
@allowed([
  'standard'
  'premium'
])
param skuName string = 'premium'


module databricks 'br/public:avm/res/databricks/workspace:0.11.1' = {
  name: 'databricksWorkspace'
  params: {
    name: workspaceName
    location: location
    skuName: skuName
  }
}

output workspaceId string = databricks.outputs.workspaceResourceId
output workspaceUrl string = databricks.outputs.workspaceUrl
