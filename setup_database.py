from conf.database import Connection


class SetupDatabase(Connection):
    def create_database(self):
        print("Criando banco de dados...")
        cur = self._db.cursor()
        sql = """
            DO $$
                BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'warrenbot') THEN
                    CREATE DATABASE warrenbot;
                END IF;
            END $$;
            """
        cur.execute(sql)
        self._db.commit()

    def create_table_alerts(self):
        cur = self._db.cursor()
        sql = """create table if not exists alerts(id serial primary key,
        ticket varchar(20),
        down_percent int not null,
        up_percent int not null,
        user_id int not null)"""
        cur.execute(sql)
        self._db.commit()

    def create_table_price_last_day(self):
        cur = self._db.cursor()
        sql = """create table if not exists price_last_day(id serial primary key,ticket varchar(20) not null,preco numeric(4,2) not null)"""
        cur.execute(sql)
        self._db.commit()

    def create_table_last_alert(self):
        cur = self._db.cursor()
        sql = """create table if not exists last_alert(id serial primary key,
        ticket varchar(20) not null,
        user_id int not null,
        dt_alert date)"""
        cur.execute(sql)
        self._db.commit()

    def create_table_users(self):
        cur = self._db.cursor()
        sql = """create table if not exists users(user_id int not null, username varchar(50) not null )"""
        cur.execute(sql)
        self._db.commit()


if __name__ == "__main__":
    a = SetupDatabase()
    a.create_database()
    a.create_table_alerts()
    a.create_table_price_last_day()
    a.create_table_last_alert()
    a.create_table_users()
