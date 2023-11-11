import psycopg2


class Connection(object):
    _db = None

    def __init__(
        self,
        host="warrenbot-postgres",
        db="warrenbot",
        user="postgres",
        password="warrenbot",
    ):
        self._db = psycopg2.connect(host=host, user=user, password=password)

    def get_user(self):
        users = []
        try:
            cur = self._db.cursor()
            sql = "select user_id from users"
            cur.execute(sql)
            data = cur.fetchall()

            for user in data:
                users.append(user[0])
        except Exception:
            return None
        return users

    def close(self):
        return self._db.close()

    def commit(self):
        return self._db.commit()

    def cursor(self):
        return self._db.cursor()
