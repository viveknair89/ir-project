from math import log
from indexerUtils import *


# retrieval class
class BM25RetrievalModule:

    def __init__(self):

        self.funigramindex = {}
        self.fdocfreqdict = {}
        self.fwordscountbyfiledict = {}
        self.ftotaltokens = 0
        self.favglenofdocumentincorpus = 0
        self.fnoofdocuments = 0
        self.foutputdirname = ""
        self.frelevanceinfodict = {}
        self.fcanuserelevanceinfo = False

    def initialize(self):

        self.funigramindex = {}
        self.fdocfreqdict = {}
        self.fwordscountbyfiledict = {}
        self.ftotaltokens = 0
        self.favglenofdocumentincorpus = 0
        self.fnoofdocuments = 0
        self.foutputdirname = ""
        self.frelevanceinfodict = {}
        self.fcanuserelevanceinfo = False

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

        ldictwithBM25scores = self.calculateBM25(p_queryid, p_queryterm)

        # Write BM25 scores to file
        self.writeBM25scores(p_queryid, ldictwithBM25scores)

    def calculateK(self, p_docid):

        b = 0.75
        k1 = 1.2
        lnooftokensfordoc = self.fwordscountbyfiledict[p_docid]

        kval = float(k1 * ((1-b) + b * float(lnooftokensfordoc)/self.favglenofdocumentincorpus))
        return kval

    def BM25val(self, ri, R, ni, N, k1, k2, K, fi, qfi):

        value1 = ((float(ri + 0.5)/float(R-ri+0.5))/(float(ni-ri+0.5)/float(N-ni-R+ri+0.5)))
        value2 = (float(float(k1+1)*fi)/float(K+fi))
        value3 = (float(float(k2+1)*qfi)/float(k2+qfi))

        result = float(log(float(value1))*value2*value3)
        return result

    def calculateBM25(self, p_queryid, p_queryterm):

        N = self.fnoofdocuments
        k1 = 1.2
        k2 = 100
        ri = 0
        R = 0

        if self.fcanuserelevanceinfo and p_queryid in self.frelevanceinfodict:
            R = len(self.frelevanceinfodict[p_queryid])
        else:
            R = 0

        # split the query term into individual words
        lqueryterms = p_queryterm.split(" ")

        # p_queryarr = list(set(lqueryterms))

        ldocscoredict = {}

        for lterm in lqueryterms:

            if lterm not in self.funigramindex:
                continue

            ltermdict = self.funigramindex[lterm]

            ni = sum(self.fdocfreqdict[lterm].values())

            ri = 0
            if self.fcanuserelevanceinfo and p_queryid in self.frelevanceinfodict:
                # calculate bm25 scores for all docs for the term
                for ldocid, ltermfreq in ltermdict.iteritems():
                    if ldocid in self.frelevanceinfodict[p_queryid]:
                        ri += 1

            # calculate bm25 scores for all docs for the term
            for ldocid, ltermfreq in ltermdict.iteritems():

                # get the bm25 score for the docid and update in dict
                Kval = self.calculateK(ldocid)

                # get freq of term in document
                fi = int(ltermdict[ldocid])

                qfi = lqueryterms.count(lterm)

                value = self.BM25val(ri, R, ni, N, k1, k2, Kval, fi, qfi)

                if ldocid not in ldocscoredict:
                    ldocscoredict[ldocid] = value
                else:
                    ldocscoredict[ldocid] += value

        ldocscoredict = OrderedDict(reversed(sorted(ldocscoredict.items(), key=itemgetter(1))))

        return ldocscoredict

    def writeBM25scores(self, p_queryId, p_dictwithBM25Scores):

        ldirpath = DIR_FOR_OUTPUT_FILES + "/" + self.foutputdirname + "/" + DIR_FOR_BM25_OUTPUT
        create_directory(ldirpath)

        # query_id Q0 doc_id rank BM25_score system_name
        lsystemname = "PC"
        lquerydelimiter = "Q0"
        lqueryid = str(p_queryId)

        llist = []
        llist.append("query_id\t\tQ0\t\tdoc_id\t\trank\t\tBM25_score\t\tsystem_name")
        lcounter = 0
        for key, value in p_dictwithBM25Scores.iteritems():
            lcounter += 1
            if lcounter <= NO_OF_REL_DOCS_FOR_RM:
                lbm25scorefordoc = str(value)
                lstring = lqueryid + "\t\t" + lquerydelimiter + "\t\t" + key + "\t\t" + str(lcounter) + "\t\t" + \
                          lbm25scorefordoc + "\t\t" + lsystemname
                llist.append(lstring)
            else:
                break

        lfilename = ldirpath + "/" + FILE_NAME_PREFIX_FOR_RM_OUTPUT + "_" + lqueryid + FILE_EXT

        # write the list to file
        convert_data_from_collection_to_file(lfilename, llist)

    def processQueriesFromFile(self, p_queryfilename):

        # process all queries from the given file and write results
        llist = convert_data_from_file_to_collection(p_queryfilename)

        counter = 0
        for litem in llist:
            counter += 1
            self.processQuery(counter, litem)

        # print str(counter) + " queries processed for BM25"































































