# -*- coding: utf-8 -*-
# @Time    : 2019/11/13 16:26
# @Author  : wenlei

'''
基本的数据分析
'''

from config import *

#将6道题的成绩表合并为一个
def sheet_concat():
    sheet_A = pd.read_excel(raw_path + '2019_A.xls', index=False)  # 781
    sheet_B = pd.read_excel(raw_path + '2019_B.xls', index=False)  # 888
    sheet_C = pd.read_excel(raw_path + '2019_C.xls', index=False)  # 1057
    sheet_D = pd.read_excel(raw_path + '2019_D.xls', index=False)  # 4259
    sheet_E = pd.read_excel(raw_path + '2019_E.xls', index=False)  # 4193
    sheet_F = pd.read_excel(raw_path + '2019_F.xls', index=False)  # 2790
    # 13968+46(雷同)=14014(总参赛队伍）

    sheet_all = pd.concat([sheet_A, sheet_B, sheet_C, sheet_D, sheet_E, sheet_F], axis=0, ignore_index=True)

    sheet_all.to_csv(save_path + '/2019_SUM.csv', encoding='utf_8_sig', index=False)
    #一等奖：188； 二等奖：2821； 三等奖：1903

def prize_dist(df):
    #6道题的答题分布
    sns.countplot(df['题号'])
    plt.title('答题分布情况')
    plt.savefig(img_path+'答题分布')
    plt.show()

    #得奖分布
    sns.countplot(df['奖项'])
    plt.title('奖项分布情况')
    plt.savefig(img_path+'奖项分布')
    plt.show()

    #答题和奖项的共同分布
    g = sns.catplot(x='题号', kind='count', hue='奖项', data=df, height=6, palette="muted")
    g.despine(left=True)
    g.set_ylabels('获奖人数')
    plt.title('答题与奖项分布情况')
    plt.savefig(img_path + '答题-奖项分布')
    plt.show()

    df_group = df[['题号', '队伍编号', '奖项']].groupby('题号')['奖项'].value_counts().unstack()
    df_group_123 = df[df['奖项']!='成功参与奖'][['题号', '队伍编号', '奖项']].groupby('题号')['奖项'].value_counts().unstack()
    #答题和奖项堆叠图
    df_group.plot(kind='bar', stacked=True, figsize=(12, 8))
    plt.savefig(img_path + '答题-奖项分布-stacked')
    plt.show()

    # 答题和奖项堆叠图（排除成功参与奖）
    df_group_123.plot(kind='bar', stacked=True, figsize=(12, 8))
    plt.savefig(img_path + '答题-奖项分布-stacked-123')
    plt.show()

# 按'队长所在单位'分别统计获奖数量
def sch_leader(df):
    sch_leader_df = df[df['奖项'] != '成功参与奖'][['题号', '奖项', '队长所在单位']].groupby(['队长所在单位', '奖项']).size().unstack()
    sch_leader_df['获奖数量'] = sch_leader_df[['一等奖', '二等奖', '三等奖']].sum(axis=1)
    sch_leader_df.sort_values(by=['获奖数量', '一等奖', '二等奖', '三等奖'], axis=0, ascending=False, inplace=True)
    sch_leader_df = sch_leader_df[['一等奖', '二等奖', '三等奖', '获奖数量']]
    sch_leader_df = sch_leader_df.reset_index().rename(columns={'队长所在单位': '学校名称'})

    print(sch_leader_df.head(20))

    # sch_leader_df.to_csv(save_path + 'sch_leader.csv', encoding='utf_8_sig', index=False)

    # 用柱状图给出获奖数量最多的前20个学校
    plt.figure(figsize=(15, 10)).subplotpars.update(bottom=0.25)
    sns.barplot(x="学校名称", y="获奖数量", data=sch_leader_df.loc[0:20],palette="muted")
    plt.title('学校获奖情况分布（按队长所在单位）')
    plt.xticks(ha='right', rotation=40)
    plt.savefig(img_path+'sch_leader.png')
    plt.show()

#按获奖人数统计
def sch_all(df):
    df_123 = df[df['奖项'] != '成功参与奖']
    leader_df = df_123[['奖项', '队长所在单位']].groupby(['队长所在单位', '奖项']).size().unstack()
    member_df1 = df_123[['奖项', '队友所在单位']].groupby(['队友所在单位', '奖项']).size().unstack()
    leader_member_df1 = leader_df.join(member_df1[['一等奖', '二等奖', '三等奖']], how='outer', rsuffix='_2')
    member_df2 = df_123[['奖项', '队友所在单位.1']].groupby(['队友所在单位.1', '奖项']).size().unstack()
    leader_member_df = leader_member_df1.join(member_df2[['一等奖', '二等奖', '三等奖']], how='outer', rsuffix='_3')

    leader_member_df.rename(columns={'一等奖': '一等奖_1', '二等奖': '二等奖_1', '三等奖': '三等奖_1', '奖项': '学校名称'}, inplace=True)
    leader_member_df['获奖总人数'] = leader_member_df.sum(axis=1)
    order = ['一等奖_1', '一等奖_2', '一等奖_3', '二等奖_1', '二等奖_2', '二等奖_3', '三等奖_1', '三等奖_2', '三等奖_3', '获奖总人数']
    leader_member_df = leader_member_df[order]
    sort_cols = ['获奖总人数', '一等奖_1', '一等奖_2', '一等奖_3', '二等奖_1', '二等奖_2', '二等奖_3', '三等奖_1', '三等奖_2', '三等奖_3']
    leader_member_df.sort_values(by=sort_cols, ascending=False, inplace=True)

    leader_member_df = leader_member_df.reset_index().rename(columns={'index': '学校名称'})

    leader_member_df.to_csv(save_path + '各学校获奖人数统计.csv', encoding='utf_8_sig', index=False)

    # 用柱状图给出获奖人数最多的前20个学校
    plt.figure(figsize=(15, 10))
    sns.barplot(x="学校名称", y="获奖总人数", data=leader_member_df.loc[0:20], palette="muted")
    plt.title('各学校获奖人数统计')
    plt.xticks(ha='right', rotation=40)
    plt.savefig(img_path+'各学校获奖人数统计.png')
    plt.show()

#对每道赛题进行统计
def sch_title(df):
    sch_title_df = df[df['奖项'] != '成功参与奖'][['题号', '奖项', '队长所在单位']]

    a = 0
    b = 1
    fig = plt.figure(figsize=(18, 22))

    for i in ['A', 'B', 'C', 'D', 'E', 'F']:
        df_name = 'title_sch_prize_' + i
        #     print(df_name)

        df_name = sch_title_df[sch_title_df['题号'] == i]
        df_name = df_name.groupby(['队长所在单位', '奖项']).size().unstack()
        df_name['获奖人数'] = df_name.sum(axis=1)
        s_cols = ['获奖人数', '一等奖', '二等奖', '三等奖']
        df_name.sort_values(by=s_cols, ascending=False, inplace=True)
        df_name = df_name.reset_index()

        #     print(df_name.loc[0:10])

        ax = fig.add_subplot(3, 2, b)
        sns.barplot(x='队长所在单位', y='获奖人数', data=df_name.loc[0:10], palette="muted")
        ax.set_title(i)
        ax.set_xticklabels(df_name['队长所在单位'], fontsize=10, rotation=40)
        a += 1
        b += 1
    plt.savefig(img_path + '每道题各学校获奖分布.png')
