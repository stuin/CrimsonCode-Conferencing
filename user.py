class User(object):
	def __init__(self, addr, name, startPos):
		self.addr = addr
		self.name = name
		self.avatar = '@'
		self.room = 0
		self.pos = startPos