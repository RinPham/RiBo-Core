import argparse
import pymongo
import json
import os
import sys
import fnmatch

##      ARGPARSE USAGE
##     <https://docs.python.org/2/howto/argparse.html>
parser = argparse.ArgumentParser(description="Import records into MongoDB")
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("max", type=int, help="the maximum records to import", default=sys.maxsize)
parser.add_argument("path", help="The input path for importing. This can be either a file or directory.")
parser.add_argument("db", help="The MongoDB name to import into.")
parser.add_argument("collection", help="The MongoDB collection to import into.")
args = parser.parse_args()

##      RETRIEVE files from filesystem
def getfiles(path):
    if len(path) <= 1:
        print("!Please Supply an Input File")
        return []
    try:
        input_path = str(path).strip()

        if os.path.exists(input_path) == 0:
            print("!Input Path does not exist (input_path = ", input_path, ")")
            return []

        if os.path.isdir(input_path) == 0:
            if args.verbose:
                print("*Input Path is Valid (input_path = ", input_path, ")")
            return [input_path]

        matches = []
        for root, dirnames, filenames in os.walk(input_path):
            for filename in fnmatch.filter(filenames, '*.json'):
                matches.append(os.path.join(root, filename))

        if len(matches) > 0:
            if args.verbose:
                print("*Found Files in Path (input_path = ", input_path, ", total-files = ", len(matches), ")")
            return matches

        print("!No Files Found in Path (input_path = ", input_path, ")")
    except ValueError:
        print("!Invalid Input (input_path, ", input_path, ")")
    return []


##     IMPORT records into mongo
def read(jsonFiles):
    from pymongo import MongoClient

    client = MongoClient('localhost', 27017)
    db = client[args.db]
    db[args.collection].remove({})
    counter = 0
    for jsonFile in jsonFiles:
        with open(jsonFile, 'r') as f:
            # for line in f:
            #     # load valid lines (should probably use rstrip)
            #     if len(line) < 10: continue
            #     try:
            #         db[args.collection].insert(json.loads(line))
            #         counter += 1
            data = f.read()
            jsondata = json.loads(data)
            try:
                db[args.collection].insert(jsondata)
                counter += 1
            except pymongo.errors.DuplicateKeyError as dke:
                if args.verbose:
                    print("Duplicate Key Error: ", dke)
            except ValueError as e:
                if args.verbose:
                    print("Value Error: ", e)

                    # friendly log message
            if 0 == counter % 100 and 0 != counter and args.verbose: print("loaded line: ", counter)
            if counter >= args.max:
                break
        f.close
    db.close

    if 0 == counter:
        print("Warning: No Records were Loaded")
    else:
        print("loaded a total of ", counter, " lines")


##      EXECUTE
files = getfiles(args.path)
read(files)