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

        axRespIrrPoint.set_ylabel('Irr points')
        axRespIrrPoint.set_ylim(-0.5, 1.5)
        axRespIrrPoint.format_coord = self.format_coord
        #axRespIrrPoint.set_xlabel('Time(msec)')
        axRespIrrPoint.get_xaxis().set_visible(False)


        axRespIrrLastPoint = plt.subplot(515,sharex=axRespLevel)
        points_endpoint=[]
        point_start_end_time_stamp=[]
        for temptimestampinfo in mbr_timestamp_info2:
            point_start_end_time_stamp.append(int(temptimestampinfo)+all_timeoffset)
            points_endpoint.append(1)
        if mbr_timestamp_info3!=None:
            for temptimestampinfo in mbr_timestamp_info3:
                point_start_end_time_stamp.append(int(temptimestampinfo)+all_timeoffset)
                points_endpoint.append(1)
        point_timestamp_msec = [i / 1000 for i in point_start_end_time_stamp]
        axRespIrrLastPoint.scatter(point_timestamp_msec, points_endpoint, color='purple', label='Irr start/end points')

        axRespIrrLastPoint.set_ylabel('Irr start/end points')
        axRespIrrLastPoint.set_ylim(-0.5, 1.5)
        axRespIrrLastPoint.format_coord = self.format_coord
        axRespIrrLastPoint.set_xlabel('Time(msec)')

        # cross line
        cursor = Cursor(axRespIrrPoint, horizOn=True, useblit=True, color='r', linewidth=1, linestyle='dotted')

        # 不显示边框
        # [axRespLevel.spines[loc_axis].set_visible(False) for loc_axis in ['top','right','bottom','left']]
        # plt.tight_layout()

        plt.show()
    def fun_show_daf_fig(self):
        # self.daf_mbr2lmdout.read_daf=read_daf.class_read_daf(self.daf_file_path)
        # self.daf_mbr2lmdout.read_mbr=read_mbr.class_read_mbr(self.mbr_file_path)
        self.daf_mbr2lmdout = read_daf.class_read_daf(self.daf_file_path)
        BeamIn_arr = np.array(self.daf_mbr2lmdout.BeamIn)
        # float to int
        BeamIn_for_plot = np.int64(BeamIn_arr > 0)

        fig = plt.figure()

        # subplot 1 Resplevel
        axRespLevel = plt.subplot(311)
        # change to msec figure x axis.
        DataNo_msec = [i / 1000 for i in self.daf_mbr2lmdout.DataNo]
        axRespLevel.plot(DataNo_msec, self.daf_mbr2lmdout.RespLevel, label='Resplevel')
        axRespLevel.get_xaxis().set_visible(False)

        axRespLevel.set_ylabel("Resplevel(%)")
        axRespLevel.get_xaxis().get_major_formatter().set_scientific(False)
        axRespLevel.format_coord = self.format_coord

        # subplot 2 RespGateOut
        axRespGateOut = plt.subplot(312, sharex=axRespLevel)
        axRespGateOut.scatter(DataNo_msec, self.daf_mbr2lmdout.GateOut, color='green', label='RespGateOut')
        axRespGateOut.get_xaxis().set_visible(False)

        axRespGateOut.set_ylabel('Gate On/Off')
        axRespGateOut.set_ylim(-0.5, 1.5)
        axRespGateOut.format_coord = self.format_coord

        # subplot 3 Beamin
        axRespBeamin = plt.subplot(313, sharex=axRespLevel)
        axRespBeamin.scatter(DataNo_msec, BeamIn_for_plot, color='orange', label='Beamin')
        #        axRespBeamin.get_xaxis().set_visible(False)

        axRespBeamin.set_ylabel('Beam On/Off')
        axRespBeamin.set_ylim(-0.5, 1.5)
        axRespBeamin.format_coord = self.format_coord

        axRespBeamin.set_xlabel('Time(msec)')

        # cross line
        cursor = Cursor(axRespBeamin, horizOn=True, useblit=True, color='r', linewidth=1, linestyle='dotted')

        # 不显示边框
        # [axRespLevel.spines[loc_axis].set_visible(False) for loc_axis in ['top','right','bottom','left']]
        # plt.tight_layout()

        plt.show()
    # rebuild format_coord to show coordinate info in int format, not the scientific format.
    def format_coord(self, x, y):
        return 'x:%i, y:%i' % (x, y)
