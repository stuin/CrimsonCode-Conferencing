from asciimatics.widgets import *
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication

from model import DataModel

class MainView(Frame):
	def __init__(self, screen, model):
		super(MainView, self).__init__(screen,
									   screen.height,
									   screen.width,
									   hover_focus=True,
									   can_scroll=False,
									   title="Crimson Conferences")
		self._model = model
		self.set_theme("green")

		# main widgets
		self._users_view = ListBox(
			10,
			model.get_users(),
			add_scroll_bar=True)
		self._message_view = ListBox(
			Widget.FILL_FRAME,
			model.get_messages(),
			add_scroll_bar=True)
		self._input_view = TextBox(
			1,
			as_string=True,
			on_change=self._check_input)
		self._map_view = Label(
			model.get_map(),
			model.get_height())
		layout = Layout([3,1, 7])
		self.add_layout(layout)

		# arrangle columns
		layout.add_widget(self._users_view, 0)
		layout.add_widget(Divider(), 0)
		layout.add_widget(self._message_view, 0)
		layout.add_widget(self._input_view, 0)
		layout.add_widget(Divider(), 0)
		layout.add_widget(Button("Quit", self._quit), 0)
		layout.add_widget(VerticalDivider(Widget.FILL_FRAME), 1)
		layout.add_widget(self._map_view, 2)
		self.fix()
		self._users_view.focus()

	def _check_input(self):
		if self._input_view.value[-1] == '\n':
			self._model.send_message(self._input_view.value)

	@staticmethod
	def _quit():
		raise StopApplication("User pressed quit")

def demo(screen, scene):
	scenes = [
		Scene([MainView(screen, model)], -1, name="Main")
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