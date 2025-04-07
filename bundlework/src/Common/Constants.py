import os
from databricks.sdk.runtime import *

class Constants:
    def __init__(self):
        
        self.TENANT_ID = dbutils.secrets.get(scope=f"secrets4me", key=f"this-tenant-id")
        self.CLIENT_ID = dbutils.secrets.get(scope=f"secrets4me", key=f"dbx-spn-2025-1-appid")
        self.CLIENT_SECRET = dbutils.secrets.get(scope=f"secrets4me", key=f"dbx-spn-2025-1-clientsecret")
        self.SUBSCRIPTION_ID = '3be2ce56-4a5f-4034-88d7-2953d1819ed3'