# read daf file and get useful informations includes:
# "GatingModeNumber:",3
# "ECGUse:",0
# "GateTotal:","17916"
# "RespAve(sec):",5.829643
# "HeartAve(sec):",0
# "DataPosi:",439
# "DataMagn:",716
# "Sample:",32646
# "Comment:","                                                                                                                                "
# "Data Time(msec):",25
# "Sweep Point:","In: 50"
# "Start Point:","Ex: 20"
# "End Point:","In: 20"
# "All Gate time(sec):","447.90"
#"***DataNo., RespLevel, RespPhase, RespGate, EcgLevel, EcgPeak, EcgGate, GateOut, BeamIn, Error Message(Inter Lock)[Magn/Posi]***"

class class_read_daf:
    def __init__(self, daf_file_path):
        self.daf_file_path = daf_file_path
        
        self.fileversion=1.0
        self.date="2022/05/12"
        self.Start_Phase="0"
        self.End_Phase="1"
        self.DataTime_msec=25000
        self.DataNo=[]
        self.RespLevel=[]
        self.RespPhase=[]
        self.RespGate=[]
        self.EcgLevel=[]
        self.EcgPeak=[]
        self.EcgGate=[]
        self.GateOut=[]
        self.BeamIn=[]
        self.Error_Message_interlock=[]
        try:
            self.fun_readdaf()
        except ValueError: 
            print("fun_readdaf error, daf file correct?")
            
    def fun_readdaf(self):
        with open(self.daf_file_path) as File:
            AllLines = File.readlines()
            for Line in AllLines:
                Line=Line.strip('\n')
                Line=Line.replace('"', '')
                listFromLine = Line.split(',')
                if ("Version" in Line):
                    self.fileversion=listFromLine[1].split()[1]
                elif ("Date" in Line):
                    self.date=listFromLine[1]
                elif("Data Time" in Line): # time step in the daf file. 25msec is the default.  change to micro-sec by multiply 1000
                    self.DataTime_msec=listFromLine[1]
                elif("Start Point" in Line):
                    self.Start_Phase=listFromLine[1]
                elif("End Point" in Line):
                    self.End_Phase=listFromLine[1]
                    break
            for Line in AllLines:
                listFromLine = Line.split(',')
                if (listFromLine[0][0].isdigit()):
                    # start data writing;
                    self.DataNo.append(int(listFromLine[0])*int(self.DataTime_msec)*1000)
                    self.RespLevel.append(int(listFromLine[1]))
                    self.RespPhase.append(int(listFromLine[2]))
                    self.RespGate.append(int(listFromLine[3]))
                    self.EcgLevel.append(int(listFromLine[4]))
                    self.EcgPeak.append(int(listFromLine[5]))
                    self.EcgGate.append(int(listFromLine[6]))
                    self.GateOut.append(int(listFromLine[7]))
                    self.BeamIn.append(int(listFromLine[8]))
                    Error_Temp=listFromLine[9].strip('\n')
                    Error_Temp=Error_Temp.replace('"', '')
                    self.Error_Message_interlock.append(Error_Temp)
            
