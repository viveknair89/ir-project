from queryutils import *


def evaluate_system(p_folderpath,
                    p_querydict,
                    p_systemmeanvaluesdict,
                    p_dictofavgprecisionvalues,
                    p_listofprecisionandrecallvalues,
                    p_listofpatkvalues
                    ):

    # Get dict with queries and ranked docs
    ldictwithqueriesandrankeddocs = get_dict_from_folder_for_queries(p_folderpath)

    # get queries relevant data
    ldictwithqueryrelevantdata = get_reldocs_dict_for_queries_from_file(CACM_REL_FILE)

    # filter out queries for whom relevance info is not present
    # counter = 0
    lfilteredquerydict = {}
    for lqueryid, lquery in p_querydict.iteritems():
        if lqueryid in ldictwithqueryrelevantdata:
            lfilteredquerydict[lqueryid] = lquery

    # Filter queries for which rel info is not there
    # lquerylist = [x for x in p_querylist if x not in lexcludedquerieslist]

    ldictwithqueryrelevantdata = OrderedDict(sorted(ldictwithqueryrelevantdata.items(), key=itemgetter(1)))
    ldictwithqueriesandrankeddocs = OrderedDict(sorted(ldictwithqueriesandrankeddocs.items(), key=itemgetter(1)))

    # counter = 0
    lsystemavgprecison = 0
    lsystemreciprocalrank = 0
    lsystempat5 = 0
    lsystempat20 = 0

    for lqueryid, lquery in lfilteredquerydict.iteritems():
        # counter += 1
        ldictwithdocrankforquery = ldictwithqueriesandrankeddocs[lqueryid]
        ldictwithdocrankforquery = OrderedDict(sorted(ldictwithdocrankforquery.items(), key=itemgetter(1)))

        lreldocslist = ldictwithqueryrelevantdata[lqueryid]

        ldictwithquerydocreldata = {}
        lreldocscount = 0
        for ldocid in ldictwithdocrankforquery:
            if ldocid in lreldocslist:
                lreldocscount += 1
                ldictwithquerydocreldata[ldocid] = True
            else:
                ldictwithquerydocreldata[ldocid] = False

        lnumerator = 0
        ldenominator = 0
        lreciprocalrank = 0
        lrecall = 0
        lpat5 = 0
        lpat20 = 0
        lqueryavgprecison = 0
        lreldocsfoundcount = 0
        for ldocid, lrank in ldictwithdocrankforquery.iteritems():

            isdocrelevant = ldictwithquerydocreldata[ldocid]
            ldenominator += 1

            if isdocrelevant:
                lnumerator += 1
                lreldocsfoundcount += 1
                lprecision = float(float(lnumerator)/ldenominator)
                lqueryavgprecison += lprecision
                lrecall = float(float(lnumerator)/lreldocscount)
            else:
                lprecision = float(float(lnumerator)/ldenominator)

            if lreldocsfoundcount == 1:
                lreciprocalrank = float(1)/lrank

            if lrank == 5:
                lpat5 = lprecision

            if lrank == 20:
                lpat20 = lprecision

            lresultforquery = []
            lresultforquery.append(str(lqueryid))
            lresultforquery.append(ldocid)
            lresultforquery.append(str(lrank))
            lresultforquery.append(str(lprecision))
            lresultforquery.append(str(lrecall))
            lresultforquery = ",".join(lresultforquery)
            p_listofprecisionandrecallvalues.append(lresultforquery)

        # add values of p@5 and p@20 to the list
        ltemplistforpatkvalues = []
        ltemplistforpatkvalues.append(str(lqueryid))
        ltemplistforpatkvalues.append(str(lpat5))
        ltemplistforpatkvalues.append(str(lpat20))
        ltemplistforpatkvalues = ",".join(ltemplistforpatkvalues)
        p_listofpatkvalues.append(ltemplistforpatkvalues)

        # Calculate average precision for query
        if lqueryavgprecison > 0:
            lqueryavgprecison = float(float(lqueryavgprecison)/lreldocscount)

        # add average precision for this query to the list to hold avg precision values
        p_dictofavgprecisionvalues[lqueryid] = lqueryavgprecison

        lsystemavgprecison += lqueryavgprecison
        lsystemreciprocalrank += lreciprocalrank
        lsystempat5 += lpat5
        lsystempat20 += lpat20

    # Calculate MAP
    lmapvalue = float(float(lsystemavgprecison)/len(lfilteredquerydict.keys()))

    # Calculate MRR
    lmrrvalue = float(float(lsystemreciprocalrank)/len(lfilteredquerydict.keys()))

    # Calculate Mean PAt5
    lmeanpat5value = float(float(lsystempat5)/len(lfilteredquerydict.keys()))

    # Calculate Mean PAt20
    lmeanpat20value = float(float(lsystempat20)/len(lfilteredquerydict.keys()))

    p_systemmeanvaluesdict[MAP_CONST] = lmapvalue
    p_systemmeanvaluesdict[MRR_CONST] = lmrrvalue
    p_systemmeanvaluesdict[PAT5_CONST] = lmeanpat5value
    p_systemmeanvaluesdict[PAT20_CONST] = lmeanpat20value













































