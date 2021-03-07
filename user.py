import ast
import re

i = 0
validreg = re.compile('[ a-zA-Z0-9_?!,./@]+\n')

class User(object):
	def __init__(self, data, pos=None):
		global i
		self.changed = 0
		if pos is None:
			data = ast.literal_eval(data)
			self.name = data[0]
			self.avatar = "@"
			self.room = data[1]
			self.pos = data[2]
			self.index = data[3]
		else:
			self.name = data
			self.avatar = "@"
			self.room = 0
			self.pos = pos
			self.index = i
			i += 1

	def serialize(self):
		return str([self.name, self.room, self.pos, self.index])
