# coding=utf-8


import tornado.web
from handlers.base import BaseHandler
from datetime import datetime
from util.strUtil import *

class StatisticsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        menu = self.active_menu("Statistics")
        return self.render("statistics.html", menu=menu)

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
            titles.append(qr["name"]+str("_AndroidScan"))
            titles.append(qr["name"]+str("_AndroidDownload"))
            titles.append(qr["name"]+str("_iOSScan"))
            titles.append(qr["name"]+str("_iOSDownload"))


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
                    temp[temp_name+"_androidScan"] = 0
                    temp[temp_name+"_iOSScan"] = 0
                    temp[temp_name+"_androidDownload"] = 0
                    temp[temp_name+"_iOSDownload"] = 0

            if record["type"] == 1:
                temp[name+"_androidScan"] = int(temp[name+"_androidScan"]) + 1
            else:
                temp[name+"_iOSScan"] = int(temp[name+"_iOSScan"]) + 1
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
                    temp[temp_name+"_androidDownload"] = 0
                    temp[temp_name+"_iOSDownload"] = 0
                    temp[temp_name+"_androidScan"] = 0
                    temp[temp_name+"_iOSScan"] = 0

            if record["type"] == 1:
                temp[name+"_androidDownload"] = int(temp[name+"_androidDownload"]) + 1
            else:
                temp[name+"_iOSDownload"] = int(temp[name+"_iOSDownload"]) + 1
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
                data.append(temp[name+"_androidScan"])
                data.append(temp[name+"_androidDownload"])
                data.append(temp[name+"_iOSScan"])
                data.append(temp[name+"_iOSDownload"])

            datas.append(data)

        return self.render("statistics_table.html", datas=datas, titles = titles)