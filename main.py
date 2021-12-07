from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line,Quad,Triangle
from kivy.properties import NumericProperty, Clock
from kivy import platform
from kivy.core.window import Window
import random
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout

""" Python Simple Game Starting and Restarting"""

# import Builder and load menu.kv then add it to simplegame.kv   
Builder.load_file("menu.kv")   

# Create The Main Widget here change the Widget to RelativeLayout   
class MainWidget(RelativeLayout):
	# Importing Functions ----->
	from transforms import transform, transform_2D, transform_perspective
	from user_actions import keyboard_closed, on_keyboard_up, on_keyboard_down, on_touch_up, on_touch_down
	perspective_point_x = NumericProperty(0)
	perspective_point_y = NumericProperty(0)

	menu_widget =ObjectProperty()

	V_NB_LINES = 10       # Number of lines
	V_LINES_SPACING = .4 # percentage in screen width
	vertical_lines = []  # Empty list of lines

	H_NB_LINES = 15
	H_LINES_SPACING = .1  # percentage in screen height
	horizontal_lines = []

	SPEED = .8
	current_offset_x = 0 # Assign offset of x
	current_offset_y = 0 # Assign offset of y


	SPEED_X = 3.0
	current_speed_x = 0
	current_offset_x = 0

	NB_TILES = 10
	tiles = []
	tiles_coordinates = []
	current_y_loop =0

	SHIP_WIDTH =  .1
	SHIP_HEIGHT = 0.035
	SHIP_BASE_Y = 0.04
	ship = None

	ship_coordinates = [(0, 0), (0, 0), (0, 0)]

	state_game_over =  False
	is_game_started = False  

	# call the __init__() constructor function
	def __init__(self, **kwargs):
		super(MainWidget, self).__init__(**kwargs)
		# Call init_vertical_lines() and init_horizontal_lines() functions to draw them in the constroctor
		self.init_vertical_lines()
		self.init_horizontal_lines()

		# call init_tiles() function
		self.init_tiles()
		# Call init_shp function
		self.init_ship()
		# call reset_game() function
		self.reset_game()

		if self.is_desktop():
			self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
			self._keyboard.bind(on_key_down=self.on_keyboard_down)
			self._keyboard.bind(on_key_up=self.on_keyboard_up)


		# Call update function every 1.0 / 60.0 sec
		Clock.schedule_interval(self.update, 1.0 / 60.0)

	# Check ship collision
	def check_ship_collision(self):
		for i in range(0, len(self.tiles_coordinates)):
			ti_x, ti_y = self.tiles_coordinates[i]
			if ti_y > self.current_y_loop + 1:
				return False
			if self.check_ship_collision_with_tile(ti_x, ti_y):
				return True
		return False

	# Check ship collision with tile
	def check_ship_collision_with_tile(self, ti_x, ti_y):
		xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
		xmax, ymax = self.get_tile_coordinates(ti_x + 1, ti_y + 1)
		for i in range(0, 3):
			px, py = self.ship_coordinates[i]
			if xmin <= px <= xmax and ymin <= py <= ymax:
				return True
		return False



	# Create Init Ship Function
	def init_ship(self):
		# Draw the Triangle Ship
		with self.canvas:
			# Black Color
			Color(0, 0, 0)
			self.ship = Triangle()
	#  Updating ship
	def update_ship(self):
		center_x = self.width / 2
		base_y = self.SHIP_BASE_Y * self.height
		ship_half_width = self.SHIP_WIDTH * self.width / 2
		ship_height = self.SHIP_HEIGHT * self.height
		# ....
		#    2
		#  1   3
		# self.transform
		self.ship_coordinates[0] = (center_x-ship_half_width, base_y)
		self.ship_coordinates[1] = (center_x, base_y + ship_height)
		self.ship_coordinates[2] = (center_x + ship_half_width, base_y)

		x1, y1 = self.transform(*self.ship_coordinates[0])
		x2, y2 = self.transform(*self.ship_coordinates[1])
		x3, y3 = self.transform(*self.ship_coordinates[2])

		self.ship.points = [x1, y1, x2, y2, x3, y3]



	# Draw Tiles
	def init_tiles(self):
		with self.canvas:
			Color(1, 1, 1)
			for i  in range(0, self.NB_TILES):
				self.tiles.append(Quad())

	# Straight line
	def pre_fill_tiles_coordinates(self):
		for i in range(0,10):
			self.tiles_coordinates.append((0,i))
	# Generate tiles_coordinates
	def generate_tiles_coordinates(self):
		last_y = 0
		last_x = 0

		for i in range(len(self.tiles_coordinates)-1, -1, -1):
			if self.tiles_coordinates[i][1] < self.current_y_loop:
				del self.tiles_coordinates[i]
		if len(self.tiles_coordinates) > 0:
			last_coordinates = self.tiles_coordinates[-1]
			last_x = last_coordinates[0]
			last_y = last_coordinates[1] +1

		for i  in range(len(self.tiles_coordinates), self.NB_TILES):
			# Generate random Tile
			r = random.randint(0,2)
			start_index = -int(self.V_NB_LINES / 2) + 1
			end_index = start_index + self.V_NB_LINES -1
			if last_x <= start_index:
				r=1
			if last_x >= end_index:
				r=2
			self.tiles_coordinates.append((last_x,last_y))
			if r == 1:
				last_x +=1
				self.tiles_coordinates.append((last_x,last_y))
				last_y +=1
				self.tiles_coordinates.append((last_x,last_y))
			if r == 2:
				last_x -=1
				self.tiles_coordinates.append((last_x,last_y))
				last_y +=1
				self.tiles_coordinates.append((last_x,last_y))
			last_y +=1

	# Draw Vertical Lines
	def init_vertical_lines(self):
		# use widget.canvas to set white color for the line and drow multiple lines
		with self.canvas:
			Color(1, 1, 1)
			#self.line = Line(points=[100, 0, 100, 100])
			for i in range(0, self.V_NB_LINES):
				self.vertical_lines.append(Line())

	# Draw Horizontal Lines
	def init_horizontal_lines(self):
		with self.canvas:
			Color(1, 1, 1)
			for i in range(0, self.H_NB_LINES):
				self.horizontal_lines.append(Line())


	# Updating Tiles Function
	def update_tiles(self):
		for i in range(self.NB_TILES):
			tile = self.tiles[i]
			tile_coordinate = self.tiles_coordinates[i]
			xmin, ymin = self.get_tile_coordinates(tile_coordinate[0],tile_coordinate[1])
			xmax, ymax = self.get_tile_coordinates(tile_coordinate[0]+1 ,tile_coordinate[1]+1)

			x1, y1 = self.transform(xmin,ymin)
			x2, y2 = self.transform(xmin,ymax)
			x3, y3 = self.transform(xmax,ymax)
			x4, y4 = self.transform(xmax,ymin)
			tile.points = [x1,y1,x2,y2,x3,y3,x4,y4]



	# Update Virtical Lines depending on  window size
	def update_vertical_lines(self):
		# -1 0 1 2 3
		# Calculate start index vertically
		start_index = -int(self.V_NB_LINES/2) + 1
		for i in range(start_index, start_index+self.V_NB_LINES):
			# Calculate line x vertically
			line_x = self.get_line_x_by_index(i)

			# Transformation list of vertical lines to 3D
			x1,y1 = self.transform(line_x,0)
			x2,y2 = self.transform(line_x,self.height)
			self.vertical_lines[i].points = [x1,y1,x2,y2]

	# Update Horizontal Lines depenging on window size
	def update_horizontal_lines(self):
		# Calculate start index and end index horizontally
		start_index = -int(self.V_NB_LINES/2) + 1
		end_index = start_index + self.V_NB_LINES -1

		# Calculate minimum of x and maximum of x horizontally
		xmin = self.get_line_x_by_index(start_index)
		xmax = self.get_line_x_by_index(end_index)

		# Calculate index of y horizontally
		for i in range(0, self.H_NB_LINES):
			# Calculate line y horizontally
			line_y =self.get_line_y_by_index(i)
			# Transformation list of horizontal lines to 3D
			x1, y1 = self.transform(xmin, line_y)
			x2, y2 = self.transform(xmax, line_y)
			self.horizontal_lines[i].points = [x1, y1, x2, y2]

	# Update the speed, time, and window size
	def update(self, dt):
		# print("dt: " + str(dt*60))
		time_factor = dt*60
		# Call update_vertical_lines() function to update virtical lines
		self.update_vertical_lines()
		# Call update_horizontal_lines() function to update virtical lines
		self.update_horizontal_lines()
		# Call update_tiles() function
		self.update_tiles()
		# Call Update Ship Function
		self.update_ship()

		if not self.state_game_over and self.is_game_started:        
			# going forward
			speed_y = self.SPEED * self.height /100
			self.current_offset_y += speed_y * time_factor

			# Loop
			spacing_y = self.H_LINES_SPACING * self.height
			while self.current_offset_y >= spacing_y:      
				self.current_offset_y -= spacing_y
				self.current_y_loop +=1
				self.generate_tiles_coordinates()

			# Moving to the left or to the  right
			speed_x = self.current_speed_x * self.width /100
			self.current_offset_x += speed_x * time_factor

		if not self.check_ship_collision() and not self.state_game_over :     
			print("GAME OVER")
			self.state_game_over = True
			self.menu_widget.opacity = 1

	# Operating system Checking !
	def is_desktop(self):
		if platform in ('linux', 'win', 'macosx'):
			return True
		return False

	# Get x by index
	def get_line_x_by_index(self, index):
		central_line_x = self.perspective_point_x
		spacing = self.V_LINES_SPACING * self.width
		offset =  index - 0.5
		line_x = central_line_x + offset*spacing +self.current_offset_x
		return line_x

	# Get y by index
	def get_line_y_by_index(self, index):
		spacing_y = self.H_LINES_SPACING*self.height
		line_y = index*spacing_y-self.current_offset_y
		return line_y

	# Getting Tile coordinates
	def get_tile_coordinates(self,ti_x,ti_y):
		ti_y = ti_y - self.current_y_loop
		x = self.get_line_x_by_index(ti_x)
		y = self.get_line_y_by_index(ti_y)
		return x,y
		
	# Start Game Function on press
	def on_menu_button_pressed(self):
		print('Clicked')
		self.reset_game()
		self.is_game_started = True
		self.menu_widget.opacity = 0

	def reset_game(self):
		self.current_offset_y = 0
		self.current_y_loop = 0
		self.current_speed_x = 0
		self.current_offset_x = 0
		self.tiles_coordinates = []
		self.pre_fill_tiles_coordinates()
		self.generate_tiles_coordinates()
		self.state_game_over = False

# Define app name
class SimpleGameApp(App):
	pass

# Run the app
SimpleGameApp().run()


