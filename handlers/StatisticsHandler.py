# coding=utf-8


import tornado.web
from handlers.base import BaseHandler
from datetime import datetime

class StatisticsHandler(BaseHandler):
    def get(self):
        if self.current_user:
            return self.redirect("/index")
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
        print(records)
        for record in records:
            temp = results[str(record["createtime"])]
            if temp:
                pass
            else:
                temp = {}
                temp.update("name", str(record["name"]))
                temp.update("osType", str(record["type"]))
                temp.update("androidCount", 0)
                temp.update("iOSCount", 0)

            print record , type(record)



