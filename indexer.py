# coding: utf-8
from indexerUtils import *
import collections
from collections import OrderedDict
from consts import *


# indexer Class
class Indexer:

    def __init__(self):

        self.ftotalunigramtokens = 0
        self.ftotalbigramtokens = 0
        self.ftotaltrigramtokens = 0

        self.fdictforunigramtokensbyfile = {}
        self.fdictforbigramtokensbyfile = {}
        self.fdictfortrigramtokensbyfile = {}

        self.fdictforunigramindex = {}
        self.fdictforbigramindex = {}
        self.fdictfortrigramindex = {}

        self.ftokenizedfilesdir = ""
        self.foutputdirname = ""

        self.fcanperformstopping = False
        self.fstoplist = []

        self.fisstemmedindex = False

        self.fcangeneratebigramindex = False
        self.fcangeneratetrigramindex = False

    def createindexes(self, p_TokenizedFilesDir):

        # get list of files from directory
        llistoffiles = get_list_of_files_from_dir(p_TokenizedFilesDir)

        llistoffinaltokenizeddocids = []
        # get list of doc ids
        for lfile in llistoffiles:
            lfileval = os.path.splitext(lfile)[0]
            llistoffinaltokenizeddocids.append(lfileval)

        # ldictfortokenizedfilemap = convert_data_from_file_to_dictionary(FILE_FOR_URL_TOKENIZED_DATA_MAPPING+FILE_EXT)
        # llistoffinaltokenizeddocids = convert_data_from_file_to_collection(FILE_FOR_URL_TOKENIZED_DATA_MAPPING+FILE_EXT)

        # sort dictionary by key
        # ldictfortokenizedfilemap = OrderedDict(sorted(ldictfortokenizedfilemap.iteritems()))
        llistoffinaltokenizeddocids.sort()

        self.ftotalwordscount = 0

        ltempcount = 0

        # while ltempcount < 2:
        # for ldocidkey, ldocidllist in ldictfortokenizedfilemap.iteritems():
        for ldocid in llistoffinaltokenizeddocids:

            # ldocid = ldocidllist[0]
            lfilename = ldocid + FILE_EXT
            lfilenamewithpath = self.ftokenizedfilesdir + "/" + lfilename

            if not os.path.exists(lfilenamewithpath):
                continue

            with open(lfilenamewithpath) as lfile:
                # remove whitespace characters like `\n` at the end of each line
                lfiledatastring = " ".join(line.strip() for line in lfile.readlines()).lower()

            # get the word list for the file
            lwordlist = lfiledatastring.split(' ')

            # update the unigram index for this file
            self.update_index(self.fdictforunigramindex, 1, lwordlist, ldocid, self.fdictforunigramtokensbyfile)

            if self.fcangeneratebigramindex:
                # update the bigram index for this file
                self.update_index(self.fdictforbigramindex, 2, lwordlist, ldocid, self.fdictforbigramtokensbyfile)

            if self.fcangeneratetrigramindex:
                # update the trigram index for this file
                self.update_index(self.fdictfortrigramindex, 3, lwordlist, ldocid, self.fdictfortrigramtokensbyfile)

        # process after all indexes are created
        self.processafterindexcreation()

    def update_index(self, p_index, p_indexind, p_wordlist, p_filename, p_dictfortokensbyfile):

        # get the ngrams dict for the wordlist
        lngrams = self.get_ngrams(p_wordlist, p_indexind)

        # iterate over the ngrams and update the entries in the index
        for key, value in lngrams.iteritems():
            # key is the word - unigram, bigram or trigram
            # value is the frequency of occurrence
            if key not in p_index:
                # create a dict as value for the key and
                # add the filename and frequency of occurence in a dict
                ldictforkey = {}
                ldictforkey[p_filename] = value
                # update index with key and its dict
                p_index[key] = ldictforkey
            else:
                # get the dict for the key which is a dict of filename and frequency of key
                ldictforkey = p_index[key]
                # add entry for filename in the dict for key if not already there
                if p_filename not in ldictforkey:
                    ldictforkey[p_filename] = value
                else:
                    # update the entry with new value if already present
                    ldictforkey[p_filename] += value

        # get the count of the no. of tokens in file
        # lwordcountforfile = len(lngrams)
        lwordcountforfile = sum(lngrams.itervalues())

        if p_indexind == 1:
            self.ftotalunigramtokens += lwordcountforfile
        elif p_indexind == 2:
            self.ftotalbigramtokens += lwordcountforfile
        elif p_indexind == 3:
            self.ftotaltrigramtokens += lwordcountforfile

        # update dictionary for maintaining word count per file
        p_dictfortokensbyfile[p_filename] = lwordcountforfile

    def get_ngrams(self, p_wordlist, p_indexind):

        # get the list of tuples for the words as per specified ngram index
        llistofngrams = zip(*[p_wordlist[litem:] for litem in range(p_indexind)])

        # convert the tuples to str for saving as key in dict
        llistofngrams = [" ".join(x) for x in llistofngrams]

        # If set by invoker to perform stopping, remove stopwords before indexing
        if self.fcanperformstopping:
            lstoplist = get_stop_list()
            if len(lstoplist) > 0:
                llistofngrams = [x for x in llistofngrams if x not in lstoplist]

        # generate the dictionary of ngrams
        ldictofwordsbyfreq = collections.Counter(llistofngrams)

        return ldictofwordsbyfreq

    def processafterindexcreation(self):

        # sort all indexes and dictionaries
        # sort all dictionaries for all items in indexes
        for key, value in self.fdictforunigramindex.iteritems():
            value = OrderedDict(sorted(value.iteritems()))

        # sort unigram index dictionary by key
        self.fdictforunigramindex = OrderedDict(sorted(self.fdictforunigramindex.iteritems()))

        # sort dictionary for word count by file for unigram index
        self.fdictforunigramtokensbyfile = OrderedDict(sorted(self.fdictforunigramtokensbyfile.iteritems()))

        if self.fcangeneratebigramindex:
            for key, value in self.fdictforbigramindex.iteritems():
                value = OrderedDict(sorted(value.iteritems()))

            # sort bigram index dictionary by key
            self.fdictforbigramindex = OrderedDict(sorted(self.fdictforbigramindex.iteritems()))

            # sort dictionary for word count by file for bigram index
            self.fdictforbigramtokensbyfile = OrderedDict(sorted(self.fdictforbigramtokensbyfile.iteritems()))

        if self.fcangeneratetrigramindex:
            for key, value in self.fdictfortrigramindex.iteritems():
                value = OrderedDict(sorted(value.iteritems()))

            # sort unigram index dictionary by key
            self.fdictfortrigramindex = OrderedDict(sorted(self.fdictfortrigramindex.iteritems()))

            # sort dictionary for word count by file for trigram index
            self.fdictfortrigramtokensbyfile = OrderedDict(sorted(self.fdictfortrigramtokensbyfile.iteritems()))

    def getunigramindex(self):
        return self.fdictforunigramindex

    def getbigramindex(self):
        return self.fdictforbigramindex

    def gettrigramindex(self):
        return self.fdictfortrigramindex

    def set_tokenized_files_dir(self, p_tokenizedfilesdir):
        self.ftokenizedfilesdir = p_tokenizedfilesdir

    def setOutputDirectory(self, p_outputdirectory):
        self.foutputdirname = p_outputdirectory

    def setCanGenerateBigramIndex(self, p_bool):
        self.fcangeneratebigramindex = p_bool

    def setCanGenerateTrigramIndex(self, p_bool):
        self.fcangeneratetrigramindex = p_bool

    def setCanPerformStopping(self, p_bool):
        self.fcanperformstopping = p_bool

    def setStopList(self, p_stoplist):
        self.fstoplist = p_stoplist

    def setIsStemmedIndex(self, p_isstemmedindex):
        self.fisstemmedindex = p_isstemmedindex

    def writecounts(self):

        # print "----------------------------------------------------------------------"
        # print "Total Unigram Tokens: " + str(self.ftotalunigramtokens)
        # print "Total Bigram Tokens: " + str(self.ftotalbigramtokens)
        # print "Total Trigram Tokens: " + str(self.ftotaltrigramtokens)
        # print "----------------------------------------------------------------------"
        # print "Writing word counts by file for unigram index..."

        if self.fcanperformstopping:
            lfileforwordcounts = FILE_FOR_WORD_COUNTS_BY_FILE_FOR + FILE_FOR_STOPPED_INDEX
        elif self.fisstemmedindex:
            lfileforwordcounts = FILE_FOR_WORD_COUNTS_BY_FILE_FOR + FILE_FOR_STEMMED_INDEX
        else:
            lfileforwordcounts = FILE_FOR_WORD_COUNTS_BY_FILE_FOR + FILE_FOR_INDEX

        lfileforwordcounts = DIR_FOR_OUTPUT_FILES + "/" + self.foutputdirname + "/" \
                             + lfileforwordcounts + FILE_EXT

        create_file(lfileforwordcounts, '')
        convert_data_from_dictionary_to_file(lfileforwordcounts, self.fdictforunigramtokensbyfile, True)

        # print "Writing word counts by file for bigram index..."
        # create_file(DIR_FOR_OUTPUT_FILES + "/" + FILE_FOR_WORD_COUNTS_BY_FILE_FOR_BIGRAM + FILE_EXT, '')
        # convert_data_from_dictionary_to_file(
        #     DIR_FOR_OUTPUT_FILES + "/" + FILE_FOR_WORD_COUNTS_BY_FILE_FOR_BIGRAM + FILE_EXT,
        #     self.findexer.fdictforbigramtokensbyfile, True)
        #
        # print "Writing word counts by file for trigram index..."
        # create_file(DIR_FOR_OUTPUT_FILES + "/" + FILE_FOR_WORD_COUNTS_BY_FILE_FOR_TRIGRAM + FILE_EXT, '')
        # convert_data_from_dictionary_to_file(
        #     DIR_FOR_OUTPUT_FILES + "/" + FILE_FOR_WORD_COUNTS_BY_FILE_FOR_TRIGRAM + FILE_EXT,
        #     self.findexer.fdictfortrigramtokensbyfile, True)

    def write_indexes_to_file(self):

        if self.fcanperformstopping:
            lfilename = FILE_FOR_STOPPED_INDEX
        elif self.fisstemmedindex:
            lfilename = FILE_FOR_STEMMED_INDEX
        else:
            lfilename = FILE_FOR_INDEX

        lfilename = DIR_FOR_OUTPUT_FILES + "/" + self.foutputdirname + "/" + lfilename + FILE_EXT

        # print "----------------------------------------------------------------------"
        # print "Writing Indexes to files..."
        # t1 = time.time()
        # print "Writing Unigram Index to file..."
        create_file(lfilename, '')
        convert_data_from_dictionary_to_file(lfilename, self.fdictforunigramindex, True)
        # print "Unigram Index writing done"
        # t2 = time.time()
        # print "Time required to print unigram index: " + str(t2-t1)

        # # print "----------------------------------------------------------------------"
        # # t1 = time.time()
        # print "Writing Bigram Index to file..."
        # create_file(DIR_FOR_OUTPUT_FILES + "/" + FILE_FOR_BIGRAM_INDEX + FILE_EXT, '')
        # # print self.findexer.fdictforbigramindex
        # convert_data_from_dictionary_to_file(DIR_FOR_OUTPUT_FILES + "/" + FILE_FOR_BIGRAM_INDEX + FILE_EXT,
        #                                      self.findexer.fdictforbigramindex, True)
        # # print "BiIndex writing done"
        # # t2 = time.time()
        # # print "Time required to print bigram index: " + str(t2 - t1)
        # # print "----------------------------------------------------------------------"
        # # t1 = time.time()
        # print "Writing Trigram Index to file..."
        # create_file(DIR_FOR_OUTPUT_FILES + "/" + FILE_FOR_TRIGRAM_INDEX + FILE_EXT, '')
        # # print self.findexer.fdictfortrigramindex
        # convert_data_from_dictionary_to_file(DIR_FOR_OUTPUT_FILES + "/" + FILE_FOR_TRIGRAM_INDEX + FILE_EXT,
        #                                      self.findexer.fdictfortrigramindex, True)
        # print "Trigram Index writing done"
        # t2 = time.time()
        # print "Time required to print trigram index: " + str(t2 - t1)
        # print "All indexes written to file"

    def startIndexing(self, p_UseStopping, p_UseStemming):

        self.fcanperformstopping = p_UseStopping
        self.fisstemmedindex = p_UseStemming

        self.createindexes(self.ftokenizedfilesdir)

    def printAll(self):

        create_directory(DIR_FOR_OUTPUT_FILES)
        ldirpath = DIR_FOR_OUTPUT_FILES + "/" + self.foutputdirname
        create_directory(ldirpath)

        # print all data to file
        self.writecounts()
        self.write_indexes_to_file()
        generate_doc_freq_table(self.fdictforunigramindex, 1, ldirpath)










