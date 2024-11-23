"""Main program"""

import sys
from helpers import Database, tokenize, search_files, rank_by_tf_idf, SPLITTERS, SYMBOLS


def search(query, database):
    """main search func"""
    query_tokens = tokenize(query)
    search_result = search_files(query_tokens, database)

    if all([x == {} for x in search_result.values()]):
        print("No matches found")

    else:
        ranked_results = rank_by_tf_idf(search_result, database, top=10)

        for file, pct, tf_idf in ranked_results:
            print(f"{file} : {pct:.2%}")


def runner(args):
    """Run the search function"""

    if len(args) == 0:
        raise Exception('No directory given to index')

    indexable_directory = args[0]
    database = Database(indexable_directory)

    while True:
        query = input("search> ")
        
        if query.strip(SPLITTERS + '|' + SYMBOLS) == '':
            continue

        if query == ":quit":
            break

        search(query, database)
        print("\n")


if __name__ == '__main__':
    args = sys.argv[1:]
    runner(args)


