import requests
from requests.auth import HTTPDigestAuth
import json, pymongo, os
from dotenv import load_dotenv


load_dotenv()

digest = HTTPDigestAuth(os.environ.get('apiPub'), os.environ.get('apiPriv'))
driverCreds = os.environ.get('driverCreds')
out_file = os.environ.get('outFile')




# JSON file in which to output the results 
#out_file = r"/Users/jason.scanzoni/mongodb/atlas_indexes/indexes.json"

# Databases to Skip
ignore_list = ['admin','config','local']

# Base URL for the MongoDB Atlas API
base_url = "https://cloud.mongodb.com/api/atlas/v1.0"

# Empty dictionary to write to
index_dict = {}

# Get a list of all the projects in your account
response = requests.get(base_url + "/groups", headers={
                        "Content-Type": "application/json"}, params={"pretty": "true"}, auth=digest)

projects = json.loads(response.text)["results"]

collections = []

# Loop through each project
for project in projects:
    # Get the project ID
    project_id = project["id"]
    project_name = project["name"]
    index_dict[project_name] = {}

    # Get a list of all the clusters in the project
    response = requests.get(base_url + "/groups/" + project_id + "/clusters", headers={
                            "Content-Type": "application/json"}, params={"pretty": "true"}, auth=digest)
    clusters = json.loads(response.text)["results"]

    # Loop through each cluster
    for cluster in clusters:
        # Get the cluster ID and standardSrv
        cluster_id = cluster["id"]
        cluster_name = cluster["name"]
        index_dict[project_name][cluster_name] = {}
        standardSrv = cluster["connectionStrings"]["standardSrv"]

        # Convert standardSrv into a connection string
        conn_str = standardSrv.replace("//", "//" + driverCreds + "@")

        # Get a list of all the collections and their indexes in the cluster
        client = pymongo.MongoClient(conn_str)
        database_list = client.list_database_names()

        for database in database_list:
            
            if database in ignore_list:
                continue

            index_dict[project_name][cluster_name][database] = {}

            db = client[database]

            collections_list = db.list_collection_names()

            collections += collections_list
            
            # Loop through each collection
            for collection in collections_list:
                
                try:
                    indexes = db[collection].index_information()
                    index_dict[project_name][cluster_name][database][collection] = indexes
                except:
                    print("SKIP: \n")
                    print("Project: " + project_name)
                    print("Cluster: " + cluster_name)
                    print("Database: " + database)
                    print("Collection: " + collection)
                    print("\n\n")


try:                
    file = open(out_file, "w+") 
    file.write(json.dumps(index_dict, indent=2))
    file.close()
    print("\n\nResults written to: \n\n"+out_file)
except:
    print("\n\nUnable to write to file... here are the results in JSON:\n\n")
    print(json.dumps(index_dict))

