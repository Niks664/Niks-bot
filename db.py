import sqlite3
import time

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("select * from users where user_id =?", (user_id,)).fetchall()
            return bool(len(result))
            
    def add_user(self, user_id):
        with self.connection:
            return self.connection.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        
    # def usernames(self,username):
    #     with self.connection:
    #         return self.connection.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        
    def add_usernames(self,username: str, user_id:int):
        with self.connection:           
            return self.connection.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))   
        
    def mute(self, user_id):
        with self.connection:
            user = self.connection.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return int(user[2]) >= int(time.time()) 
    
    def add_mute(self, user_id, mute_time):
        with self.connection:
            return self.connection.execute("UPDATE users SET mute_time = ? WHERE user_id = ?", (int(time.time()) + (mute_time * 60), user_id))
    
    def un_mute(self, user_id):
        with self.connection:
            return self.connection.execute("UPDATE users SET mute_time = 0 WHERE user_id =?", (user_id,))

    def get_balance(self, user_id):
        with self.connection:
            balance = self.connection.execute("SELECT balance FROM users WHERE user_id =?", (user_id,)).fetchone()[0]
            return balance
        
    def update_balance(self, user_id, new_balance):
        with self.connection:
            return self.connection.execute("UPDATE users SET balance =? WHERE user_id =?", (new_balance, user_id))
    
    def add_balance(self, user_id, amount):
        with self.connection:
            return self.connection.execute("UPDATE users SET balance = balance +? WHERE user_id =?", (amount, user_id))
    
    def remove_balance(self, user_id, amount):
        with self.connection:
            return self.connection.execute("UPDATE users SET balance = balance -? WHERE user_id =?", (amount, user_id))
    
