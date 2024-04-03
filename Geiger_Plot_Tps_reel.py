#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 10:29:08 2024

@author: Jonas Forlot Modifications Compteur Geiger 2024 Cédric Vanden Driessche puis C. Bellessort
Dernière mofif : détection du port Arduino sur nom du périphérique plutôt que sur le nom du port
Tracé du diagramme en "temps réel"
Ajout des données statistiques sur le graph
Tracé de la gaussienne de même moyenne et de même écart-type
"""

# Importation des modules
import serial
import serial.tools.list_ports   # pour la communication avec le port série
import time  # gestion du temps
import matplotlib.pyplot as plt  # pour le tracé de graphe
from matplotlib import animation  # pour la figure animée
from math import e, pi
from statistics import mean, stdev, pstdev

# initialisation des listes
liste_temps_mesure = []  # liste pour stocker le temps"brut"
liste_temps = []  # liste pour stocker les valeurs de temps en partant de t=0
liste_impulsion = []  # liste pour stocker les impulsions
liste_duree = []

t_acquisition = 3600  # Durée totale de l'acquisition en secondes
cps_total = 0  # Nombre total de détections
N = 0  # Nombre de mesures


def recup_port_Arduino():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p.description)
        if "Arduino Uno" or "ttyACM0" in p.description or "ttyACM1" in p.description or "ttyACM2" in p.description:  # On cherche dans la description le nom de la carte "Arduino Uno"
            mData = serial.Serial(p.device, 9600)
    print(mData.is_open)
    print(mData.name)
    return mData


def gauss(m, s, c):
    return 1 / (s * (2 * pi)**0.5)*e**(-0.5 * ((c-m) / s)**2)


Titre = input("Nom de l'échantillon testé (titre du graphique) : ")
Titre = Titre + " - Coups par fenêtre de 10 s"
t0 = time.time()
Data = recup_port_Arduino()

while N < int(t_acquisition / 10):
    plt.clf()
    ligne1 = Data.readline()
    liste_données = ligne1.strip().split()

    if len(liste_données) != 0:
        liste_impulsion.append(int(liste_données[3].decode()))
        liste_temps.append(int(time.time()-t0))
        cps_total = cps_total + liste_impulsion[-1]
        N = N + 1
    m = min(liste_impulsion)
    M = max(liste_impulsion)
    print("t=" + str(liste_temps[-1]))
    if len(liste_impulsion) > 1:
        cps_moy = mean(liste_impulsion)
        cps_ecartype = stdev(liste_impulsion)
        cps_pecartype = pstdev(liste_impulsion)
        if cps_ecartype != 0:
            x = [m + i * (M - m) / 500 for i in range(501)]
            y = [N * gauss(cps_moy, cps_pecartype, val) for val in x]
            plt.plot(x, y, color="red")
            plt.text(0.7, 0.83, r"$cps_{total}=$"+f"{cps_total:.0f}",
                     transform=plt.gcf().transFigure, fontsize="large")
            plt.text(0.7, 0.80, r"$N=$"+f"{N:.0f}",
                     transform=plt.gcf().transFigure, fontsize="large")
            plt.text(0.7, 0.77, r"$\overline {cps_{10s}}=$"+f"{cps_moy:.1f}",
                     transform=plt.gcf().transFigure, fontsize="large")
            plt.text(0.7, 0.74, r"$\sigma_{n-1}=$"+f"{cps_ecartype:.2e}",
                     transform=plt.gcf().transFigure, fontsize="large")
            plt.text(0.7, 0.71, r"$\sigma_{n}=$"+f"{cps_pecartype:.2e}",
                     transform=plt.gcf().transFigure, fontsize="large")

    plt.title(Titre)
    plt.xlabel(r'$Coups_{10s}$')
    plt.ylabel('Nombre de coups')
    plt.hist(liste_impulsion, bins=[
             i + 0.5 for i in range(m-1, M+1)], density=False, rwidth=0.8, color="blue")
    plt.pause(0.0001)
plt.show()

# pour arrêter la lecture des données série


"""#Ecriture dans un fichier txt
lines=['N \t duree \n'] #première ligne du fichier txt
for i in range (len (liste_impulsion)):
    line = (str(liste_impulsion[i])+'\t'+ str(liste_duree[i])+'\n')
    lines.append(line)

fichier = open('data_arduino2.txt', 'w').writelines(lines) # création d'un nouveau fichier texte
"""
