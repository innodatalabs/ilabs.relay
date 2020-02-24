# Innodata Labs API:

## Authentication:

All API calls must be authenticated with the 'user-key' added to the header as a key-value pair.

> **user-key**: your_key (each user has a unique key)

User keys are generated from the [3scale dashboard](https://innodatalabs-admin.3scale.net/buyers/applications).

# Using the API:

There are two main use cases:

## Document references (inline cross-references)

![alt text](https://github.com/innodatalabs/ilabs-api/blob/master/docs/citable-reference-api.png "Document references API diagram")

### 1.0) POST a document in the input file store

Perform a POST operation at:
> http://api.innodatalabs.com/v1/documents/input/{filename}

NOTE: If the filename is left blank, a filename will be automatically generated (i.e. random_filename.file)

Where:
* {filename} is the filename you want to create
* request data contains the file content (the XML or HTML content)

The corresponding CURL call (using, for instance, the file name 'OLM_002.htm'):

    curl --request POST \
      --url http://api.innodatalabs.com/v1/documents/input/my-OLM-file.htm \
      --header 'user-key: <your_key>' \
      --header 'content-type: application/octet-stream' \
      --data-binary "@OLM_002.xml"

Alternatively, the same can be achieved by passing the file content string directly

    curl --request POST \
      --url http://api.innodatalabs.com/v1/documents/input/my-OLM-file.htm \
      --header 'user-key: <your_key>' \
      --header 'content-type: text/plain;charset=UTF-8' \
      --data '<html><body><h1>1. Hello</h1><p>a. Ola</p></body></html>'

This call returns JSON response with filename and number of bytes:

  {"input_filename": "my-OLM-file.htm", "bytes_accepted": 56}

### 2.0) Reference annotation

Perform a GET operation at:
> http://api.innodatalabs.com/v1/reference/{domain}/{filename}?{param}={value}

Where:
* {domain} is either affiliation, bibliography or legal
* {filename} is the filename save at step 1
* {param} and {value} are arbitrary query parameters(optional)

Here's a sample CURL call:

    curl --request GET \
       --url 'http://api.innodatalabs.com/v1/reference/legal/my_input.xml?name=john&age=32 \
       --header 'user-key: <your_key>' \

This call returns HTTP 202 (accepted), the model version, the name of output file (always XML) and an uri to perform a GET operation to retrieve the progress of the task:

  {
  "document_output_url": "http://api.innodatalabs.com/v1/documents/output/my_input.xml",
  "task_id": "task_id", 
  "task_cancel_url": "http://api.innodatalabs.com/v1/reference/legal/task_id/cancel", 
  "task_status_url": "http://api.innodatalabs.com/v1/reference/legal/task_id/status", 
  "output_filename": "my_input.xml", 
  "version": "Checkpoints-Dec-v14"
  }


### 2.1) Status

Perform a GET operation at:
> http://api.innodatalabs.com/v1/reference/{domain}/{task_id}/status

Where:
* {domain} and {task_id} are given within the output at step 2.0

The corresponding CURL call:

    curl --request GET \
      --url http://api.innodatalabs.com/v1/reference/legal/task_id/status \
      --header 'user-key: <your_key>' \

This call returns HTTP 200 (OK) and JSON data in the format as follows: 

  {'progress': INTEGER, 'completed': BOOLEAN, 'steps': INTEGER, 'exception': 'STRING'}

NOTE: exception will only appear if the task has failed

### 2.2) Cancel

Perform a GET operation at:
> http://api.innodatalabs.com/v1/reference/{domain}/{task_id}/cancel

Where:
* {domain} and {task_id} are given within the output at step 2.0

The corresponding CURL call:

    curl --request GET \
      --url http://api.innodatalabs.com/v1/reference/legal/task_id/cancel \
      --header 'user-key: <your_key>' \

This may return several responses as follows:

a) HTTP 404 (Not Found) and Invalid task ID: {task_id}
b) HTTP 200 (OK) and Task ID: {task_id} is beening proceeded and can not be cancelled
c) HTTP 200 (OK) and Task ID: {task_id} has already been proccessed
d) HTTP 200 (OK) and Task ID: {task_id} has already failed
e) HTTP 202 (Accepted) and Cancelled task ID: {task_id} 

### 3.0) GET a document in the output file store:

Perform a GET operation at:
> http://api.innodatalabs.com/v1/documents/output/{filename}

Where {filename} is the file name you want to read

The corresponding CURL call (assuming there is a file named 'abc.htm.xml' in the output folder):

    curl --request GET \
      --url http://api.innodatalabs.com/v1/documents/output/abc.htm.xml \
      --header 'user-key: <your_key>' \

This call returns the file content.

## Document structure (levels)

![alt text](https://github.com/innodatalabs/ilabs-api/blob/master/docs/citable-structure-api.png "Document structure API diagram")

### 1.0) POST a document in the input file store

Refer to section 1.0 of section 'Document references'

### 2.0) Struture annotation

Perform a GET operation at:
> http://api.innodatalabs.com/v1/structure/{domain}/{filename}?type={type}&path={path}&override={key:value}

Where:
* {domain} is either affiliation, bibliography or legal
* {filename} is the filename save at step 1
* {type} is either 'xml' or 'html' (xhtml content must be declared as 'xml')
* {path} is a path string as defined at then end of this document
* {override} is a dictionary of {key, value} pairs to override in the parameters

Here's a sample CURL call:

    curl --request GET \
       --url 'http://api.innodatalabs.com/v1/structure/legal/my_input.html?type=html&path=/$us/$nasdrules/<h2>/<div class="indent_firstpara">/<div class="indent_secondpara">/<div class="indent">&override={"siblings_bonus" : 3}' \
      --header 'user-key: <your_key>' \

This call returns HTTP 202 (accpeted), the name of output file (always XML) and the expected processing time:

  {"output_filename": "my_input.html", "excepted_processing_time_seconds": 1}

### 3.0) GET a document in the output file store:

Refer to section 3.0 of section 'Document references'

## How to build the path string:

A path is an expression describing the citable levels in a document.

For instance:

> /$cfr/0/0/0/$Appendix A/0/A

Elements with '$' are constants. 

The path has 2 parts:

1- (optional) The head made of all the leading constant elements (e.g., $cfr). Elements of head are hard-coded and simply used as prefix in final paths instanciations.

2- The tail made of all variables following the head (some might be in the format "constant, space, variable" (e.g., $Appendix A). Elements of the tail serve as the guideline for citable structure extraction. 

Variables are a combination of the following characters:

- a: means the section identifier is a lowercase letter
- A: means the section identifier is an uppercase letter
- 0: means the section identifier is a digit
- i: means the section identifier is a lowercase roman number
- I: means the section identifier is an uppercas roman number

Optionally, a variable can be preceeded by a tag (e.g., &lt;h1&gt;, to guide structure identification.) 

Moreover, it is allowed to only provide a tag and no section identifier. This allows capturing unnumbered sections such as &lt;h1&gt;Intro&lt;/h1&gt;.

It is also allowed to provide one (1) attribute beisde a tag, e.g., &lt;h1 class="abc"&gt; to make the resolution even more specific.

Here are valid path examples:

> /A/i/0/a

> /$us/$usc/a0/a0/a/0/A

> /$sr-finra/$2016/0/a/0/A/i

> /&lt;h1&gt;/&lt;h2&gt;0/a

> /$us/&lt;h1 class="blue"&gt;