import read_daf
import read_mbr
import daf_mbr2lmdout
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import numpy as np

class class_show_daf_fig:
    def __init__(self, daf_file_path, mbr_file_path, all_timeoffset):
        self.daf_file_path = daf_file_path
        self.mbr_file_path= mbr_file_path
        
        self.all_timeoffset=all_timeoffset
        self.point_time_stamp=[]
        self.points=[] # only 1 to show points in figure
        self.random_offset=0
        self.daf_mbr2lmdout=[]
        #try:
        self.fun_showfigure()
        #except ValueError: 
        #    print("daf file correct?")
    def fun_showfigure(self):
        #self.daf_mbr2lmdout.read_daf=read_daf.class_read_daf(self.daf_file_path)
        #self.daf_mbr2lmdout.read_mbr=read_mbr.class_read_mbr(self.mbr_file_path)
        self.daf_mbr2lmdout=daf_mbr2lmdout.class_daf_mbr2lmdout(self.daf_file_path, self.mbr_file_path, 0,0)
        BeamIn_arr=np.array(self.daf_mbr2lmdout.read_daf.BeamIn)
        # float to int
        BeamIn_for_plot=np.int64(BeamIn_arr>0)

        fig=plt.figure()
        
        #subplot 1 Resplevel
        axRespLevel=plt.subplot(511)
        #change to msec figure x axis.
        DataNo_msec=[i /1000 for i in self.daf_mbr2lmdout.read_daf.DataNo]
        axRespLevel.plot(DataNo_msec, self.daf_mbr2lmdout.read_daf.RespLevel, label = 'Resplevel')
        axRespLevel.get_xaxis().set_visible(False)
        
        axRespLevel.set_ylabel("Resplevel(%)")
        axRespLevel.get_xaxis().get_major_formatter().set_scientific(False)
        axRespLevel.format_coord =self.format_coord
        
        
        #subplot 2 RespGateOut
        axRespGateOut=plt.subplot(512, sharex=axRespLevel)
        axRespGateOut.scatter(DataNo_msec, self.daf_mbr2lmdout.read_daf.GateOut, color='green', label = 'RespGateOut')
        axRespGateOut.get_xaxis().set_visible(False)

        axRespGateOut.set_ylabel('Gate On/Off')
        axRespGateOut.set_ylim(-0.5, 1.5)
        axRespGateOut.format_coord =self.format_coord
        
        #subplot 3 Beamin
        axRespBeamin=plt.subplot(513, sharex=axRespLevel)
        axRespBeamin.scatter(DataNo_msec, BeamIn_for_plot, color='orange',  label = 'Beamin')
        axRespBeamin.get_xaxis().set_visible(False)

        axRespBeamin.set_ylabel('Beam On/Off')
        axRespBeamin.set_ylim(-0.5, 1.5)
        axRespBeamin.format_coord =self.format_coord
        
        #subplot 4 irr_point match the first irr point with first daf beam in point
        axRespIrrPoint=plt.subplot(514, sharex=axRespLevel)
        start_point_timeoffset=self.daf_mbr2lmdout.fun_determin_start_point_timeoffset()
        for tempvoxelinfo in self.daf_mbr2lmdout.read_mbr.voxel_info:
            #self.point_time_stamp.append(int(tempvoxelinfo[10])+start_point_timeoffset)
            self.point_time_stamp.append(int(tempvoxelinfo[10])+self.all_timeoffset)
            self.points.append(1)
        point_timestamp_msec=[i /1000 for i in self.point_time_stamp]
        axRespIrrPoint.scatter(point_timestamp_msec, self.points, color='purple',  label = 'Irr points')
        axRespIrrPoint.get_xaxis().set_visible(False)
       
        axRespIrrPoint.set_ylabel('Irr points')
        axRespIrrPoint.set_ylim(-0.5, 1.5)
        axRespIrrPoint.format_coord =self.format_coord
       
        #subplot 5 irr_point modified and shifted
        axRespIrrPoint_mod=plt.subplot(515, sharex=axRespLevel)
        point_timestamp_mod_msec=[((int(i) /1000)+self.all_timeoffset/1000) for i in self.daf_mbr2lmdout.mbr_modified_timestamp]
        axRespIrrPoint_mod.scatter(point_timestamp_mod_msec, self.points, color='purple',  label = 'Irr points')

        axRespIrrPoint_mod.set_ylabel('Irr points mod')
        axRespIrrPoint_mod.set_ylim(-0.5, 1.5)
        axRespIrrPoint_mod.format_coord =self.format_coord
        axRespIrrPoint_mod.set_xlabel('Time(msec)')
        
        #cross line
        cursor = Cursor(axRespIrrPoint_mod, horizOn = True, useblit=True, color='r', linewidth=1, linestyle='dotted')

        #不显示边框
        #[axRespLevel.spines[loc_axis].set_visible(False) for loc_axis in ['top','right','bottom','left']]
        #plt.tight_layout()

        plt.show()
        
# rebuild format_coord to show coordinate info in int format, not the scientific format.        
    def format_coord(self, x, y):
        return 'x:%i, y:%i' % (x, y)


