import read_daf
class class_daf2mpos:
    def __init__(self, daf_file_path, mpos_file_path):
        self.daf_file_path = daf_file_path
        self.mpos_file_path=mpos_file_path
        self.timeoffset=0
        try:
            self.fun_daf2mpos()
        except ValueError: 
            print("fun_daf2mpos error, daf/mpos file correct?")
            
    def fun_daf2mpos(self):
        daf_file_info=read_daf.class_read_daf(self.daf_file_path)
     
        #print(daf_file_info.DataNo)
        fileversion="1.0"
        dateinfo=daf_file_info.date
        Start_Phase=daf_file_info.Start_Phase
        End_Phase=daf_file_info.End_Phase

        with open(self.mpos_file_path,  "w") as mposFile:
            #mposFile.write("!comment This file was created by python script daf_mbr2mpos_lmdout tool\n")
            #mposFile.write("!The original file is in:"+self.daf_file_path+"\n")
            mposFile.write("!filetype MPOS\n")
            mposFile.write("!fileversion "+ fileversion+"\n")
            mposFile.write("!filedate "+ dateinfo+"\n")
            mposFile.write("!Patient_name Unknown\n")
            mposFile.write("!timeunit 1000\n")
            mposFile.write("!timeoffset "+str(self.timeoffset)+"\n")
            mposFile.write("!nomarkers 1\n")
            mposFile.write("!corrctno NO\n")
            mposFile.write("!mpos\n")
            mposFile.write("# Meaning of the values is: time(*1000usec) | corrctno | marker1_x | marker1_y | marker1_z | marker2_x | . . .\n")
            for i in range(0, len(daf_file_info.DataNo)):
                    mposFile.write(str(daf_file_info.DataNo[i]))
                    # corresponding CT number, should be implemented in the future.
                    mposFile.write(" -1 ")
                    mposFile.write(str(daf_file_info.RespLevel[i])+" 0.000 0.000\n")
            print("mpos file was generated in: ", self.mpos_file_path)
