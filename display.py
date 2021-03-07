from asciimatics.widgets import Frame, ListBox, Layout, VerticalDivider, \
	Widget, Button, Label
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

		self._list_view = ListBox(
			Widget.FILL_FRAME,
			model.get_users(),
			name="Users",
			add_scroll_bar=True)
		self._map_view = Label(
			model.get_map(),
			model.get_height())
		layout = Layout([2,1, 8], 9)
		self.add_layout(layout)
		layout.add_widget(self._list_view, 0)
		layout.add_widget(VerticalDivider(Widget.FILL_FRAME), 1)
		layout.add_widget(self._map_view, 2)
		layout2 = Layout([1])
		self.add_layout(layout2)
		layout2.add_widget(Button("Quit", self._quit), 0)
		self.fix()

	@staticmethod
	def _quit():
		raise StopApplication("User pressed quit")

def demo(screen, scene):
	scenes = [
		Scene([MainView(screen, model)], -1, name="Main")
	]

	screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

model = DataModel()
def start_display(map, users):
	model.setup(map, users)
	last_scene = None
	while True:
		try:
			Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
			return
		except ResizeScreenError as e:
			last_scene = e.scene

def test(map, users):
	model.setup(map, users)
	print(model.get_users())