import ast

i = 0

class User(object):
	def __init__(self, data, pos=None):
		global i
		if pos is None:
			data = ast.literal_eval(data)
			self.name = data[0]
			self.avatar = data[1]
			self.room = data[2]
			self.pos = data[3]
			self.index = i
			i += 1
		else:
			self.name = data
			self.avatar = '@'
			self.room = 0
			self.pos = pos
			self.index = i
			i += 1

	def serialize(self):
		return str([self.name, self.avatar, self.room, self.pos])
