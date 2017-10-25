import sys
import Task1
import Task2
import Task3A
import Task3B
import evalTask
from snippetGenerator import *

# read command line params for data files folder
input_arguments = sys.argv[:]
ldatafilesdir = CACM_DATA
if len(input_arguments) > 1:
    ldatafilesdir = input_arguments[1]

# read command line params for stemmed data file
lstemmeddatafile = CACM_STEM_FILE + FILE_EXT
if len(input_arguments) > 2 :
    lstemmeddatafile = input_arguments[2]

# Tokenize raw text
tokenize_raw_data(ldatafilesdir)

# Write given queries to a file
create_directory(DIR_FOR_OUTPUT_FILES)
write_given_queries_to_file(CACM_QUERY_FILE + FILE_EXT, DIR_FOR_OUTPUT_FILES + "/" + FILE_FOR_QUERIES + FILE_EXT)

Task1.execute_system(ldatafilesdir)
Task2.execute_system(ldatafilesdir)
Task3A.execute_system(ldatafilesdir)
Task3B.execute_system(lstemmeddatafile)

ldictoffolderpaths = {}
ldictoffolderpaths[1] = DIR_FOR_OUTPUT_FILES + "/" + TASK1_CONST + "/" + DIR_FOR_BM25_OUTPUT
ldictoffolderpaths[2] = DIR_FOR_OUTPUT_FILES + "/" + TASK1_CONST + "/" + DIR_FOR_TFIDF_OUTPUT
ldictoffolderpaths[3] = LUCENE + "/" + LUCENE_RESULTS
ldictoffolderpaths[4] = DIR_FOR_OUTPUT_FILES + "/" + TASK2_CONST + "/" + DIR_FOR_BM25_OUTPUT
ldictoffolderpaths[5] = DIR_FOR_OUTPUT_FILES + "/" + TASK2_CONST + "/" + DIR_FOR_TFIDF_OUTPUT
ldictoffolderpaths[6] = DIR_FOR_OUTPUT_FILES + "/" + TASK3A_CONST + "/" + DIR_FOR_BM25_OUTPUT
ldictoffolderpaths[7] = DIR_FOR_OUTPUT_FILES + "/" + TASK3A_CONST + "/" + DIR_FOR_TFIDF_OUTPUT

# Evaluate all systems
evalTask.evaluate_all_systems(ldictoffolderpaths, False)

# Generate snippets for systems
generate_snippets_for_systems()

print "All tasks successfully run."