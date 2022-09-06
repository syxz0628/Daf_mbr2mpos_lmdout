# todo: -t 250 -250 write to lmdout
# todo: change lmdout name, with percentage of match points
# todo: show mbr fig directly only ( not share x axis)



import argparse
import daf2mpos as d2m
import show_daf_figure as sdaf
import daf_mbr2lmdout as dmlmdout
#import test
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--daf", required=True, help=".daf file path(mandatory)") 
    #parser.add_argument("-p","--mpos", required=False , nargs='?',  const="default_directory", help="write to .mpos file, following by directory and file name or default the same path as .daf",  default="nompos")
    parser.add_argument("-o", "--mpos", required=False, nargs='?',
                        help="write to .mpos file, following by directory and file name or default the same path as .daf")
    parser.add_argument("-s","--showfigs", required=False,  action='store_true', help="show daf and related figures", default=False)
    parser.add_argument("-m","--mbr", nargs='?',required=False, help="machine beam record .xml file path")
    parser.add_argument("-p", "--ptom", nargs='?', required=False, help="PTOM record .dat file path")
    parser.add_argument("-t", "--timeoffset", required=False, type=int, nargs='+',
                        help="Time offset in msec,to adjust results in ~250ms level that was added to system determined timeoffset value;multiple values are acceptable, e.g. -t 250 -250 100",
                        default=250)
    parser.add_argument("-w", "--writetxt", required=False, action='store_true', help="write all data in txt for plot",
                        default=False)
    parser.add_argument("-l", "--lmdout", required=False, nargs='?',
                        help="write to .lmdout file directory, following by directory and file name or default the same path as MBR .xml")
    parser.add_argument("-i", "--initialspot", required=False, type=int, nargs='+',
                        help="Time offset of the first spot of each spill in .msec., default 10ms", default=10)
    parser.add_argument("-z", "--showdebug", required=False, type=int, help="show all DAF and MBR figures for debug. MBR shows start and end points only")
    parser.add_argument("-Z", "--showdebug2", required=False, type=int,
                        help="show all figures for debug. MBR time shift by the given value")
    parser.add_argument("-g", "--log", required=False, nargs='?',
                        help="write error/successed information to .log file")
    args = parser.parse_args()

# define daf file path.   mandatory.
    daf_file_path=args.daf
#
# define mpos file path. User defined or the same directory as daf.
    if (args.mpos==None):
        directory = daf_file_path[:daf_file_path.rfind(".")+1]
        mpos_file_path=directory+"mpos"
    else:
        mpos_file_path=args.mpos
#
# write mpos file.
    print("Detects write of mpos from .daf.")
    d2m.class_daf2mpos(daf_file_path, mpos_file_path,args.log)
#
# define Time offset
    manual_timeoffset = []
    mbr_modified_timestamp = []
    MBR_filepath=""
    lmdout_file_path=""
    all_timeoffset=0
    if (args.timeoffset != None):
        manual_timeoffset = args.timeoffset
        print("Timeoffset relative to system determined optical timeoffset was set to", str(manual_timeoffset),
              "m-sec")
# define lmdout file path
    if (args.mbr!=None and args.lmdout == None):
        MBR_filepath = args.mbr
        directory = MBR_filepath[:MBR_filepath.rfind(".") + 1]
        lmdout_file_path = directory + "lmdout"
    elif (args.mbr!=None and args.lmdout != None):
        MBR_filepath = args.mbr
        directory = MBR_filepath[:MBR_filepath.rfind(".") + 1]
        lmdout_file_path = args.lmdout
# write lmdout file or show MBR figure
    if (args.mbr==None and args.showfigs==True): #show daf figure only
        print("No mbr file detected, script runs without generate the lmdout file")
        print("Detects show figures of daf.")
        showfig=sdaf.class_show_daf_MBR_fig(daf_file_path)
        showfig.fun_show_daf_fig()
    elif (args.mbr != None and args.showdebug == None and args.showdebug2 == None): # write lmdout and/or show mbr figure or debug figure.
        print("Detects write of lmdout from .daf and .mbr.")
        writelmdout = dmlmdout.class_daf_mbr2lmdout(daf_file_path, MBR_filepath, manual_timeoffset*1000,
                                                    args.initialspot * 1000,args.log)
        writelmdout.fun_daf_mbr2lmdout(lmdout_file_path)
        writelmdout.fun_daf_MBR_figs(args.showfigs,args.showdebug,args.showdebug2)
    elif (args.mbr != None and args.showdebug2 != None): # show daf and MBR with given offset
        print("Detects show figures of daf and MBR with offset:", args.showdebug2)
        writelmdout = dmlmdout.class_daf_mbr2lmdout(daf_file_path, MBR_filepath, manual_timeoffset * 1000,
                                                    args.initialspot * 1000, args.log)
        writelmdout.fun_daf_MBR_figs(args.showfigs,args.showdebug,args.showdebug2)
