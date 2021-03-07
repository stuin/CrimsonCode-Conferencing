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
			self.avatar = data[1]
			self.room = data[2]
			self.pos = data[3]
			self.index = data[4]
		else:
			self.name = data
			self.avatar = '@'
			self.room = 0
			self.pos = pos
			self.index = i
			i += 1

	def serialize(self):
		return str([self.name, self.avatar, self.room, self.pos, self.index])
