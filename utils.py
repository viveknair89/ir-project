import os
from os import listdir
from os.path import isfile, join
from urlparse import urlparse
from consts import *
from bs4 import BeautifulSoup


def is_string_valid(p_string):
    """
    Method to validate whether the input string is a valid string or not
    :param p_string: Input string which needs to be validated
    :return: true if string is valid else false
    """
    if p_string == '':
        return False
    elif not isinstance(p_string, basestring):
        return False
    elif p_string.strip() == '':
        return False
    else:
        return True

def is_number(p_param):
    try:
        float(p_param)
        return True
    except ValueError:
        return False

def create_directory(p_Directory):
    """
    Method to create directory for each site for storing files
    :param p_Directory: Directory path which needs to be created
    :return: nothing
    """
    if not os.path.exists(p_Directory):
        print('creating directory: ' + p_Directory)
        os.makedirs(p_Directory)


def create_file(p_filename, p_filepath):
    """
    Method to create a file with the given name
    :param p_filename: Filename with which the file is to be created
    :param p_filepath: Path at which the file is to be created
    :return: nothing
    """

    if is_string_valid(p_filepath):
        p_filename += p_filepath

    if not os.path.isfile(p_filename):
        write_to_file(p_filename, '')

def write_to_file(p_filepath, p_data):
    """
    Method to write input data to file
    :param p_filepath: Path at which the file is to be created
    :param p_data: Data which needs to be written to the file
    :return: nothing
    """
    with open(p_filepath, 'w') as lfile:
        lfile.write(p_data)


def append_to_file(p_FilePath, p_Data):
    """
    Method to append data to file
    :param p_FilePath: File's complete path at which the file is there in which the data needs to be appended
    :param p_Data: Data to be appended to the file
    :return: Nothing
    """
    with open(p_FilePath, 'a') as lfile:
        lfile.write(p_Data + '\n')


def delete_contents_of_file(p_FilePath):
    """
    Method to delete contents of a file
    :param p_FilePath: File whose contents need to be deleted
    :return: Nothing
    """
    open(p_FilePath, 'w').close()


def convert_data_from_file_to_collection(p_FileName):
    """
    Method to get data from a file into a set
    :param p_FileName: Location of the file to read the contents from
    :return: Set containing the entries in the file
    """
    result = []
    # open the file in read mode
    with open(p_FileName, 'rt') as lfile:
        # iterate over each line in the file and add it to the set
        for line in lfile:
            # replace the newline character in line
            result.append(line.replace('\n', ''))
    # return the set after adding all the links from the file
    return result


def convert_data_from_collection_to_file(p_filename, p_data):
    """
    Method to convert data from a set to file
    :param p_filename: File in which the data from the set needs to be written
    :param p_data: Dataset from which the data needs to be written to a file
    :return: Nothing
    """
    # open the file in write mode
    with open(p_filename, "w") as lfile:
        # iterate over each item in set and add it to file
        for litem in p_data:
            if isinstance(litem, basestring):
                try:
                    litem = litem.encode('utf-8')
                except:
                    pass

            lfile.write(str(litem) + "\n")


def get_domain_name_from_url(p_Url):
    """
    Method to return domain name from url
    :param p_Url: Url from which the domain name is to be retrieved
    :return: Domain name from the url
    """
    try:
        lresult = urlparse(p_Url).netloc
    except:
        lresult = ''

    try:
        lresult = lresult.split('.')
        lresult = lresult[-2] + '.' + lresult[-1]
    except:
        lresult = ''

    print lresult
    return lresult


def can_add_link(p_linkhref):

    """
    Method to check whether a link can be crawled by the crawler or not
    :param p_linkhref: href url from an anchor tag
    :return: True if the link can be crawled else False
    """

    if not is_string_valid(p_linkhref):
        return False

    # get the lowercase for href
    llinkhref = p_linkhref.lower()

    if ":" in llinkhref:
        return False

    if "#" in llinkhref:
        return False

    if "/wiki/" not in llinkhref:
        return False

    if (".jpeg" in llinkhref)or (".jpg" in llinkhref) or (".png" in llinkhref) \
            or (".gif" in llinkhref) or (".svg" in llinkhref):
        return False

    #if "main_page" in llinkhref:
    #    return False

    if "wikimediafoundation.org" in llinkhref:
        return False

    return True


def get_complete_url(p_domain, p_url):
    """
    Method to return the complete url with domain name
    :param p_domain: Domain name to be added to url
    :param p_url: Url
    :return: Url with domain name if it is not already there, else the same url
    """

    lresult = p_url

    if p_domain not in p_url:
        lresult = p_domain + p_url

    return lresult

def contains_keyword(p_keyword, p_anchortag):

    """
    Method used to check whether the keyword occurs in the anchor tag text or href
    :param p_keyword: Keyword to be searched for
    :param p_anchortag: Anchor tag in which the keyword is to be searched
    :return: Nothing
    """

    if not is_string_valid(p_keyword):
        return False

    llinkhref = p_anchortag.get("href")
    llinkstring = p_anchortag.string

    p_keyword = p_keyword.lower()

    if ( is_string_valid(llinkhref) and p_keyword not in llinkhref.lower() ) and \
            (is_string_valid(llinkstring) and p_keyword not in llinkstring.lower()):
        return False

    return True

def get_document_id_from_url(p_url, p_converttolowercase=False):

    if p_converttolowercase:
        p_url = p_url.lower()

    wikiprefixindex = p_url.find(WIKI_URL_PREFIX,0)
    wikiprefixindex += len(WIKI_URL_PREFIX)

    result = p_url[wikiprefixindex:]
    return result

def convert_data_from_dictionary_to_file(p_filename, p_dictionary, p_issorteddict=False):

    """
    Method to convert data from a dictionary to a file
    :param p_filename: Name of the file to be written with the dictionary data
    :param p_dictionary: Dictionary from which the data is to be taken
    :param p_issorteddict: Whether the dictionary is already sorted or not
    :return: Nothing
    """

    llist = []
    for key, value in p_dictionary.iteritems():
        if isinstance(value, list):
            lstring = ' '.join(map(str, value))
        elif isinstance(value, dict):
            ltempstr = ""
            for lk, lv in value.iteritems():
                lv = str(lv)
                ltempstr += lk + "=" + lv + ","
            lstring = ltempstr
            # lstring = str(value)
        elif is_string_valid(value):
            lstring = value
        elif is_number(value):
            lstring = str(value)

        lstring = key + " " + lstring

        if isinstance(value, dict):
            llist.append(lstring)
        elif lstring not in llist:
            llist.append(lstring)

    if not p_issorteddict:
        # reverse the list to maintain order
        llist.reverse()

    # llistdata = ("\n").join(llist)

    convert_data_from_collection_to_file(p_filename, llist)
    # write_to_file(p_filename, llistdata)


def convert_data_from_dictionary_with_nesteddict_to_file(p_filename, p_dictionary, p_issorteddict=False):
    llist = []
    for key, value in p_dictionary.iteritems():
        lstring = ""
        for litem, litemvalue in value.iteritems():
            lstring += str(litem) + "=" + str(litemvalue) + ","
        lstring += str(key) + " " + lstring
        llist.append(lstring)

    if not p_issorteddict:
        # reverse the list to maintain order
        llist.reverse()

    convert_data_from_collection_to_file(p_filename, llist)
    # write_to_file(p_filename, lstring)


def convert_data_from_file_to_dictionary(p_filename):

    """
    Method to convert data from a file to a dictionary
    :param p_filename: Name of the file to read the dictionary data from
    :return: A dictionary containing the data from the file
    """

    # read the data from the file into a list
    llist = convert_data_from_file_to_collection(p_filename)
    ldict = {}

    for litem in llist:
        llistofitems = litem.split()
        lkey = llistofitems[0]
        lvalue = llistofitems[1:]
        if isinstance(lvalue, list):
            if len(lvalue) == 1:
                if is_number(lvalue[0]):
                    lvalue = int(lvalue[0])
                    ldict[lkey] = lvalue
        else:
            ldict[lkey] = lvalue

    return ldict

def add_new_entry_to_graph(p_graph, key, value):

    if not p_graph.has_key(key):
        # link is not present in graph, add it to the graph
        p_graph[key] = [value]
    else:
        # key is already present in graph, retrieve the list for it and append the new value to it
        llist = p_graph.get(key,[])
        # if value not in llist:
        llist.append(value)

    return p_graph

def build_graph_from_graph(p_sourcegraph):

    lgraph = {}
    for key, value in p_sourcegraph.iteritems():

        for val in value:
            if not lgraph.has_key(val):
                # link is not present in graph, add it to the graph
                lgraph[val] = [key]
            else:
                # key is already present in graph, retrieve the list for it and append the new value to it
                llist = lgraph.get(val, [])
                llist.append(key)

    return lgraph

def get_list_of_files_from_dir(p_directory):

    lresult = []
    if not os.path.isdir(p_directory):
        return lresult

    # read files from directory
    lresult = [f for f in listdir(p_directory) if isfile(join(p_directory, f))]

    return lresult

def convert_data_from_file_to_dict_for_nested_dict(p_filename, p_listtrim, p_keyvalsep, p_valsep):

    """
    Method to convert data from a file to a dictionary
    :param p_filename: Name of the file to read the dictionary data from
    :return: A dictionary containing the data from the file
    """

    # read the data from the file into a list
    llist = convert_data_from_file_to_collection(p_filename)
    ldict = {}

    llist = llist[p_listtrim:]

    for litem in llist:
        llistofitems = litem.split()
        lkey = llistofitems[0]
        lkeyvalue = llistofitems[1:]
        if len(lkeyvalue) > 0:
            lkeyvalue = lkeyvalue[0].split(p_keyvalsep)
            lvaldict = {}
            for lvalueitem in lkeyvalue:
                if is_string_valid(lvalueitem):
                    lvalueitem = lvalueitem.split(p_valsep)
                    lvaldict[lvalueitem[0]] = lvalueitem[1]
            ldict[lkey] = lvaldict

    return ldict

def convert_data_from_file_to_dict_for_nested_dict_withoutsep(p_filename, p_listtrim, p_valsep):

    """
    Method to convert data from a file to a dictionary
    :param p_filename: Name of the file to read the dictionary data from
    :return: A dictionary containing the data from the file
    """

    # read the data from the file into a list
    llist = convert_data_from_file_to_collection(p_filename)
    ldict = {}

    llist = llist[p_listtrim:]

    if p_valsep == "\t\t":
        p_valsep = ""

    for litem in llist:
        llistofitems = litem.split()
        lkey = llistofitems[0]
        lkeyvalue = llistofitems[1:]
        if len(lkeyvalue) > 0:
            lvaldict = {}
            if is_string_valid(p_valsep):
                lvalueitem = lkeyvalue.split(p_valsep)
                lvaldict[lvalueitem[0]] = lvalueitem[1]
            else:
                if is_number(lkeyvalue[1]):
                    lkeyvalue[1] = int(lkeyvalue[1])
                lvaldict[lkeyvalue[0]] = lkeyvalue[1]
            ldict[lkey] = lvaldict

    return ldict


def writegivenqueriestofile(p_filename):

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

    # write list to file
    convert_data_from_collection_to_file(FILE_FOR_QUERIES+FILE_EXT, llist)

def get_no_of_files_in_dir(p_directory):

    llist = get_list_of_files_from_dir(p_directory)

    return len(llist)


