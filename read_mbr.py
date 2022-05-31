# read mbr file and get useful information includes:
#############分割线##################
import xml.dom.minidom
import xml.etree.ElementTree
#############分割线##################

class class_read_mbr:
    def __init__(self, mbr_file_path):
        self.mbr_file_path = mbr_file_path
        self.ETtree=[]
        self.MachineBeamRecordVersion="None"
        self.RstFormat="None"
        self.TxRoom="None"
        self.projectile="None"
        self.Gantry_angle="None"
        self.Gating_signals="None"
        self.interruption="None"
        self.Treatment_Start_Time="None"
        self.Treatment_End_Time="None"
        self.Energy_Layer=[]
        self.Energy_Number=[]
        self.Layer_Voxel_Count=[]
        self.focusX=[]
        self.focusY=[]
        self.FocLevId=[]
        self.intensity=[]
        self.IrradTimeIes=[]
        self.DeliveryTimeIes=[]
        self.IesStartTimeStamp=[]
        self.IesStartTimeStampAbs=[]
        self.IrradTimeIes=[]
# voxel information includes all main information for each points. its formats is:
# list voxel={[IESNumber,IESenergy, TotalVoxelIndex,ActFocusX,ActFocusY,ScannerX,ScannerY,MwpcPosX,MwpcPosY,IcImCharge,TimeStamp,TimeStampAbs,VxCnt_in_one_layer]}
# search index     0         1           2             3       4          5         6         7        8       9          10           11      12e
# example voxel_info[8][11] is the TimeStampabs  value from IES: voxel_info[8][0], Voxel: voxel_info[8][2].
        self.voxel_info=[]
        try:
            self.fun_readmbr()
        except ValueError: 
            print("fun_readmbr error, mbr file correct?")
            
    def fun_readmbr(self):
# read xml file as ET
        self.ETtree = xml.etree.ElementTree.ElementTree(file=self.mbr_file_path)
# get some information
        for elem in self.ETtree.iter(tag='ProcessPTTxRecord'):
            self.MachineBeamRecordVersion=elem.get('MachineBeamRecordVersion')
        for elem in self.ETtree.iter(tag='RstFormat'):
            self.RstFormat=elem.text
        for elem in self.ETtree.iter(tag='TxRoom'):
            self.TxRoom=elem.get('name')
            self.projectile=elem.get('projectile')
        for elem in self.ETtree.iter(tag='Gantry'):
            self.Gantry_angle=elem.get('angle')
        for elem in self.ETtree.iter(tag='Gating'):
            self.Gating_signals=elem.get('signals')
        for TT in self.ETtree.iter(tag='TreatmentTime'):
            self.Treatment_Start_Time=TT.get('treatmentStart')
            self.Treatment_End_Time=TT.get('treatmentEnd')   
        for elem in self.ETtree.iter(tag='BeamInfo'):
            self.interruption=elem.get('interruption')

        total_voxel_count=0
        # get energy layer information
        for elemlayer in self.ETtree.iterfind('./ProcessPTTxRecord/Beam/IES'):
            self.Energy_Number.append(elemlayer.get('number'))
            self.Energy_Layer.append(elemlayer.get('energy'))
            self.Layer_Voxel_Count.append(elemlayer.get('VxCnt'))
            self.focusX.append(elemlayer.get('focusX'))
            self.focusY.append(elemlayer.get('focusY'))
            self.FocLevId.append(elemlayer.get('FocLevId'))
            self.intensity.append(elemlayer.get('intensity'))
            self.IrradTimeIes.append(elemlayer.get('IrradTimeIes'))
            self.DeliveryTimeIes.append(elemlayer.get('DeliveryTimeIes'))
            self.IesStartTimeStamp.append(elemlayer.get('IesStartTimeStamp'))
            self.IesStartTimeStampAbs.append(elemlayer.get('IesStartTimeStampAbs'))
            self.IrradTimeIes.append(elemlayer.get('IrradTimeIes'))
# get the voxel information includes:
# list voxel=[energyNumber, energyLayer,TotalVoxelIndex,ActFocusX,ActFocusY,ScannerX,ScannerY,MwpcPosX,MwpcPosY,IcImCharge,TimeStamp,TimeStampAbs,VxCnt_in_one_layer]:
            #Current_Energy_Number=int(int(elemlayer.get('number'))/2)
            #print("write energy number: ",  Current_Energy_Number)
            for elemvoxel in elemlayer:
                tempvoxel=[]
                # voxel_info index 0-11
                tempvoxel.append(elemlayer.get('number'))
                tempvoxel.append(elemlayer.get('energy'))
                current_voxel_count=total_voxel_count+int(elemvoxel.get('VoxelIndex'))
                tempvoxel.append(str(current_voxel_count))
                tempvoxel.append(elemvoxel.get('ActFocusX'))
                tempvoxel.append(elemvoxel.get('ActFocusY'))
                tempvoxel.append(elemvoxel.get('ScannerX'))
                tempvoxel.append(elemvoxel.get('ScannerY'))
                tempvoxel.append(elemvoxel.get('MwpcPosX'))
                tempvoxel.append(elemvoxel.get('MwpcPosY'))
                tempvoxel.append(elemvoxel.get('IcImCharge'))
                tempvoxel.append(elemvoxel.get('TimeStamp'))
                tempvoxel.append(elemvoxel.get('TimeStampAbs'))
                tempvoxel.append(elemlayer.get('VxCnt'))
                self.voxel_info.append(tempvoxel)
            total_voxel_count=int(elemlayer.get('VxCnt'))+total_voxel_count
            #print(total_voxel_count)
    
        
# Beam = self.ETtree.findall('./ProcessPTTxRecord/Beam')
#        for elem in ETtree.iter(tag='TxRoom'):
#               projectile=elem.get('projectile')
#        for EnergyLayers in self.ETtree.iterfind('./ProcessPTTxRecord/Beam/IES'):
#            xmlEnergy=EnergyLayers.get('energy')
#            print(xmlEnergy)
#            for VoxelValues in EnergyLayers:
#                TimeStampAbs=VoxelValues.get('TimeStampAbs')
#            print(TimeStampAbs)
#        for elem in self.ETtree.iter(tag='RstFormat'):
#             self.RstFormat=elem.text
