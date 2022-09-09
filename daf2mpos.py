import read_daf
import related_funs
class class_daf2mpos:
    def __init__(self, daf_file_path, mpos_file_path , path2logfile):
        self.path2logfile=path2logfile
        self.daf_file_path = daf_file_path
        self.mpos_file_path=mpos_file_path
        self.mpos_ab_file_path = mpos_file_path[:mpos_file_path.rfind('.')]+'_ab.mpos'
        self.timeoffset=0
        try:
            self.fun_daf2mpos()
        except ValueError: 
            loginfo="fun_daf2mpos error, daf/mpos file correct?"
            print(loginfo)
            related_funs.writelog(self.path2logfile,loginfo)

    def fun_daf2mpos(self):
        loginfo = '\nFor: ' + self.daf_file_path
        related_funs.writelog(self.path2logfile, loginfo)

        daf_file_info=read_daf.class_read_daf(self.daf_file_path)
     
        #print(daf_file_info.DataNo)
        fileversion="20090508"
        dateinfo=daf_file_info.date
        Start_Phase=daf_file_info.Start_Phase
        End_Phase=daf_file_info.End_Phase
        #


        writehead=''
        writehead='!filetype MPOS\n'+"!fileversion "+ fileversion+"\n"+"!filedate "+ dateinfo+"\n"+\
                  "!Patient_name Unknown\n"+"!timeunit 1000\n"+"!timeoffset "+str(self.timeoffset)+"\n"+"!nomarkers 1\n"+\
                  "!corrctno NO\n"+"!mpos\n"+\
                  "# Meaning of the values is: time(*1000usec) | corrctno | marker1_x | marker1_y | marker1_z | marker2_x | . . .\n"

# write mpos file
        with open(self.mpos_file_path,  "w") as mposFile:
            #mposFile.write("!comment This file was created by python script daf_mbr2mpos_lmdout tool\n")
            #mposFile.write("!The original file is in:"+self.daf_file_path+"\n")
            mposFile.writelines(writehead)
            for i in range(0, len(daf_file_info.DataNo)):
                    mposFile.write(str(daf_file_info.DataNo[i]/1000))
                    # corresponding CT number, should be implemented in the future.
                    mposFile.write(" -1 ")
                    mposFile.write(str(daf_file_info.RespLevel[i])+" 0.0 0.0\n")
            loginfo="mpos file was generated in: "+ self.mpos_file_path
            print(loginfo)
            related_funs.writelog(self.path2logfile, loginfo)

# write amplitude baed mpos file.
        writempos_ab=''
        peakflag=False
        vallyflag=True
        for i in range(0, len(daf_file_info.DataNo)):
            # self.DataNo.append(int(listFromLine[0]) * int(self.DataTime_msec) * 1000)
            # self.RespLevel.append(int(listFromLine[1]))
            # self.RespPhase.append(int(listFromLine[2]))
            writempos_ab += str(daf_file_info.DataNo[i]/1000)
            writempos_ab += " -1 "

            if daf_file_info.RespPhase=='2':
                peakflag=True
                vallyflag = False
            elif daf_file_info.RespPhase=='4':
                peakflag = False
                vallyflag = True

            if float(daf_file_info.RespLevel[i])<=0.2:
                RespLevel=0.01
            elif  float(daf_file_info.RespLevel[i])>99.99:
                RespLevel = 9.99
            else:
                RespLevel=("%.2f" % (float(daf_file_info.RespLevel[i])/20.0))

            if vallyflag:
                writempos_ab += str(RespLevel) + " 0.0 0.0\n"
            elif peakflag:
                writempos_ab += str(10.00-RespLevel) + " 0.0 0.0\n"
        with open(self.mpos_ab_file_path, "w") as mposabFile:
            mposabFile.writelines(writehead)
            mposabFile.writelines(writempos_ab)
        loginfo="mpos amplitude based file was generated in: "+ self.mpos_ab_file_path
        print(loginfo)
        related_funs.writelog(self.path2logfile, loginfo)

