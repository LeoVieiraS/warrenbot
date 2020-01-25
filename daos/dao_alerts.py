from conf.database import Connection
from app.models.alert import Alert
import json
from app import pubsub
class DaoAlerts(Connection):


    def get_alerts(self):
        alerts = []
        try:
            cur = self._db.cursor()
            sql = 'select * from alerts'
            cur.execute(sql)
            data = cur.fetchall()

            for alert in data:
                a = Alert(alert[1], alert[2], alert[3], alert[4])
                alerts.append(a)
            return alerts
        except:
            return None

    def insert_alert(self, alert):
        try:
            cur = self._db.cursor()
            sql = 'insert into alerts(ticket,down_percent, up_percent,user_id) values (%s, %s, %s, %s)'
            cur.execute(sql, (alert.ticket, alert.down_percent, alert.up_percent, alert.user_id))
            self._db.commit()
            pubsub.publish('alerts', [alert.user_id, f"{alert.ticket}  inserido com sucesso"])
        except:
            pubsub.publish('alerts', [alert.user_id, f"falha ao inserir {alert.ticket}"])

    def get_alerts_by_ticket(self, ticket, user_id):
        try:
            cur = self._db.cursor()
            sql = 'select * from alerts where ticket = %s and user_id = %s'
            cur.execute(sql, (ticket, user_id,))
            data = cur.fetchall()

            if len(data) > 0:
                for i in data:
                    alert = Alert(i[1], i[2], i[3], i[4])
                    return alert
            else:
                return False
        except:
            return None


    def update_alerts(self, alert):
        try:
            DaoAlert = DaoAlerts()
            cur = self._db.cursor()
            sql = 'update alerts set down_percent = %s, up_percent = %s where ticket = %s and user_id = %s'
            cur.execute(sql, (alert.down_percent, alert.up_percent, alert.ticket, alert.user_id))
            self._db.commit()
            return json.dumps(({alert.ticket: "Alerta atualizado com sucesso"}))
        except:
            return json.dumps(({alert.ticket: "erro ao inserir"}))