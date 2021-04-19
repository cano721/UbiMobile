class Users:
    def __init__(self, u_id, u_nick, u_pwd,u_name,u_age):
        self.u_id = u_id;
        self.u_nick = u_nick;
        self.u_pwd = u_pwd;
        self.u_name = u_name;
        self.u_age = u_age;

    def __str__(self):
        return self.u_id + ' ' + self.u_nick + ' ' + self.u_pwd + ' ' \
               + self.u_name + ' ' + str(self.u_age)