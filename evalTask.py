from evaluation import *
from queryutils import *
import Task1
import Task2
import Task3A
import Task3B
from scipy import stats


ldirpath = DIR_FOR_OUTPUT_FILES + "/" + EVALUATION_FOLDER


def evaluate_all_systems(p_dictoffolderpaths, p_run_all_systems=True):

    if p_run_all_systems:
        Task1.execute_system('')
        Task2.execute_system('')
        Task3A.execute_system('')
        Task3B.execute_system('')

    print "Evaluating all systems..."

    create_directory(ldirpath)

    lquerydict = get_given_queries_in_dict(CACM_QUERY_FILE + FILE_EXT)
    lquerydict = get_sorted_dict(lquerydict)

    lallsystemsmeanvaluesdict = {}
    lallsystemsavgprecisionvaluesdict = {}
    for lkey, lvalue in p_dictoffolderpaths.iteritems():

        lsystemname = get_system_name(lkey)
        print "Evaluating system: " + lsystemname

        lsystemmeanvaluesdict = {}
        ldictofavgprecisionvalues = {}
        llistofprecisionandrecallvalues = ["Query Id,DocId,Rank,Precision,Recall"]
        llistofpatkvalues = ["Query Id,P@5,P@20"]

        evaluate_system(lvalue,  # results folder path to evaluate
                        lquerydict,  # dictionary containing all queries with query id
                        lsystemmeanvaluesdict,  # dictionary to hold the mean values for all systems
                        ldictofavgprecisionvalues,  # dictionary to hold avg precision values of systems
                        llistofprecisionandrecallvalues,  # results of precision recall values for all queries
                        llistofpatkvalues  # list to hold pat5 and pat20 values for all queries for this system
                        )  # evaluate_system..

        lallsystemsmeanvaluesdict[lkey] = lsystemmeanvaluesdict

        # ldictofavgprecisionvalues = get_sorted_dict(ldictofavgprecisionvalues)
        lallsystemsavgprecisionvaluesdict[lkey] = ldictofavgprecisionvalues

        # print "Writing Precision and Recall values for system: " + lsystemname
        llfilename = ldirpath + "/" + FILE_FOR_PRECISON_RECALL_RESULTS_OF_SYSTEM + "_" + lsystemname + CSV_FILE_EXT
        create_file(llfilename, '')
        convert_data_from_collection_to_file(llfilename, llistofprecisionandrecallvalues)

        # print "Writing P@5 and P@20 values for system: " + lsystemname
        llfilename = ldirpath + "/" + FILE_FOR_PATK_RESULTS_OF_SYSTEM + "_" + lsystemname + CSV_FILE_EXT
        create_file(llfilename, '')
        convert_data_from_collection_to_file(llfilename, llistofpatkvalues)

    # print "Writing mean values to file"
    llistofmeanvalues = ["System,MAP,MRR,P@5,P@20"]
    for lkey, lvalue in lallsystemsmeanvaluesdict.iteritems():
        lsystemname = get_system_name(lkey)
        lstr = lsystemname + "," + str(lvalue[MAP_CONST]) + "," + str(lvalue[MRR_CONST]) + \
               "," + str(lvalue[PAT5_CONST]) + "," + str(lvalue[PAT20_CONST])
        llistofmeanvalues.append(lstr)

    lfilename = ldirpath + "/" + FILE_FOR_ALL_SYSTEMS_MEAN_VALUES + CSV_FILE_EXT
    create_file(lfilename, '')
    convert_data_from_collection_to_file(lfilename, llistofmeanvalues)

    # print "Writing average precision values to file"
    llistavgprecisionresults = ["System,Query Id,Average Precision"]
    for lkey, lvalue in lallsystemsavgprecisionvaluesdict.iteritems():
        lsystemname = get_system_name(lkey)
        for ljkey, ljvalue in lvalue.iteritems():
            lstr = lsystemname + "," + str(ljkey) + "," + str(ljvalue)
            llistavgprecisionresults.append(lstr)

    lfilename = ldirpath + "/" + FILE_FOR_ALL_SYSTEMS_AVG_PRECISION_VALUES + CSV_FILE_EXT
    create_file(lfilename, '')
    convert_data_from_collection_to_file(lfilename, llistavgprecisionresults)

    # print "Run t-tests for models"
    run_tests_for_models(lallsystemsavgprecisionvaluesdict, len(lquerydict))


def run_tests_for_models(p_dictwithsystemavgprecisionvalues, p_noofqueries):

    llist = ["System A,System B,P-Value"]
    for lkey, lvalue in p_dictwithsystemavgprecisionvalues.iteritems():
        lsystemname = get_system_name(lkey)

        # Get all avg precision values for the system from dict
        lvalue = get_sorted_dict(lvalue)
        lsystemoneavgprecisionvalues = lvalue.values()

        for ljkey, ljvalue in p_dictwithsystemavgprecisionvalues.iteritems():
            if lkey != ljkey:
                lcomparedsystemname = get_system_name(ljkey)
                ljvalue = get_sorted_dict(ljvalue)
                lsystemtwoavgprecisionvalues = ljvalue.values()
                lpvalue = get_p_value_for_avg_precision_sets(lsystemoneavgprecisionvalues,
                                                             lsystemtwoavgprecisionvalues,
                                                             p_noofqueries)
                liseffective = "No"
                if lpvalue < ALPHA_VALUE_FOR_T_TESTS:
                    liseffective = "Yes"

                ltemplist = [lsystemname, lcomparedsystemname, str(lpvalue)]
                llist.append(",".join(ltemplist))

    lfilename = ldirpath + "/" + FILE_FOR_ALL_SYSTEMS_T_TESTS_RESULTS + CSV_FILE_EXT
    create_file(lfilename, '')
    convert_data_from_collection_to_file(lfilename, llist)


def get_p_value_for_avg_precision_sets(p_list1, p_list2, p_noofqueries):

    result = stats.ttest_ind(p_list1, p_list2)
    ttest_val = numpy.abs(result[0])
    n = p_noofqueries
    pval = float(stats.t.sf(ttest_val, n - 1))  # /2

    # print "The t-statistic is %.3f " % ttest_val
    # print "The p-value is %.3f." % pval
    return pval

