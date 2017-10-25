from QueryExpansion import *
from BM25RetrievalModule import BM25RetrievalModule
from TFIDFRetrievalModule import TFIDFRetrievalModule
from queryutils import *


# retrieval modules base class
class RMBase:

    def __init__(self):

        self.funigramindex = {}
        self.fdocfreqdict = {}
        self.fwordscountbyfiledict = {}
        self.ftotaltokens = 0
        self.favglenofdocumentincorpus = 0
        self.fnoofdocuments = 0

        self.findexfilename = ""
        self.fdocfreqdictfilename = ""
        self.fwordscountbyfiledictfilename = ""

        self.foutputdirname = ""
        self.frelevanceinfodict = {}
        self.fcanuserelevanceinfo = False
        self.fisstemmedindex = False

        self.ftermdict = {}
        self.ftermfreqdict = {}

        self.fbm25retrievalmodule = None
        self.ftfidfretrievalmodule = None

    def initialize(self):

        self.funigramindex = {}
        self.fdocfreqdict = {}
        self.fwordscountbyfiledict = {}
        self.ftotaltokens = 0
        self.favglenofdocumentincorpus = 0

        self.ftermdict = {}
        self.ftermfreqdict = {}

    def initializeRM(self):

        # Initialize all dictionaries required by retrieval module
        self.initialize()

        # Get the index data from a file
        # self.funigramindex = convert_data_from_file_to_dictionary(FILE_FOR_UNIGRAM_INDEX+FILE_EXT)
        self.funigramindex = convert_data_from_file_to_dict_for_nested_dict(self.findexfilename, 0, ",", "=")

        # get the doc freq index from file
        self.fdocfreqdict = convert_data_from_file_to_dict_for_nested_dict_withoutsep(self.fdocfreqdictfilename, 3, "\t\t")

        # get the words count by file dict
        self.fwordscountbyfiledict = convert_data_from_file_to_dictionary(self.fwordscountbyfiledictfilename)

        # get the total no. of tokens in all documents
        self.ftotaltokens = sum(self.fwordscountbyfiledict.itervalues())

        self.favglenofdocumentincorpus = self.ftotaltokens/self.fnoofdocuments

        if self.fcanuserelevanceinfo:
            if self.fisstemmedindex:
                # get relevance information for stemmed queries from the relevance dictionary
                lrelinfodict = get_reldocs_dict_for_queries_from_file(CACM_REL_FILE)
                for lkey, lvalue in lrelinfodict.iteritems():
                    if lkey in INDEXES_FOR_STEMMED_QUERIES:
                        self.frelevanceinfodict[lkey] = lvalue
                self.frelevanceinfodict = get_sorted_dict(self.frelevanceinfodict)
            else:
                self.frelevanceinfodict = get_reldocs_dict_for_queries_from_file(CACM_REL_FILE)
                self.frelevanceinfodict = get_sorted_dict(self.frelevanceinfodict)

        # print "Total Tokens: " + str(self.ftotaltokens)
        # print "Average length of documents: " + str(self.favglenofdocumentincorpus)

        self.fbm25retrievalmodule = BM25RetrievalModule()
        self.fbm25retrievalmodule.initializeRM(self)

        self.ftfidfretrievalmodule = TFIDFRetrievalModule()
        self.ftfidfretrievalmodule.initializeRM(self)

    def setNoOfDocuments(self, p_noofdocuments):
        self.fnoofdocuments = p_noofdocuments

    def setOutputDirectory(self, p_outputdirectory):
        self.foutputdirname = p_outputdirectory

    def setIndexFileName(self, p_indexfilename):
        self.findexfilename = p_indexfilename

    def setDocFreqDictFileName(self, p_docfreqdictfilename):
        self.fdocfreqdictfilename = p_docfreqdictfilename

    def setWordCountsByFileDictFileName(self, p_wordscountbyfiledictfilename):
        self.fwordscountbyfiledictfilename = p_wordscountbyfiledictfilename

    def isStemmedIndex(self, p_boolisstemmedindex):
        self.fisstemmedindex =  p_boolisstemmedindex

    def setCanUseRelevanceInfo(self, p_boolCanUseRelInfo):
        if isinstance(p_boolCanUseRelInfo, bool):
            self.fcanuserelevanceinfo = p_boolCanUseRelInfo
        else:
            self.fcanuserelevanceinfo = False

    def processQueriesFromFile(self, p_querydict, p_performquerystopping):

        p_querydict = get_sorted_dict(p_querydict)

        for lqueryid, lquery in p_querydict.iteritems():
            # print "Query before tokenization: " + lquery
            lquery = tokenize_query(lquery)
            # print "Query After tokenization: " + lquery

            if p_performquerystopping:
                lquery = get_stopped_query(lquery)
                # print "Query after stopping: " + lquery

            self.fbm25retrievalmodule.processQuery(lqueryid, lquery)
            # print "BM25: Processing Query no. " + str(lqueryid)

            self.ftfidfretrievalmodule.processQuery(lqueryid, lquery)
            # print "TFIDF: Processing Query no. " + str(lqueryid)

    def processQueriesWithQueryExpansion(self, p_querydict, p_performquerystopping):

        p_querydict = get_sorted_dict(p_querydict)

        for lqueryid, lquery in p_querydict.iteritems():
            # print "Query before tokenization: " + lquery
            litem = tokenize_query(lquery)
            # print "BM25: Query before expansion: " + lquery

            if p_performquerystopping:
                lquery = get_stopped_query(lquery)
                # print "Query after stopping: " + lquery

            ldictwithbm25scores = self.fbm25retrievalmodule.calculateBM25(lqueryid, lquery)
            lbm25newquery = get_expanded_query(litem, self.funigramindex, ldictwithbm25scores)
            self.fbm25retrievalmodule.processQuery(lqueryid, lbm25newquery)
            # print "BM25: Query after expansion: " + lbm25newquery
            # print "BM25: Processing Query no. " + str(lqueryid)

            # print "TFIDF: Query before expansion: " + lquery
            ldictwithtfidfscores = self.ftfidfretrievalmodule.calculatetfidfscores(lquery)
            ltfidfnewquery = get_expanded_query(litem, self.funigramindex, ldictwithtfidfscores)
            self.ftfidfretrievalmodule.processQuery(lqueryid, ltfidfnewquery)
            # print "TFIDF: Query after expansion: " + ltfidfnewquery
            # print "TFIDF: Processing Query no. " + str(lqueryid)



