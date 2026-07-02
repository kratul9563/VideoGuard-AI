# azure opentelemetry integration

import os
import logging

from azure.monitor.opentelemetry import configure_azure_monitor

# creates a dedicated logger

logger = logging.getLogger("brand-guardian-telemetry")

def setup_telemetry():
    '''
    Initializes Azure Monitor opentelemetry
    Tracks: HTTP requests, database queries, errors, performance metrics
    Sends this data to azure monitor

    it autocapture every API requests
    No need to manually log each endpoint

    '''

    ## retrive the connection string 
    connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

    # check if comfigure
    if not connection_string:
        logger.warning("No instrumentation key found. Telemetry is Disabled")
        return
    
    # configure the azure monitor
    try:
        configure_azure_monitor(
            connection_string=connection_string,
            logger_name = "brand-guardian-tracer"
        )
        logger.info("Azure Monitor Tracking Enabled and Connected")
    except Exception as e:
        logger.error(f"Failed to Initial Azure Monitor: {e}")


'''
Why do we use telemetry ?

Without:
API is slow -> No idea which Part
How many users today ? No visibility

With:
/audit endpoint averages 4.5s (Indexer takes 3.8s)
Error logs show : 12% of audits fail due to youtube download errors
Metrics show: 450 API calls today, 89% success rate 
'''
