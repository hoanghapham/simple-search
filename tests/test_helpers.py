import os
import sys
import math
from pytest import fixture

PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PARENT_DIR)

import helpers

DATA_FOLDER = 'tests/data'

def test_tokenize():
    text = "This is a Test text, a part of a test"
    tokens = helpers.tokenize(text)

    assert tokens == ['this', 'is', 'a', 'test', 'text', 'a', 'part', 'of', 'a', 'test']

@fixture(scope='module')
def database():
    db = helpers.Database(DATA_FOLDER)
    return db

def test_count_words():
    files_word_count = helpers.count_words(DATA_FOLDER)
    expected = {
        'file1.txt': 6,
        'file2.txt': 5
    }
    assert files_word_count == expected

def test_search_files_one_word(database):
    query = "five"
    tokens = helpers.tokenize(query)
    result = helpers.search_files(tokens, database)
    expected = {
        'five': {'file1.txt': 2, 'file2.txt': 1}
    }
    assert result == expected

def test_search_files_two_words(database):
    query = "five six"
    tokens = helpers.tokenize(query)
    result = helpers.search_files(tokens, database)
    expected = {
        'five': {'file1.txt': 2, 'file2.txt': 1},
        'six': {'file2.txt': 1}
    }
    assert result == expected

def test_search_files_zero_word(database):
    query = ""
    tokens = helpers.tokenize(query)
    result = helpers.search_files(tokens, database)
    expected = {}
    assert result == expected

def test_search_files_no_match(database):
    query = "invalid query"
    tokens = helpers.tokenize(query)
    result = helpers.search_files(tokens, database)
    expected = {'invalid': {}, 'query': {}}
    assert result == expected


def test_rank_by_matched_non_empty(database):
    query = "five six"
    tokens = helpers.tokenize(query)
    search_result = helpers.search_files(tokens, database)
    rank_result = helpers.rank_by_matched(search_result)
    expected = {
        'file2.txt': 2,
        'file1.txt': 1
    }
    assert rank_result == expected

def test_rank_by_matched_empty(database):
    query = "invalid query"
    tokens = helpers.tokenize(query)
    search_result = helpers.search_files(tokens, database)
    rank_result = helpers.rank_by_matched(search_result)
    expected = {}
    assert rank_result == expected

def test_calc_term_tf_idf(database):
    query = "four five six"
    tokens = helpers.tokenize(query)
    search_result = helpers.search_files(tokens, database)
    term_tf_idf = helpers.calc_term_tf_idf(search_result, database)

    expected = {
        'four': {'file1.txt': 1/6 * math.log(3/2)},
        'five': {'file1.txt': 0.0, 'file2.txt': 0.0},
        'six': {'file2.txt': 1/5 * math.log(3/2)}
    }
    assert term_tf_idf == expected


def test_rank_by_tf_idf_non_empty(database):
    query = "four five six"
    tokens = helpers.tokenize(query)
    search_result = helpers.search_files(tokens, database)

    result = helpers.rank_by_tf_idf(search_result, database)
    expected = [
        ('file2.txt', 2/3, 0.0 + 0.0 + 1/5 * math.log(3/2)),
        ('file1.txt', 2/3, 1/6 * math.log(3/2) + 0.0 + 0.0)
    ]
    assert result == expected


def test_rank_by_tf_idf_empty(database):
    query = "invalid query"
    tokens = helpers.tokenize(query)
    search_result = helpers.search_files(tokens, database)

    result = helpers.rank_by_tf_idf(search_result, database)
    expected = []
    assert result == expected