# Constants for Project

# Constants for TASKS
TASK1_CONST = "TASK1"
TASK2_CONST = "TASK2"
TASK3A_CONST = "TASK3A"
TASK3B_CONST = "TASK3B"
LUCENE = "LUCENE"
LUCENE_RESULTS = "LUCENE-RESULTS"
LUCENE_RESULTS_SNIPPETS = "LUCENE-RESULTS-SNIPPETS"

# DIR names for CACM data and stemmed data
CACM_FOLDER = "CACM"
CACM_DATA = "CACM-DATA"
CACM_STEMMED_FILES_FOLDER = "CACM-STEMMED-DATA"
CACM_STEMMED_FILE_NAME = "CACM-"

# File names for cacm files
CACM_QUERY_FILE = CACM_FOLDER + "/" + "cacm.query"
CACM_REL_FILE = CACM_FOLDER + "/" + "cacm.rel"
CACM_STEM_QUERY_FILE = CACM_FOLDER + "/" + "cacm_stem.query"
CACM_STEM_FILE = CACM_FOLDER + "/" + "cacm_stem"
CACM_COMMON_WORDS = CACM_FOLDER + "/" + "common_words"

# Folder name for storing parsed and tokenized files
DIR_FOR_TOKENIZED_FILES = "TOKENIZED-DATA"

# Directory for output files
DIR_FOR_OUTPUT_FILES = "OUTPUT"

# Extension for files
FILE_EXT = ".txt"
CSV_FILE_EXT = ".csv"
HTML_FILE_EXT = ".html"

# File names for Retrieval Modules Output
FILE_NAME_PREFIX_FOR_RM_OUTPUT = "DOCUMENTS_RANKED_FOR_QUERY"
# FILE_NAME_PREFIX_FOR_TFIDF_OUTPUT = "DOCUMENTS_RANKED_FOR_QUERY"

# Name for file containing queries extracted from given queries
FILE_FOR_QUERIES = "Querylist"

# Constants for Retrieval Models
CONST_FOR_BM25 = "BM25"
CONST_FOR_TFIDF = "TFIDF"

# DIR FOR Retrieval Modules Output files
DIR_FOR_BM25_OUTPUT = "BM25_RESULTS"
DIR_FOR_TFIDF_OUTPUT = "TFIDF_RESULTS"

# Index file names for indexes generated
FILE_FOR_INDEX = "INDEX"
FILE_FOR_STOPPED_INDEX = "STOPPED_INDEX"
FILE_FOR_STEMMED_INDEX = "STEMMED_INDEX"

# File for word counts by file for indexes
FILE_FOR_WORD_COUNTS_BY_FILE_FOR = "WORD_COUNTS_BY_FILE_FOR_"

# File name for doc frequency table
FILE_FOR_DOC_FREQ_TABLE = "DOC_FREQ_TABLE_FOR"

CONSTS_FOR_UNIGRAM = "_UNIGRAM"
CONSTS_FOR_BIGRAM = "_BIGRAM"
CONSTS_FOR_TRIGRAM = "_TRIGRAM"

# Constant for total no. of relevant documents for retrieval models
NO_OF_REL_DOCS_FOR_RM = 100

# Constant for no. of top records to be extracted from retrieval modules
NO_OF_TOP_DOCS_FROM_RM = 50

# Constant for no. of top terms to be used in query expansion
NO_OF_TOP_TERMS_FOR_QUERY_EXPANSION = 20

# Constant for system names
SYSTEM_NAME_CONST = "SYSTEM-"

# Constant for evaluation folder
EVALUATION_FOLDER = "EVALUATION_RESULTS"

# Constant for snippet generation results folder
SNIPPET_GEN_RESULTS_FOLDER = "SNIPPETS_GENERATION_RESULTS_FOR_"

# Constant for snippets file for a query
SNIPPETS_FOR_QUERY = "SNIPPETS_FOR_QUERY_"

# Constant for mean values file
FILE_FOR_ALL_SYSTEMS_MEAN_VALUES = "ALL_SYSTEMS_MEAN_VALUES"

# Constant for file for precision and recall values of a system
FILE_FOR_PRECISON_RECALL_RESULTS_OF_SYSTEM = "PRECISION_RECALL_VALUES_OF_"

# Constant for file for p@5 and p@20 values of a system
FILE_FOR_PATK_RESULTS_OF_SYSTEM = "P@K_VALUES_OF_"

# Constant for average precision values file
FILE_FOR_ALL_SYSTEMS_AVG_PRECISION_VALUES = "ALL_SYSTEMS_AVG_PRECISION_VALUES"

# Constant for file indicating t-test results
FILE_FOR_ALL_SYSTEMS_T_TESTS_RESULTS = "ALL_SYSTEMS_T_TESTS_RESULTS"

# Constant for MEAN Values identifiers
MAP_CONST = "MAP"
MRR_CONST = "MRR"
PAT5_CONST = "P@5"
PAT20_CONST = "P@20"

# Constant for stemmed queries indexes in query list
INDEXES_FOR_STEMMED_QUERIES = [12, 13, 19, 23, 24, 25, 50]

# Constant for system names
SYSTEM_NAME_DEFAULT = "SYSTEM"
SYSTEM_FIRST = "BM25-Baseline"
SYSTEM_SECOND = "TFIDF-Baseline"
SYSTEM_THIRD = "Lucene-Baseline"
SYSTEM_FOURTH = "BM25-QueryExpansion"
SYSTEM_FIFTH = "TFIDF-QueryExpansion"
SYSTEM_SIXTH = "BM25-Stopping"
SYSTEM_SEVENTH = "TFIDF-Stopping"

# Constant for alpha value for t-tests
ALPHA_VALUE_FOR_T_TESTS = 0.05