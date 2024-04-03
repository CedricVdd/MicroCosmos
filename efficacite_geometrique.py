# Script de depart Scilab en 2 dimensions Jean Christophe Pelhate
#reecriture et modification Scilab en 3 dimensions  Cedric Vanden Driessche 2016
# Adaptation python Cedric Vanden Driessche 2024

import numpy as np

l=7.5 #demi-largeur du scintillateur
L=14.5 #demi-longueur du scintillateur
#d=20 //distance entre les 2pm
muon=0 #initialisation du nombre de muons détectés
somtau=0
tau=[]
phi=0
theta=0
beta=0
omega=0
omegad=0
X=0

print("calcul du facteur de correction géomètrique")

d=float(input("distance inter raquettes ?"))

omegad=input("inclinaison des raquettes en degre ?")

omega=(float(omegad)/360)*(2*np.pi)

M=int(input("combien d expériences ?"))
N=int(input("combien de tirages par expérience ?"))

for k in range(M):
    acc=0
    muon=0

    for i in range(1,N):
                
        #les deux lignes suivantes simulent les coordonnées d'arrivées d'un muon sur le scintillateur du haut (tirage uniforme) 
        alpha=np.random.uniform(-l,l)
        beta=np.random.uniform(-L,L)
        x= alpha*np.cos(omega)
        y= beta
        z= alpha*np.sin(omega)
        
        #loi de distribution de l angle zénithal en cos**2
        u=np.random.uniform(0,1)
        theta=np.arccos(u**(0.25))
        #tirage aléatoire uniforme de 0 à 2 pi sur l'angle longitudinal
        phi=np.random.uniform(0,2*np.pi)
              
        #position du muon sur le 2eme scintillateur
        X=np.sin(theta)*np.cos(phi)*np.sin(omega)-np.cos(theta)*np.cos(omega)
        
        x2=alpha*np.cos(omega)+(d*np.sin(theta)*np.cos(phi))/(X)
        y2=(d*np.sin(theta)*np.sin(phi)+beta*X)/(X) 
        z2=alpha*np.sin(omega)+(d*np.cos(theta))/(X)
        
        
        #calcul des coordonnées en x de la 2eme raquette
        xbord1= d*np.sin(omega)-l*np.cos(omega)
        xbord2= d*np.sin(omega)+l*np.cos(omega)
        
        if xbord1<xbord2 :
            xmin=xbord1
            xmax=xbord2
        else :
            xmin=xbord2
            xmax=xbord1
            
        #test pour savoir si le muon est arrivé sur la deuxième raquette , x et z dependantes donc seules les coordonnees de x sont necessaires            
        if (xmin <= x2) and (x2 <= xmax) and (-L <= y2 ) and (y2 <= L):
            muon=muon+1


    #rapport muons détecté par les 2 scintillateurs sur le nombre total de muons qui a satisafait la condition de distribtion
    acc=(muon/N)*100 

    somtau=somtau+acc

    print(acc)

    tau.append(acc)

moytau=somtau/M

#Calcul de l ecart quadratique
quad=0
ecarttau=0

for j in range(M):
    ecarttau=ecarttau +(tau[j-1]-moytau)**2    


quad=np.sqrt(ecarttau)/M


# affichage de la moyenne et de l'incertitude
print("taux =",moytau,"%","+/-",quad,"%")
