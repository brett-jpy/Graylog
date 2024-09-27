import requests
import json
import os
from requests.auth import HTTPBasicAuth

"""
Author: Brett
Purpose: Queries the Graylog API for available health metrics
"""

#####
# Global
#####
base_url = "http://192.168.1.12:9000{}"
headers = {"Content-Type": "application/json"}

graylog_endpoints = {"cluster_traffic": "/api/system/cluster/traffic?days=30&daily=true&includeToday=false", "load_balancer": "/api/system/lbstatus", "basic_system": "/api/system", 
                "jvm": "/api/system/jvm", "journal": "/api/system/journal", "metric_names": "/api/system/metrics/names", 
                "core_metrics": {"base": "/api/system/metrics/", "metric_names": ["org.graylog.plugins.cef.pipelines.rules.CEFParserFunction.parseTime",
                        "org.apache.logging.log4j.core.Appender.trace",
                        "org.apache.logging.log4j.core.Appender.debug",
                        "org.apache.logging.log4j.core.Appender.info",
                        "org.apache.logging.log4j.core.Appender.warn",
                        "org.apache.logging.log4j.core.Appender.error",
                        "org.apache.logging.log4j.core.Appender.fatal",
                        "org.graylog2.journal.entries-uncommitted",
                        "org.graylog2.shared.buffers.processors.ProcessBufferProcessor.processTime"]},
                "verify_compatability": "/api/system/searchVersion/satisfiesVersion/opensearch?version=2.4.0", "current_throughput": "/api/system/throughput", 
                "telemtry": "/api/telemetry"}

opensearch_endpoint = {"opensearch_health": "http://localhost:9200/_cluster/health?pretty"}

"""
These are 'skips' because they're either NOT json responses (i.e., load_balancer) or because they require an additional loop to work properly (i.e., core_metrics)
"""
common_skip = ["core_metrics", "metric_names", "load_balancer"]

#####
# Functions
#####
def mk_req(endpoint):
    r = requests.get(base_url.format(endpoint), headers=headers, auth=HTTPBasicAuth("admin", "password here")) # Should use token OR .netrc file
    return r

def mk_pretty(data):
    return json.dumps(data, indent=4)


#####
# Run
#####
k = graylog_endpoints.keys()

for item in k:
    if item not in common_skip:
        print(item)
        print(mk_pretty(mk_req(graylog_endpoints[item]).json()))
    elif item == "core_metrics":
        for name in graylog_endpoints[item]["metric_names"]:
            print(name)
            print(mk_pretty(mk_req("{}{}".format(graylog_endpoints[item]["base"], name)).json()))

