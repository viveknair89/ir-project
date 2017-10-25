from math import log
from indexerUtils import *


# retrieval class
class TFIDFRetrievalModule:

    def __init__(self):

        self.funigramindex = {}
        self.fdocfreqdict = {}
        self.fwordscountbyfiledict = {}
        self.ftotaltokens = 0
        self.favglenofdocumentincorpus = 0
        self.fnoofdocuments = 0
        self.foutputdirname = ""

    def initialize(self):

        self.funigramindex = {}
        self.fdocfreqdict = {}
        self.fwordscountbyfiledict = {}
        self.ftotaltokens = 0
        self.favglenofdocumentincorpus = 0
        self.fnoofdocuments = 0
        self.foutputdirname = ""

    def initializeRM(self, p_owner):

        # Initialize all dictionaries required by retrieval module
        self.initialize()

        # Get the index data from a file
        self.funigramindex = p_owner.funigramindex

        # get the doc freq index from file
        self.fdocfreqdict = p_owner.fdocfreqdict

        # get the words count by file dict
        self.fwordscountbyfiledict = p_owner.fwordscountbyfiledict

        # get the total no. of tokens in all documents
        self.ftotaltokens = p_owner.ftotaltokens

        self.favglenofdocumentincorpus = p_owner.favglenofdocumentincorpus

        self.fnoofdocuments = p_owner.fnoofdocuments

        self.foutputdirname = p_owner.foutputdirname

        if p_owner.fcanuserelevanceinfo:
            self.fcanuserelevanceinfo = p_owner.fcanuserelevanceinfo
            self.frelevanceinfodict = p_owner.frelevanceinfodict
        else:
            self.fcanuserelevanceinfo = False

        # print "Total Tokens: " + str(self.ftotaltokens)
        # print "Average length of documents: " + str(self.favglenofdocumentincorpus)

    def processQuery(self, p_queryid, p_queryterm):

        # print "Processing query: " + p_queryterm

        ldictwithtfidfscores = self.calculatetfidfscores(p_queryterm)

        # Write BM25 scores to file
        self.writetfidfscores(p_queryid, ldictwithtfidfscores)

    def calculatetfidfscores(self, p_queryterm):

        # split the query term into individual words
        lqueryterms = p_queryterm.split(" ")

        ldocscoredict = {}

        for lterm in lqueryterms:

            if lterm not in self.funigramindex:
                continue

            # get the dict of docid and freq from unigram index
            ltermdict = self.funigramindex[lterm]

            # No of documents in which the term is there
            noofdocsinwhichtermappears = sum(self.fdocfreqdict[lterm].values())

            # calculate bm25 scores for all docs for the term
            for ldocid, ltermfreq in ltermdict.iteritems():

                # calculate tf
                tf = float(ltermfreq)/float(self.fwordscountbyfiledict[ldocid])

                # calculate idf
                idf = float(log(self.fnoofdocuments)/noofdocsinwhichtermappears)

                value = float(tf*idf)

                if ldocid not in ldocscoredict:
                    ldocscoredict[ldocid] = value
                else:
                    ldocscoredict[ldocid] += value

        ldocscoredict = OrderedDict(reversed(sorted(ldocscoredict.items(), key=itemgetter(1))))

        return ldocscoredict

    def writetfidfscores(self, p_queryId, p_dictwithtfidfcores):

        ldirpath = DIR_FOR_OUTPUT_FILES + "/" + self.foutputdirname + "/" + DIR_FOR_TFIDF_OUTPUT
        create_directory(ldirpath)

        # query_id Q0 doc_id rank TFIDF_score system_name
        lsystemname = "PC"
        lquerydelimiter = "Q0"
        lqueryid = str(p_queryId)

        llist = []
        llist.append("query_id\t\tQ0\t\tdoc_id\t\trank\t\tTF-IDF Score\t\tsystem_name")
        lcounter = 0
        for key, value in p_dictwithtfidfcores.iteritems():
            lcounter += 1
            if lcounter <= NO_OF_REL_DOCS_FOR_RM:
                ltfidfscorefordoc = str(value)
                lstring = lqueryid + "\t\t" + lquerydelimiter + "\t\t" + key + "\t\t" + str(lcounter) + "\t\t" + \
                          ltfidfscorefordoc + "\t\t" + lsystemname
                llist.append(lstring)
            else:
                break

        lfilename = ldirpath + "/" + FILE_NAME_PREFIX_FOR_RM_OUTPUT + "_" + lqueryid + FILE_EXT

        # write the list to file
        convert_data_from_collection_to_file(lfilename, llist)



