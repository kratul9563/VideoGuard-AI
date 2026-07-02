
''' 
Main execution entry point for brand Guardian AI

This file is the "Control Center" that starts and manages the entire
compliance audit workflow. Think of it as the master switch that:
1. Set up the audit request
2. Runs the AI workflow
3. Display the final compliance report
'''
import uuid   ## Generates the unique ID (like session tracking number)
import json   ## Handle json data formatting (convert python dicts to readable text)
import logging  ## Records what happens during execution  (like a flight recorder)
from pprint import pprint     ### like pretty print data strcutures (unused here but available)


## Load enviornment variable from .env file
## This reads API Keys, database credentials etc. without hardcoding them 

from dotenv import load_dotenv
load_dotenv(override = True)  # overite True means .env values take priority over system variable

## import the main workflow graph (the brain of your compliance system )
from backend.src.graph.workflow import app
print("WORKFLOW IMPORTED")

##Config logging - sets up the "flight recorder" for your application
logging.basicConfig(
    level=logging.INFO,    ## INFO = show important 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    ## Format : timestamp - logger_name - severity - message
    ## Example : "2026-07-01 10:30:45" - brand guardian - INFO - starting audit
)

logger = logging.getLogger("brand-guardian-runner")   ## create a name logger for this module 

def run_cli_simulation():
    '''
    Simulates the video compliance audit request

    This funaction orchestrates the entire audit process
    - Creates a unique session ID
    - Prepares the video URL and metadata
    - Runs it through the AI workflow
    - Displays the compliance results
    '''

    # ===========  STEP - 1: Generate the session ID =============

    # Creates a unique identifier for this audit session
    # Example: "czZtYwWb-VOMP3FkXLmrW-g4rqxvW-XTyhdfkjhfjkhj"

    session_id = str(uuid.uuid4())  #uuid4() generates random UUID
    logger.info(f"Starting Audit Session : {session_id}")  ## Log to console/file


    # ============== STEP - 2: DEFINE INITIAL STATE ===============

    ## THIS DICTIONARY CONTAINS ALL THE INPUT DATA FOR THE WORKFLOW
    ## Think of it as the "intake form" for the compliance audit 

    initial_inputs = {
        # This YouTube video is audit
        "video_url" : "https://youtu.be/dT7S75eYhcQ",
        
        # Short video ID for easier tracking (first 8 character of session ID)
        # Ex- "vid_czZtYwWb"
        "video_id" : f"vid_{session_id[:8]}",

        # Empty list that will store compliance violations found
        "compliance_results" : [],

        ## Empty list for any errors during processing
        ## Ex- ["Download failed", "Transcript_unavailable"]
        "errors" : []
    }

    # ======== Display Section: Input Summary ==========

    print("\n----- 1. Initializing workflow.........")
    # json.dumps() converts python dict to formatted json string
    # indent = 2 makes it readable with 2-space indentation
    print(f"Input:\n{json.dumps(initial_inputs, indent=2)}")


    # ================= STEP - 3 EXECUTE GRAPH =============
    # This is where magic happens - runs the entire workflow 
    try:

        # app.invoke() trigger the langgraph workflow
        # it process it : START -> INDEXER -> AUDITOR -> END
        # Returns the final state with all results 
        final_state = app.invoke(initial_inputs)

        # ======= DISPLAY SECTION: EXECUTION COMPLETE =========
        print("\n----- 2. Workflow execution is complete......")

        # ================= ST EP - 3 OUTPUT RESULTS =============

        print("\n ==== Compliance Audit Report ==== ")
        # .get() safely retrives values (returs None if key doesn't exist)
        # Displays the Video Id that was audited
        print(f"Video ID : {final_state.get('video_id')}")

        # Show PASS or FAIL status
        print(f"Status : {final_state.get('final_status')}")

        # ===============  VIOLATION DETECTED =============
        print("\n [VIOLATIONS DETECTED]")

        # Extract the list compliance violations 
        # Default to empty list if no reults 
        results = final_state.get('compliance_results',[])

        if results:
            # Loop through each violations and display it
            for issue in results:
                # Each issue is a dict with: severity, category, description
                # Ex - "-[CRITICAL] Misleading Claims: Absoulte guarantee detected"
                print(f"- [{issue.get('severity')}] {issue.get('category')} : {issue.get('description')}")
        else:
            print("No violations detected........")


        # ===========  SUMMARY SECTION  =============
        print("\n[FINAL SUMMARY]")
        # Display the AI generated natural language summary
        # ex- "Video contains 2 critical violations... "
        print(final_state.get('final_report'))

    except Exception as e:
        logger.error(f"Workflow Execution has failed : {str(e)}")

        # Re-raise the exception so we see the full error traceback
        # This helps with debuging (shows exactly where / why it failed)
        raise e
    

# ================= PROGRAM ENTRY POINT =============
# This block only runs when you execute: python main.py
# It will not run if you import this file as a module

# if __name__ == "__main__":
#     run_cli_simulation()  ## staert the complkiance audit simulation


'''
You have moved from "coding" to "Product"

Ingestion: (YouTube -> Azure)

Indexing: (Speech-To-Text + OCR)

Retrieval: (Found the rules about claims)

Reasoning: (Applied rules to the specific claims in the video)

You are done. Your pipeline is fully operational

'''

