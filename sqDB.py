from settings_project import con



class DB():

    def __init__(self, con):
        self.__db = con
        self.__cur = self.__db.cursor()

    def getUser(self, id):
        try:
            self.__cur.execute('select * from customer where id=%s;', ((id,)))
            res = self.__cur.fetchall()
            if not res:
                print('Пользователь не найден')
                return False
            result = []
            for i in res:
                r = {
                    'id': i[0],
                    'name': i[1],
                    'phone': i[2],
                    'email': i[3],
                    'password': i[4]
                }
                result.append(r)

        except:
            self.__cur.close()
            self.__db.close()
            print('Ошибка чтения данных')
            return False
        return result
    
    def getUseremail(self, email):
        self.__cur.execute('select * from customer where email = %s', ((email,)))
        res = self.__cur.fetchall()
        infem = []
        for i in res:
            r = {
                'id': i[0],
                'name': i[1],
                'phone': i[2],
                'email': i[3],
                'surname': i[4],
                'password': i[5]
            }
            infem.append(r)
        return infem




    def adduser(self, name, surname, email, phone, password):

        with self.__db:
            with self.__cur as self.__c:
                self.__c.execute('select count(*) from customer where email=%s', ((email,)))
                res = self.__c.fetchone()
                if int(res) > 0:
                    print('пользаватель с таким именем уже существует')
                    return False
                self.c.execute(""" insert into customer (name, surname, email, phone, password)
                values(%s, %s, %s, %s, %s)""",
                ((name), (surname), (email), (phone), (password)))
            self.__db.commit()
        return True