from pymongo import MongoClient
class Database:
	def __init__(self):
		self.client = MongoClient('localhost', 27017)
		self.db = self.client.twitch_chat
		self.collection = self.db.messages

	def insert(self, document):
		if document == None:
			return None
		id = self.collection.insert_one(dict(document)).inserted_id
		return id
