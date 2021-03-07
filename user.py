class User(object):
	def __init__(self, name, pos):
		self.name = name
		self.avatar = '@'
		self.room = 0
		self.pos = pos

	def serialize(self):
		return str([self.name, self.avatar, self.room, self.pos])

	def deserialize(self, data):
		data = list(data)
		self.name = data[0]
		self.avatar = data[1]
		self.room = data[2]
		self.pos = data[3]