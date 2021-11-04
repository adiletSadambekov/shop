from settings_project import con

con = con

class Data_users:
    def __init__(self, con):
        self.__con = con
    
    def adduser(self, name, surname, email, phone, password):
        with self.__con:
            with self.__con.cursor() as self.__cur:
                self.__cur.execute('select count(*) from customer where email=%s', ((email,)))
                presence = self.__cur.fetchone()
                if sum(presence) > 0:
                    is_precent = 'Пользаватель с таким именем уже существует'
                    return is_precent, False
                else:
                    self.__cur.execute('insert into customer (name, surname, email, phone, password) values (%s, %s, %s, %s, %s)', ((name), (surname), (email), (phone), (password)))
                self.__con.commit()
        return True

    def getuser_id(self, id):
        with self.__con:
            with self.__con.cursor() as self.__cur:
                self.__cur.execute('select * from customer where id = %s;', ((id,)))
                res = self.__cur.fetchall()
                if not res:
                    print('Пользователь с id %s не найден', id)
                    return False
                data_user = []
                for i in res:
                    r = {
                        'id': i[0],
                        'name': i[1],
                        'phone': i[2],
                        'email': i[3],
                        'surname': i[4],
                        'password': i[5]
                        }
                    data_user.append(r)
        return data_user
    

    def getuser_email(self, email):
        with self.__con:
            with self.__con.cursor() as self.__cur:
                self.__cur.execute('select * from customer where email = %s;', (email))
                res = self.__cur.fetchall()
                if not res:
                    print('пользователь с email %s не найден', (email))
                    return False
                data_user = []
                for i in res:
                    r = {
                        'id': i[0],
                        'name': i[1],
                        'phone': i[2],
                        'email': i[3],
                        'surname': i[4],
                        'password': i[5]
                        }
                    data_user.append(r)
        return data_user


class Products:
    def __init__(self, con):
        self.__con = con
    
    def get_topprod(self, id):
        with self.__con:
            with self.__con.cursor() as self.__cur:
                self.__cur.execute('select * from product where id < %s;', ((id,)))
                m = self.__cur.fetchall()
                main_products = []
                for p in m:
                    r = {
                        'id': p[0],
                        'name': p[1],
                        'des': p[2],
                        'price': p[3]
                    }
                    main_products.append(r)

        return main_products

