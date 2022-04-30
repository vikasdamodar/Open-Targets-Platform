# Open-Targets-Platform
The key features of the Platform is our target-disease associations, which are unique target-disease pairs that are supported by one or more pieces of evidence (JSON objects) that connect the two entities.


# Prerequisite

* Pandas Library

    Install using "pip install pandas"
 
* Other libraries:

     ftplib
     
     datetime
     
     multiprocessing
     
     io.BytesIO
     
 # Working Documentation
 
 * Can be downloaded all evidence json files using "download_evidence_files.py" script.
 * Can be downloaded all targets json files using "download_targets_files.py" script.
 * Can be downloaded all disease json files using "download_disease_files.py" script.
 
 * Parsing and processing all files will perform by "parse_and_process_data.py" script.
 * All the results and actions mentioned in the task will be performed here and will print the result.
 * Using pandas DataFrame to process json files and ftplib to download files from FTP Sever

# Assumptions

* Tasks 3-5 performed on the grouped Dataset since it's grouping for the score actions.
* The last task (extended) performed on the main data set and from the question assuming that "to find count of targets which are associated to atleast two deseases"

# Challenges
* Downloading files from FTP server with same piece of code throws different errors from socket.
* setting different "CWD" in the same method causes connection error.
* FTP connection defined one place is not fetching files in other/child methods.
* Getting "too many connections" error when downloading all files with same class.
* ___Thus solution added by adding download with different scripts___

