from app.models.alert import Alert
from daos.dao_alerts import DaoAlerts
import json
from app import pubsub
from check_last_price import GetLastPrice
class ControllerAlert:
    
    @staticmethod
    def get_alert():
        DaoAlert = DaoAlerts()

        alerts = DaoAlert.get_alerts()

        return alerts

    @staticmethod
    def insert(alerts, user_id):
        DaoAlert = DaoAlerts()
        alerts_insert = []
        last_price = GetLastPrice()

        for alert in alerts:

            alert = alert.split(":")
            ticket = alert[0].upper()
            down_percent = alert[1]
            up_percent = alert[2]

            new_alert = Alert(ticket, down_percent, up_percent, user_id)
            if new_alert.is_ticket() and new_alert.is_percents():
                if not DaoAlert.get_alerts_by_ticket(ticket, user_id):
                    DaoAlert.insert_alert(new_alert)
                    last_price.last_price_tickets(ticket)


                else:
                    alerts_insert.append(DaoAlert.update_alerts(new_alert))
                    # last_price.last_price_tickets()
            else:
                pubsub.publish('alerts', [user_id, f"Valore invalidos, consulte o manual com /help"])
            return alerts_insert

    @staticmethod
    def delete(ticket, user_id):
        DaoAlert = DaoAlerts()
        DaoAlert.delete_alert(ticket, user_id)






if __name__ == "__main__":
    a = ControllerAlert()
    a.insert('WEGE3:10:10')