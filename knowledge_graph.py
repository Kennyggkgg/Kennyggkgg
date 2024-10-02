import sqlite3

class KnowledgeGraph:
    def __init__(self, db_path):
        self.db_path = db_path
        self.initialize_db()

    def initialize_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS knowledge (
                    concept TEXT PRIMARY KEY, 
                    related_concepts TEXT, 
                    data TEXT
                )'''
            )
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS user_profiles (
                    username TEXT PRIMARY KEY, 
                    data TEXT
                )'''
            )
            conn.commit()

    def store_knowledge(self, concept, related_concepts, data):
        related_concepts_str = ','.join(related_concepts)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT OR REPLACE INTO knowledge (concept, related_concepts, data) 
                VALUES (?, ?, ?)''', 
                (concept, related_concepts_str, data)
            )
            conn.commit()

    def retrieve_knowledge(self, concept):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''SELECT related_concepts, data FROM knowledge 
                WHERE concept = ?''', 
                (concept,)
            )
            result = cursor.fetchone()
            if result:
                related_concepts = result[0].split(',')
                data = result[1]
                return related_concepts, data
            else:
                return None, None