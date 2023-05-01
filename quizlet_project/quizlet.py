import sqlite3 as sq
import random as rd 

class Instance:
    def __init__(self,   word, translation):
        
        DATA_BASE = "quizlet.db"
        self.word = word
        self.translation = translation
        self.connection = sq.connect(DATA_BASE)
        self.cursor = self.connection.cursor()
        self.create_table()  
    
    def __len__(self):
        self.cursor.execute('SELECT COUNT(*) FROM vocab')
        return self.cursor.fetchone()[0]    

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vocab (
                ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                word TEXT,
                translation TEXT
            )
        ''')
        self.connection.commit()

    def load_word(self):
        self.cursor.execute(''' 
        SELECT COUNT (*) FROM vocab;
        
        ''')
        lol = self.cursor.fetchone()
        choice = rd.randint(1, int (lol[0]))
        self.cursor.execute('''
            SELECT * FROM vocab
            WHERE id = ?
            ''',(choice,))
        results = self.cursor.fetchone()
        
        self.word = results[1]
        self.translation = results[2]
        return self.word,self.translation

    def insert_word(self):
        self.cursor.execute(
            """
            INSERT INTO vocab (word, translation)
            VALUES (?, ?)
            """, (self.word, self.translation))
        self.connection.commit()