from indexerUtils import *
import math


def get_expanded_query(p_query, p_unigramindex, p_dictwithscoresbyrm):

    # print "Perform Query Expansion"

    lqueryterms = p_query.split(" ")

    # Get top 50 from the dictionary
    ltop50docs = OrderedDict(reversed(sorted(p_dictwithscoresbyrm.items(), key=itemgetter(1))))
    ltop50docs = list(ltop50docs)[:NO_OF_TOP_DOCS_FROM_RM]

    # Initialize dictionary to hold top terms to be added in query expansion
    ltoptermsdict = {}

    # Get the stoplist
    lstoplist = get_stop_list()

    # Process for each term in unigram index
    for lindexterm in p_unigramindex:
        # Get the all the frequent terms except the terms in the query
        if lindexterm not in lqueryterms:

            # Get the dict for the term from the unigram index
            ldictforterm = p_unigramindex[lindexterm]
            ltermfrequency = 0
            lnoofrelevantdocs = 0
            for ldocid in ldictforterm:
                if ldocid in ltop50docs:
                    lnoofrelevantdocs += 1
                    ltermfrequency += int(ldictforterm[ldocid])

            if lnoofrelevantdocs > 0 and (not isWordAStopWord(lindexterm, lstoplist)):

                # Calculate idf for the term
                lidfvalue = float(math.log(NO_OF_TOP_DOCS_FROM_RM/lnoofrelevantdocs))
                ltoptermsdict[lindexterm] = (lidfvalue*ltermfrequency)

    # Get the top terms for query expansion
    ltoptermsdict = OrderedDict(reversed(sorted(ltoptermsdict.items(), key=itemgetter(1))))
    ltoptermsdict = list(ltoptermsdict)[:NO_OF_TOP_TERMS_FOR_QUERY_EXPANSION]

    lqueryterms += ltoptermsdict
    return " ".join(lqueryterms)



























    def query_expansion_using_tfidf(self):

        print "Query Expansion using BM25"
