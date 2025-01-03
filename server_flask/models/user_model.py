from models.database import Database

class User:
    @staticmethod
    def get_user_by_email(email):
        query = f"SELECT * FROM Users WHERE Email = '{email}' LIMIT 1"
        user=Database.execute_query(query)
        return user[0] if user else None
    
    @staticmethod
    def add_user(fullname, email, password, role):
        query= f'INSERT INTO Users (Fullname, Email, Password, Role) VALUES ("{fullname}", "{email}", "{password}", "{role}")'
        Database.execute_non_query(query)
    
    @staticmethod
    def get_all_roles():
        roles =[
            "Admin",
            "Executive",
            "Manager",
            "Receptionist",
            "Customer"
        ]
        return roles

    @staticmethod
    def get_area_by_user_id(user_id):
        query = f"SELECT ua.Area_Id, a.Name FROM User_Area ua join Areas a on ua.Area_Id = a.id WHERE ua.User_Id = {user_id}"
        return Database.execute_query(query)
