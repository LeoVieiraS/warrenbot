import datetime
from datetime import timedelta

from pandas_datareader import data as wb
from pandas_datareader._utils import RemoteDataError


class Alert(object):
    def __init__(self, ticket, down_percent, up_percent, user_id):
        self.ticket = ticket
        self.down_percent = down_percent
        self.up_percent = up_percent
        self.user_id = user_id

    def properties_validate(self):
        pass

    def is_ticket(self):
        yesterday = (datetime.datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
        try:
            wb.DataReader(self.ticket + ".SA", data_source="yahoo", start=yesterday)
            return True
        except RemoteDataError:
            return False

    def is_percents(self):
        if int(self.down_percent) and int(self.up_percent):
            return True
        else:
            return False
