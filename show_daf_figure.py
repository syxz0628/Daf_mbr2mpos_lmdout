import read_daf
import read_mbr
import daf_mbr2lmdout
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import numpy as np


class class_show_daf_MBR_fig:
    def __init__(self, daf_file_path):
        self.daf_file_path = daf_file_path
        self.point_time_stamp = []
        self.points = []  # only 1 to show points in figure
        self.daf_file = []
    # def fun_show_daf_fig_MBR_debug(self,all_timeoffset,mbr_timestamp_info,mbr_timestamp_info2,mbr_timestamp_info3):
    #
    #     self.daf_file = read_daf.class_read_daf(self.daf_file_path)
    #     BeamIn_arr = np.array(self.daf_file.BeamIn)
    #     # float to int
    #     BeamIn_for_plot = np.int64(BeamIn_arr > 0)
    #     fig = plt.figure()
    #
    #     # subplot 1 Resplevel
    #     axRespLevel = plt.subplot(511)
    #     # change to msec figure x axis.
    #     DataNo_msec = [i / 1000 for i in self.daf_file.DataNo]
    #     axRespLevel.plot(DataNo_msec, self.daf_file.RespLevel, label='Resplevel')
    #     axRespLevel.get_xaxis().set_visible(False)
    #
    #     axRespLevel.set_ylabel("Resplevel(%)")
    #     axRespLevel.get_xaxis().get_major_formatter().set_scientific(False)
    #     axRespLevel.format_coord = self.format_coord
    #
    #     # subplot 2 RespGateOut
    #     axRespGateOut = plt.subplot(512, sharex=axRespLevel)
    #     axRespGateOut.scatter(DataNo_msec, self.daf_file.GateOut, color='green', label='RespGateOut')
    #     axRespGateOut.get_xaxis().set_visible(False)
    #
    #     axRespGateOut.set_ylabel('Gate On/Off')
    #     axRespGateOut.set_ylim(-0.5, 1.5)
    #     axRespGateOut.format_coord = self.format_coord
    #
    #     # subplot 3 Beamin
    #     axRespBeamin = plt.subplot(513, sharex=axRespLevel)
    #     axRespBeamin.scatter(DataNo_msec, BeamIn_for_plot, color='orange', label='Beamin')
    #     axRespBeamin.get_xaxis().set_visible(False)
    #
    #     axRespBeamin.set_ylabel('Beam On/Off')
    #     axRespBeamin.set_ylim(-0.5, 1.5)
    #     axRespBeamin.format_coord = self.format_coord
    #
    #     # subplot 4 irr_point match the first irr point with first daf beam in point
    #     axRespIrrPoint = plt.subplot(514,sharex=axRespLevel)
    #     point_time_stamp=[]
    #     points=[]
    #     for temptimestampinfo in mbr_timestamp_info:
    #         # self.point_time_stamp.append(int(tempvoxelinfo[10])+start_point_timeoffset)
    #         point_time_stamp.append(int(temptimestampinfo) + all_timeoffset)
    #         points.append(1)
    #     point_timestamp_msec = [i / 1000 for i in point_time_stamp]
    #     axRespIrrPoint.scatter(point_timestamp_msec, points, color='purple', label='Irr points')
    #
    #     axRespIrrPoint.set_ylabel('Irr points')
    #     axRespIrrPoint.set_ylim(-0.5, 1.5)
    #     axRespIrrPoint.format_coord = self.format_coord
    #     #axRespIrrPoint.set_xlabel('Time(msec)')
    #     axRespIrrPoint.get_xaxis().set_visible(False)
    #
    #
    #     axRespIrrLastPoint = plt.subplot(515,sharex=axRespLevel)
    #     points_endpoint=[]
    #     point_start_end_time_stamp=[]
    #     for temptimestampinfo in mbr_timestamp_info2:
    #         point_start_end_time_stamp.append(int(temptimestampinfo)+all_timeoffset)
    #         points_endpoint.append(1)
    #     for temptimestampinfo in mbr_timestamp_info3:
    #         point_start_end_time_stamp.append(int(temptimestampinfo)+all_timeoffset)
    #         points_endpoint.append(1)
    #     point_timestamp_msec = [i / 1000 for i in point_start_end_time_stamp]
    #     axRespIrrLastPoint.scatter(point_timestamp_msec, points_endpoint, color='purple', label='Irr start/end points')
    #
    #     axRespIrrLastPoint.set_ylabel('Irr start/end points')
    #     axRespIrrLastPoint.set_ylim(-0.5, 1.5)
    #     axRespIrrLastPoint.format_coord = self.format_coord
    #     axRespIrrLastPoint.set_xlabel('Time(msec)')
    #
    #     # cross line
    #     cursor = Cursor(axRespIrrPoint, horizOn=True, useblit=True, color='r', linewidth=1, linestyle='dotted')
    #
    #     # 不显示边框
    #     # [axRespLevel.spines[loc_axis].set_visible(False) for loc_axis in ['top','right','bottom','left']]
    #     # plt.tight_layout()
    #
    #     plt.show()
    def fun_show_daf_MBR_fig(self,all_timeoffset,mbr_timestamp_info,mbr_timestamp_info2,mbr_timestamp_info3):
        self.daf_file = read_daf.class_read_daf(self.daf_file_path)
        BeamIn_arr = np.array(self.daf_file.BeamIn)
        # float to int
        BeamIn_for_plot = np.int64(BeamIn_arr > 0)
        fig = plt.figure()

        # subplot 1 Resplevel
        axRespLevel = plt.subplot(511)
        # change to msec figure x axis.
        DataNo_msec = [i / 1000 for i in self.daf_file.DataNo]
        axRespLevel.plot(DataNo_msec, self.daf_file.RespLevel, label='Resplevel')
        axRespLevel.get_xaxis().set_visible(False)

        axRespLevel.set_ylabel("Resplevel(%)")
        axRespLevel.get_xaxis().get_major_formatter().set_scientific(False)
        axRespLevel.format_coord = self.format_coord

        # subplot 2 RespGateOut
        axRespGateOut = plt.subplot(512, sharex=axRespLevel)
        axRespGateOut.scatter(DataNo_msec, self.daf_file.GateOut, color='green', label='RespGateOut')
        axRespGateOut.get_xaxis().set_visible(False)

        axRespGateOut.set_ylabel('Gate On/Off')
        axRespGateOut.set_ylim(-0.5, 1.5)
        axRespGateOut.format_coord = self.format_coord

        # subplot 3 Beamin
        axRespBeamin = plt.subplot(513, sharex=axRespLevel)
        axRespBeamin.scatter(DataNo_msec, BeamIn_for_plot, color='orange', label='Beamin')
        axRespBeamin.get_xaxis().set_visible(False)

        axRespBeamin.set_ylabel('Beam On/Off')
        axRespBeamin.set_ylim(-0.5, 1.5)
        axRespBeamin.format_coord = self.format_coord

        # subplot 4 irr_point match the first irr point with first daf beam in point
        axRespIrrPoint = plt.subplot(514,sharex=axRespLevel)
        point_time_stamp=[]
        points=[]
        for temptimestampinfo in mbr_timestamp_info:
            # self.point_time_stamp.append(int(tempvoxelinfo[10])+start_point_timeoffset)
            point_time_stamp.append(int(temptimestampinfo) + all_timeoffset)
            points.append(1)
        point_timestamp_msec = [i / 1000 for i in point_time_stamp]
        axRespIrrPoint.scatter(point_timestamp_msec, points, color='purple', label='Irr points')

        axRespIrrPoint.set_ylabel('Irr MBR ori points')
        axRespIrrPoint.set_ylim(-0.5, 1.5)
        axRespIrrPoint.format_coord = self.format_coord
        #axRespIrrPoint.set_xlabel('Time(msec)')
        axRespIrrPoint.get_xaxis().set_visible(False)


        axRespIrrLastPoint = plt.subplot(515,sharex=axRespLevel)
        points_endpoint=[]
        point_start_end_time_stamp=[]
        if mbr_timestamp_info3 != None and mbr_timestamp_info2!=None: # shows start and end points only for debug
            for temptimestampinfo in mbr_timestamp_info2:
                point_start_end_time_stamp.append(int(temptimestampinfo)+all_timeoffset)
                points_endpoint.append(1)

            for temptimestampinfo in mbr_timestamp_info3:
                point_start_end_time_stamp.append(int(temptimestampinfo)+all_timeoffset)
                points_endpoint.append(1)
            point_timestamp_msec = [i / 1000 for i in point_start_end_time_stamp]
            axRespIrrLastPoint.scatter(point_timestamp_msec, points_endpoint, color='purple', label='Irr start/end points')

            axRespIrrLastPoint.set_ylabel('Irr start/end points')
            axRespIrrLastPoint.set_ylim(-0.5, 1.5)
            axRespIrrLastPoint.format_coord = self.format_coord
            axRespIrrLastPoint.set_xlabel('Time(msec)')
        elif mbr_timestamp_info2!=None:
            for temptimestampinfo in mbr_timestamp_info2:
                point_start_end_time_stamp.append(int(temptimestampinfo)+all_timeoffset)
                points_endpoint.append(1)
            point_timestamp_msec = [i / 1000 for i in point_start_end_time_stamp]
            axRespIrrLastPoint.scatter(point_timestamp_msec, points_endpoint, color='purple',
                                       label='Irr MBR mod points')

            axRespIrrLastPoint.set_ylabel('Irr MBR mod points')
            axRespIrrLastPoint.set_ylim(-0.5, 1.5)
            axRespIrrLastPoint.format_coord = self.format_coord
            axRespIrrLastPoint.set_xlabel('Time(msec)')
        # cross line
        cursor = Cursor(axRespIrrPoint, horizOn=True, useblit=True, color='r', linewidth=1, linestyle='dotted')

        # 不显示边框
        # [axRespLevel.spines[loc_axis].set_visible(False) for loc_axis in ['top','right','bottom','left']]
        # plt.tight_layout()

        plt.show()
    def fun_show_daf_fig(self,mpos_ab_file_path):
        # self.daf_mbr2lmdout.read_daf=read_daf.class_read_daf(self.daf_file_path)
        # self.daf_mbr2lmdout.read_mbr=read_mbr.class_read_mbr(self.mbr_file_path)
        self.daf_mbr2lmdout = read_daf.class_read_daf(self.daf_file_path)
        BeamIn_arr = np.array(self.daf_mbr2lmdout.BeamIn)
        # float to int
        BeamIn_for_plot = np.int64(BeamIn_arr > 0)
        mpos_ab_time_for_plot,mpos_ab_data_for_plot=self.read_mpos(mpos_ab_file_path)



        fig = plt.figure()

        # subplot 1 Resplevel
        axRespLevel = plt.subplot(411)
        # change to msec figure x axis.
        DataNo_msec = [i / 1000 for i in self.daf_mbr2lmdout.DataNo]
        axRespLevel.plot(DataNo_msec, self.daf_mbr2lmdout.RespLevel, label='Resplevel')
        axRespLevel.get_xaxis().set_visible(False)

        axRespLevel.set_ylabel("Resplevel(%)")
        axRespLevel.get_xaxis().get_major_formatter().set_scientific(False)
        axRespLevel.format_coord = self.format_coord

        # subplot 2 RespGateOut
        # axRespGateOut = plt.subplot(412, sharex=axRespLevel)
        # axRespGateOut.scatter(DataNo_msec, self.daf_mbr2lmdout.GateOut, color='green', label='RespGateOut')
        # axRespGateOut.get_xaxis().set_visible(False)
        #
        # axRespGateOut.set_ylabel('Gate On/Off')
        # axRespGateOut.set_ylim(-0.5, 1.5)
        # axRespGateOut.format_coord = self.format_coord

        # subplot 5 daf resp phase
        axdaf_phase = plt.subplot(412, sharex=axRespLevel)
        axdaf_phase.scatter(DataNo_msec, self.daf_mbr2lmdout.RespPhase, color='black', label='daf_phase')
        axdaf_phase.get_xaxis().set_visible(False)
        axdaf_phase.set_ylabel('daf phase')
        axdaf_phase.set_ylim(0, 5)
        axdaf_phase.format_coord = self.format_coord

        # subplot 3 Beamin
        axRespBeamin = plt.subplot(413, sharex=axRespLevel)
        axRespBeamin.scatter(DataNo_msec, BeamIn_for_plot, color='orange', label='Beamin')
        axRespBeamin.get_xaxis().set_visible(False)

        axRespBeamin.set_ylabel('Beam On/Off')
        axRespBeamin.set_ylabel('Beam On/Off')
        axRespBeamin.set_ylim(-0.5, 1.5)
        axRespBeamin.format_coord = self.format_coord

        # subplot 4 amplitude based mpos
        axmpos_ab_state = plt.subplot(414, sharex=axRespLevel)
        axmpos_ab_state.scatter(DataNo_msec, mpos_ab_data_for_plot, color='purple', label='mpos_ab_state')
        #axmpos_ab_state.get_xaxis().set_visible(False)
        #axmpos_ab_state.set_ylabel('amplitude \nbased state')
        axmpos_ab_state.set_ylim(0, 10)
        axmpos_ab_state.format_coord = self.format_coord

        axmpos_ab_state.set_xlabel('Time(msec)')

        # cross line
        cursor = Cursor(axmpos_ab_state, horizOn=True, useblit=True, color='r', linewidth=1, linestyle='dotted')

        # 不显示边框
        # [axRespLevel.spines[loc_axis].set_visible(False) for loc_axis in ['top','right','bottom','left']]
        # plt.tight_layout()

        plt.show()
    # rebuild format_coord to show coordinate info in int format, not the scientific format.
    def format_coord(self, x, y):
        return 'x:%i, y:%i' % (x, y)
    def read_mpos(self,mpospath):
        timemsec=[]
        datamsec=[]
        timeunit=1 # usec
        with open(mpospath,'r') as mposfile:
            alllines=mposfile.readlines()
        for oneline in alllines:
            if 'timeunit' in oneline:
                timeunit = float(oneline.split()[1])
        for oneline in alllines:
            onelinesplit=oneline.split()
            if (onelinesplit[0][0].isdigit()):
                timemsec.append(float(onelinesplit[0])*timeunit/1000)
                datamsec.append(float(onelinesplit[2]))
        return np.array(timemsec),np.array(datamsec)

