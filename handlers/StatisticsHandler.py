# coding=utf-8


import tornado.web
from handlers.base import BaseHandler
from datetime import datetime
from common.strUtil import *



class StatisticsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        menu = self.active_menu("Statistics")
        return self.render("statistics.html", menu=menu)
    
    @tornado.web.authenticated
    def post(self):
        beginDate = self.get_argument("beginDate", None)
        endDate = self.get_argument("endDate", None)
        osType = self.get_argument("osType", None)
        qrType = self.get_argument("qrType", None)

        beginDate = datetime.min
        endDate = datetime.max

        records = self.datastore.queryScanDataWithBeginAndEnd(beginDate, endDate, osType, qrType)

        results = {}

        qrs = self.datastore.queryQrs()
        temp_qrs = qrs

        titles = []
        titles.append("时间")
        for qr in qrs:
            titles.append(qr["name"]+"_安卓扫描量")
            titles.append(str(qr["name"])+str("_安卓下载量"))
            titles.append(qr["name"]+str("_苹果扫描量"))

        for record in records:
            createtime = datetime_toString(record["createtime"])
            name = record["name"].encode('utf-8')
            type_ = record["type"]
            temp = results.get(createtime)
            if temp:
                pass
            else:
                temp = {}
                temp["osType"] = type_
                qrs = self.datastore.queryQrs()
                for qr in qrs:
                    temp_name = qr["name"].encode("utf-8")
                    temp[temp_name+"_安卓扫描量"] = 0
                    temp[temp_name+"_苹果扫描量"] = 0
                    temp[temp_name+"_安卓下载量"] = 0

            if record["type"] == 1:
                temp[name+"_安卓扫描量"] = int(temp[name+"_安卓扫描量"]) + 1
            else:
                temp[name+"_苹果扫描量"] = int(temp[name+"_苹果扫描量"]) + 1
            temp["createtime"] = createtime

            results[createtime] = temp

        records = self.datastore.queryDownloadDataWithBeginAndEnd(beginDate, endDate, osType, qrType)
        for record in records:
            createtime = datetime_toString(record["createtime"])
            name = record["name"].encode('utf-8')
            type_ = record["type"]
            temp = results.get(createtime)
            if temp:
                pass
            else:
                temp = {}
                temp["osType"] = type_
                qrs = self.datastore.queryQrs()
                for qr in qrs:
                    temp_name = qr["name"].encode("utf-8")
                    temp[temp_name+"_安卓下载量"] = 0
                    temp[temp_name+"_安卓扫描量"] = 0
                    temp[temp_name+"_苹果扫描量"] = 0

            if record["type"] == 1:
                temp[name+"_安卓下载量"] = int(temp[name+"_安卓下载量"]) + 1
            temp["createtime"] = createtime

            results[createtime] = temp


        datas = []
        items = results.keys()
        items.sort()

        for item in items:
            data = []
            temp = results[item]
            data.append(item)
            qrs = self.datastore.queryQrs()
            for qr in qrs:
                name = qr["name"].encode('utf-8')
                data.append(temp[name+"_安卓扫描量"])
                data.append(temp[name+"_安卓下载量"])
                data.append(temp[name+"_苹果扫描量"])

            datas.append(data)

        return self.render("statistics_table.html", datas=datas, titles = titles)