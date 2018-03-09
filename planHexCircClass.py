# -*- coding: utf-8 -*-

from cellHexClass import *
import math

class PlanHex:
	def __init__(self, diamHex, arete, x_centre, y_centre):

		rac3 = math.sqrt(3)

		self.a = arete

		self.diamHex = diamHex
		self.diamPx = rac3*arete*diamHex
		self.rad = rac3*arete*diamHex/2
		self.repere = dict()
		self.voisins = dict()
		self.voisins_nr = dict()
		self.bord = []
		self.recep = []
		self.glace = []
		self.evol = []

		# les conditions sur i et j sont issus de la résolution de d >= sqrt((rac3*a*x)**2 + (rac3*a*y)**2 - 3*a*a*x*y)
		for j in range(-int((2*self.rad)/(3*self.a)), int((2*self.rad)/(3*self.a)) + 1):
		    for i in range(int((j - math.sqrt(((4*self.rad*self.rad)/(3*self.a*self.a)) - 3*j*j))/2), int((j + math.sqrt(((4*self.rad*self.rad)/(3*self.a*self.a)) - 3*j*j))/2) + 1):
		       	xc = x_centre + j*self.a*3/2
		       	yc = y_centre +((rac3*j/2) - i*rac3)*self.a
		       	sommets = [(xc + self.a, yc), (xc + self.a/2, yc + self.a*rac3/2), (xc - self.a/2, yc + self.a*rac3/2), (xc - self.a, yc), (xc - self.a/2, yc - self.a*rac3/2), (xc + self.a/2, yc - self.a*rac3/2)]
		       	self.repere[(i,j)] = CellHex(xc, yc, sommets)
		       	if abs(self.distanceAuCentre((i,j)) - self.rad) < rac3*self.a:
		       		self.bord.append((i,j))
		       	else:
		       		self.evol.append((i,j))
		for (i,j) in self.repere:
			self.voisins[(i,j)] = self.genererVoisins((i,j))
			self.voisins_nr[(i,j)] = self.genererVoisinsNR((i,j))

	def distanceAuCentre(self, (x, y)):
		#(x,y) : coordonnees du centre d'un hex

		return math.sqrt(3*self.a*self.a*(x**2 + y**2 - x*y))

	def genererVoisins(self, (i,j)):
		v_tab = []
		if (i+1,j) in self.repere:
			v_tab.append((i+1,j))
		if (i+1,j+1) in self.repere:
			v_tab.append((i+1,j+1))
		if (i,j+1) in self.repere:
			v_tab.append((i,j+1))
		if (i-1,j) in self.repere:
			v_tab.append((i-1,j))
		if (i-1,j-1) in self.repere:
			v_tab.append((i-1,j-1))
		if (i,j-1) in self.repere:
			v_tab.append((i,j-1))

		return v_tab

	def renvoyerVoisins(self, (i,j)):
		return self.voisins[(i,j)]

	def genererVoisinsNR(self, (i,j)):
		v_tab = self.voisins[(i,j)]
		v_nr_tab = []
		for (i,j) in v_tab:
			if (i,j) not in self.recep:
				v_nr_tab.append((i,j))
		return v_nr_tab

	def renvoyerVoisinsNR(self, (i,j)):
		return self.voisins_nr[(i,j)]

	def glacer(self, (i,j)):
		self.repere[(i,j)].setGlace()
		if (i,j) not in self.glace:
			self.glace.append((i,j))
			self.evol.remove((i,j))
		v_tab = self.voisins[(i,j)]
		for (u,v) in v_tab:
			if (u,v) not in self.recep:
				self.recep.append((u,v))
		for (u,v) in self.repere:
			self.voisins_nr[(u,v)] = self.genererVoisinsNR((u,v))