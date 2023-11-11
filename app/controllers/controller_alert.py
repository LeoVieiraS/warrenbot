from app import pubsub
from app.models.alert import Alert
from check_last_price import GetLastPrice
from conf.database import Connection


class ControllerAlert:
    @staticmethod
    def get_alerts(user_id):
        conn = Connection()
        cur = conn.cursor()

        try:
            sql = f"select * from alerts where user_id = {user_id}"
            print(sql)
            cur.execute(
                sql,
            )
            data = cur.fetchall()
            pubsub.publish("alerts", [user_id, "Seus alertas:"])
            for alert in data:
                a = Alert(alert[1], alert[2], alert[3], alert[4])
                mensagem = (
                    f"TICKET:{a.ticket} QUEDA: {a.down_percent}% ALTA:{a.up_percent}%"
                )
                pubsub.publish("alerts", [a.user_id, mensagem])
        except Exception:
            return None

    @staticmethod
    def get_alerts_by_ticket(ticket, user_id):
        try:
            conn = Connection()
            cur = conn.cursor()
            sql = "select * from alerts where ticket = %s and user_id = %s"
            cur.execute(
                sql,
                (
                    ticket,
                    user_id,
                ),
            )
            data = cur.fetchall()

            if len(data) > 0:
                for i in data:
                    alert = Alert(i[1], i[2], i[3], i[4])
                    return alert
            else:
                return False
        except Exception:
            return None

    @staticmethod
    def insert(alerts, user_id):
        conn = Connection()
        cur = conn.cursor()

        alerts_insert = []
        last_price = GetLastPrice()
        for alert in alerts:
            alert = alert.split(":")
            ticket = alert[0].upper()
            down_percent = alert[1]
            up_percent = alert[2]
            new_alert = Alert(ticket, down_percent, up_percent, user_id)
            if new_alert.is_ticket() and new_alert.is_percents():
                if not ControllerAlert.get_alerts_by_ticket(ticket, user_id):
                    try:
                        sql = "insert into alerts(ticket,down_percent, up_percent,user_id) values (%s, %s, %s, %s)"
                        print(
                            new_alert.ticket,
                            new_alert.down_percent,
                            new_alert.up_percent,
                            new_alert.user_id,
                        )
                        cur.execute(
                            sql,
                            (
                                new_alert.ticket,
                                new_alert.down_percent,
                                new_alert.up_percent,
                                new_alert.user_id,
                            ),
                        )
                        conn.commit()
                        pubsub.publish(
                            "alerts",
                            [
                                new_alert.user_id,
                                f"{new_alert.ticket}  inserido com sucesso",
                            ],
                        )
                        last_price.last_price_tickets(ticket)
                    except Exception:
                        pubsub.publish(
                            "alerts", [user_id, f"falha ao inserir {alert.ticket}"]
                        )

                else:
                    alerts_insert.append(ControllerAlert.update_alerts(new_alert))
                    last_price.last_price_tickets()
            else:
                pubsub.publish(
                    "alerts",
                    [user_id, "Valores inválidos, consulte o manual com /help"],
                )
            return alerts_insert

    @staticmethod
    def delete_alert(ticket, user_id):
        try:
            conn = Connection()
            cur = conn.cursor()
            sql = "delete from alerts where ticket = %s and user_id = %s"
            cur.execute(sql, (ticket, user_id))
            conn.commit()
            pubsub.publish("alerts", [user_id, f"{ticket} excluido com sucesso "])
        except Exception:
            pubsub.publish("alerts", [user_id, f"erro ao excluir {ticket}"])

    @staticmethod
    def update_alerts(alert):
        try:
            conn = Connection()
            cur = conn.cursor()
            sql = "update alerts set down_percent = %s, up_percent = %s where ticket = %s and user_id = %s"
            cur.execute(
                sql, (alert.down_percent, alert.up_percent, alert.ticket, alert.user_id)
            )
            conn.commit()
            pubsub.publish("alerts", [alert.user_id, "Alerta atualizado com sucesso"])
        except Exception:
            pubsub.publish("alerts", [alert.user_id, "erro ao atualizar alerta"])


if __name__ == "__main__":
    a = ControllerAlert()

    a.insert(["WEGE3:4:5"], 409891117)
