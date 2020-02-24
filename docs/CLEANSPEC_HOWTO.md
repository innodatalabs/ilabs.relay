# Standalone script cleanspec.py:

The cleanspec.py script was created to modify the spec.json as follows:
  - removes documentation on endpoint '/v1/documents/input/'
  - removes documentation on endpoint '/v1/ping'
  - removes keys when vaue is null 
  - modifies dictionary basePath key to an empty string value
  - adds dictionary host key with value api.innodatalabs.com

After running the cleanspec.py script, the output could be copied to 3scale https://innodatalabs-admin.3scale.net/admin/api_docs/services

## Running the script:

    python endpoints/cleanspec.py (assumes default port 8080)
    python endpoints/cleanspec.py -p NNNN, where NNNN is the port
    python endpoints/cleanspec.py --port, NNNN where NNNN is the port

Help message

    python endpoints/cleanspec.py -h

NOTE: ilabs-api must be running locally via dev_appserver.py 

View spec.json via browser @ url_address ='http://localhost:NNNN/api/spec.json', where NNNN is the port

