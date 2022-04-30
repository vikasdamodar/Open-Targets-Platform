import datetime

import pandas as pd
import json
import statistics
import datetime

def parse_and_process_files():
    print("Parsing evidence json file.....")
    # Parsing evidence json values to DF by chucks because of large size
    evidence_dfs = pd.read_json("evidence.json", lines=True, chunksize=25000)
    # Concatinating all chunks of DFs
    evidence_dfs_combined = pd.concat(evidence_df[['diseaseId', 'targetId', 'score']] for evidence_df in evidence_dfs)

    # finding list of score values for each deseaseID and targetID pair
    format_evidence_df = evidence_dfs_combined.groupby(['diseaseId','targetId'])['score'].apply(list).reset_index()

    print("Processing evidence file.....")
    # Finding median of score
    format_evidence_df['medianScore'] = format_evidence_df['score'].apply(statistics.median)
    # Finding 3 greatest score values
    format_evidence_df['3greatestScore'] = format_evidence_df['score'].apply(lambda x: sorted(x, reverse=True)[:3])

    print("Parsing and processing targets json file......")
    # Importing all targets from targets json file by chunks
    target_dfs = pd.read_json("targets.json", lines=True, chunksize=25000)
    # Concatinating all chunk DFs to one
    target_df_ed  = pd.concat(target_df[['id', 'approvedSymbol']] for target_df in target_dfs)
    # Merging target DF to Evidence DF based on IDs
    joined_df = format_evidence_df.merge(target_df_ed[['id', 'approvedSymbol']], how='left', left_on='targetId', right_on='id')

    print("Parsing and processing desease json file......")
    # Importing all deseases from json file to DF
    desease_df = pd.read_json("deseases.json", lines=True)
    # Merge deseases to evidence DF based on IDs
    joined_df = joined_df.merge(desease_df[['id', 'name']], how='left', left_on='diseaseId', right_on='id')
    joined_df = joined_df.sort_values(by=['medianScore'])

    print("Converting final result to json file......")
    # Converting the dataframe to json file with only required fields
    joined_df[['diseaseId', 'targetId', 'score', 'medianScore','3greatestScore', 'approvedSymbol', 'name']].to_json(
        "result_table.json", orient='records', lines=True)
    print("Successfully completed file processing.\n")

    print("Extended processing to find count of target pairs sharing at least two deseases.")
    evidence_dfs_combined2 = evidence_dfs_combined[
        ['diseaseId', 'targetId']].groupby(['targetId'])['diseaseId'].apply(list).reset_index()
    targer_pair_count = evidence_dfs_combined2[evidence_dfs_combined2['diseaseId'].map(len) >= 2].shape[0]
    print("Count of target-target pairs share a connection to at least two diseases: ", targer_pair_count)
    return



if __name__ == '__main__':
    parse_and_process_files()
