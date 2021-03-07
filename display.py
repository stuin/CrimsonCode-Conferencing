from asciimatics.widgets import *
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.parsers import AsciimaticsParser
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication

from model import DataModel
from map import DIRECTION
from user import validreg

class MainView(Frame):
	def __init__(self, screen, model):
		super(MainView, self).__init__(screen,
									   screen.height,
									   screen.width,
									   hover_focus=True,
									   can_scroll=False,
									   title="Crimson Conferences")
		self.model = model
		self.parser = AsciimaticsParser()
		self.set_theme("green")
		self.bmap = {
			'w': (self.model.add_move, DIRECTION.UP),
			's': (self.model.add_move, DIRECTION.DOWN),
			'a': (self.model.add_move, DIRECTION.LEFT),
			'd': (self.model.add_move, DIRECTION.RIGHT),
			'h': (self.help, 0),
			'q': (self.quit, 0)
		}
		self.cmap = {
			'kick': self.kick,
			'say': self.say,
			'help': self.help,
			'quit': self.quit
		}

		# main widgets
		self._me_label = Label(model.me.name, 1)
		self._me_label.disabled = True
		self._me_label.custom_colour = "label"
		self._users_list = ListBox(10, model.user_list)
		self._users_list.disabled = True
		self._users_list.custom_colour = "label"
		self._message_list = ListBox(Widget.FILL_FRAME, model.log)
		self._message_list.disabled = True
		self._message_list.custom_colour = "label"
		self._input_box = TextBox(1, as_string=True, on_change=self._check_input)
		self._move_box = Text(on_change=self._check_movement)
		self._map_view = TextBox(Widget.FILL_FRAME, as_string=True, line_wrap=True)
		self._map_view.disabled = True
		self._map_view.custom_colour = "label"
		self._room_label = Label(model.room, 1)
		self._room_label.disabled = True
		self._room_label.custom_colour = "label"

		# arrangle main columns
		layout = Layout([4,1, 6])
		self.add_layout(layout)
		layout.add_widget(self._me_label, 0)
		layout.add_widget(self._users_list, 0)
		layout.add_widget(Divider(), 0)
		layout.add_widget(self._message_list, 0)
		layout.add_widget(self._input_box, 0)
		layout.add_widget(Divider(), 0)
		layout.add_widget(self._move_box, 0)
		layout.add_widget(VerticalDivider(Widget.FILL_FRAME), 1)
		layout.add_widget(self._map_view, 2)
		layout.add_widget(self._room_label, 2)

		# Finalization
		self._layout = Layout
		self.fix()
		self.model.log_height = self._message_list._h

	def _reset(self):
		if self.model.quit:
			quit(0)
		self.model.refresh()
		self._move_box.value = "move: "
		self._map_view.value = self.model.map
		self._room_label.text = self.model.room
		self._users_list.options = self.model.user_list
		self._message_list.options = self.model.log
		self.model.log_height = self._message_list._h

	def _check_input(self):
		if len(self._input_box.value) > 1:
			if validreg.match(self._input_box.value):
				cmd = self._input_box.value[:-1].split(' ')
				if cmd[0].lower() in self.cmap:
					self.cmap[cmd[0].lower()](cmd[1:])
				else:
					self.model.send_message(self._input_box.value)
				self._input_box.value = ""
			elif self._input_box.value[-1] == '\n':
				self._input_box.value = ""
		self._reset()

	def _check_movement(self):
		if len(self._move_box.value) == 7 and self._move_box.value != "move: ":
			button = self._move_box.value[6].lower()
			if button in self.bmap:
				self.bmap[button][0](self.bmap[button][1])
		self._reset()

	def kick(self, p):
		if self.model.me.op and p[0] != self.model.me.name:
			for user in self.model.users.values():
				if p[0] == user.name:
					self.model.add_message("{Kicked %s}" % p[0])
					self.model.send.put('L%d$' % user.index)

	def say(self, p):
		if self.model.me.op:
			self.model.add_message("[SERVER] " + ' '.join(p))
			self.model.send.put("C-1&[SERVER] %s$" % ' '.join(p))

	def help(self, a):
		self.model.help = True
		self.model.map = self.model.hall.help
		self._map_view.value = self.model.map

	def quit(self, a):
		if self.model.quit or qd:
			quit(0)
		else:
			raise NextScene("Quit")

qd = False
def _close(a):
	if a == 0:
		raise StopApplication("User pressed quit")
	else:
		qd = True
		raise NextScene("Main")

def demo(screen, scene):
	scenes = [
		Scene([MainView(screen, model)], -1, name="Main"),
		Scene([PopUpDialog(screen, "Are you sure you want to quit?", [ "Quit", "Cancel" ], _close)], -1, name="Quit")
	]

	screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

model=DataModel()
def start_display(other):
	global model
	model = other
	last_scene = None
	while True:
		try:
			Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
			return
		except ResizeScreenError as e:
			last_scene = e.scene