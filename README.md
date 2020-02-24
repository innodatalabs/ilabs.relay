# ilabs.relay
Utility GAE service that relays HTTP requiests to workers. Useful to diagnoze connectivity problems between GAE and workers.


## Running unit tests

First, create and activate virtual environment:

    python3.7 -m venv .venv
    . .venv/bin/activate
    pip install pytest -r requirements.txt
    pip install -t lib -r private_requirements.txt
    export PYTHONPATH=.:lib

## Running web application locally

    gunicorn -b :8000 endpoints.main:app


## Deploy to Google app engine

Please, use Linux machine with `python3.7` to do the deployment (or a virtual machine). The reason for this is to ensure that `pip` command below
picks right packages (otherwise there may be a mismatch between installed private packages and runtime environment in Google Cloud).

### Prepare private dependencies

Do this to populate `lib/` with required private dependencies:

    pip3.7 install -t lib -r private_requirements.txt

### Deploy app

Review the `app.yaml`, making sure that all settigns are correct.

Actually deploy the main app:

    gcloud app deploy --no-promote

To make sure that GAE engine is up, query GAE's `/ping` endpoint:

    curl https://{{GAE-ADDRESS}}/ping


## Use the GAE to ping workers

Every worker responds to `/ping` endpoint with `pong` message.

    curl https://{{GAE-ADDRESS}}/relay/{{ADDRESS}}/ping

Here `{{ADDRESS}}` is the IP address of the worker. GAE will issue an HTTP (not HTTPS!) GET request to that address and url.

You can also request other websites, for example

    curl https://{{GAE-ADDRESS}}/relay/google.com


