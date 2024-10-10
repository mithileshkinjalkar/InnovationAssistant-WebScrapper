"""
    Module housing Airtable integration functions
"""

import requests
from tqdm import tqdm

class Airtable:

    """
        Class to programmatically declare the project's Airtable Base.
    """

    def __init__(self, baseId, tableId, authToken):
        """
            Params:
                --baseId: ID of the Airtable Base that is to be integrated
                --tableId: ID of the table in the Airtable base to access
                --authToken: Access Token to access Airtable using REST API calls
                                **must be passed in the request header
        """
        self.baseId = baseId
        self.tableId = tableId
        self.authToken = authToken
        self.url = f"https://api.airtable.com/v0/{self.baseId}/{self.tableId}"
        self.headers = {
            "Authorization": f"Bearer {self.authToken}"
        }
        self.write_headers = {
            "Authorization": f"Bearer {self.authToken}",
            "Content-Type": "application/json"
        }

    def integrate_airtable(self):
        """
            Return:
                --base_table: Requested Airtable Base as a List of records
        """
        url = self.url
        base_table = list()

        while True:
            table_slice = requests.get(url, headers=self.headers).json()
            base_table.extend(table_slice["records"])

            if len(table_slice) == 1: break
            else: url = self.url + f"?offset={table_slice["offset"]}"
        
        return base_table

    
    def write_to_airtable(self, data_to_write, field):
        """
            Params:
                --data_to_write: List of tuples with data to write and the record ID to be modified
                --field: Airtable column to be populated
            
            Return:
                --None
        """
        for data, id in tqdm(data_to_write,
                             desc="Writing to Airtable", 
                             ncols=100,
                             unit="resource",
                             colour="#35e48f"):
            url = self.url + f"/{id}"
            payload = {
                "fields": {
                    f"{field}": data
                }
            }
            response = requests.patch(url, headers=self.write_headers, json=payload)

        print()
