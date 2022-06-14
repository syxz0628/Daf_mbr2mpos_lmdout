import read_mbr as rmbr
import read_daf as rdaf
import numpy as np
import related_funs as r_funs
import show_daf_figure as s_fig


class class_daf_mbr2lmdout:
    def __init__(self, daf_file_path, mbr_file_path, manual_timeoffset, init_spot_timeoffset):
        self.daf_file_path = daf_file_path
        self.mbr_file_path = mbr_file_path
        self.init_spot_timeoffset = init_spot_timeoffset
        self.lmdout_file_path = ""
        self.manual_timeoffset = manual_timeoffset  # this is very small offset scale of ~250ms based on optimal determined timeoffset by the code. the time offset between daf and mbr are calculated automatically.
        self.random_offset = 0  # some other offset maybe introduced by the system time variation.
        # this is all the time offset includes: 1. system time offsett between the gating and IRONTRI system. Automatically calculated. 2. manual_timeoffset. 3. random offset
        self.all_timeoffset = 0
        self.start_point_timeoffset = 0  # for display only.
        self.lmdout_info = []
        self.mbr_modified_timestamp = []
        self.mbr_start_points = []
        self.mbr_end_points = []
        # item info
        self.current_time_stamp = 0
        self.current_number_point = 0
        self.current_begin_spill = 0
        self.current_end_spill = 0
        self.current_end_of_plane = 0
        self.current_energy = 0
        self.current_focus = 0
        self.previous_timestamp = 0
        self.MBR_beamoff_last_point_timestamp = []
        self.daf_beamoff_last_point_timestamp = []
        self.mbr_origin_timestamp = []
        self.total_charge = 0
        self.total_timestamp = 0
        # get daf and mbr information
        self.read_daf = rdaf.class_read_daf(self.daf_file_path)
        self.read_mbr = rmbr.class_read_mbr(self.mbr_file_path)
        self.start_point_timeoffset = self.fun_determin_start_point_timeoffset()
        for i in self.read_mbr.voxel_info:
            self.mbr_origin_timestamp.append(int(i[10]))

    def fun_daf_mbr2lmdout(self, lmdout_file_path):
        # steps to determin time offset and correct the last point of each spill/energies.
        # 1. use MBR-orinal timestamp data find the temp best match timeoffset with daf (maybe more than 1, choose the first)
        # 2. check MBR-temp-best last point according to the last point alg.
        #    last point alg:
        #    # record first start point
        #    # search until next daf last point,
        #      * any energy change, last point found, record next start point
        #      * if next daf last point- next+1 daf start point <300ms
        #        check 10 points between the next daf last point and start point using last point alg
        #         (points >115ms to the previous_timestamp and <20ms after the point is empty)
        #         find the last match of "last point alg" or the last point instead(no change of ).
        #      * if next daf last point- next+1 daf start point >=300ms
        #        check 10 points between the middle of next daf last point and start point using last point alg
        #         (points >115ms to the previous_timestamp and <20ms after the point is empty)
        #    # modify MBR last point according to charge and get the mbr_mod_timestamp
        # 3 use MBR-mod-timestamp data find the best match timeoffset with daf (maybe more than 1, choose the first)
        print("Starting find temp best match timeoffset of MBR and Daf")
        mbr_temp_bestmatch_timeoffset_in_daf = self.fun_mbr_bestmatch_daf_timeoffset_in_daf(self.mbr_origin_timestamp,
                                                                                            0)
        if (mbr_temp_bestmatch_timeoffset_in_daf == 0):
            print("~~~could not match well(<90%), match of start point will be shown in figure.")
            print("~~~~~~~You need to check daf and mbr file if they really matches")
            self.all_timeoffset = self.start_point_timeoffset
        else:
            # determin self.mbr_start_points and self.mbr_end_points.
            self.fun_determin_MBR_endpoints_timestamp(115000, 20000, mbr_temp_bestmatch_timeoffset_in_daf - int(
                self.read_mbr.voxel_info[0][10]))
            mbr_end_point_offsets = []
            mbr_end_point_offsets = self.fun_determin_endpoint_offset()
            self.fun_mod_MBR(self.mbr_end_points, mbr_end_point_offsets)
            mbr_bestmatch_timeoffset_in_daf = self.fun_mbr_bestmatch_daf_timeoffset_in_daf(self.mbr_modified_timestamp,
                                                                                           mbr_temp_bestmatch_timeoffset_in_daf)
            self.all_timeoffset = mbr_bestmatch_timeoffset_in_daf - int(self.read_mbr.voxel_info[0][10])
        # for test only
        # self.all_timeoffset = self.start_point_timeoffset
        # self.all_timeoffset = mbr_temp_bestmatch_timeoffset_in_daf-int(self.read_mbr.voxel_info[0][10])
        # self.mbr_modified_timestamp=self.mbr_origin_timestamp
        # for test only
        print("the first beam in timestamp in MBR is: ", int(self.read_mbr.voxel_info[0][10]), " usec")
        print("the first beam in timestamp in Daf is: ",
              (self.start_point_timeoffset + int(self.read_mbr.voxel_info[0][10])),
              " usec")
        print("the daf(beam in)-mbr(start point)timeoffset is: ", self.start_point_timeoffset, " usec")
        print("the best match possible timeoffset is: ", self.all_timeoffset, " usec")

        self.lmdout_file_path = lmdout_file_path
        print('Energy layers in MBR:')
        print(self.read_mbr.Energy_Number)
        if (mbr_temp_bestmatch_timeoffset_in_daf != 0):
            self.fun_write_lmdout_info()
            print("lmdout file was generated in: ", self.lmdout_file_path)

    def fun_write_lmdout_info(self):
        with open(self.lmdout_file_path, "w") as lmdoutFile:
            lmdoutFile.write("!comment This file was created by daf_mbr2lmdout script\n")
            lmdoutFile.write("!modality CVS\n")
            lmdoutFile.write("!fileversion 1.0\n")
            lmdoutFile.write("!date " + self.read_daf.date + "\n")
            lmdoutFile.write("!patient_name Unkown\n")
            lmdoutFile.write("!comment Offset, timeunit are consistent 0 sec and 1 micro-sec\n")
            lmdoutFile.write("!offset 0\n")
            lmdoutFile.write("!timeunit 1\n")
            lmdoutFile.write(
                "!comment Timestamp NoofPoint BeginofSpill EndofSpill EndofPlane EnergyValue Focus Intensity\n")
            lmdoutFile.write(
                "!items T NP BS ES EOP E F I\n")
            lmdoutFile.write("0 0 0 0 0 0 0 0\n")
            # write the first line
            # self.current_time_stamp = int(self.read_mbr.voxel_info[0][10]) + self.all_timeoffset - self.init_spot_timeoffset
            self.current_time_stamp = int(
                self.mbr_modified_timestamp[0]) + self.all_timeoffset - self.init_spot_timeoffset
            self.current_number_point = 0
            self.current_begin_spill = 1
            self.current_end_spill = 0
            self.current_end_of_plane = 0
            self.current_energy = int(float(self.read_mbr.voxel_info[0][1]))
            self.current_focus = self.read_mbr.FocLevId[0]
            self.fun_write_one_line_info_to_lmdout_info()
            # write other lines
            self.previous_timestamp = self.current_time_stamp
            count_voxels_in_one_layer = 0
            count_voxels_all = -1
            start_begin_of_spill_even_before_NP = False
            # find lmdout_info include
            # list voxel={[IESNumber,IESenergy,TotalVoxelIndex,ActFocusX,ActFocusY,ScannerX,ScannerY,MwpcPosX,MwpcPosY,IcImCharge,TimeStamp,TimeStampAbs]}
            # search index     0                     1                 2                   3                4                   5                 6                 7                 8                  9                   10                 11
            #
            for tempvoxel_info in self.read_mbr.voxel_info:
                count_voxels_in_one_layer += 1
                count_voxels_all += 1
                # BS event after ES is true
                if (start_begin_of_spill_even_before_NP):
                    self.fun_BS_event(count_voxels_all)
                    start_begin_of_spill_even_before_NP = False
                # NP event
                self.fun_NP_event(count_voxels_all)
                # EOP event
                if count_voxels_in_one_layer == int(tempvoxel_info[12]):
                    self.fun_EOP_event()
                    self.fun_ES_event()
                    count_voxels_in_one_layer = 0
                    start_begin_of_spill_even_before_NP = True
                    print("found an end of plan, in ", int(self.mbr_modified_timestamp[count_voxels_all]))
                    self.previous_timestamp = self.current_time_stamp
                    continue
                if (self.current_time_stamp - self.all_timeoffset) in self.MBR_beamoff_last_point_timestamp:
                    self.fun_ES_event()
                    start_begin_of_spill_even_before_NP = True
                    print("found an end of spill, in ", self.mbr_modified_timestamp[count_voxels_all])
                    self.previous_timestamp = self.current_time_stamp
                    continue
            for templmdout in self.lmdout_info:
                lmdoutFile.write(templmdout)
                lmdoutFile.write('\n')

    def fun_NP_event(self, count_voxels_all):
        self.current_time_stamp = int(self.mbr_modified_timestamp[count_voxels_all]) + self.all_timeoffset
        self.current_number_point += 1
        # self.current_begin_spill no change
        # self.current_end_spill no change
        # self.current_end_of_plane no change
        self.current_energy = int(float(self.read_mbr.voxel_info[self.current_number_point - 1][1]))
        Current_Energy_Number = int(int(self.read_mbr.voxel_info[self.current_number_point - 1][0]) / 2)
        self.current_focus = self.read_mbr.FocLevId[Current_Energy_Number]
        self.fun_write_one_line_info_to_lmdout_info()
        self.previous_timestamp = self.current_time_stamp

    def fun_EOP_event(self):
        self.current_time_stamp = self.previous_timestamp + 1
        # self.current_number_point no change
        # self.current_begin_spill no change
        # self.current_end_spill no changee
        self.current_end_of_plane += 1
        self.current_energy = int(float(self.read_mbr.voxel_info[self.current_number_point - 1][1]))
        Current_Energy_Number = int(int(self.read_mbr.voxel_info[self.current_number_point - 1][0]) / 2)
        self.current_focus = self.read_mbr.FocLevId[Current_Energy_Number]
        self.fun_write_one_line_info_to_lmdout_info()
        self.previous_timestamp = self.current_time_stamp

    def fun_ES_event(self):
        self.current_time_stamp = self.previous_timestamp + 100
        # self.current_number_point no change
        # self.current_begin_spill no change
        self.current_end_spill += 1
        # self.current_end_of_plane+=1
        self.current_energy = int(float(self.read_mbr.voxel_info[self.current_number_point - 1][1]))
        Current_Energy_Number = int(int(self.read_mbr.voxel_info[self.current_number_point - 1][0]) / 2)
        self.current_focus = self.read_mbr.FocLevId[Current_Energy_Number]
        self.fun_write_one_line_info_to_lmdout_info()
        self.previous_timestamp = self.current_time_stamp

    def fun_BS_event(self, count_voxels_all):
        self.current_time_stamp = int(
            self.mbr_modified_timestamp[count_voxels_all]) + self.all_timeoffset - self.init_spot_timeoffset
        # self.current_number_point no change
        self.current_begin_spill += 1
        # self.current_end_spill no change
        # self.current_end_of_plane no change
        self.current_energy = int(float(self.read_mbr.voxel_info[self.current_number_point - 1][1]))
        Current_Energy_Number = int(int(self.read_mbr.voxel_info[self.current_number_point - 1][0]) / 2)
        self.current_focus = self.read_mbr.FocLevId[Current_Energy_Number]
        self.fun_write_one_line_info_to_lmdout_info()
        self.previous_timestamp = self.current_time_stamp

    def fun_write_one_line_info_to_lmdout_info(self):
        list_write_to_lmdout = []
        list_write_to_lmdout.append(self.current_time_stamp)
        list_write_to_lmdout.append(self.current_number_point)
        list_write_to_lmdout.append(self.current_begin_spill)
        list_write_to_lmdout.append(self.current_end_spill)
        list_write_to_lmdout.append(self.current_end_of_plane)
        list_write_to_lmdout.append(self.current_energy)
        list_write_to_lmdout.append(self.current_focus)
        list_write_to_lmdout.append(0)
        self.lmdout_info.append(" ".join(str(i) for i in list_write_to_lmdout))
        #print(self.lmdout_info)

    def fun_mbr_bestmatch_daf_timeoffset_in_daf(self, mbr_timestamp, init_timeoffset):
        shift_MBR_and_daf_match_info_timeoffset = []
        shift_MBR_and_daf_match_info_matchpoints_percent = []
        determin_auto_timeoffset = 0
        temp_timeoffset = []
        if (init_timeoffset == 0):
            # use the first match point and the other 4 big time gap to find possible match of mbr and daf
            daf_first_and_4_longest_timestamp = self.fun_find_daf_first_and_longest_4_timestamp()
            print("Starting loop in gap of daf to find possible match timeoffset of MBR and Daf")
            for longtimegap in daf_first_and_4_longest_timestamp:
                print("loop in longest 5 beam in timestamp gap in daf (including the very first):", longtimegap / 1000,
                      "msec")
                if ((longtimegap + int(mbr_timestamp[-1]) - int(mbr_timestamp[0])) > self.read_daf.DataNo[-1]):
                    continue
                delta_daf_mbr_start_point = longtimegap - mbr_timestamp[0]
                for n in range(0, 2000000, 1000):  # cycle in 2000msec time step 1000us
                    mod_MBR_all_timestamp = []
                    mod_MBR_all_timestamp = [(int(i) + delta_daf_mbr_start_point + n)
                                             for i in mbr_timestamp]
                    shift_MBR_and_daf_match_info_timeoffset.append(longtimegap + n)
                    shift_MBR_and_daf_match_info_matchpoints_percent.append(
                        self.fun_check_percentage_match_daf_shifted_MBR_match(mod_MBR_all_timestamp))
                    if (shift_MBR_and_daf_match_info_matchpoints_percent[-1] > 0.95):
                        print("possible timestamp offset in daf (msec):", (longtimegap + n) / 1000)
                        print("point matches percentage:", shift_MBR_and_daf_match_info_matchpoints_percent[-1])
        else:
            delta_daf_mbr_start_point = init_timeoffset - mbr_timestamp[0]
            print("Starting loop in ±2000msec to find the best match timeoffset of MBR and Daf")
            for n in range(-2000000, 2000000, 1000):  # cycle in init_timeoffset ±2000msec time step 1000us
                mod_MBR_all_timestamp = []
                mod_MBR_all_timestamp = [(int(i) + delta_daf_mbr_start_point + n)
                                         for i in mbr_timestamp]
                shift_MBR_and_daf_match_info_timeoffset.append(init_timeoffset + n)
                shift_MBR_and_daf_match_info_matchpoints_percent.append(
                    self.fun_check_percentage_match_daf_shifted_MBR_match(mod_MBR_all_timestamp))
                if (shift_MBR_and_daf_match_info_matchpoints_percent[-1] > 0.95):
                    print("possible timestamp offset in daf (msec):", (delta_daf_mbr_start_point + n) / 1000)
                    print("point matches percentage:", shift_MBR_and_daf_match_info_matchpoints_percent[-1])
        bestmatchlist = []
        try:
            bestmatchlist = r_funs.max_index(shift_MBR_and_daf_match_info_matchpoints_percent)
        except:
            return 0
        if (max(shift_MBR_and_daf_match_info_matchpoints_percent) > 0.95):
            if (len(bestmatchlist) > 1):
                print(len(bestmatchlist), " best match timeoffset were found:")
                for bestmatchi in bestmatchlist:
                    print(shift_MBR_and_daf_match_info_timeoffset[bestmatchi] / 1000, "msec",
                          shift_MBR_and_daf_match_info_matchpoints_percent[bestmatchi], "points matches")
                    temp_timeoffset.append(shift_MBR_and_daf_match_info_timeoffset[bestmatchi])
                print("the minimal timestamp will be selected for further calculation")
                determin_auto_timeoffset = min(temp_timeoffset)
            elif (len(bestmatchlist) == 1):
                determin_auto_timeoffset = shift_MBR_and_daf_match_info_timeoffset[bestmatchlist[0]]
        else:
            determin_auto_timeoffset = 0
            # for test only
            # determin_auto_timeoffset = 340975000
            # for test only
        return determin_auto_timeoffset

    def fun_determin_MBR_endpoints_timestamp(self, point_last_thresold, point_behind_good_thresold, temp_timeoffset):
        found_end_point = False
        count_voxels_in_one_layer = 0
        temp_timestamp_array = []
        temp_IcImCharge_array = []

        daf_start_points, daf_end_points = self.fun_find_daf_startpoint_endpoint_timestamp()
        # mbr_start_point.append(self.read_mbr.voxel_info[0][10])
        count_voxels_in_MBR = 0
        temp_count_voxels_in_MBR = 0
        for temp_daf_starttimeindex in range(0, len(daf_start_points) - 1):  # 最后一个daf startpoint后面直接写进去。
            if count_voxels_in_MBR >= (len(self.mbr_origin_timestamp) - 1):  # reach the last voxel in MBR
                break
            temp_count_voxels_in_MBR = count_voxels_in_MBR
            if ((self.mbr_origin_timestamp[temp_count_voxels_in_MBR] + temp_timeoffset)
                    > daf_end_points[temp_daf_starttimeindex]):  # beam-in in daf doesn't have matched beam-in in MBR.
                continue
            if (daf_start_points[temp_daf_starttimeindex + 1] - daf_end_points[temp_daf_starttimeindex]) > 300000:
                # larger than 300ms means a normal case.
                half_start_end_point = daf_end_points[temp_daf_starttimeindex] + (
                            daf_start_points[temp_daf_starttimeindex + 1] -
                            daf_end_points[temp_daf_starttimeindex]) / 2
                for temp_mbr_timestamp_index in range(temp_count_voxels_in_MBR, len(self.mbr_origin_timestamp) - 1):
                    count_voxels_in_MBR += 1
                    temp_timestamp_array.append(self.mbr_origin_timestamp[temp_mbr_timestamp_index])
                    temp_IcImCharge_array.append(self.read_mbr.voxel_info[temp_mbr_timestamp_index][9])
                    if ((self.mbr_origin_timestamp[temp_mbr_timestamp_index + 1] + temp_timeoffset)
                            > half_start_end_point):
                        self.mbr_start_points.append(self.mbr_origin_timestamp[temp_count_voxels_in_MBR])  # start point
                        self.mbr_end_points.append(
                            self.mbr_origin_timestamp[temp_mbr_timestamp_index])  # this end point
                        #
                        # if (temp_mbr_timestamp_index == temp_count_voxels_in_MBR):
                        #     self.mbr_start_points[-1] = 0  # 仅1个spot，直接判定为endpoint，ms,start point设置为0.
                        break
            else:  # 两spill间距过小。尝试猜测end point。查找 daf start point前10个以内数据里，第一个符合>115ms,20ms的数据。
                for temp_mbr_timestamp_index in range(temp_count_voxels_in_MBR, len(self.mbr_origin_timestamp) - 1):
                    count_voxels_in_MBR += 1
                    temp_timestamp_array.append(self.mbr_origin_timestamp[temp_mbr_timestamp_index])
                    temp_IcImCharge_array.append(self.read_mbr.voxel_info[temp_mbr_timestamp_index][9])
                    if ((self.mbr_origin_timestamp[temp_mbr_timestamp_index + 1] + temp_timeoffset)
                            > daf_start_points[temp_daf_starttimeindex + 1]):
                        if len(temp_timestamp_array) == 1:
                            self.mbr_start_points.append(0)
                            self.mbr_end_points.append(temp_timestamp_array[0])
                            break
                        elif len(temp_timestamp_array) < 10 and len(temp_timestamp_array) > 1:
                            how_many_spots_to_judge = len(temp_timestamp_array)
                        else:
                            how_many_spots_to_judge = 10
                        self.mbr_start_points.append(self.mbr_origin_timestamp[temp_count_voxels_in_MBR])
                        temp_timestamp_array.append(self.mbr_origin_timestamp[temp_mbr_timestamp_index + 1])
                        for i in range(len(temp_timestamp_array) - 2,
                                       len(temp_timestamp_array) - 2 - how_many_spots_to_judge, -1):
                            if ((temp_timestamp_array[i] - temp_timestamp_array[i - 1]) > point_last_thresold and
                                    (temp_timestamp_array[i + 1] - temp_timestamp_array[
                                        i] > point_behind_good_thresold)):
                                print("found possible end point in spill interval of less than 300ms")
                                self.mbr_end_points.append(temp_timestamp_array[i])
                                temp_timestamp_array.pop()
                                found_end_point = True
                                break
                        # could not find proper endpoint, use the last point of this tempvoxelset instead.
                        if found_end_point == False:
                            temp_timestamp_array.pop()
                            self.mbr_end_points.append(temp_timestamp_array[-1])
                        found_end_point = False
                        break
            temp_timestamp_array.clear()
            temp_IcImCharge_array.clear()
        self.mbr_start_points.append(
            self.mbr_origin_timestamp[self.mbr_origin_timestamp.index(self.mbr_end_points[-1]) + 1])
        self.mbr_end_points.append(self.mbr_origin_timestamp[-1])

    def fun_determin_endpoint_offset(self, ):
        mbr_endpoint_offset = []
        temp_IcImCharge_array_float = []
        temp_timestamp_array = 0
        temp_IcImCharge_array = 0
        tempendpoint_offset = 0
        tempendpoint_offset_determinby_2ndpoint = 0
        for temp in range(0, len(self.mbr_end_points)):
            if self.mbr_start_points[temp] == self.mbr_end_points[temp]:
                tempendpoint_offset = 0
            else:
                tempendpoint_index = self.mbr_origin_timestamp.index(self.mbr_end_points[temp])
                tempstartpoint_index = self.mbr_origin_timestamp.index(self.mbr_start_points[temp])
                if tempendpoint_index - tempstartpoint_index >= 3:
                    total_IcImCharge = 0
                    total_timestamp = 0
                    for timestampindex in range(tempstartpoint_index + 2, tempendpoint_index):
                        total_IcImCharge += float(self.read_mbr.voxel_info[timestampindex][9])
                    total_timestamp = self.mbr_origin_timestamp[tempendpoint_index - 1] - self.mbr_origin_timestamp[
                        tempstartpoint_index + 1]  # remove first and end point
                    end_ICImcharge = float(self.read_mbr.voxel_info[tempendpoint_index][9])
                    tempendpoint_offset = self.mbr_origin_timestamp[
                                              tempendpoint_index - 1] + end_ICImcharge * total_timestamp / total_IcImCharge - \
                                          self.mbr_origin_timestamp[tempendpoint_index]
                    tempendpoint_offset_determinby_2ndpoint = self.mbr_origin_timestamp[
                                                                  tempendpoint_index - 1] + 1000 - \
                                                              self.mbr_origin_timestamp[tempendpoint_index]
                else:
                    tempendpoint_offset = self.mbr_origin_timestamp[
                                              tempendpoint_index - 1] + 1000 - self.mbr_origin_timestamp[
                                              tempendpoint_index]
            mbr_endpoint_offset.append(max(tempendpoint_offset, tempendpoint_offset_determinby_2ndpoint))
        return mbr_endpoint_offset

    def fun_mod_MBR(self, mbr_end_point, mbr_end_point_offset):
        print("start modify the end point of MBR")
        for i in range(0, len(self.mbr_origin_timestamp)):
            self.mbr_modified_timestamp.append(self.mbr_origin_timestamp[i])
        for j in range(0, len(mbr_end_point)):
            self.mbr_modified_timestamp[self.mbr_modified_timestamp.index(mbr_end_point[j])] = mbr_end_point[j] + \
                                                                                               mbr_end_point_offset[j]
        print("Mod_MBR generated")

    def fun_find_daf_startpoint_endpoint_timestamp(self):  # use 1 and 0 to determin the timestamp of beam on and off.
        possible_daf_last_timestamp_flag = False
        count_non_zero_points = 0
        daf_endpoint_timestamp = []
        daf_startpoint_timestamp = []
        start_beamin_flag = False
        for m in range(1, len(self.read_daf.DataNo)):
            if self.read_daf.BeamIn[m] >= 1 and self.read_daf.BeamIn[m - 1] == 0:
                daf_startpoint_timestamp.append(self.read_daf.DataNo[m])  # if beam in time is A, startpoint time is A
            elif self.read_daf.BeamIn[m] == 0 and self.read_daf.BeamIn[m - 1] >= 1:
                daf_endpoint_timestamp.append(self.read_daf.DataNo[m])  # if beam off time is B, endpoint time is B
            else:
                continue
        return daf_startpoint_timestamp, daf_endpoint_timestamp

    def fun_find_daf_first_and_longest_4_timestamp(self):
        delta_timestamp = []
        daf_first_and_4_longest_timestamp = [0, 0, 0, 0, 0]
        start_beamin_time_in_daf = 0
        m = 0
        for m in range(0, len(self.read_daf.BeamIn)):
            if self.read_daf.BeamIn[m] >= 1:
                start_beamin_time_in_daf = self.read_daf.DataNo[m]
                break
            delta_timestamp.append(0)
        daf_first_and_4_longest_timestamp[0] = start_beamin_time_in_daf
        count_zero = 0
        for n in range(m, len(self.read_daf.BeamIn)):
            if self.read_daf.BeamIn[n] == 0:
                count_zero += 1
                delta_timestamp.append(0)
            else:
                delta_timestamp.append(count_zero)
                count_zero = 0
        for i in range(1, 5):
            daf_first_and_4_longest_timestamp[i] = self.read_daf.DataNo[delta_timestamp.index(max(delta_timestamp)) - 1]
            delta_timestamp[delta_timestamp.index(max(delta_timestamp))] = 0
        return (daf_first_and_4_longest_timestamp)

    def fun_check_percentage_match_daf_shifted_MBR_match(self, mod_MBR_all_timestamp):
        count_match = 0
        for m in mod_MBR_all_timestamp:
            if self.read_daf.BeamIn[int(m / 25000)] > 0:
                count_match += 1
        return (float(count_match / len(mod_MBR_all_timestamp)))

    def fun_determin_start_point_timeoffset(self):
        start_beamin_time_in_daf = 0
        for m in range(0, len(self.read_daf.BeamIn)):
            if self.read_daf.BeamIn[m] >= 1:
                start_beamin_time_in_daf = self.read_daf.DataNo[m]
                break
        start_point_timeoffset = start_beamin_time_in_daf - int(self.read_mbr.voxel_info[0][10])
        return start_point_timeoffset

    def fun_daf_MBR_figs(self, showfigs, showdebugfigs):
        show_fig_info = s_fig.class_show_daf_MBR_fig(self.daf_file_path)
        if showdebugfigs != None:
            print("Detects show of figures of daf and MBR in debug mode.")
            show_fig_info.fun_show_daf_MBR_fig(self.all_timeoffset, self.mbr_origin_timestamp, self.mbr_start_points,
                                               self.mbr_end_points)
        elif showfigs == True:
            print("Detects show of figures of daf and MBR.")
            show_fig_info.fun_show_daf_MBR_fig(self.all_timeoffset, self.mbr_origin_timestamp,
                                               self.mbr_modified_timestamp, None)
        else:
            print("No show of figures.")
        # # Show debug fig
        # if (args.mbr != None and args.showdebug != None):
        #     print("Detects show of figures of daf and MBR in debug mode, no lmdout will be generated.")
        #     showfig = sdaf.class_show_daf_MBR_fig(daf_file_path,
        #                                           args.showdebug)  # showdebug is the manual timeoffset for debuging.
        #     showfig.fun_show_daf_fig_MBR_debug(args.mbr, lmdout_file_path)
