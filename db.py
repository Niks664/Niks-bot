import sqlite3
import time
from singleton import Singleton

class Database(Singleton):
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'user' WHERE 'user_id' =?", (user_id,)).fetchall()
            return bool(len(result))
        
    def add_user(self, user_id):
        with self.connection:
            return self.connection.execute("REPLACE INTO 'user' ('user_id') VALUES (?)", (user_id,))
        
    def mute(self, user_id):
        with self.connection:
            user = self.cursor.execute("SELECT * FROM 'user' WHERE 'user_id' = ?", (user_id,)).fetchone()
            return int(user[2]) >= int(time.time()) 
    
    def add_mute(self, mute_min, user_id):
        with self.connection:
            return self.connection.execute(f"UPDATE 'user' SET 'mute_time' = {int(time.time() + mute_min * 60)} WHERE 'user_id' = {user_id}")
        