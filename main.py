# -*- coding: utf-8 -*-
# @Time    : 2019/11/12 15:27
# @Author  : wenlei

'''
主函数
'''

from Heatmap import *
from basicAnalysis import *

if __name__ == '__main__':
    #合并表
    # sheet_concat()
    #读取合并后的表
    all_df = pd.read_csv(save_path + '2019_SUM.csv')

    #答题和奖项分布
    prize_dist(all_df)

    #学校获奖分布(按队长所在单位）
    sch_leader(all_df)

    #学校获奖人数分布
    sch_all(all_df)

    #每道题各学校获奖人数分布
    sch_title(all_df)

    #获奖学校地区分布
    # baidu map api
    get_school_info()
    input_path = save_path + 'school_loc_prize_nums.csv'
    out_path = save_path + 'heat_map.html'
    draw_heatmap(input_path, out_path)
