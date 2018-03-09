# -*- coding: utf-8 -*-

class CellHex:
	def __init__(self, x_centre, y_centre, sommets):
		self.centre = (x_centre, y_centre)
		self.sommets = sommets
		self.hum = 0
		self.estGlace_b = False

	def getHum(self):
		return self.hum

	def setHum(self, hum):
		self.hum = hum

	def estGlace(self):
		return self.estGlace_b

	def setGlace(self):
		self.estGlace_b = True