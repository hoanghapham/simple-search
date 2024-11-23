import os
import sys
import pytest


PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PARENT_DIR)

import helpers
from main import runner, search


@pytest.fixture(scope='module')
def database():
    db = helpers.Database('tests/data')
    return db


def test_runner_no_dir():
    with pytest.raises(Exception, match='No directory given to index') as e:
        runner([])
    

def test_search_no_match(database, capsys):
    search('invalid query', database)
    captured = capsys.readouterr()
    expected = "No matches found"
    assert captured.out.strip() == expected


def test_search_blank(database, capsys):
    search('', database)
    captured = capsys.readouterr()
    expected = 'No matches found'
    assert captured.out.strip() == expected


def test_search_one_term(database, capsys):
    search("five", database)
    captured = capsys.readouterr()
    expected = "file2.txt : 100.00%\nfile1.txt : 100.00%"
    assert captured.out.strip() == expected


def test_search_two_terms(database, capsys):
    search("five six", database)
    captured = capsys.readouterr()
    expected = "file2.txt : 100.00%\nfile1.txt : 50.00%"
    assert captured.out.strip() == expected


def test_search_three_terms(database, capsys):
    search("four five six", database)
    captured = capsys.readouterr()
    expected = "file2.txt : 66.67%\nfile1.txt : 66.67%"
    assert captured.out.strip() == expected