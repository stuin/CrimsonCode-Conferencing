import ast

class Map(object):
	def __init__(self, content):
		self.doors = {}
		self.rooms = []
		self.width = max([ len(s) for s in content ])
		content = [(x + ' ' * (self.width - len(x))) for x in content]
		self.content = ''.join(content)
		self.startPos = self.content.find('>')

	def pos(self, x, y):
		return (y * self.width + x)

	def add_door(self, x, y, side1, side2):
		p = self.pos(x-1, y-1)
		if(self.content[p] == '-'):
			self.doors[p] = (side1, side2)
		else:
			print("No door at (%d, %d) %c" % (x-1, y-1, self.content[0]))

	def move(self, user, to):
		if self.content.get(to) == '#':
			return False
		if self.content.get(user.pos) == '-':
			if user.pos in self.doors:
				if to > user.pos:
					user.room = self.doors[user.pos][1]
				else:
					user.room = self.doors[user.pos][0]

	def serialize(self):
		return ('D' + str(self.doors) + '\n' + str(self.rooms)).encode()

	def deserialize(self, data):
		data = data[1:].split('\n')
		self.doors = ast.literal_eval(data[0])
		self.rooms = list(data[1])

	# default map setup
	def setup_1(self):
		self.rooms = [
			'Entrance Hall', 'Main Theatre', 'Side Theatre',
			'Side Hallway', 'Room 1', 'Room 2', 'Room 3']

		# large doors
		for x in range (12, 15):
			self.add_door(x, 11, 0, 1)
		for x in range (19, 22):
			self.add_door(x, 16, 0, 2)
		for x in range (26, 29):
			self.add_door(x, 16, 0, 3)

		# side rooms
		self.add_door(29, 14, 3, 4)
		self.add_door(29, 10, 3, 5)
		self.add_door(29,  6, 3, 6)




