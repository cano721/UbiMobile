from frame.parkapp.parking_db import Db
from frame.parkapp.parking_sql import Sql
from frame.parkapp.parking_value import Parking_floor


class ParkDb(Db):
    # def select(self):
    #     conn = super().getConnection();
    #     cursor = conn.cursor();
    #     cursor.execute(Sql.parking_floor_select);
    #     u = cursor.fetchone();
    #     super().close(conn,cursor);
    #     return u[0];

    def select(self):
        conn = super().getConnection();
        cursor = conn.cursor();
        cursor.execute(Sql.parking_floor_select);
        result = cursor.fetchall();
        all = [];
        for u in result:
            parking_floor = Parking_floor(u[0],u[1],u[2],u[3]);
            all.append(parking_floor);
        super().close(conn,cursor);
        return all;

    def update(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect("192.168.0.202", 1883, 60)
        if rc == 0:
            client.subscribe("mydata/function")
        else:
            print("연결실패")
        conn = super().getConnection();
        cursor = conn.cursor();
        cursor.execute(Sql.parking_floor_select);
        result = cursor.fetchall();
        all = [];
        for u in result:
            parking_floor = Parking_floor(u[0], u[1], u[2], u[3]);
            all.append(parking_floor);
        super().close(conn, cursor);
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
    parking = UsersDb().select();
    for i in parking:
        print(i)
#
#
#
if __name__ == '__main__':
    # users_counter_test(10,20)
    select_test()
