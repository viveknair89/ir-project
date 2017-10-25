from genUtils import *
from consts import *
from collections import OrderedDict
from operator import itemgetter
import matplotlib.pyplot as plt
import math
import numpy
from tokenizer import Tokenizer
import time


def get_term_freq_table_from_file(p_filename):
    '''
    Method to return dictionary for a index from a file
    :param p_filename: Filename containing the unigram data
    :return: Dictionary containing the index data
    '''

    # get data from file into list
    llist = convert_data_from_file_to_collection(p_filename)
    llist = llist[3:]

    ldict = {}
    for litem in llist:
        larr = litem.split("\t\t")
        ldict[larr[0]] = int(larr[1])

    ldict = OrderedDict(reversed(sorted(ldict.items(), key=itemgetter(1))))

    return ldict


def get_doc_freq_table_from_file(p_filename):
    '''
    Method to return dictionary for a index from a file
    :param p_filename: Filename containing the unigram data
    :return: Dictionary containing the index data
    '''

    # get data from file into list
    llist = convert_data_from_file_to_collection(p_filename)
    llist = llist[3:]

    ldict = {}
    for litem in llist:
        larr = litem.split("\t\t")
        ldict[larr[0]] = larr[1:]

    # ldict = OrderedDict(reversed(sorted(ldict.items(), key=itemgetter(1))))

    return ldict


def get_stop_list():

    # Get stop list from the common words file
    llist = convert_data_from_file_to_collection(CACM_COMMON_WORDS)

    return llist


def isWordAStopWord(p_term, p_stoplist):

    result = False

    if p_stoplist is None:
        p_stoplist = get_stop_list()

    if p_term in p_stoplist:
        result = True

    return result


def split_cacm_stem_file_into_files(p_file):

    lfileobject = open(p_file, 'r')
    lfiletext = lfileobject.read()
    lfileobject.close()
    lfiletext = lfiletext.split("#")
    # print lfiletext

    create_directory(CACM_STEMMED_FILES_FOLDER)
    count = 0
    for line in lfiletext:
        # CACM_STEMMED_FILE_NAME
        if is_string_valid(line):

            line = line.split("\n")
            line = line[1:]
            line = "\n".join(line)

            # Remove trailing numbers from the files
            line = remove_numbers_from_file(line)

            count += 1
            if count <= 9:
                lfileno = "000" + str(count)
            elif 10 <= count <= 99:
                lfileno = "00" + str(count)
            elif 100 <= count <= 999:
                lfileno = "0" + str(count)
            else:
                lfileno = str(count)

            lfilename = CACM_STEMMED_FILE_NAME + lfileno + FILE_EXT
            lfilename = CACM_STEMMED_FILES_FOLDER + "/" + lfilename
            create_file(lfilename, '')
            write_to_file(lfilename, line.strip())


def generate_doc_freq_table(p_index, p_indexind, p_dirpath):

    # t1 = time.time()

    # sort each dict of each key
    for key, value in p_index.iteritems():
        value = OrderedDict(sorted(value.iteritems()))

    # sort index by key
    p_index = OrderedDict(sorted(p_index.iteritems()))

    llist = []
    lstring = "Document Frequency Table\n"
    lstring += "Term \t\t Document Id \t\t DocFrequency\n"
    llist.append(lstring)

    for key, value in p_index.iteritems():
        lkeysarray = value.keys()
        lstring = key + "\t\t" + ','.join(map(str, lkeysarray)) + "\t\t" + str(len(lkeysarray))
        llist.append(lstring)

    # reverse the file
    # llist.reverse()

    # t2 = time.time()
    # print "Time to generate doc freq table data: " + str(t2 - t1)

    lfilename = FILE_FOR_DOC_FREQ_TABLE

    if p_indexind == 1:
        lfilename += CONSTS_FOR_UNIGRAM
    elif p_indexind == 2:
        lfilename += CONSTS_FOR_BIGRAM
    elif p_indexind == 3:
        lfilename += CONSTS_FOR_TRIGRAM

    lfilename = p_dirpath + "/" + lfilename + FILE_EXT
    create_file(lfilename, '')
    convert_data_from_collection_to_file(lfilename, llist)
    # write_to_file(lfilename, lstring)
    # t3 = time.time()
    # print "Time to write doc freq table data: " + str(t3 - t2)


def get_term_freq_table(self, p_index):

    lsumdict = {}
    for key, value in p_index.iteritems():
        lsumdict[key] = sum(value.itervalues())

    lsumdict = OrderedDict(reversed(sorted(lsumdict.items(), key=itemgetter(1))))

    return lsumdict

# def generate_term_freq_table(self, p_index, p_indexind):
#
#     # time to generate term freq table
#     # t1 = time.time()
#
#     # generate term freq table for the given index using the indexer class
#     llist = []
#     lstring = "Term Frequency Table \n"
#     lstring += "Term \t\t Term Frequency\n"
#     llist.append(lstring)
#
#     # get term frequency table from given index
#     ldict = self.get_term_freq_table(p_index)
#
#     for key in ldict:
#         lstring = key + "\t\t" + str(ldict[key])  # + "\n"
#         llist.append(lstring)
#
#     # reverse the list
#     # llist.reverse()
#
#     # time after generating the term freq table data
#     # t2 = time.time()
#     # print "Time to generate term freq table data: " + str(t2-t1)
#
#     if p_indexind == 1:
#         lfilename = FILE_FOR_UNIGRAM_TERM_FREQ_TABLE
#     elif p_indexind == 2:
#         lfilename = FILE_FOR_BIGRAM_TERM_FREQ_TABLE
#     elif p_indexind == 3:
#         lfilename = FILE_FOR_TRIGRAM_TERM_FREQ_TABLE
#
#     lfilename = DIR_FOR_OUTPUT_FILES + "/" + lfilename + FILE_EXT
#
#     create_file(lfilename, '')
#     convert_data_from_collection_to_file(lfilename, llist)
#     # t3 = time.time()
#     # print "Time to write term freq table data: " + str(t3 - t2)
#     # write_to_file(lfilename, lstring)


def generate_graph(self, p_filename, p_indexind, p_graphfilename):
# def generate_graph(self, p_index,  p_indexind, p_graphfilename):

    # get term freq table from index
    # ltermfreqdict = self.get_term_freq_table(p_index)
    ltermfreqdict = self.get_term_freq_table_from_file(p_filename)

    # get list of ranks
    llistofranks = numpy.array(xrange(1, len(ltermfreqdict.keys())+1))
    # llistofranks = range(1, len(ltermfreqdict.keys()) + 1)

    # get list of frequencies
    llistoffreqs = ltermfreqdict.values()

    llistoflogofranks = map(math.log, llistofranks)
    llistoflogoffreqs = map(math.log, llistoffreqs)

    plt.figure()
    plt.title("Zipf Curve {}-gram index".format(p_indexind))
    plt.xlabel("Rank")
    plt.ylabel("Frequency of occurrence")
    plt.plot(llistoflogofranks, llistoflogoffreqs, 'r+', label="Wikipedia Corpus")
    plt.legend(loc='upper right')
    plt.savefig(p_graphfilename)

    # curve using probability of occurrence and ranks
    # ltotalnooffreqsoftokens = sum(llistoffreqs)
    # lprobabilities = map(lambda f: f * 1.0 / ltotalnooffreqsoftokens, llistoffreqs)
    # lprobabilities.sort(reverse=True)
    # lrank_probabilities = [(rank + 1, probability) for rank, probability in enumerate(lprobabilities)]
    # lranks, lprobabilities = zip(*lrank_probabilities)
    #
    # llistoflogofranks = map(math.log, lranks)
    #
    # llistoflogoffreqs = map(math.log, lprobabilities)
    #
    # plt.title("Zipfian Curve (Prob vs Rank) - Word {}-Gram".format(p_indexind))
    # plt.xlabel("Rank (by decreasing frequency)")
    # plt.ylabel("Probability (of occurrence)")
    # plt.plot([1, len(llistofranks)], [0.1, 0.1 / len(llistofranks)], label='Expected')
    # plt.plot(llistoflogofranks, llistoflogoffreqs, 'r+', label='Actual')
    # plt.legend(loc='upper right')
    # plt.savefig("outputfiles/" + 'zipfian_curve_(Prob vs Rank)_' + str(p_indexind) + "-ngram.png")


def remove_numbers_from_file(p_text):

    if is_string_valid(p_text):
        if p_text.rfind("pm") != -1:
            k = p_text.rfind("pm")
        elif p_text.rfind("am") != -1:
            k = p_text.rfind("am")
        # filenum = re.search(r'\d+', line).group()
        # line = line.replace(filenum, "", 1)
        p_text = p_text[:k + 2]

    return p_text


def tokenize_raw_data(p_directory):

    # Create output directory
    create_directory(DIR_FOR_OUTPUT_FILES)
    ldirpathfortask = DIR_FOR_OUTPUT_FILES + "/" + DIR_FOR_TOKENIZED_FILES
    create_directory(ldirpathfortask)

    t1 = time.time()
    # create tokenizer and generate token documents
    ltokenizer = Tokenizer()
    ltokenizer.setTokenizedFilesOutputDir(ldirpathfortask)
    ltokenizer.tokenizedir(p_directory)
    t2 = time.time()
    # print "Time for Tokenizer Module: " + str(t2 - t1)


