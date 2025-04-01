#!/usr/bin/env python3
import json
import glob
from collections import Counter
from DataFormats.FWLite import Lumis
from tqdm import tqdm


# Function to group sorted lumi numbers into contiguous ranges
def group_contiguous(lumiDict):
    for run in lumiDict:
        lumi_list = lumiDict[run]
        lumi_list = sorted(set(lumi_list))
        if not lumi_list:
            return []
        ranges = []
        start = prev = lumi_list[0]
        for lumi in lumi_list[1:]:
            if lumi == prev + 1:
                prev = lumi
            else:
                ranges.append([start, prev])
                start = prev = lumi
        # Append the final range
        ranges.append([start, prev])
        lumiDict[run] = ranges
    # return lumiDict           ## modifies in-place.

def check_duplicates(lumiDict):
    """Check for duplicates in the lumi list for each run"""
    print("\nChecking for duplicates...")
    duplicates_info = {}

    for run, lumi_list in lumiDict.items():
        counter = Counter(lumi_list)
        
        duplicates = {lumi: count for lumi, count in counter.items() if count > 1}
        if duplicates:
            duplicates_info[run] = duplicates

    if duplicates_info:
        print("Duplicate lumi sections found:")
        for run, dups in duplicates_info.items():
            print(f"Run {run}:")
            for lumi, count in dups.items():
                print(f"  Lumi {lumi} appears {count} times.")
        raise ValueError("Duplicates found in luminosity sections, please check your input files.")
    else:
        print("No duplicates found. Check O.K. ☑️\n")

def format_like_golden(lumiDict):
    """Convert run numbers to strings (JSON keys are usually strings)"""
    lumiDict_str_keys = { str(run): ranges for run, ranges in lumiDict.items() }
    return lumiDict_str_keys


def main(glob_patterns, output):
    """
    Iterates over a directory of MiniAODs, accumulates the luminostiy blocks and run numbers in a dictionary.
    """
    files = []
    for pattern in glob_patterns:
        files.extend(glob.glob(pattern, recursive=True))
    
    
    lumiDict = {}
    for lumi in tqdm(Lumis(files)):
        run = lumi.luminosityBlockAuxiliary().run()
        lumiSection = lumi.luminosityBlockAuxiliary().luminosityBlock()
        
        # Initialize the list if the run is not yet in the dictionary
        if run not in lumiDict:
            lumiDict[run] = []
        lumiDict[run].append(lumiSection)


    check_duplicates(lumiDict)
    group_contiguous(lumiDict)

    lumiDict_str_keys = format_like_golden(lumiDict)


    # Write the result to a JSON file in a format similar to a Golden JSON
    with open(output, "w") as jsonFile:
        json.dump(lumiDict_str_keys, jsonFile, indent=1)
    print("Aggregated JSON file has been saved as aggregatedLumis.json")

    # Pretty print
    # for key, value in lumiDict_str_keys.items():
    #     print(f"'{key}': {value}")

if __name__ == '__main__':
    patterns = ['/eos/vbc/experiments/cms/store/user/aguven/JetMET0/Run2023B0_mini_v1/**/*.root',
                '/eos/vbc/experiments/cms/store/user/aguven/JetMET1/Run2023B1_mini_v1/**/*.root',
                '/eos/vbc/experiments/cms/store/user/aguven/JetMET0/Run2023C0_mini_v1/**/*.root',
                '/eos/vbc/experiments/cms/store/user/aguven/JetMET1/Run2023C1_mini_v1/**/*.root',
                '/eos/vbc/experiments/cms/store/user/aguven/JetMET0/Run2023D0_mini_v1/**/*.root',
                '/eos/vbc/experiments/cms/store/user/aguven/JetMET1/Run2023D1_mini_v1/**/*.root',]

    output = "aggregatedLumis.json"
    main(patterns, output)

