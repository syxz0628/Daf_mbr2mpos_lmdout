import read_daf
import related_funs
class class_daf2mpos:
    def __init__(self, daf_file_path, mpos_file_path , path2logfile):
        self.path2logfile=path2logfile
        self.daf_file_path = daf_file_path
        self.mpos_file_path = mpos_file_path
        self.mpos_ab_file_path = mpos_file_path[:mpos_file_path.rfind('.')]+'_ab.mpos'
        self.timeoffset=0
        self.daf_file_info = read_daf.class_read_daf(self.daf_file_path)
        self.writehead=''
        try:
            self.fun_writehead()
            self.fun_daf2mpos()
            self.fun_daf2mpos_ab()
        except ValueError: 
            loginfo="fun_daf2mpos error, daf/mpos file correct?"
            print(loginfo)
            related_funs.writelog(self.path2logfile,loginfo)

    def fun_writehead(self):
        loginfo = '\nFor: ' + self.daf_file_path
        related_funs.writelog(self.path2logfile, loginfo)

        daf_file_info = read_daf.class_read_daf(self.daf_file_path)

        # print(daf_file_info.DataNo)
        fileversion = "20090508"
        dateinfo = daf_file_info.date
        Start_Phase = daf_file_info.Start_Phase
        End_Phase = daf_file_info.End_Phase
        #
        self.writehead = ''
        self.writehead = '!filetype MPOS\n' + "!fileversion " + fileversion + "\n" + "!filedate " + dateinfo + "\n" + \
                    "!Patient_name Unknown\n" + "!timeunit 1000\n" + "!timeoffset " + str(
            self.timeoffset) + "\n" + "!nomarkers 1\n" + \
                    "!corrctno NO\n" + "!mpos\n" + \
                    "# Meaning of the values is: time(*1000usec) | corrctno | marker1_x | marker1_y | marker1_z | marker2_x | . . .\n"
    def fun_daf2mpos(self):
# write mpos file
        with open(self.mpos_file_path,  "w") as mposFile:
            #mposFile.write("!comment This file was created by python script daf_mbr2mpos_lmdout tool\n")
            #mposFile.write("!The original file is in:"+self.daf_file_path+"\n")
            mposFile.writelines(self.writehead)
            for i in range(0, len(self.daf_file_info.DataNo)):
                    mposFile.write(str(self.daf_file_info.DataNo[i]/1000))
                    # corresponding CT number, should be implemented in the future.
                    mposFile.write(" -1 ")
                    mposFile.write(str(self.daf_file_info.RespLevel[i])+" 0.0 0.0\n")
            loginfo="mpos file was generated in: "+ self.mpos_file_path
            print(loginfo)
            related_funs.writelog(self.path2logfile, loginfo)
    def fun_daf2mpos_ab(self):
# write amplitude based mpos file.
        writempos_ab=''
        peakflag=False
        vallyflag=True
        Exflag=True
        Inflag=False
        for i in range(0, len(self.daf_file_info.DataNo)):
            # self.DataNo.append(int(listFromLine[0]) * int(self.DataTime_msec) * 1000)
            # self.RespLevel.append(int(listFromLine[1]))
            # self.RespPhase.append(int(listFromLine[2]))
            writempos_ab += str(self.daf_file_info.DataNo[i]/1000)
            writempos_ab += " -1 "
            # 2 means peak flag, 4 means vally flag
            if self.daf_file_info.RespPhase[i]==2:
                peakflag=True
                vallyflag = False
            elif self.daf_file_info.RespPhase[i]==4:
                peakflag = False
                vallyflag = True
            # 2, define as IN flag.(decline)
            # 4, define as EX flag.(incline)
            # 1, vally flag and 1-3-2 exist, define as EX flag; else, In flag.
            # 3, peak flag and 3-1-4 exist, define as In flag; else, Ex flag.
            checkRespPhase=[]
            for j in range (i, len(self.daf_file_info.DataNo)):
                if self.daf_file_info.RespPhase[j]==2 or self.daf_file_info.RespPhase[j]==4:
                    break
                checkRespPhase.append(self.daf_file_info.RespPhase[j])

            if self.daf_file_info.RespPhase[i]==1:
                if vallyflag and (3 in checkRespPhase):
                        Exflag = True
                        Inflag = False
                else:
                    Inflag = True
                    Exflag = False
            elif self.daf_file_info.RespPhase[i]==2:
                pass
            elif self.daf_file_info.RespPhase[i]==3:
                if peakflag and (1 in checkRespPhase):
                        Inflag = True
                        Exflag = False
                else:
                    Exflag = True
                    Inflag = False
            if self.daf_file_info.RespPhase[i]==4:
                pass

            if float(self.daf_file_info.RespLevel[i])<=10:
                RespState=0.01
            elif float(self.daf_file_info.RespLevel[i])>10 and float(self.daf_file_info.RespLevel[i])<=30:
                if Inflag:
                    RespState = 1.01
                elif Exflag:
                    RespState = 9.01
            elif float(self.daf_file_info.RespLevel[i])>30 and float(self.daf_file_info.RespLevel[i])<=50:
                if Inflag:
                    RespState = 2.01
                elif Exflag:
                    RespState = 8.01
            elif float(self.daf_file_info.RespLevel[i])>50 and float(self.daf_file_info.RespLevel[i])<=70:
                if Inflag:
                    RespState = 3.01
                elif Exflag:
                    RespState = 7.01
            elif float(self.daf_file_info.RespLevel[i])>70 and float(self.daf_file_info.RespLevel[i])<=90:
                if Inflag:
                    RespState = 4.01
                elif Exflag:
                    RespState = 6.01
            elif float(self.daf_file_info.RespLevel[i])>90:
                RespState=5.01
            else:
                loginfo = "error data Resplevel found as " + str(self.daf_file_info.DataNo[i])
                print(loginfo)
                related_funs.writelog(self.path2logfile, loginfo)

            writempos_ab += str(RespState) + " 0.0 0.0\n"
        with open(self.mpos_ab_file_path, "w") as mposabFile:
            mposabFile.writelines(self.writehead)
            mposabFile.writelines(writempos_ab)
        loginfo = "mpos amplitude based file was generated in: " + self.mpos_ab_file_path
        print(loginfo)
        related_funs.writelog(self.path2logfile, loginfo)

