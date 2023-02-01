# MongoDB Atlas Index Inventory

This script will inventory indexes in and MongoDB Atlas clusters you have permission to view and output it to a JSON file.

This script will first use the Atlas API to:
- find all projects
- find all clusters 
- grab the connection string

Using the connection string:
- find all databases
- find all collections
- grab indexes from each collection

The output will either push formatted JSON to the `outFile` you define in your `.env` file, or it will output in JSON into the terminal window.

## Instructions
The script runs off of a `.env` file with the following contents:


```bash
#contents of .env file

apiPub = "abcdefgh"
apiPriv = "11111111-1111-1111-1111-111111111111"
driverCreds = "user:pass"
outFile = "/path/to/output/index_inventory.json"

```


To run the script:
- API credentials will require `Project Read Only` permission for each project
- Database/driver credentials will require `readAnyDatabase` permission for each cluster 