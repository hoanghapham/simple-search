"""Module containing all helper classes and functions"""

import re
import os
import math

SPLITTERS = "\n|\t| |-"
SYMBOLS = ",|;|:|.|!|?|\"|%|$|&"


def tokenize(text: str) -> list:
    """Simple tokenizer: split the sentence using some common delimiters, then lower and strip special symbols."""
    tokens = [w.lower().strip(SYMBOLS) for w in re.split(SPLITTERS, text) if w != '']

    return tokens


class Database():
    """Representation of the folder as an in-memory database"""
    def __init__(self, folder) -> None:
        self.data = self.index(folder)
        self.files_word_count = count_words(folder)
        self.n_files = len(self.files_word_count)

    def index(self, folder: str) -> dict:
        """Read text files in the folder, tokenize, and return a dictionary acting as the database
        """
        dta: dict = {}

        for file in os.listdir(folder):
            with open(os.path.join(folder, file), 'r') as f:
                for line in f.readlines():
                    words = tokenize(line)
                    
                    for word in words:
                        if word not in dta:
                            dta[word] = {}
                            dta[word][file] = 1
                        else:
                            dta[word][file] = dta[word].get(file, 0) + 1
        return dta


def count_words(folder: str) -> dict:
    """Count words in files"""
    files: dict = {}

    for file_name in os.listdir(folder):
        with open(os.path.join(folder, file_name), 'r') as f:
            for line in f.readlines():
                words = tokenize(line)
                files[file_name] = files.get(file_name, 0) + len(words)
    
    return files


def search_files(query_tokens: list, database: Database) -> dict:
    """Go through each token in query_tokens, get entries from the database"""
    search_result = {}
    
    for token in query_tokens:
        search_result[token] = database.data.get(token, {})
    
    assert len(query_tokens) == len(search_result)

    return search_result


def rank_by_matched(search_result: dict) -> dict:
    """Rank search result by number of matched tokens"""
    result: dict = {}

    for token, files in search_result.items():
        for file in files:
            result[file] = result.get(file, 0) + 1
    
    sorted_files = dict(sorted(result.items(), key=lambda x: x[-1], reverse=True))
    
    return sorted_files


def calc_term_tf_idf(search_result: dict, database: Database) -> dict:
    """Calculate TF-IDF score of each term in the search query"""
    result: dict = {}

    for term, matched_files in search_result.items():
        result[term] = {}

        for file_name, term_count in matched_files.items():
            tf = term_count / database.files_word_count.get(file_name)
            idf = math.log((database.n_files + 1) / (len(matched_files) + 1))    
            result[term][file_name] = tf*idf
        
    return result


def rank_by_tf_idf(search_result: dict, database: Database, top=10):
    """Rank search results by total TF-IDF score of its matched query terms"""
    n_query_tokens = len(search_result)

    # Return matched files ordered by number of matched tokens
    matched_tokens_count = rank_by_matched(search_result)

    # Calculate TF-IDF for each term in a document
    term_tf_idf = calc_term_tf_idf(search_result, database)

    # For each file, file score = sum(TF-IDF of all matched terms)
    file_score: dict = {}

    for term, files in term_tf_idf.items():
        for file_name in files:
            file_score[file_name] = file_score.get(file_name, 0) + term_tf_idf[term][file_name]

    # Sorting
    # Group files by number of matched words
    file_groups: dict = {}

    for file, matched_tokens in matched_tokens_count.items():
        if matched_tokens not in file_groups:
            file_groups[matched_tokens] = {}
        file_groups[matched_tokens][file] = file_score.get(file)

    # Go through each group, sort files in group by TF-IDF score
    sorted_results = []

    for group, files in file_groups.items():
        sorted_files = sorted(files.items(), key=lambda x: x[-1], reverse=True)

        for file, score in sorted_files:
            sorted_results.append((file, group / n_query_tokens, score))
            
    return sorted_results[:top]

