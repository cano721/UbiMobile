from frame.adminapp.adamin_sql import Sql
from frame.adminapp.admin_value import Parking
from frame.parkapp.parking_db import Db


class AdminDb(Db):
    # def select(self):
    #     conn = super().getConnection();
    #     cursor = conn.cursor();
    #     cursor.execute(Sql.parking_floor_select);
    #     u = cursor.fetchone();
    #     super().close(conn,cursor);
    #     return u[0];

    def select(self,u_id):
        conn = super().getConnection();
        cursor = conn.cursor();
        cursor.execute(Sql.parking_select % u_id);
        result = cursor.fetchall();
        all = [];
        for u in result:
            parking = Parking(u[0],u[1],u[2],u[3],u[4]);
            all.append(parking);
        super().close(conn,cursor);
        return all;





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

def select_test():
    parking = AdminDb().select('id01');
    for i in parking:
        print(i)
#
#
#
if __name__ == '__main__':
    # users_counter_test(10,20)
    select_test()
