# -*- coding: utf-8 -*-

import Tkinter as tk
from planHexCircClass import *
import math
from time import clock

rac3 = math.sqrt(3)

#### Parametres :

hum_bg = 0.7 # humidite en condition initiale

# hum_tab = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

seuilHum = 1

seuilChute_tab = [100, 200, 300, 400, 500]
seuilChuteMax = seuilChute_tab[-1]

# T = -15

D_T_tab = dict()
D_T_tab[-40] = 0.204
D_T_tab[-30] = 0.211
D_T_tab[-20] = 0.198
D_T_tab[-10] = 0.202

# D = D_T_tab[T] #coeff de diffusion, en cm**2/s
a = 5 #arete d'un hexagone, en pixel
diamHex = 51 #diametre du cercle délimitant l'étude, en nombre d'hexagone (il y a nbHexDiam hexagones sur le diametre vertical). Entier impair car cercle centré sur le centre d'un hex


diam = rac3*a*diamHex
rad = rac3*a*diamHex/2

margeBord = 10
widthFen = 2*margeBord + diam
heightFen = 2*margeBord + diam
h = 2*a #pas d'echantillonnage : distance entre deux centres d'hexagones

#### Fonctions

def tracerHex(canv, p):
    for (i,j) in p.repere:
    	if p.repere[(i,j)].estGlace():
    		canv.create_polygon(p.repere[(i,j)].sommets, fill='black', outline='grey')
    	else:
    		canv.create_polygon(p.repere[(i,j)].sommets, fill='white', outline='grey')


def tracerCercle(canv,x,y,rad):
    canv.create_oval(x-rad,y-rad,x+rad,y+rad,width=1)


def cristallise((i,j), p):
	global nb_crist
	p.glacer((i,j))
	nb_crist+=1


def evolution(p):
	hum_tmp_d = dict()
	crist = []

	for (i,j) in p.evol:
		hum_tmp = 0
		v_nr_tab = p.renvoyerVoisinsNR((i,j))

		for (u,v) in v_nr_tab:
			hum_tmp += p.repere[(u,v)].getHum()

		if (i,j) not in p.recep:
			hum_tmp-=8*p.repere[(i,j)].getHum()

		hum_tmp = hum_tmp*(2*D/(3*h*h)) + p.repere[(i,j)].getHum() + (2*D/(h*h))*(hum_bg)
		hum_tmp_d[(i,j)] = hum_tmp

		if hum_tmp>=seuilHum and (i,j) in p.recep:
			crist.append((i,j))

	for (i,j) in hum_tmp_d:
		p.repere[(i,j)].setHum(hum_tmp_d[(i,j)])

	for (i,j) in crist:
		cristallise((i,j), p)
		# print("oooooooooooooooooooooooooooooooook")


for T in D_T_tab:

	D = D_T_tab[T]

	k_chute = 0
	seuilChute = seuilChute_tab[k_chute]

	t_gen_1 = clock()
	plan = PlanHex(diamHex, a, widthFen//2, heightFen//2)
	t_gen_2 = clock()

	nb_crist = 0

	for (i,j) in plan.repere:
		plan.repere[(i,j)].setHum(hum_bg)

	cristallise((0, 0), plan)
	plan.repere[(0,0)].setHum(1)

	k = 0
	while nb_crist < seuilChuteMax:
		evolution(plan)
		k+=1
		if nb_crist > seuilChute:
			fen = tk.Tk()
			can = tk.Canvas(fen, width=widthFen, height=heightFen, bg='white')
			can.pack()
			tracerCercle(can, widthFen//2, heightFen//2, rad)

			t_aff_1 = clock()
			tracerHex(can, plan)
			t_aff_2 = clock()

			# print(diam, widthFen, heightFen)

			print("Generation : " + str(t_gen_2-t_gen_1))
			print("Affichage : " + str(t_aff_2-t_aff_1))

			# fen.mainloop()


			titre = "h" + str(int(10*hum_bg)) + "d" + str(diamHex) + "t" + str(abs(T)) + "s" + str(abs(seuilChute)) + ".ps"
			can.update()
			can.postscript(file=titre, colormode='color')

			k_chute+=1
			if k_chute < 5:
				seuilChute = seuilChute_tab[k_chute]

		print(k, nb_crist, hum_bg, T, seuilChute, k_chute)

	fen = tk.Tk()
	can = tk.Canvas(fen, width=widthFen, height=heightFen, bg='white')
	can.pack()
	tracerCercle(can, widthFen//2, heightFen//2, rad)

	t_aff_1 = clock()
	tracerHex(can, plan)
	t_aff_2 = clock()

	# print(diam, widthFen, heightFen)

	print("Generation : " + str(t_gen_2-t_gen_1))
	print("Affichage : " + str(t_aff_2-t_aff_1))

	# fen.mainloop()


	titre = "h" + str(int(10*hum_bg)) + "d" + str(diamHex) + "t" + str(abs(T)) + "s" + str(abs(seuilChute)) + ".ps"
	can.update()
	can.postscript(file=titre, colormode='color')
	fen.quit()
	fen.destroy()