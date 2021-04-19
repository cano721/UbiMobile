class Sql:
    users_counter = """SELECT COUNT(*) FROM users
                        WHERE u_age>= %d and u_age< %d"""

    recipe_select = """SELECT ROW_NUMBER() OVER (ORDER BY r_view DESC), r_name,r_recommend,r_view,r_public
                        FROM recipe
                        LIMIT 10"""

    parking_floor_select = """SELECT * FROM parking_floor"""