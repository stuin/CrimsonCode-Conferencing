class DataModel(object):
	def __init__(self):
		self.map = None
		self.users = None

	def setup(self, map, users):
		self.map = map
		self.users = users

	def get_users(self):
		return [ (user.name, user.index) for user in self.users.values() ]

	def get_map(self):
		return self.map.content

	def get_height(self):
		return len(self.map.content)
