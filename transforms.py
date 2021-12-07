
# This function will transform all lines to 3D perspective or 2D
def transform(self,x,y):
	#return self.transform_2D(x,y)
	return self.transform_perspective(x,y)

# Transform to 2D
def transform_2D(self,x,y):
	return x,y


def transform_perspective(self,x,y):
	# transform y
	lin_y = y * self.perspective_point_y / self.height
	if lin_y > self.perspective_point_y:
		lin_y = self.perspective_point_y

	diff_x = x-self.perspective_point_x
	diff_y = self.perspective_point_y-lin_y
	factor_y = diff_y/self.perspective_point_y
	factor_y = pow(factor_y, 4)
	# transform x
	tr_x = self.perspective_point_x + diff_x * factor_y
	tr_y = self.perspective_point_y - factor_y*self.perspective_point_y
	return int(tr_x),int(tr_y)

