from bs4 import BeautifulSoup
from indexerUtils import *
import re


# File for utility methods for queries
def get_reldocs_dict_for_queries_from_file(p_filename):

    # read the given relevance information in list
    llist = convert_data_from_file_to_collection(p_filename)

    ldict = {}

    for litem in llist:

        # strip each item to retrieve query id and document name
        larr = litem.split(" ")
        larr = larr[:4]
        lqueryid = int(larr[0])
        if lqueryid not in ldict:
            ldict[lqueryid] = [larr[2]]
        else:
            templist = ldict[lqueryid]
            templist.append(larr[2])

    return ldict


def get_given_queries_in_list(p_filename):

    # read contents of the file
    lfilesoup = BeautifulSoup(open(p_filename), "html.parser")

    llist = []
    counter = 0
    for tag in lfilesoup.findAll(['doc']):
        lstr = ''
        counter += 1
        # get the docno tag from the tag
        docnotag = tag.select("docno")
        try:
            docnotag = docnotag[0]
            docnoofquery = int(docnotag.get_text())
            docnotag.decompose()
        except:
            docnoofquery = counter

        lstr = tag.get_text().split("\n")
        lstr = [x.strip() for x in lstr]
        lstr = " ".join(lstr).strip()

        llist.append(lstr)

    return llist


def write_given_queries_to_file(p_filename, p_outputfile):

    llist = get_given_queries_in_list(p_filename)
    create_file(p_outputfile, '')
    # write list to file
    convert_data_from_collection_to_file(p_outputfile, llist)


def tokenize_query(p_query):

    p_query = " ".join(p_query.split())

    # remove punctuations
    p_query = re.sub(r"[!\"#$%&\'()*+/:;<=>?@[\\\]^_`{|}~]", " ", p_query)
    # return p_text

    # remove all "-" not between text
    p_query = re.sub(r"(?<![a-zA-Z0-9])-|-(?![a-zA-Z0-9])", " ", p_query)

    # remove all ",", "." in text not between digits
    p_query = re.sub(r"(?<![0-9])[,.]|[,.](?![0-9])", " ", p_query)

    p_query = re.sub(r"&nbsp;", " ", p_query)
    p_query = re.sub(r"  ", " ", p_query)

    # Remove unprintable characters
    p_query = re.sub(r'[^\x00-\x7F]+', ' ', p_query)

    p_query = " ".join(p_query.split())

    return p_query


def get_stopped_query(p_query):

    lqueryterms = p_query.split(" ")
    lstoplist = get_stop_list()
    lqueryterms = [x for x in lqueryterms if not isWordAStopWord(x, lstoplist)]
    lqueryterms = " ".join(lqueryterms)
    return lqueryterms


def get_given_queries_in_dict(p_filename, p_caseFold=True):

    # read the data from the file into a list
    llist = get_given_queries_in_list(p_filename)
    if p_caseFold:
        llist = [x.lower() for x in llist]
    ldict = convert_list_to_dict(llist)
    return ldict


def get_given_queries_in_dict_with_given_keys(p_filename, p_keyslist, p_caseFold=True):

    # read the data from the file into a list
    llist = convert_data_from_file_to_collection(p_filename)
    if p_caseFold:
        llist = [x.lower() for x in llist]

    ldict = {}
    counter = 0
    for litem in llist:
        lkey = p_keyslist[counter]
        ldict[lkey] = litem
        counter += 1

    return ldict


# Convert output file containing documents ranked for a retrieval model to a dict
def get_dict_from_output_file(p_filename):

    llist = convert_data_from_file_to_collection(p_filename)
    llist = llist[1:]

    ldict = {}
    for litem in llist:

        litem = litem.split("\t\t")
        ldocid = litem[2]
        lrank = int(litem[3])
        ldict[ldocid] = lrank

    return ldict


def get_dict_from_folder_for_queries(p_directory):

    # Get list of files of the folder
    llistoffilesindir = get_list_of_files_from_dir(p_directory)

    ldict = {}
    for lfile in llistoffilesindir:
        lfilepath = p_directory + "/" + lfile

        # Get dict with doc ids and ranks
        lfiledatadict = get_dict_from_output_file(lfilepath)

        # Sort the dictionary by rank
        lfiledatadict = get_sorted_dict(lfiledatadict, True)

        # Extract query no from file name
        lfilename = os.path.splitext(lfile)[0]

        lprefixindex = lfilename.find(FILE_NAME_PREFIX_FOR_RM_OUTPUT+"_")
        lprefixindex += len(FILE_NAME_PREFIX_FOR_RM_OUTPUT+"_")
        lqueryid = lfilename[lprefixindex:]
        lqueryid = int(lqueryid)

        ldict[lqueryid] = lfiledatadict

    return ldict


def get_system_name(p_systemno):

    if p_systemno == 1:
        lresult = SYSTEM_FIRST
    elif p_systemno == 2:
        lresult = SYSTEM_SECOND
    elif p_systemno == 3:
        lresult = SYSTEM_THIRD
    elif p_systemno == 4:
        lresult = SYSTEM_FOURTH
    elif p_systemno == 5:
        lresult = SYSTEM_FIFTH
    elif p_systemno == 6:
        lresult = SYSTEM_SIXTH
    elif p_systemno == 7:
        lresult = SYSTEM_SEVENTH
    else:
        lresult = SYSTEM_NAME_DEFAULT

    return lresult










