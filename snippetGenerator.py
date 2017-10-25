from queryutils import *
from consts import *
import time

def is_significant_word(p_term, p_queryterms):

    result = False
    if p_term in p_queryterms:
        result = True

    return result


def generate_snippet(p_queryfile, p_directory, p_outputdirectory, p_isstemmedversion=False):

    # print "Generating snippets from directory: " + p_directory
    t1 = time.time()

    # Create output directory
    create_directory(p_outputdirectory)

    # Convert query list to query dict
    lquerydict = get_given_queries_in_dict(p_queryfile)
    lquerydict = get_sorted_dict(lquerydict)

    lstoplist = get_stop_list()

    # Get dictionary from folder for queries
    ldictwithdocsforqueries = get_dict_from_folder_for_queries(p_directory)

    for lqueryid, ldocsdict in ldictwithdocsforqueries.iteritems():

        # get query from query dict
        lquery = lquerydict[lqueryid]

        lquery = tokenize_query(lquery)
        lquery = lquery.lower()

        # get stopped query
        lquery = get_stopped_query(lquery)

        # split the query term into individual words
        lqueryterms = lquery.split(" ")

        lresultlist = []

        ldoccounter = 0
        for ldocid in ldocsdict:

            # if ldoccounter > 10:
            #     break

            # print "Processing Query: " + str(lqueryid)
            # print "Processing document:" + ldocid

            lresultstr = ""

            lfilepath = CACM_DATA + "/" + ldocid + HTML_FILE_EXT

            lfileobject = open(lfilepath, 'r')
            lsoup = BeautifulSoup(lfileobject.read(), "html.parser")
            lfiletext = lsoup.find("pre").get_text()
            # sent = sent_tokenize(text)
            lfileobject.close()

            lfiletext = lfiletext.split(".")

            lsentencewithmaxscore = ""
            lsentencewithmaxscoresigwords = []
            lsentencemaxscore = 0
            for lsentence in lfiletext:
                if not is_string_valid(lsentence):
                    continue

                lsentencescore = 0

                # tokenize sentence
                ltokenizedsentence = tokenize_query(lsentence)
                # ltokenizedsentence = lsentence
                ltokenizedsentence = ltokenizedsentence.lower()

                lwords = ltokenizedsentence.split(" ")
                lwords = [x for x in lwords if not isWordAStopWord(x, lstoplist)]

                lsignificantwordscount = 0
                lsignificantwords = []
                for lword in lwords:
                    if is_significant_word(lword, lqueryterms):
                        lsignificantwordscount += 1
                        lsignificantwords.append(lword)

                if lsignificantwordscount > 0:
                    lsentencescore = (lsignificantwordscount*lsignificantwordscount)/len(lwords)

                if lsentencescore > lsentencemaxscore:
                    lsentencewithmaxscoresigwords = lsignificantwords
                    lsentencewithmaxscore = lsentence
                    lsentencemaxscore = lsentencescore

            if is_string_valid(lsentencewithmaxscore):

                ldoccounter += 1

                for lword in lsentencewithmaxscoresigwords:
                    lwordtext = '<span style="background-color:yellow;">' + lword + '</span>'
                    lsentencewithmaxscore = re.sub(lword, lwordtext, lsentencewithmaxscore)

                lresultstr += "<div>"
                lresultstr += '<span style="font-weight:bold;">' + ldocid + HTML_FILE_EXT + "</span><br>"
                lresultstr += '<span">' + lsentencewithmaxscore + "</span><br>"
                lresultstr += "</div><br>"
                lresultlist.append(lresultstr)

        lresultlist.insert(0, '<span>Results for Query: <span style="font-style:italic">' + lquery +
                           "</span></span><br><br>")
        lresultfile = p_outputdirectory + "/" + SNIPPETS_FOR_QUERY + str(lqueryid) + HTML_FILE_EXT
        create_file(lresultfile, '')
        convert_data_from_collection_to_file(lresultfile, lresultlist)

    t2 = time.time()
    # print "Time taken for snippet generation: " + str(t2-t1)


def generate_snippets_for_systems():

    print "Generating snippets for systems"

    ldirpathfortask = DIR_FOR_OUTPUT_FILES + "/" + TASK1_CONST

    # Generate snippets for BM25 output
    generate_snippet(CACM_QUERY_FILE + FILE_EXT,
                     ldirpathfortask + "/" + DIR_FOR_BM25_OUTPUT,
                     ldirpathfortask + "/" + SNIPPET_GEN_RESULTS_FOLDER + CONST_FOR_BM25)

    # Generate snippets for TF-IDF output
    generate_snippet(CACM_QUERY_FILE + FILE_EXT,
                     ldirpathfortask + "/" + DIR_FOR_TFIDF_OUTPUT,
                     ldirpathfortask + "/" + SNIPPET_GEN_RESULTS_FOLDER + CONST_FOR_TFIDF)

    # Generate snippets for Lucene
    # generate_snippet(CACM_QUERY_FILE + FILE_EXT,
    #                  LUCENE + "/" + LUCENE_RESULTS,
    #                  LUCENE + "/" + LUCENE_RESULTS_SNIPPETS)


































