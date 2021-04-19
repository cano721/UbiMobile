from frame.loginapp.login_db import Db
from frame.loginapp.login_sql import Sql
from frame.loginapp.login_value import Users




class UsersDb(Db):
    # def select(self):
    #     conn = super().getConnection();
    #     cursor = conn.cursor();
    #     cursor.execute(Sql.parking_floor_select);
    #     u = cursor.fetchone();
    #     super().close(conn,cursor);
    #     return u[0];

    def selectid(self,id):
        conn = super().getConnection();
        cursor = conn.cursor();
        cursor.execute(Sql.selectid % id);
        u = cursor.fetchone();

        users = Users(u[0],u[1],u[2],u[3],u[4]);
        super().close(conn,cursor);
        return users;





# userlist Test Function ..........
# def userlist_test():
#     users = ReviewDb().select_review();
#     for u in users:
#         print(u);

# def users_counter_test(num1,num2):
#     counter = UsersDb().select(num1,num2);
#     print(counter)
#
# def recipe_select_test():
#     recipe = UsersDb().recipe_select();
#     for r in recipe:
#         print(r)


def select_idtest():
    login = UsersDb().selectid("id01");
    print(login)
#
#
#
if __name__ == '__main__':
    # users_counter_test(10,20)
    select_idtest()
