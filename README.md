# Simple text search tool


## Usage
To use the search tool, run:

```bash
python main.py data
```
where `data` is the path to the folder containing some text files. After that, you can start typing in your search queries, and press Enter to search.

To quit, type `:quit` and press Enter.


## How it works
1. At the start, the tool will read files within the folder, tokenize the file content, and store it in a dictionary as an in-memory database
2. When receiving a query, the tool will tokenize the query string, iterate over the query tokens and search for files containing that token
3. Output files will be printed out as follow:
    - First, the files are sorted in descending order by the number of matched tokens
    - Next, if two files have the same number of matched tokens, sort them in descending order by the "file score"
4. The "file score" is the sum of TF-IDF scores of all tokens matched by the file. TF-IDF of each token is calculated as TF*IDF, where:
    - TF = count of that token in the file / total word count of the file
    - IDF = (number of files in folder + 1) / (number of matched documents + 1)
    (Added 1 to avoid division by zero error)


## Folder structure
- `main.py`: Containing the script to run the search tool
- `helpers.py`: Module containing helper classes and functions
- `tests/`: folder containing tests for the `main` and `helpers` modules


## Test
Assuming that you already have the `pytest` package installed, simply run this at the current folder:

```bash
pytest . -vvv
```

