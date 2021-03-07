import json
from enum import IntEnum

class DIRECTION(IntEnum):
	UP = -2
	DOWN = 2
	LEFT = -1
	RIGHT = 1

class Map(object):
	def __init__(self, content=None, helpfile=None):
		self.doors = {}
		self.rooms = []
		self.pinned = []
		self.blocked = ['#', '>']
		self.content = ''
		if content:
			self.width = max([ len(s) for s in content ])
			content = [(x[:-1] + ' ' * (self.width - len(x))) for x in content]
			self.content = '\n'.join(content)
			self.startPos = self.content.find('>') + 1
			self.help = ''.join(helpfile)

	def pos(self, x, y):
		return (y * self.width + x)

	def add_door(self, x, y, side1, side2):
		p = self.pos(x-1, y-1)
		if(self.content[p] == '-'):
			self.doors[p] = (side1, side2)
		else:
			print("No door at (%d, %d) %c" % (x-1, y-1, self.content[0]))

	def move(self, user, dir):
		to = user.pos
		if dir == DIRECTION.LEFT or dir == DIRECTION.RIGHT:
			to += dir.value
		else:
			to += int(dir.value / 2 * self.width)

		if self.content[to] in self.blocked:
			return False

		if self.content[user.pos] == '-' and self.content[to] != '-' and str(user.pos) in self.doors:
			r = user.room
			if to < user.pos:
				user.room = self.doors[str(user.pos)][1]
			else:
				user.room = self.doors[str(user.pos)][0]
			if user.room != r:
				user.changed = 2
			user.pos = to
			return True

		user.pos = to
		return True

	def draw(self, users):
		output = self.content
		for u in users.values():
			output = output[:u.pos] + u.avatar + output[u.pos + 1:]
		return output

	def serialize(self):
		return ('D' + json.dumps(self.__dict__) + "$").encode()

	def deserialize(self, data):
		data = json.loads(data[1:])
		self.doors = data['doors']
		self.rooms = data['rooms']
		self.pinned = data['pinned']
		self.width = data['width']
		self.content = data['content']
		self.startPos = data['startPos']
		self.help = data['help']

	# default map setup
	def setup_1(self):
		self.rooms = [
			'Entrance Hall', 'Main Theatre', 'Side Theatre',
			'Side Hallway', 'Room 1', 'Room 2', 'Room 3', "Room 4"
		]
		self.pinned = [
			'Users enter here', 'https://github.com/stuin/CrimsonCode-Conferencing', 'https://www.linkedin.com/in/stuin01/',
			'Passage to smaller rooms', 'Example topic 1', 'Example topic 2', 'Example topic 3', 'Example topic 4'
		]

		# large doors
		for x in range (9, 12):
			self.add_door(x, 11, 0, 1)
		for x in range (16, 19):
			self.add_door(x, 16, 0, 2)
		for x in range (25, 28):
			self.add_door(x, 16, 0, 3)

		# side rooms
		self.add_door(28, 14, 4, 3)
		self.add_door(28, 10, 5, 3)
		self.add_door(28,  6, 6, 3)
		self.add_door(24,  6, 3, 7)
		self.add_door(21,  2, 3, 1)
		self.add_door(21,  3, 3, 1)




