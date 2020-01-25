from conf.database import Connection
from datetime import datetime
class LastVerify(Connection):


    def get(self, token, user_id):
        now = datetime.now()
        date = datetime.strftime(now, '%Y-%m-%d')

        sql = 'SELECT * FROM last_alert WHERE ticket = %s AND user_id = %s AND dt_alert = %s'

        cur = self._db.cursor()
        cur.execute(sql, (token, user_id, date, ))


        if cur.rowcount > 0:
           return False
        else:
            return True



    def insert(self, ticket,user_id):
        now = datetime.now()
        date = datetime.strftime(now, '%Y-%m-%d')
        sql = '''insert into last_alert(ticket, user_id, dt_alert) values (%s,%s,%s)'''

        cur = self._db.cursor()
        cur.execute(sql, (ticket, user_id, date,))
        self._db.commit()


if __name__ == "__main__":
    a = LastVerify()

    a.get('ITSA4', '409891117')
    a.insert('ENBR3', '409891117')