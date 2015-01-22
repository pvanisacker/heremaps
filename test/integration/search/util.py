import splunklib.results as results
from splunklib.client import connect


def return_first_result(service, search):
    response = service.jobs.oneshot(search)
    reader = results.ResultsReader(response)
    for result in reader:
        if isinstance(result, dict):
            return result

def create_connection():
    return connect(host="localhost", port=8089, username="admin", password="admin", app="heremaps")