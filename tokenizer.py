# coding: utf-8
from bs4 import BeautifulSoup
from genUtils import *
from consts import *
import re
import os

# Tokenizer Class
class Tokenizer:

    def __init__(self):
        self.ftokenizedfilesoutputdir = ""

    def removetags(self, p_soup):

        # Clean text by removing the following html entities from wiki pages

        for tag in p_soup.findAll(['script', 'style']):
            tag.decompose()
        # for tag in p_soup.findAll(['script', 'style', 'sub', 'sup']):
        #     tag.decompose()
        # for tag in p_soup.findAll("sup", {"class": ["reference"]}):
        #     tag.decompose()
        # for tag in p_soup.findAll("span", {"class": ["mw-editsection", "mwe-math-element"]}):
        #     tag.decompose()
        # for tag in p_soup.findAll("span", {"id": "References"}):
        #     tag.decompose()
        # for tag in p_soup.findAll("div", {"id": "toc"}):
        #     tag.decompose()
        # for tag in p_soup.findAll("div", {"class":"reflist"}):
        #     tag.decompose()
        # for tag in p_soup.findAll("span", {"id": "Further_reading"}):
        #     tag.decompose()
        # for tag in p_soup.findAll("table", {"class": "plainlinks"}):
        #     tag.decompose()
        # for tag in p_soup.findAll("span", {"id": "External_links"}):
        #     tag.decompose()
        # for tag in p_soup.findAll("a", {"class": ["external free"]}):
        #     tag.decompose()

        return p_soup

    def removeurls(self, p_text):

        lregexp = re.compile(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''')

        p_text = re.sub(lregexp, "", p_text)

        return p_text

    def removepunctuation(self, p_text):

        # regex = re.compile('[%s]' % re.escape(string.punctuation))
        # p_text = regex.sub("", p_text)

        p_text = re.sub(r"[!\"#$%&\'()*+/:;<=>?@[\\\]^_`{|}~]", " ", p_text)
        # return p_text

        # remove all "-" not between text
        p_text = re.sub(r"(?<![a-zA-Z0-9])-|-(?![a-zA-Z0-9])", " ", p_text)

        # remove all ",", "." in text not between digits
        p_text = re.sub(r"(?<![0-9])[,.]|[,.](?![0-9])", " ", p_text)

        # remove all tab separated numbers in text
        # p_text = re.sub(r"([0-9])\t([0-9])\t([0-9])", "", p_text)
        p_text = re.sub(r"^\d+\t\d+\t\d+$", " ", p_text, flags=re.M)

        return p_text

    def finalizetext(self, p_text):

        if not is_string_valid(p_text):
            return ""

        ltext = p_text

        # remove wiki references numbers
        # ltext = re.sub(r"\[[0-9]]", '', ltext)
        # ltext = re.sub(r"\[[\d+]*]", '', ltext)

        # ltext = re.sub('[^0-9a-zA-Z]+', '', ltext)
        # ltext = re.sub(ur"[^\w\d,.$%\-\s]+", '', ltext)

        # remove whitespace
        ltext = re.sub(r"&nbsp;", " ", ltext)
        ltext = re.sub(r"  ", " ", ltext)
        # ltext = re.sub(r"\t", " ", ltext)
        # ltext = ltext.replace("[edit]", "")

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in ltext.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        ltext = '\n'.join(chunk for chunk in chunks if chunk)

        # Apply case folding
        ltext = ltext.lower()

        # Encode text to prevent errors while printing
        # ltext = ltext.encode('utf-8')

        return ltext

    def tokenizefile(self, p_filename):

        # read contents of the file
        lfilesoup = BeautifulSoup(open(p_filename), "html.parser")
        # lfilesoup = lfilesoup.select("div[id='content']")[0]
        lfilesoup = self.removetags(lfilesoup)

        # Get the header from the soup
        # lheaderele = lfilesoup.select("h1[id='firstHeading']")[0]
        # ltextdiv = lfilesoup.select("div[id='mw-content-text']")[0]

        # get text from header
        ltext = lfilesoup.get_text() + "\n"

        # get text from text div
        # ltext = ltext + ltextdiv.get_text()

        # Remove unprintable characters
        ltext = re.sub(r'[^\x00-\x7F]+', ' ', ltext)

        # remove urls
        ltext = self.removeurls(ltext)

        # remove punctuation
        ltext = self.removepunctuation(ltext)

        # Finalize text
        ltext = self.finalizetext(ltext)

        # print(ltext)
        return ltext

    def doTokenization(self, p_directory, p_listoffiles):

        ldictfordocidtokenizeddatamapping = {}
        llistfortokenizedfilenames = []
        llistoffinaltokenizeddocids = []

        # read the file containing the mapping of urls and file data list and process each file
        # for lurl, lfile in ldictforurldatafilemapping.iteritems():
        for lfileval in p_listoffiles:

            lfile = p_directory + "/" + lfileval

            if not os.path.exists(lfile):
                continue

            # get the tokenized text
            ltokenizedtext = self.tokenizefile(lfile)

            # get the docid from url
            # ldocidforurl = get_document_id_from_url(lurl)

            # replace characters in name
            lfileval = os.path.splitext(lfileval)[0]
            # ldocid = re.sub(r"[-_/(),.]", "", lfileval)
            ldocid = lfileval

            if ldocid in llistfortokenizedfilenames:
                # print "Creating separate file for :" + ldocid
                ldocid += str(llistfortokenizedfilenames.count(ldocid))
            else:
                llistfortokenizedfilenames.append(ldocid)

            # print "Creating file for :" + ldocid

            lfilename = self.ftokenizedfilesoutputdir + "/" + ldocid + FILE_EXT

            # write parsed data to file
            create_file(lfilename, '')
            write_to_file(lfilename, ltokenizedtext.encode("utf-8"))

            llistoffinaltokenizeddocids.append(ldocid)

            # update dictionary for tokenized files mapping
            # ldictfordocidtokenizeddatamapping[ldocid] = lfilename

        # print dict for url tokenized data mapping to file
        # convert_data_from_dictionary_to_file(FILE_FOR_URL_TOKENIZED_DATA_MAPPING+FILE_EXT, ldictfordocidtokenizeddatamapping)
        # convert_data_from_collection_to_file(FILE_FOR_URL_TOKENIZED_DATA_MAPPING+FILE_EXT, llistoffinaltokenizeddocids)

    def tokenizedir(self, p_directory):

        if not os.path.isdir(p_directory):
            print "No directory provided for raw data files, proceeding with default directory: " + CACM_DATA
            p_directory = CACM_DATA
        # else:
            # ldictforurldatafilemapping = convert_data_from_file_to_dictionary(FILE_FOR_URL_DATA_MAPPING + FILE_EXT)
            # llistoffiles = ldictforurldatafilemapping.values()

        # get list of files from directory
        llistoffiles = get_list_of_files_from_dir(p_directory)

        if len(llistoffiles) < 1:
            print "No files exist in the directory to tokenize."
            return

        print "Proceeding with files in the directory: " + p_directory
        create_directory(self.ftokenizedfilesoutputdir)
        self.doTokenization(p_directory, llistoffiles)

    def setTokenizedFilesOutputDir(self, p_tokenizedfilesoutputdir):
        self.ftokenizedfilesoutputdir = p_tokenizedfilesoutputdir











