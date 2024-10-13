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

    # Method to read information from the Airtable
    def integrate_airtable(self):
        """
            Return:
                --base_table: Requested Airtable Base as a List of records
        """
        url = self.url # URL pointing to our Airtable base
        base_table = list()

        # In a single read call Airtable API outputs only 100 records
        # Additionally, it outputs and 'offset' parameter which indicates
        # the leftover/offset records beyond the 100 records threshold

        # Iteratively reading data till no 'offset' remains
        while True:
            table_slice = requests.get(url, headers=self.headers).json()
            base_table.extend(table_slice["records"])

            if len(table_slice) == 1: break
            else: url = self.url + f"?offset={table_slice["offset"]}"
        
        return base_table

    
    # Method to write information to the Airtable
    def write_to_airtable(self, data_to_write, field):
        """
            Params:
                --data_to_write: List of tuples with data to write and the record ID to be modified
                --field: Airtable column to be populated
            
            Return:
                --None
        """

        # Write the data provided to this method to the given 'field' in the Airtable
        # Each instance is iterated over and individually written to the Airtable
        # using the cell ID
        # 'data_to_write' is a List of Tuples of the form (<data>, <id>)
        for data, id in tqdm(data_to_write,
                             desc="Writing to Airtable", 
                             ncols=100,
                             unit="resource",
                             colour="#35e48f"):
            url = self.url + f"/{id}" # Using the Airtable base URL and adding the cell ID for writing
            payload = {
                "fields": {
                    f"{field}": data
                }
            }
            response = requests.patch(url, headers=self.write_headers, json=payload) # Using 'patch' to write data

        print()
