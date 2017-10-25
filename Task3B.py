from tokenizer import Tokenizer
from indexer import Indexer
import time
from RMBase import RMBase
from snippetGenerator import *


def execute_system(p_stemmeddatafile,
                   p_tokenizefiles=True,
                   p_createindex=True,
                   p_createsnippets=False):

    print "Executing Task 3B..."
    startTime = time.time()

    lstemmeddatafile = CACM_STEM_FILE + FILE_EXT
    if is_string_valid(p_stemmeddatafile):
        lstemmeddatafile = lstemmeddatafile

    # Convert stemmed data to files
    # print "Convert stemmed data to files"
    split_cacm_stem_file_into_files(lstemmeddatafile)

    ldatafilesdir = CACM_STEMMED_FILES_FOLDER

    # Create output directory
    create_directory(DIR_FOR_OUTPUT_FILES)
    ldirpathfortask = DIR_FOR_OUTPUT_FILES + "/" + TASK3B_CONST
    create_directory(ldirpathfortask)

    # Variable for no of documents
    NoOfDocuments = get_no_of_files_in_dir(ldatafilesdir)

    ltokenizedfilesdir = ldirpathfortask + "/" + DIR_FOR_TOKENIZED_FILES
    if p_tokenizefiles:
        t1 = time.time()
        # create tokenizer and generate token documents
        ltokenizer = Tokenizer()
        ltokenizer.setTokenizedFilesOutputDir(ltokenizedfilesdir)
        ltokenizer.tokenizedir(ldatafilesdir)
        t2 = time.time()
        # print "Time for Tokenizer Module: " + str(t2-t1)

    if p_createindex:
        t1 = time.time()
        # create instance of Indexer class and create indexes
        lindexer = Indexer()
        lindexer.set_tokenized_files_dir(ltokenizedfilesdir)
        lindexer.setOutputDirectory(TASK3B_CONST)
        lindexer.startIndexing(False, True)
        lindexer.printAll()
        t2 = time.time()
        # print "Time for Indexer Module: " + str(t2-t1)

    # Convert query list to query dict
    lquerydict = get_given_queries_in_dict_with_given_keys(CACM_STEM_QUERY_FILE + FILE_EXT, INDEXES_FOR_STEMMED_QUERIES)
    lquerydict = get_sorted_dict(lquerydict)

    t1 = time.time()
    lrm = RMBase()
    # Set the no. of documents with the retrieval module
    lindexfilename = ldirpathfortask + "/" + FILE_FOR_STEMMED_INDEX + FILE_EXT
    ldocfreqtableforunigramfilename = ldirpathfortask + "/" + FILE_FOR_DOC_FREQ_TABLE + CONSTS_FOR_UNIGRAM + FILE_EXT
    lwordcountsbyfilefilename = ldirpathfortask + "/" + FILE_FOR_WORD_COUNTS_BY_FILE_FOR + FILE_FOR_STEMMED_INDEX + FILE_EXT

    lrm.setNoOfDocuments(NoOfDocuments)
    lrm.setOutputDirectory(TASK3B_CONST)
    lrm.setCanUseRelevanceInfo(True)
    lrm.isStemmedIndex(True)
    lrm.setIndexFileName(lindexfilename)
    lrm.setDocFreqDictFileName(ldocfreqtableforunigramfilename)
    lrm.setWordCountsByFileDictFileName(lwordcountsbyfilefilename)

    lrm.initializeRM()
    # Process all the queries for the retrieval module
    lrm.processQueriesFromFile(lquerydict, False)
    t2 = time.time()
    # print "Time for Retrieval Module: " + str(t2-t1)

    endTime = time.time()
    print "Task 3B execution completed in " + str(endTime - startTime)

    if p_createsnippets:
        # Generate snippets for BM25 output
        generate_snippet(CACM_STEM_QUERY_FILE + FILE_EXT,
                         ldirpathfortask + "/" + DIR_FOR_BM25_OUTPUT,
                         ldirpathfortask + "/" + SNIPPET_GEN_RESULTS_FOLDER + CONST_FOR_BM25,
                         True)

        # Generate snippets for TF-IDF output
        generate_snippet(CACM_STEM_QUERY_FILE + FILE_EXT,
                         ldirpathfortask + "/" + DIR_FOR_TFIDF_OUTPUT,
                         ldirpathfortask + "/" + SNIPPET_GEN_RESULTS_FOLDER + CONST_FOR_TFIDF,
                         True)



