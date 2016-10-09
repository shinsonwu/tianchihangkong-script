# coding: utf-8
import numpy as np
import pandas as pd
import xgboost as xgb


class RULES(object):
    def __init__(self, WIFI_Records, pre_time, pre_WIFIAPTag):
        self.WIFI_Records = WIFI_Records
        self.pre_time = [w.strftime("%Y-%m-%d-%H-%M") for w in pre_time]
        for i in range(len(self.pre_time)):
            self.pre_time[i] = self.pre_time[i][0:-1]
        self.pre_WIFIAPTag = pre_WIFIAPTag
        print (self.pre_time)
        print("RULES is inited OK!")

    def mean_solution_one(self):
        '''
        均值规则一：
        取总体的平均，作为结果
        '''
        print("Mean_solution_one Run!")
        pre_value = self.WIFI_Records.groupby("WIFIAPTag")["passengerCount"].mean().round(1).reset_index()
        # 转换成标准格式
        lst = list(1 for i in range(1, len(self.pre_time)+1))
        trans = pd.DataFrame({'slice10min':self.pre_time, 'flag':lst})
        pre_value['flag'] = 1
        pre_value = pre_value.merge(trans, how='left', on='flag')
        del pre_value['flag']
        pd.DataFrame(pre_value, columns=['PassengerCount', 'WIFIAPTag', 'slice10min'])
        # pre_value.to_csv("submissions/airport_gz_passenger_predict_mean.csv", index=True)
        print("Mean_solution_one END!")
        return pre_value
    def mean_solution_two(self):
        print("Mean_solution_two Run!")
        train_data = self.WIFI_Records
        train_data["slice10min"] = train_data["timeStamp"].apply(lambda x: x[0:15])
        # train_data = train_data.sort_values(by=["WIFIAPTag", "slice10min"])
        train_data = train_data.groupby(by=["WIFIAPTag", "slice10min"])["passengerCount"].sum().reset_index()
        train_data["passengerCount"] = (train_data["passengerCount"]/10).round(2)
        train_data["time"] = train_data["slice10min"].apply(lambda x: x[-4:])
        train_data = train_data.groupby(by=["time", "WIFIAPTag"])["passengerCount"].mean().round(2).reset_index()
        pre_oldtime = [every_time[-4:] for every_time in self.pre_time]
        train_data["slice10min"] = train_data["time"].apply(lambda x: "2016-09-14-"+x)
        del train_data["time"]
        train_data["slice10min"] == "2016-09-14-15-0"
        pre_value = train_data.loc[train_data["slice10min"].isin(self.pre_time),
                                   ["passengerCount", "WIFIAPTag", "slice10min"]]
        pre_value.to_csv("submissions/train_data.csv", index=False)
        '''
        print (pre_oldtime)
        # for group in train_data.groupby(by=["WIFIAPTag"]):
            # print group[1]["slice10min"]
            # break
            # group[1]["slice10min"]
        for group in train_data.groupby(by=["time"]):
            # print group[0]
            # if group[0] in pre_oldtime:


            break
        '''

        # train_data.to_csv("clean_data/train_data.csv", index=False)
        print("Mean_solution_two END!")
        return pre_value






