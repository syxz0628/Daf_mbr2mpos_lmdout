import read_mbr as rmbr
import read_daf as rdaf
import numpy as np
import related_funs as r_funs
import datetime

class class_daf_mbr2lmdout:
    def __init__(self, daf_file_path, mbr_file_path, manual_timeoffset,init_spot_timeoffset):
        self.daf_file_path = daf_file_path
        self.mbr_file_path = mbr_file_path
        self.init_spot_timeoffset=init_spot_timeoffset
        self.lmdout_file_path = ""
        self.manual_timeoffset = manual_timeoffset  # this is very small offset scale of ~250ms based on optimal determined timeoffset by the code. the time offset between daf and mbr are calculated automatically.
        self.random_offset = 0  # some other offset maybe introduced by the system time variation.
        # this is all the time offset includes: 1. system time offsett between the gating and IRONTRI system. Automatically calculated. 2. manual_timeoffset. 3. random offset
        self.all_timeoffset = 0
        self.start_point_timeoffset = 0 #for display only.
        self.lmdout_info = []
        self.mbr_modified_timestamp = []
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

        # get daf and mbr information
        self.read_daf = rdaf.class_read_daf(self.daf_file_path)
        self.read_mbr = rmbr.class_read_mbr(self.mbr_file_path)
        self.mbr_modified_timestamp = self.fun_determin_point_status_correct_timestamp(100000,
                                                                                       20000)  # >100ms to the
        # previous_timestamp and <20ms is empty then determined Last point

    def fun_daf_mbr2lmdout(self, lmdout_file_path):
        self.lmdout_file_path = lmdout_file_path
        print('Energy layers in MBR:')
        print(self.read_mbr.Energy_Number)

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
                "!items Timestamp NoofPoint BeginofSpill EndofSpill EndofPlane EnergyValue Focus Intensity\n")
            lmdoutFile.write("0 0 0 0 0 0 0 0\n")
            lmdoutFile.write("0 0 0 0 0 0 0 0\n")
            self.fun_find_all_correspond_info()
            for templmdout in self.lmdout_info:
                lmdoutFile.write(templmdout)
                lmdoutFile.write('\n')
        print("lmdout file was generated in: ", self.lmdout_file_path)

    def fun_find_all_correspond_info(self):
        # find lmdout_info include
        # list voxel={[IESNumber,IESenergy,TotalVoxelIndex,ActFocusX,ActFocusY,ScannerX,ScannerY,MwpcPosX,MwpcPosY,IcImCharge,TimeStamp,TimeStampAbs]}
        # search index     0                     1                 2                   3                4                   5                 6                 7                 8                  9                   10                 11
        #
        self.start_point_timeoffset = self.fun_determin_start_point_timeoffset()
        self.all_timeoffset = self.fun_auto_determin_timeoffset_in_daf2()-int(self.read_mbr.voxel_info[0][10])
        # for test only
        #self.all_timeoffset = self.start_point_timeoffset
        #self.all_timeoffset=0
        # for test only

        print("the first beam in timestamp in MBR is: ", int(self.read_mbr.voxel_info[0][10]), " usec")
        print("the first beam in timestamp in Daf is: ", (self.start_point_timeoffset + int(self.read_mbr.voxel_info[0][10]))," usec")
        print("the daf(beam in)-mbr(start point)timeoffset is: ", self.start_point_timeoffset," usec")
        print("the best match possible timeoffset is: ", self.all_timeoffset," usec")
        # write the first line
        #self.current_time_stamp = int(self.read_mbr.voxel_info[0][10]) + self.all_timeoffset - self.init_spot_timeoffset
        self.current_time_stamp = int(self.mbr_modified_timestamp[0]) + self.all_timeoffset - self.init_spot_timeoffset
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
        count_voxels_all=-1
        start_begin_of_spill_even_before_NP = False

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
                print("found an end of plan, in ",int(self.mbr_modified_timestamp[count_voxels_all]))
                self.previous_timestamp = self.current_time_stamp
                continue
            if (self.current_time_stamp-self.all_timeoffset) in self.MBR_beamoff_last_point_timestamp:
                self.fun_ES_event()
                start_begin_of_spill_even_before_NP = True
                print("found an end of spill, in ",self.mbr_modified_timestamp[count_voxels_all])
                self.previous_timestamp = self.current_time_stamp
                continue

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
        self.current_time_stamp = int(self.mbr_modified_timestamp[count_voxels_all])  + self.all_timeoffset-self.init_spot_timeoffset
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
    def fun_determin_point_status_correct_timestamp(self, point_last_thresold, point_behind_good_thresold):
        #     调整MBR首末点位的timestamp .
        #      1. 查找last point.
        #         a. end of energy,
        #         b. 与前一个timestamp相比>piont_last_thresold(default,100000), 且后方point_behind_good_thresold(default 20000) 内
        #         注：last point stamp 保存在self.last_point_timestamp[]中。
        #      2. 查找first point.
        #          first point以及last point 之后的第一个point
        #      3. others are good point.
        possible_last_timestamp_flag = False
        count_voxels_in_one_layer = 0
        temp_timestamp_array = []
        temp_IcImCharge_array = []
        mod_timestamp = []
        previous_timestamp = self.read_mbr.voxel_info[0][10]
        first_point_flag = False

        for tempvoxel_info in self.read_mbr.voxel_info:
            count_voxels_in_one_layer += 1
            if count_voxels_in_one_layer == int(tempvoxel_info[12]):  # last point detected due to end of layers.
                temp_timestamp_array.append(tempvoxel_info[10])
                temp_IcImCharge_array.append(tempvoxel_info[9])
                for i in self.fun_correct_first_last_timestamp_from_temp_time_array(temp_timestamp_array,
                                                                                    temp_IcImCharge_array):
                    mod_timestamp.append(i)
                temp_timestamp_array.clear()
                temp_IcImCharge_array.clear()
                count_voxels_in_one_layer = 0
                first_point_flag = True
                continue
            elif possible_last_timestamp_flag == True:  # last point detected due to MBR last point_last_thresold.
                if ((int(tempvoxel_info[10]) - int(previous_timestamp)) > point_behind_good_thresold):
                    for i in self.fun_correct_first_last_timestamp_from_temp_time_array(temp_timestamp_array,
                                                                                        temp_IcImCharge_array):
                        mod_timestamp.append(i)
                    temp_timestamp_array.clear()
                    temp_IcImCharge_array.clear()
                    temp_timestamp_array.append(tempvoxel_info[10])
                    temp_IcImCharge_array.append(tempvoxel_info[9])
                else:
                    temp_timestamp_array.append(tempvoxel_info[10])
                    temp_IcImCharge_array.append(tempvoxel_info[9])
                possible_last_timestamp_flag = False
            else:
                temp_timestamp_array.append(tempvoxel_info[10])
                temp_IcImCharge_array.append(tempvoxel_info[9])
            if first_point_flag == False:
                if ((int(tempvoxel_info[10]) - int(previous_timestamp)) > point_last_thresold and (
                        int(tempvoxel_info[10]) - int(previous_timestamp)) < 500000):
                    possible_last_timestamp_flag = True
                elif ((int(tempvoxel_info[10]) - int(previous_timestamp)) >= 500000):
                    self.MBR_beamoff_last_point_timestamp.append(
                        int(previous_timestamp))  # this data was for the fun_auto_determin_timeoffset_in_daf
            else:
                first_point_flag = False
            previous_timestamp = tempvoxel_info[10]
        return mod_timestamp
    def fun_correct_first_last_timestamp_from_temp_time_array(self, temp_timestamp_array, temp_IcImCharge_array):
        mod_first_last_timestamp = []
        # total_charge=0
        temp_IcImCharge_array_float = map(float, temp_IcImCharge_array)
        temp_IcImCharge_array_float = list(temp_IcImCharge_array_float)
        total_charge = np.sum(np.array(temp_IcImCharge_array_float[-3:-1]))
        total_timestamp = int(temp_timestamp_array[-2]) - int(temp_timestamp_array[-3]) # average last 2 values
        # print(temp_timestamp_array)
        # first_time_duration=int(temp_IcImCharge_array_float[0]*total_timestamp/total_charge)
        last_time_duration = int(temp_IcImCharge_array_float[-1] * total_timestamp / total_charge)
        # modify first point(default unactive)
        # mod_first_last_timestamp.append(str(int(temp_timestamp_array[1])-first_time_duration))
        mod_first_last_timestamp = mod_first_last_timestamp + temp_timestamp_array[0:-1]
        mod_first_last_timestamp.append(str(int(temp_timestamp_array[-2]) + last_time_duration))
        self.MBR_beamoff_last_point_timestamp.append(int(
            temp_timestamp_array[-2]) + last_time_duration)  # this data was for the fun_auto_determin_timeoffset_in_daf
        return mod_first_last_timestamp
    def fun_find_daf_beamoff_lastpoint_timestamp(self):  # use 1 and 0 to determin the timestamp of beam on and off.
        possible_daf_last_timestamp_flag = False
        count_non_zero_points = 0
        daf_beamoff_last_point_timestamp = []
        for m in range(0, len(self.read_daf.BeamIn)):
            if self.read_daf.BeamIn[m] >= 1:
                possible_daf_last_timestamp_flag = True
                count_non_zero_points += 1
            elif (
                    possible_daf_last_timestamp_flag == True and count_non_zero_points > 1):  # sometimes there is one/two/three beam on spot in daf however not really beam on in MBR
                daf_beamoff_last_point_timestamp.append(self.read_daf.DataNo[m - 1])
                possible_daf_last_timestamp_flag = False
                count_non_zero_points = 0
        return daf_beamoff_last_point_timestamp
    def fun_find_daf_first_and_longest_4_timestamp(self):
        delta_timestamp = []
        daf_first_and_4_longest_timestamp = [0, 0, 0, 0, 0]
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
    def fun_auto_determin_timeoffset_in_daf2(self):
        #
        # this is all the time offset includes:
        # 1. system time offsett between the gating and IRONTRI system. Automatically calculated. 2. manual_timeoffset.
        # all_timeoffset=system_timeoffset determined automaticall
        # manual_timeoffset was ~250ms offset defined by user and all lmdout file will be generated accroding to the -t parameter.
        #
        # system_timeoffset timestamp of each point  was determined by :
        # "MBR voxel timestamp-first point Timestamp in MBR+first beamin Timestamp in Daf"
        #
        # so the system_timeoffset was defined by inner function "self.fun_find_all_timeoffset":
        # first beamin Timestamp in Daf-first point Timestamp in MBR
        #
        # shift_MBR_and_daf_match_info collects info of
        # 0:timeoffset,
        # 1: how many points in sMBR was beam on in daf (higher better)
        # 2: last point distance (lower better)
        shift_MBR_and_daf_match_info_timeoffset = []
        shift_MBR_and_daf_match_info_matchpoints_percent = []
        shift_MBR_and_daf_match_info_lastpoint_distance = 0
        determin_auto_timeoffset_in_daf = 0
        last_point_variation_bewteen_MBR_and_daf_for_found_timeoffset = 0
        possible_lastpoint_match_flag = False
        mod_MBR_beamoff_last_point_timestamp = []
        mod_mod_MBR_beamoff_last_point_timestamp = []
        possible_timeoffset = []


        # use the first match point and the other 4 big time gap to find possible match of mbr and daf
        daf_first_and_4_longest_timestamp = self.fun_find_daf_first_and_longest_4_timestamp()
        self.start_point_timeoffset = self.fun_determin_start_point_timeoffset()
        print("Starting loop in gap of daf to find possible match timeoffset of MBR and Daf")
        for longtimegap in daf_first_and_4_longest_timestamp:
            print("loop in biggest 5 beam in timestamp gap in daf (including the very first):",longtimegap/1000,"msec")
            if ((longtimegap + int(self.read_mbr.voxel_info[-1][10]) - int(self.read_mbr.voxel_info[0][10]))
                    >self.read_daf.DataNo[-1]):
                continue
            # mod MBR timestamp 必须首先和daf在一个起跑线(MBR的0等于Lmdout 的 0)然后平移。防止出现daf比MBR时间戳小的情况。
            # 因此第一步是让MBR起始Beam In点平移为0.
            mod_MBR_all_timestamp = []
            mod_MBR_all_timestamp = [(int(i) - int(self.read_mbr.voxel_info[0][10]) )
                                     for i in self.mbr_modified_timestamp]
           #for n in range(0, self.read_daf.DataNo[-1]-mod_MBR_all_timestamp[-1]+mod_MBR_all_timestamp[0], 1000):  # cycle in all daf time step 1000us
            for n in range(0, 2000000, 1000):  # cycle in 2000msec time step 1000us

                mod_mod_MBR_all_timestamp=[]
                mod_mod_MBR_all_timestamp = [(int(i) + longtimegap + n)
                                         for i in mod_MBR_all_timestamp]
                shift_MBR_and_daf_match_info_timeoffset.append(longtimegap + n)
                shift_MBR_and_daf_match_info_matchpoints_percent.append(
                    self.fun_check_percentage_match_daf_shifted_MBR_match \
                        (mod_mod_MBR_all_timestamp))

                if (shift_MBR_and_daf_match_info_matchpoints_percent[-1]>0.90):
                    print("possible timestamp offset in daf (msec):", (longtimegap+n) / 1000)
                    print("point matches percentage:", shift_MBR_and_daf_match_info_matchpoints_percent[-1])
        bestmatchlist=[]
        bestmatchlist=r_funs.max_index(shift_MBR_and_daf_match_info_matchpoints_percent)
        if (len(bestmatchlist)>1):
            shift_MBR_and_daf_match_info_lastpoint_distance=[]
            print(len(bestmatchlist)," best match timeoffset were found:")
            for bestmatchi in bestmatchlist:
                print(shift_MBR_and_daf_match_info_timeoffset[bestmatchi]/1000,"msec",
                      shift_MBR_and_daf_match_info_matchpoints_percent[bestmatchi],"points matches")
                # get MBR  shifted last point timestamp
                mod_MBR_beamoff_last_point_timestamp = []
                mod_MBR_beamoff_last_point_timestamp = [(int(i) + shift_MBR_and_daf_match_info_timeoffset[bestmatchi])
                                                        for i in self.MBR_beamoff_last_point_timestamp]
                # get daf last point timestamp
                daf_beamoff_last_point_timestamp = self.fun_find_daf_beamoff_lastpoint_timestamp()
                # check match last point and the variation
                shift_MBR_and_daf_match_info_lastpoint_distance.append(self.fun_check_lastpoint_A_lessthan_B_plus_C2 \
                     (mod_MBR_beamoff_last_point_timestamp, daf_beamoff_last_point_timestamp,
                     float(self.read_daf.DataTime_msec) * 1000 / 2))
            determin_auto_timeoffset_in_daf=shift_MBR_and_daf_match_info_timeoffset[bestmatchlist[shift_MBR_and_daf_match_info_lastpoint_distance.index
                (min(shift_MBR_and_daf_match_info_lastpoint_distance))]]

        elif (len(bestmatchlist)==1):
            determin_auto_timeoffset_in_daf=shift_MBR_and_daf_match_info_timeoffset[bestmatchlist[0]]
        if (max(shift_MBR_and_daf_match_info_matchpoints_percent)>0.95):
            print("~~~found best match timeoffset in daf file: ",determin_auto_timeoffset_in_daf/1000,
                  " msec. ",max(shift_MBR_and_daf_match_info_matchpoints_percent)," points matches")
        elif (max(shift_MBR_and_daf_match_info_matchpoints_percent)<=0.95
              and max(shift_MBR_and_daf_match_info_matchpoints_percent)>0.8):
            print("~~~found match timeoffset in daf file, but not very good matched at timeoffset: ",determin_auto_timeoffset_in_daf/1000,
                  " msec. ", max(shift_MBR_and_daf_match_info_matchpoints_percent)," points matches")
            print("~~~~~~~You may check daf and mbr file if they really matches")
        else:
            print("~~~could not match well(<80%), match of start point will be shown in figure.")
            print("~~~~~~~You need to check daf and mbr file if they really matches")
            determin_auto_timeoffset_in_daf=self.start_point_timeoffset + int(self.read_mbr.voxel_info[0][10])
            # for test only
            #determin_auto_timeoffset_in_daf = 340975000
            # for test only
        return determin_auto_timeoffset_in_daf
    def fun_check_lastpoint_A_lessthan_B_plus_C2(self, AAA, BBB, CCC):
        # check if each points in list A always less than each point in list B plus offset float C
        # idea is timestamp in MBR should be always within daf. so try to match the last point of daf+12.5msec with MBR last point.
        last_point_variation_bewteen_MBR_and_daf_for_found_timeoffset = 0
        for i in range(0, len(BBB) - len(AAA)):
            if ((BBB[i] + CCC) > AAA[0]):
                for j in range(0, len(AAA) - 1):
                    last_point_variation_bewteen_MBR_and_daf_for_found_timeoffset += (BBB[i + j] - AAA[j])
                break
        return last_point_variation_bewteen_MBR_and_daf_for_found_timeoffset
    def fun_check_percentage_match_daf_shifted_MBR_match(self,mod_MBR_all_timestamp):
        count_match=0
        for m in mod_MBR_all_timestamp:
            if self.read_daf.BeamIn[int(m/25000)]>0:
                count_match+=1
        return (float(count_match/len(mod_MBR_all_timestamp)))
    def fun_determin_start_point_timeoffset(self):
        start_beamin_time_in_daf = 0
        for m in range(0, len(self.read_daf.BeamIn)):
            if self.read_daf.BeamIn[m] >= 1:
                start_beamin_time_in_daf = self.read_daf.DataNo[m]
                break
        start_point_timeoffset = start_beamin_time_in_daf - int(self.read_mbr.voxel_info[0][10])
        return start_point_timeoffset
