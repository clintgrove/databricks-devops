param(
  [parameter(Mandatory = $true)]
  [String] $databricksWorkspaceResourceId,
  [parameter(Mandatory = $true)]
  [String] $databricksWorkspaceUrl,
  [parameter(Mandatory = $false)]
  [int] $tokenLifeTimeSeconds = 300
)

$azureDatabricksPrincipalId = "2ff814a6-3304-4ab8-85cb-cd0e6f879c1d"
$headers = @{}
# From this site https://medium.com/@akshaybagal/mastering-ci-cd-for-azure-databricks-notebooks-using-azure-devops-pipeline-a-comprehensive-guide-cfe7538e4944
# Get Azure AD access token for Databricks API
$azureAccessToken = (az account get-access-token --resource $azureDatabricksPrincipalId | ConvertFrom-Json).accessToken

# Construct authorization header
$headers["Authorization"] = "Bearer $azureAccessToken"

# Construct X-Databricks-Azure-SP-Management-Token header (assuming Azure AD integration)
$managementToken = (az account get-access-token --resource https://management.core.windows.net/ | ConvertFrom-Json).accessToken
$headers["X-Databricks-Azure-SP-Management-Token"] = "$managementToken"

# Set Databricks workspace resource ID header
$headers["x-Databricks-Azure-Workspace-Resource-Id"] = $databricksWorkspaceResourceId

# Create JSON payload for token request
$json = @{}
$json["lifetime_seconds"] = $tokenLifeTimeSeconds

# Send request to Databricks API to create token
$req = Invoke-WebRequest -Uri "https://$databricksWorkspaceUrl/api/2.0/token/create" -Body ($json | ConvertTo-Json) -ContentType "application/json" -Headers $headers

# Extract bearer token from response
$bearerToken = ($req.Content | ConvertFrom-Json).token_value

# Return the bearer token
return $bearerToken