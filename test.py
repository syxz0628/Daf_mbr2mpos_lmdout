# def fun_determin_point_status_correct_timestamp(self, point_last_thresold, point_behind_good_thresold):
#     #     调整MBR首末点位的timestamp .
#     #      1. 查找last point.
#     #         a. end of energy,
#     #         b. 与前一个timestamp相比>piont_last_thresold(default,100000), 且后方point_behind_good_thresold(default 20000) 内
#     #         注：last point stamp 保存在self.last_point_timestamp[]中。
#     #      2. 查找first point.
#     #          first point以及last point 之后的第一个point
#     #      3. others are good point.
#     possible_last_timestamp_flag = False
#     count_voxels_in_one_layer = 0
#     temp_timestamp_array = []
#     temp_IcImCharge_array = []
#     mod_timestamp = []
#     previous_timestamp = self.read_mbr.voxel_info[0][10]
#     first_point_flag = False
#
#     for tempvoxel_info in self.read_mbr.voxel_info:
#         count_voxels_in_one_layer += 1
#         if count_voxels_in_one_layer == int(tempvoxel_info[12]):  # last point detected due to end of layers.
#             temp_timestamp_array.append(tempvoxel_info[10])
#             temp_IcImCharge_array.append(tempvoxel_info[9])
#             for i in self.fun_correct_first_last_timestamp_from_temp_time_array(temp_timestamp_array,
#                                                                                 temp_IcImCharge_array):
#                 mod_timestamp.append(i)
#             temp_timestamp_array.clear()
#             temp_IcImCharge_array.clear()
#             count_voxels_in_one_layer = 0
#             first_point_flag = True
#             continue
#         elif possible_last_timestamp_flag == True:  # last point detected due to MBR last point_last_thresold.
#             if ((int(tempvoxel_info[10]) - int(previous_timestamp)) > point_behind_good_thresold):
#                 for i in self.fun_correct_first_last_timestamp_from_temp_time_array(temp_timestamp_array,
#                                                                                     temp_IcImCharge_array):
#                     mod_timestamp.append(i)
#                 temp_timestamp_array.clear()
#                 temp_IcImCharge_array.clear()
#                 temp_timestamp_array.append(tempvoxel_info[10])
#                 temp_IcImCharge_array.append(tempvoxel_info[9])
#             else:
#                 temp_timestamp_array.append(tempvoxel_info[10])
#                 temp_IcImCharge_array.append(tempvoxel_info[9])
#             possible_last_timestamp_flag = False
#         else:
#             temp_timestamp_array.append(tempvoxel_info[10])
#             temp_IcImCharge_array.append(tempvoxel_info[9])
#         if first_point_flag == False:
#             if ((int(tempvoxel_info[10]) - int(previous_timestamp)) > point_last_thresold and (
#                     int(tempvoxel_info[10]) - int(previous_timestamp)) < 500000):
#                 possible_last_timestamp_flag = True
#             elif ((int(tempvoxel_info[10]) - int(previous_timestamp)) >= 500000):
#                 self.MBR_beamoff_last_point_timestamp.append(
#                     int(previous_timestamp))  # this data was for the fun_auto_determin_timeoffset_in_daf
#         else:
#             first_point_flag = False
#         previous_timestamp = tempvoxel_info[10]
#     return mod_timestamp

# def fun_correct_first_last_timestamp_from_temp_time_array(self, temp_timestamp_array, temp_IcImCharge_array):
#     mod_first_last_timestamp = []
#     # total_charge=0
#     temp_IcImCharge_array_float = map(float, temp_IcImCharge_array)
#     temp_IcImCharge_array_float = list(temp_IcImCharge_array_float)
#     if (len(temp_timestamp_array) > 4):
#         self.total_charge = np.sum(np.array(temp_IcImCharge_array_float[-5:-1]))
#         self.total_timestamp = int(temp_timestamp_array[-2]) - int(
#             temp_timestamp_array[-5])  # average last 4 values
#         last_time_duration = int(temp_IcImCharge_array_float[-1] * self.total_timestamp / self.total_charge)
#     else:  # some layer/spill has only 2 points... [-5] will be out of index.
#         last_time_duration = int(temp_IcImCharge_array_float[-1] * self.total_timestamp / self.total_charge)
#     # modify first point(default unactive)
#     # mod_first_last_timestamp.append(str(int(temp_timestamp_array[1])-first_time_duration))
#     mod_first_last_timestamp = mod_first_last_timestamp + temp_timestamp_array[0:-1]
#     mod_first_last_timestamp.append(str(int(temp_timestamp_array[-2]) + last_time_duration))
#     self.MBR_beamoff_last_point_timestamp.append(int(
#         temp_timestamp_array[-2]) + last_time_duration)  # this data was for the fun_auto_determin_timeoffset_in_daf
#     return mod_first_last_timestamp

# def fun_find_daf_beamoff_endpoint_timestamp(self):  # use 1 and 0 to determin the timestamp of beam on and off.
#     possible_daf_last_timestamp_flag = False
#     count_non_zero_points = 0
#     daf_beamoff_last_point_timestamp = []
#     for m in range(0, len(self.read_daf.BeamIn)):
#         if self.read_daf.BeamIn[m] >= 1:
#             possible_daf_last_timestamp_flag = True
#             count_non_zero_points += 1
#         elif (
#                 possible_daf_last_timestamp_flag == True and count_non_zero_points > 1):  # sometimes there is one/two/three beam on spot in daf however not really beam on in MBR
#             daf_beamoff_last_point_timestamp.append(self.read_daf.DataNo[m - 1])
#             possible_daf_last_timestamp_flag = False
#             count_non_zero_points = 0
#     return daf_beamoff_last_point_timestamp
#
# def fun_auto_determin_timeoffset_in_daf2(self):
#     #
#     # this is all the time offset includes:
#     # 1. system time offsett between the gating and IRONTRI system. Automatically calculated. 2. manual_timeoffset.
#     # all_timeoffset=system_timeoffset determined automaticall
#     # manual_timeoffset was ~250ms offset defined by user and all lmdout file will be generated accroding to the -t parameter.
#     #
#     # system_timeoffset timestamp of each point  was determined by :
#     # "MBR voxel timestamp-first point Timestamp in MBR+first beamin Timestamp in Daf"
#     #
#     # so the system_timeoffset was defined by inner function "self.fun_find_all_timeoffset":
#     # first beamin Timestamp in Daf-first point Timestamp in MBR
#     #
#     # shift_MBR_and_daf_match_info collects info of
#     # 0:timeoffset,
#     # 1: how many points in sMBR was beam on in daf (higher better)
#     # 2: last point distance (lower better)
#     shift_MBR_and_daf_match_info_timeoffset = []
#     shift_MBR_and_daf_match_info_matchpoints_percent = []
#     shift_MBR_and_daf_match_info_endpoint_distance = 0
#     determin_auto_timeoffset_in_daf = 0
#     last_point_variation_bewteen_MBR_and_daf_for_found_timeoffset = 0
#     possible_endpoint_match_flag = False
#     mod_MBR_beamoff_last_point_timestamp = []
#     mod_mod_MBR_beamoff_last_point_timestamp = []
#     possible_timeoffset = []
#
#     # use the first match point and the other 4 big time gap to find possible match of mbr and daf
#     daf_first_and_4_longest_timestamp = self.fun_find_daf_first_and_longest_4_timestamp()
#     self.start_point_timeoffset = self.fun_determin_start_point_timeoffset()
#     print("Starting loop in gap of daf to find possible match timeoffset of MBR and Daf")
#     for longtimegap in daf_first_and_4_longest_timestamp:
#         print("loop in longest 5 beam in timestamp gap in daf (including the very first):", longtimegap / 1000,
#               "msec")
#         if ((longtimegap + int(self.read_mbr.voxel_info[-1][10]) - int(self.read_mbr.voxel_info[0][10]))
#                 > self.read_daf.DataNo[-1]):
#             continue
#         # mod MBR timestamp 必须首先和daf在一个起跑线(MBR的0等于Lmdout 的 0)然后平移。防止出现daf比MBR时间戳小的情况。
#         # 因此第一步是让MBR起始Beam In点平移为0.
#         mod_MBR_all_timestamp = []
#         mod_MBR_all_timestamp = [(int(i) - int(self.read_mbr.voxel_info[0][10]))
#                                  for i in self.mbr_modified_timestamp]
#         # for n in range(0, self.read_daf.DataNo[-1]-mod_MBR_all_timestamp[-1]+mod_MBR_all_timestamp[0], 1000):  # cycle in all daf time step 1000us
#         for n in range(0, 2000000, 1000):  # cycle in 2000msec time step 1000us
#
#             mod_mod_MBR_all_timestamp = []
#             mod_mod_MBR_all_timestamp = [(int(i) + longtimegap + n)
#                                          for i in mod_MBR_all_timestamp]
#             shift_MBR_and_daf_match_info_timeoffset.append(longtimegap + n)
#             shift_MBR_and_daf_match_info_matchpoints_percent.append(
#                 self.fun_check_percentage_match_daf_shifted_MBR_match \
#                     (mod_mod_MBR_all_timestamp))
#
#             if (shift_MBR_and_daf_match_info_matchpoints_percent[-1] > 0.90):
#                 print("possible timestamp offset in daf (msec):", (longtimegap + n) / 1000)
#                 print("point matches percentage:", shift_MBR_and_daf_match_info_matchpoints_percent[-1])
#     bestmatchlist = []
#     bestmatchlist = r_funs.max_index(shift_MBR_and_daf_match_info_matchpoints_percent)
#     if (len(bestmatchlist) > 1):
#         shift_MBR_and_daf_match_info_endpoint_distance = []
#         print(len(bestmatchlist), " best match timeoffset were found:")
#         for bestmatchi in bestmatchlist:
#             print(shift_MBR_and_daf_match_info_timeoffset[bestmatchi] / 1000, "msec",
#                   shift_MBR_and_daf_match_info_matchpoints_percent[bestmatchi], "points matches")
#             # get MBR  shifted last point timestamp
#             mod_MBR_beamoff_last_point_timestamp = []
#             mod_MBR_beamoff_last_point_timestamp = [(int(i) + shift_MBR_and_daf_match_info_timeoffset[bestmatchi])
#                                                     for i in self.MBR_beamoff_last_point_timestamp]
#             # get daf last point timestamp
#             daf_beamoff_last_point_timestamp = self.fun_find_daf_beamoff_endpoint_timestamp()
#             # check match last point and the variation
#             shift_MBR_and_daf_match_info_endpoint_distance.append(self.fun_check_endpoint_A_lessthan_B_plus_C2 \
#                                                                       (mod_MBR_beamoff_last_point_timestamp,
#                                                                        daf_beamoff_last_point_timestamp,
#                                                                        float(
#                                                                            self.read_daf.DataTime_msec) * 1000 / 2))
#         determin_auto_timeoffset_in_daf = shift_MBR_and_daf_match_info_timeoffset[
#             bestmatchlist[shift_MBR_and_daf_match_info_endpoint_distance.index
#             (min(shift_MBR_and_daf_match_info_endpoint_distance))]]
#
#     elif (len(bestmatchlist) == 1):
#         determin_auto_timeoffset_in_daf = shift_MBR_and_daf_match_info_timeoffset[bestmatchlist[0]]
#     if (max(shift_MBR_and_daf_match_info_matchpoints_percent) > 0.95):
#         print("~~~found best match timeoffset in daf file: ", determin_auto_timeoffset_in_daf / 1000,
#               " msec. ", max(shift_MBR_and_daf_match_info_matchpoints_percent), " points matches")
#     elif (max(shift_MBR_and_daf_match_info_matchpoints_percent) <= 0.95
#           and max(shift_MBR_and_daf_match_info_matchpoints_percent) > 0.8):
#         print("~~~found match timeoffset in daf file, but not very good matched at timeoffset: ",
#               determin_auto_timeoffset_in_daf / 1000,
#               " msec. ", max(shift_MBR_and_daf_match_info_matchpoints_percent), " points matches")
#         print("~~~~~~~You may check daf and mbr file if they really matches")
#     else:
#         print("~~~could not match well(<80%), match of start point will be shown in figure.")
#         print("~~~~~~~You need to check daf and mbr file if they really matches")
#         determin_auto_timeoffset_in_daf = self.start_point_timeoffset + int(self.read_mbr.voxel_info[0][10])
#         # for test only
#         # determin_auto_timeoffset_in_daf = 340975000
#         # for test only
#     return determin_auto_timeoffset_in_daf

# def fun_check_endpoint_A_lessthan_B_plus_C2(self, AAA, BBB, CCC):
#     # check if each points in list A always less than each point in list B plus offset float C
#     # idea is timestamp in MBR should be always within daf. so try to match the last point of daf+12.5msec with MBR last point.
#     last_point_variation_bewteen_MBR_and_daf_for_found_timeoffset = 0
#     for i in range(0, len(BBB) - len(AAA)):
#         if ((BBB[i] + CCC) > AAA[0]):
#             for j in range(0, len(AAA) - 1):
#                 last_point_variation_bewteen_MBR_and_daf_for_found_timeoffset += (BBB[i + j] - AAA[j])
#             break
#     return last_point_variation_bewteen_MBR_and_daf_for_found_timeoffset
