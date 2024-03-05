from tkinter import*
from math import*
import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
import pandas as pd
import pyrolite
from pyrolite.plot import pyroplot
from pyrolite.util.plot.style import color_ternary_polygons_by_centroid
from pyrolite.plot.templates import QAP, TAS,FeldsparTernary
from pyrolite.util.synthetic import normal_frame
import mpltern
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import csv 
from tkinter.filedialog import asksaveasfile, asksaveasfilename, askopenfilename
import webbrowser
from tkinter import ttk
import fitz
import unittest

Liste_des_elements = ["SiO2","Al2O3", "Fe2O3", "FeO", "MgO", "CaO", "Na2O", "K2O", "TiO2", "P2O5", "MnO"]

root = tk.Tk()
root.title("CIPoWer")
root.geometry("1920x1000")
logo = PhotoImage(file = 'Data\\CIPoWer_logo.png')
root.iconphoto(False, logo, logo)
#root.resizable(width=False, height=False)
# CADRE POUR LA FENETRE
cadre_titre = tk.Frame(root)
cadre_titre.pack(side=TOP)
cadre = tk.Frame(root)
cadre.pack(side=tk.LEFT)
label_width = 15 
#ENTREE DES VALEURS PAR L'UTILISATEUR
titrewtSiO2=tk.Label(cadre,text="wt% SiO2 :",width=label_width)
titrewtSiO2.grid(row=2,column=1)
wtSiO2=tk.Entry(cadre,width=label_width)
wtSiO2.grid(row=2,column=2)
#Al2O3
titrewtAl2O3=tk.Label(cadre,text="wt% Al2O3 :",width=label_width)
titrewtAl2O3.grid(row=3,column=1)
wtAl2O3=tk.Entry(cadre,width=label_width)
wtAl2O3.grid(row=3,column=2)
#Fe2O3
titrewtFe2O3=tk.Label(cadre,text="wt% Fe2O3 :",width=label_width)
titrewtFe2O3.grid(row=4,column=1)
wtFe2O3=tk.Entry(cadre,width=label_width)
wtFe2O3.grid(row=4,column=2)
#FeO
titrewtFeO=tk.Label(cadre,text="wt% FeO :",width=label_width)
titrewtFeO.grid(row=5,column=1)
wtFeO=tk.Entry(cadre,width=label_width)
wtFeO.grid(row=5,column=2)
#MgO
titrewtMgO=tk.Label(cadre,text="wt% MgO :",width=label_width)
titrewtMgO.grid(row=6,column=1)
wtMgO=tk.Entry(cadre,width=label_width)
wtMgO.grid(row=6,column=2)
#CaO
titrewtCaO=tk.Label(cadre,text="wt% CaO :",width=label_width)
titrewtCaO.grid(row=7,column=1)
wtCaO=tk.Entry(cadre,width=label_width)
wtCaO.grid(row=7,column=2)
#Na2O
titrewtNa2O=tk.Label(cadre,text="wt% Na2O :")
titrewtNa2O.grid(row=8,column=1)
wtNa2O=tk.Entry(cadre,width=label_width)
wtNa2O.grid(row=8,column=2)
#K2O
titrewtK2O=tk.Label(cadre,text="wt% K2O :",width=label_width)
titrewtK2O.grid(row=9,column=1)
wtK2O=tk.Entry(cadre,width=label_width)
wtK2O.grid(row=9,column=2)
#TiO2
titrewtTiO2=tk.Label(cadre,text="wt% TiO2 :",width=label_width)
titrewtTiO2.grid(row=10,column=1)
wtTiO2=tk.Entry(cadre,width=label_width)
wtTiO2.grid(row=10,column=2)
#P2O5
titrewtP2O5=tk.Label(cadre,text="wt% P2O5 :",width=label_width)
titrewtP2O5.grid(row=11,column=1)
wtP2O5=tk.Entry(cadre,width=label_width)
wtP2O5.grid(row=11,column=2)
#MnO
titrewtMnO=tk.Label(cadre,text="wt% MnO :")
titrewtMnO.grid(row=12,column=1)
wtMnO=tk.Entry(cadre,width=label_width)
wtMnO.grid(row=12,column=2)

ListeCasesElements = [wtSiO2, wtAl2O3, wtFe2O3, wtFeO, wtMgO, wtCaO, wtNa2O, wtK2O, wtTiO2, wtP2O5, wtMnO]
diagramme_est_dessine = False

affichage_photo = Canvas(root, width=300, height=200) #création de l'espace d'affichage de la photo
photo = PhotoImage(file='Data\\images\\image_rien.png')
Image_Affichee = affichage_photo.create_image(0,0, image=photo, anchor='nw') # Affichage de l'image
affichage_photo.place(x=300, y=100) #placer l'image a droite du tableau
affichage_photo.pack(expand=True, side=LEFT)

def calcul_norme(PoidsOxyd) : 
  PoidsMol = [60,102,160,72,40,56,62,94,80,142,71]
  PropMol = []
  for i in range(len(PoidsMol)) : 
    N = PoidsOxyd[i]/PoidsMol[i]*1000
    PropMol.append(round(N))
  Mineraux = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

  # MnO+FeO
  PropMol[3] = PropMol[3] + PropMol[10]
  del PropMol[10]



  # formation apatite
  i=0
  while PropMol[9]!=0 and PropMol[5] >= 3.3 :
    i=i+1
    PropMol[9]=PropMol[9]-1
    PropMol[5]=PropMol[5]-3.3
  Mineraux[0]=i

  # formation ilménite
  i=0
  while PropMol[8]!=0 and PropMol[3] != 0 :
    i=i+1
    PropMol[8]=PropMol[8]-1
    PropMol[3]=PropMol[3]-1
    
  Mineraux[1]=i

  #Prise d'information dans le cas de la formation de Leucite a partir de l'Orthose
  # L3 = [SiO2 , K2O ]
  L3 = [ PropMol[0] , PropMol[7] ]

  # formation Orthose
  i=0
  while PropMol[1] > 0 and PropMol[7] > 0 :
    i=i+1
    PropMol[0]=PropMol[0]-6
    PropMol[1]=PropMol[1]-1
    PropMol[7]=PropMol[7]-1

  Mineraux[2]=i

  # prise d'information dans le cas de la 3e passe
  # L2 = [ SiO2 , Na2O ]
  L2 = [ PropMol[0] , PropMol[6] ]

  # formation albite
  i=0
  while PropMol[1] != 0 and PropMol[6] != 0 :
    i=i+1
    PropMol[0]=PropMol[0]-6
    PropMol[1]=PropMol[1]-1
    PropMol[6]=PropMol[6]-1
  Mineraux[5]=i


  # formation anorthite
  i=0
  while PropMol[1] > 0 and PropMol[5] > 0 :
    i=i+1
    PropMol[0]=PropMol[0]-2
    PropMol[1]=PropMol[1]-1
    PropMol[5]=PropMol[5]-1
 
  Mineraux[7]=i

  # formation corindon
  i=0
  while PropMol[1]>0 :
    i=i+1
    PropMol[1]=PropMol[1]-1
  Mineraux[8]=i

  # formation aegyrine
  i=0
  while PropMol[6]!=0 and PropMol[2]!=0 :
    i=i+1
    PropMol[6]=PropMol[6]-1
    PropMol[0]=PropMol[0]-1
    PropMol[2]=PropMol[2]-1
  Mineraux[9]=i

  # formation magnetite
  i=0
  while PropMol[2]!=0 and PropMol[3]!=0 :
    i=i+1
    PropMol[3]=PropMol[3]-1
    PropMol[2]=PropMol[2]-1
  Mineraux[10]=i

  # formation hematite
  i=0
  while PropMol[2]!=0 :
    i += 1
    PropMol[2]=PropMol[2]-1
  Mineraux[11]=i

  # formation Diopside WO
  i = 0
  MgFe = PropMol[3] + PropMol[4]
  while MgFe > 0 and PropMol[5] > 0 :
    PropMol[3] -= PropMol[3]/MgFe
    PropMol[4] -= PropMol[4]/MgFe
    PropMol[5] -= 1
    PropMol[0] -= 1
    MgFe -= 1
    i=i+1
  Mineraux[12]=i
  Mineraux[13]=i*(PropMol[4]/MgFe)
  Mineraux[14]=i*(PropMol[3]/MgFe)

  # formation wollastonite
  i = 0
  while PropMol[5]>0 :
    PropMol[5] -= 1
    PropMol[0] -= 1
    i+=1
  Mineraux[15] = i

  # formation Larnite

  # prise d'information dans le cas de la 2e passe
  # quantité de SiO, FeO, et MgO
  # L1 = [ SiO , FeO , MgO ]

  L1 = [PropMol[0],PropMol[3],PropMol[4]]

  # formation hypersthène Mg
  i=0
  while PropMol[4] > 0 :
    i+=1
    PropMol[4] -= 1
    PropMol[0] -= 1
  Mineraux[17] = i

  # formation hypersthène Fe
  i=0
  while PropMol[3] > 0 :
    i+=1
    PropMol[3] -= 1
    PropMol[0] -= 1
  Mineraux[18] = i

  # formation silice
  if PropMol[0] >= 0 :
    Mineraux[21] = PropMol[0]
  else :

    #1ere passe
    #x+y= SiO2 dispo
    #x+2y=MnO_FeO_3+MgO_1
    MgFe = L1[1] + L1[2]
    y = MgFe - L1[0]
    x = MgFe - 2*y


    if x>=0 and y>0 :

      Mineraux[17] = x * (L1[1]/(L1[2]+L1[1]))
      Mineraux[18] = x * (L1[2]/(L1[2]+L1[1]))
      Mineraux[19] = y * (L1[1]/(L1[2]+L1[1]))
      Mineraux[20] = y * (L1[2]/(L1[2]+L1[1]))

    else :
      #deficit de silice toujours présent -> formation d'olivine uniquement
      Mineraux[17] = 0
      Mineraux[18] = 0
      Mineraux[19] = y * (PropMol[3]/(PropMol[3]+PropMol[4]))
      Mineraux[20] = y * (PropMol[4]/(PropMol[3]+PropMol[4]))
      deficitsilice = L1[0] - y

  #deficit de silice persistant apres la formation de l'Olivine =  formation de nephiline
      if deficitsilice < 0 :
          deficit=abs(deficitsilice)
          y = deficit / 4
          x = L2[1]+deficit/6-1/3*y
          if x>=0 and y>=0 :
            Mineraux[5] = x
            Mineraux[6] = y

          else :

            if x<0 or y<0 :

              deficitsilice = deficitsilice + Mineraux[5] * 6- 2 * y
              Mineraux[5] = 0
              Mineraux[6] = y # 0% albite détruite, 100% nephiline formée

              # deficit de silice persistant apres la formation de la nephiline =  formation de leucite

              deficit=abs(deficitsilice)
              y = deficit/2
              x = L3[1] + deficit/6 - 2/3 * y

              if x>=0 and y>=0 :
                Mineraux[2] = x
                Mineraux[3] = y

              else :

                if x<0 or y<0 :

                  deficitsilice = deficitsilice + Mineraux[2] * 6 - 4 * y
                  Mineraux[2] = 0
                  Mineraux[3] = y

                  # deficit de silice persistant apres la formation de la leucite, derniere passe avec formation de la kalsilite

                  deficit=abs(deficitsilice)
                  y= deficit/2
                  x= L3[1] + deficit/4 - y/2

                  Mineraux[3] = x
                  Mineraux[4] = y




  PoidsMolMineraux = [336,152,556,436,316,524,284,278,102,462,232,160,116,100,132,116,172,100,132,140,204,60]
  PropMin = []
  for i in range(len(PoidsMolMineraux)) :
    PropMin.append((Mineraux[i] * PoidsMolMineraux[i]) / 1000)


  F = PropMin[6] + PropMin[3] + PropMin[4]

  A = PropMin[2]

  P = PropMin[5] + PropMin[7]

  Q = PropMin[21]

  


  return Q,A,P,F,PropMin

def CIPower():
  def Calcul_Norme():
    global diagramme_est_dessine, ax, canvas, indexphoto, nom_roche, P_prim, PoidsOxyd
    indexphoto = ""
    PoidsOxyd = [
        float(wtSiO2.get()), 
        float(wtAl2O3.get()), 
        float(wtFe2O3.get()), 
        float(wtFeO.get()), 
        float(wtMgO.get()), 
        float(wtCaO.get()), 
        float(wtNa2O.get()), 
        float(wtK2O.get()), 
        float(wtTiO2.get()), 
        float(wtP2O5.get()), 
        float(wtMnO.get())
    ]

    Q,A,P,F,PropMin = calcul_norme(PoidsOxyd)

    CalcoAlcalin =   PoidsOxyd[6] + PoidsOxyd[7]
    Neph_Leuc = [PropMin[6], PropMin[3]]
    Str_Neph_Leuc = ["Néphéline", "Leucite"]
    print('SiO2 =', PoidsOxyd[0], '| Na2O + K2O =', CalcoAlcalin)
    print(Q, A, P, F)
    pourcApatite.configure(text=PropMin[0])
    pourcIlmenite.configure(text=PropMin[1])
    pourcOrthose.configure(text=PropMin[2])
    pourcLeucite.configure(text=PropMin[3])
    pourcKalsilite.configure(text=PropMin[4])
    pourcAlbite.configure(text=PropMin[5])
    pourcNepheline.configure(text=PropMin[6])
    pourcAnorthite.configure(text=PropMin[7])
    pourcCorindon.configure(text=PropMin[8])
    pourcAegyrine.configure(text=PropMin[9])
    pourcMagnetite.configure(text=PropMin[10])
    pourcHematite.configure(text=PropMin[11])
    pourcDiopside_Wo.configure(text=PropMin[12])
    pourcDiopside_CEn.configure(text=PropMin[13])
    pourcDiopside_CFs.configure(text=PropMin[14])
    pourcWollastonite.configure(text=PropMin[15])
    pourcLarnite.configure(text=PropMin[16])
    pourcHypersthene.configure(text=PropMin[17]+PropMin[18])
    pourcOlivine_Fo.configure(text=PropMin[19])
    pourcOlivine_Fa.configure(text=PropMin[20])
    pourcQuartz.configure(text=PropMin[21])
    pourcTotal_valeur = 0
    for i in range(len(PropMin)):
       pourcTotal_valeur = pourcTotal_valeur + PropMin[i]
    pourcTotal.configure(text=pourcTotal_valeur)
    if roche_volca == True :
        #CONDITION DES ROCHES VOLCANIQUES
      P_prim = 100 * P / (A + P)
      Petit_q = (100*Q)/(Q-(A + P))
      ########################################################$ Quartz Dominant (On rajoute le 0.00000000000001 pour les cas où on a 0 F et 0 Q)
      if Q+.00001 > F :
        if Q < 90 and Q > 60 :
          nom_roche.configure(text="Quartzolite")
          indexphoto = 'Quartzolite'
        ########################################################$
        if Q <= 60 and Q > 20:
          if P_prim <= 10 and P_prim >= 0:
              nom_roche.configure(text="Rhyolite alcaline")
              indexphoto = 'Rhyolite'
          elif P_prim <= 65 and P_prim > 10:
              nom_roche.configure(text="Rhyolite")
              indexphoto = 'Rhyolite'
          elif P_prim <= 90 and P_prim > 65:
              nom_roche.configure(text="Dacite")
              indexphoto = 'Dacite'
          elif P_prim <= 100 and P_prim > 90:
              nom_roche.configure(text="Dacite")
              indexphoto = 'Dacite'
        ########################################################
        elif Q <= 20 and Q > 5:
          if P_prim <= 10 and P_prim >= 0:
              nom_roche.configure(text="Trachyte alcaline et à quartz")
              indexphoto = 'trachyte'
          elif P_prim <= 35 and P_prim >=10:
              nom_roche.configure(text="Trachyte à quartz")
              indexphoto = 'trachyte'
          elif P_prim <= 65 and P_prim > 35:
              nom_roche.configure(text="Latite à quartz")
              indexphoto = 'latite'
          elif P_prim <= 90 and P_prim > 65:
              if PoidsOxyd[0] <= 52 : #Normalement c'est 52 mais on fait 52*1000/60
                  nom_roche.configure(text="Trachybasalte")
                  indexphoto = 'TrachyBasalte'
              elif PoidsOxyd[0] > 52 :
                  nom_roche.configure(text="Trachyandésite")
                  indexphoto = 'TrachyAndesite'
          elif P_prim <= 100 and P_prim > 90:
              if PoidsOxyd[0] <= 52 : #Normalement c'est 52 mais on fait 52*1000/60
                  nom_roche.configure(text="Basalte")
                  indexphoto = 'Basalte'
              elif PoidsOxyd[0] > 52 :
                  nom_roche.configure(text="Andésite")
                  indexphoto = 'Andesite'
        ########################################################
        elif Q <= 5 and Q+1 >= 0:
          if P_prim <= 10 and P_prim >= 0:
              nom_roche.configure(text="Trachyte alcaline")
              indexphoto = 'trachyte'
          elif P_prim <= 35 and P_prim > 10:
              if Petit_q > .2 :
                nom_roche.configure(text="Trachydacite")
                indexphoto = 'trachyte'
              elif Petit_q < .2 :
                nom_roche.configure(text="Trachyte")
                indexphoto = 'trachyte'
          elif P_prim <= 65 and P_prim > 35:
              nom_roche.configure(text="Latite")
              indexphoto = 'latite'
          elif P_prim <= 90 and P_prim > 65:
              if PoidsOxyd[0] <= 52 :
                  if (PoidsOxyd[6]) - 2 >= (PoidsOxyd[7]):
                      nom_roche.configure(text="Hawaiite")
                      print('hawaiite')
                      indexphoto = 'Hawaiite'
                  if (PoidsOxyd[6]) - 2 < (PoidsOxyd[7]):
                      nom_roche.configure(text="Trachybasalte potassique")
                      indexphoto = 'TrachyBasalte'
              if PoidsOxyd[0] > 52 and PoidsOxyd[0] <= 57:
                  if (PoidsOxyd[6]) - 2 >= (PoidsOxyd[7]):
                      nom_roche.configure(text="Mugearite")
                      indexphoto = 'Mugearite'
                  if (PoidsOxyd[6]) - 2 < (PoidsOxyd[7]):
                      nom_roche.configure(text="Shoshonite")
                      indexphoto = 'Shoshonite'
              if PoidsOxyd[0] > 57 :
                  if (PoidsOxyd[6]) - 2 >= (PoidsOxyd[7]):
                      nom_roche.configure(text="Benmoreite")
                      indexphoto = 'Benmoreite'
                  if (PoidsOxyd[6]) - 2 < (PoidsOxyd[7]):
                      nom_roche.configure(text="Latite")
                      indexphoto = 'latite'
          elif P_prim <= 100 and P_prim > 90:
            if PoidsOxyd[0] <= 52 :
              nom_roche.configure(text="Basalte")
              indexphoto = 'Basalte'
              print('basalte')
            elif PoidsOxyd[0] > 52 :
              nom_roche.configure(text="Andésite")
              indexphoto = 'Andesite'
        ########## Bon faut remettre les variables pour que ça fonctionne jsp pq
        if diagramme_est_dessine == True:
          ax.clear()
          canvas.draw()
          canvas.get_tk_widget().destroy()
        diagramme_est_dessine = True
        ax = TAS(add_labels=True, which_model="LeMaitreCombined", fontsize=7,linewidth=0.5,figsize=(6,6), fill=True, alpha = 0.2)
        ValeursTAS = (PoidsOxyd[0], CalcoAlcalin)
        tas = pd.DataFrame(data = ValeursTAS)
        tas.pyroplot.scatter(ax=ax, c="r", s=5000, marker="+", alpha=1, axlabels=False)
        #Ajout de la légende d'après LeMaitre(2004)
        plt.plot([], [], ' ', label=" F : Foidite \n Pc : Picro-Basalte \n Bs : Basalte \n O1 : Andésite Basaltique \n O2 : Andésite \n O3 : Dacite \n S1 : Trachybasalte \n S2 : Trachy-Andésite Basaltique \n S3 : Trachyandésite \n T1 : Trachyte \n T2 : Trachydacite \n R : Rhyolite \n U1 : Basanite - Tephrite \n U2 : Phonotephrite \n U3 : Tephriphonolite \n Ph : Phonolite")
        plt.legend(loc = "upper right", bbox_to_anchor=(1,1),prop={'size': 6})
        canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.RIGHT,  expand=1)
        root.update()
      ################################################### FELDSPATHOIDES DOMINANTS
      elif F > Q+.00001:
        if F <= 10 and F >= 0 :
          if P_prim <= 10 and P_prim >= 0:
            nom_roche.configure(text="Trachyte à feldpsaths alcalins à "+ Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))])
            indexphoto = 'trachyte'
          elif P_prim <= 35 and P_prim >= 10:
            nom_roche.configure(text="Trachyte à "+ Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))])
            indexphoto = 'trachyte'
          elif P_prim <= 65 and P_prim >= 35:
            nom_roche.configure(text="Latite à "+ Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))])
            indexphoto = 'latite'
          elif P_prim <= 100 and P_prim >= 65:
            if PoidsOxyd[0] <= 52 :
              nom_roche.configure(text="Basalte")
              indexphoto = 'Basalte'
            elif PoidsOxyd[0] > 52 :
              nom_roche.configure(text="Andésite")
              indexphoto = 'Andesite'
      ############################################################# * Correspond au fait que la roche dépends du color index
        if F <= 60 and F > 10:
          pourc_olivine = PropMin[21] + PropMin[20]
          if P_prim <= 10 and P_prim >= 0:
            nom_roche.configure(text="Phonolite")
            indexphoto = 'Phonolite'
          elif P_prim <= 50 and P_prim >= 10:
            nom_roche.configure(text="Tephriphonolite")
            indexphoto = 'Tephriphonolite'
          elif P_prim <= 90 and P_prim >= 50:
              if pourc_olivine <= 10 :
                nom_roche.configure(text="Phonotephrite")
                indexphoto = 'Tephriphonolite'
              if pourc_olivine > 10 :
                nom_roche.configure(text="Phonobasanite")
                indexphoto = 'Phonolite'
          elif P_prim <= 100 and P_prim >= 90:
              if pourc_olivine <= 10 :
                nom_roche.configure(text="Tephrite")
                indexphoto = 'Tephrite'
              elif pourc_olivine > 10 :
                nom_roche.configure(text="Basanite")
                indexphoto = 'basanite'
        ########################################################
        elif F <= 90 and F > 60:
          Str_Neph_Leuc = ["Néphélite", "Leucitite"]
          if P_prim <= 50 and P_prim >= 0:
            nom_roche.configure(text=Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))]+ "Phonolitique")
            indexphoto = 'Phonolite'
          elif P_prim <= 50 and P_prim >= 10:
            nom_roche.configure(text=Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))]+ "Tephritique")
            indexphoto = 'Tephrite'
        ########################################################
        elif F <= 100 and F > 90:
          nom_roche.configure(text="Foïdite")
          indexphoto = 'Foïdite'
        #######################################################
        if diagramme_est_dessine == True:
          ax.clear()
          canvas.draw()
          canvas.get_tk_widget().destroy()
        diagramme_est_dessine = True
        ax = TAS(add_labels=True, which_model="LeMaitreCombined", fontsize=7,linewidth=0.5,figsize=(6,6), fill=True, alpha = 0.2)
        ValeursTAS = (PoidsOxyd[0], CalcoAlcalin)
        tas = pd.DataFrame(data = ValeursTAS)
        tas.pyroplot.scatter(ax=ax, c="r", s=5000, marker="+", alpha=1, axlabels=False)
        #Ajout de la légende d'après LeMaitre(2004)
        plt.plot([], [], ' ', label=" F : Foidite \n Pc : Picro-Basalte \n Bs : Basalte \n O1 : Andésite Basaltique \n O2 : Andésite \n O3 : Dacite \n S1 : Trachybasalte \n S2 : Trachy-Andésite Basaltique \n S3 : Trachyandésite \n T1 : Trachyte \n T2 : Trachydacite \n R : Rhyolite \n U1 : Basanite - Tephrite \n U2 : Phonotephrite \n U3 : Tephriphonolite \n Ph : Phonolite")
        plt.legend(loc = "upper right", bbox_to_anchor=(1,1),prop={'size': 6})
        canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=0)
        root.update()
      #GENERER LE DIAGRAMME DE STREKEISEN (Roches plutoniques)
    elif roche_pluto == True :
      #CONDITION DES ROCHES PLUTONIQUES
      P_prim = 100 * P / (A + P)
      if Q+0.00001 > F :
      ######################################################## Quartz Dominant (On rajoute le 0.00000000000001 pour les cas où on a 0 F et 0 Q)
        if Q <= 60 and Q > 20:
          if P_prim <= 10 and P_prim >= 0:
            nom_roche.configure(text="Granite à feldpsaths alcalins")
            indexphoto = 'Granite_a_fds_alcalin'
          elif P_prim <= 65 and P_prim >= 10:
            nom_roche.configure(text="Granite")
            indexphoto = 'Granite_a_fds_alcalin'
          elif P_prim <= 90 and P_prim >= 65:
            nom_roche.configure(text="Granidiorite")
            indexphoto = 'Granidiorite'
          elif P_prim <= 100 and P_prim >= 90:
            nom_roche.configure(text="Tonalite")
            indexphoto = 'Tonalite'
        ########################################################
        elif Q <= 20 and Q > 5:
          if P_prim <= 10 and P_prim >= 0:
            nom_roche.configure(text="Syénite à feldpsaths alcalins et à quartz")
            indexphoto = 'Syenite'
          elif P_prim <= 35 and P_prim >= 10:
            nom_roche.configure(text="Syénite à quartz")
            indexphoto = 'Syenite'
          elif P_prim <= 65 and P_prim >= 35:
            nom_roche.configure(text="Monzonite à quartz")
            indexphoto = 'Monzonite'
          elif P_prim <= 90 and P_prim >= 65:
              if PropMin[7] > 50 :
                nom_roche.configure(text="Monzodiorite à quartz")
                indexphoto = 'Monzodiorite'
              elif PropMin[7] <= 50 :
                nom_roche.configure(text="Monzogabbro à quartz")
                indexphoto = 'Monzogabbro'
          elif P_prim <= 100 and P_prim >= 90:
              if PropMin[7] <= 50 :
                nom_roche.configure(text="Diorite à quartz")
                indexphoto = 'Diorite'
              elif PropMin[7] > 50 :
                nom_roche.configure(text="Gabbro à quartz")
                indexphoto = 'gabbro'
      ########################################################
        elif Q <= 5 and Q >= 0 :
          if P_prim <= 10 and P_prim >= 0:
            nom_roche.configure(text="Syénite à feldpsaths alcalins")
            indexphoto = 'Syenite'
          elif P_prim <= 35 and P_prim >= 10:
            nom_roche.configure(text="Syénite")
            indexphoto = 'Syenite'
          elif P_prim <= 65 and P_prim >= 35:
            nom_roche.configure(text="Monzonite")
            indexphoto = 'Monzonite'
          elif P_prim <= 90 and P_prim >= 65:
              if PropMin[7] > 50 :
                nom_roche.configure(text="Monzodiorite")
                indexphoto = 'Monzodiorite'
              elif PropMin[7] <= 50 :
                nom_roche.configure(text="Monzogabbro")
                indexphoto = 'Monzogabbro'
          elif P_prim <= 100 and P_prim >= 90:
              if PropMin[7] > 50 :
                nom_roche.configure(text="Diorite")
                indexphoto = 'Diorite'
              elif PropMin[7] <= 50 :
                nom_roche.configure(text="Gabbro")
                indexphoto = 'gabbro'
        if diagramme_est_dessine == True:
          ax.clear()
          canvas.draw()
          canvas.get_tk_widget().destroy()
        diagramme_est_dessine == True
        ax = QAP(fontsize=5,linewidth=0.5,figsize=(6,6))
        Roche = (Q, A, P)
        df = pd.DataFrame(data=Roche)
        df.pyroplot.scatter(ax=ax, marker = '+',c='r', s = 5000, axlabels=False)
        canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
        root.update()
      elif F > Q+.00001 :
      ######################################################## Feldspathoïdes dominant
        if F <= 10 and Q >= 0 :
          if P_prim <= 10 and P_prim >= 0:
            nom_roche.configure(text="Syénite à feldpsaths alcalins à "+ Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))])
            indexphoto = 'Syenite'
          elif P_prim <= 35 and P_prim >= 10:
            nom_roche.configure(text="Syénite à "+ Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))])
            indexphoto = 'Syenite'
          elif P_prim <= 65 and P_prim >= 35:
            nom_roche.configure(text="Monzonite à "+ Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))])
            indexphoto = 'Monzonite'
          elif P_prim <= 90 and P_prim >= 65:
              if PropMin[7] <= 50 :
                nom_roche.configure(text="Monzodiorite à "+ Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))])
                indexphoto = 'Monzodiorite'
              elif PropMin[7] > 50 :
                nom_roche.configure(text="Monzogabbro à "+ Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))])
                indexphoto = 'Monzogabbro'
          elif P_prim <= 100 and P_prim >= 90:
              if PropMin[7] <= 50 :
                nom_roche.configure(text="Diorite à "+ Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))])
                indexphoto = 'Diorite'
              elif PropMin[7] > 50 :
                nom_roche.configure(text="Gabbro à "+ Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))])
                indexphoto = 'gabbro'
      ############################################################# * Correspond au fait que la roche dépends du color index
        if F <= 60 and F > 10:
          Str_Neph_Leuc = ["Néphélinitique", "Leucitique"]
          if P_prim <= 10 and P_prim >= 0:
            nom_roche.configure(text="*Shokinite - Malignite - Syénite"+ Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))])
            indexphoto = 'Shokinite_Malignite_Syenite'
          elif P_prim <= 50 and P_prim >= 10:
            nom_roche.configure(text="Monzosyénite"+ Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))])
            indexphoto = 'Monzosyenite'
          elif P_prim <= 90 and P_prim >= 50:
              if PropMin[7] <= 50 :
                nom_roche.configure(text="Monzodiorite"+ Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))])
                indexphoto = 'Monzodiorite'
              if PropMin[7] > 50 :
                nom_roche.configure(text="Monzogabbro"+ Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))])
                indexphoto = 'Monzogabbro'
          elif P_prim <= 100 and P_prim >= 90:
              if PropMin[7] <= 50 :
                nom_roche.configure(text="Diorite"+ Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))])
                indexphoto = 'Diorite'
              elif PropMin[7] > 50 :
                nom_roche.configure(text="Gabbro"+ Str_Neph_Leuc[Neph_Leuc.index(max(Neph_Leuc))])
                indexphoto = 'gabbro'
        ########################################################
        elif F <= 100 and F > 60:
          if PropMin[6] > PropMin[3] :
            nom_roche.configure(text="*Melteigite - Ijolite - Urtite")
            indexphoto = 'Ijolite'
          if PropMin[3] > PropMin[6]:
            nom_roche.configure(text="*Missourite - Fergusite - Italite")
            indexphoto = 'Missourite'

        ## On génère les diagramme avec FDLS en haut
        if diagramme_est_dessine == True:
          ax.clear()
          canvas.draw()
          canvas.get_tk_widget().destroy()
        diagramme_est_dessine == True
        ax = plt.subplot(projection="ternary")
        ligne_horizontale = list(range(2))
        ligne_horizontale[0] = [0.1, 0.8, 0.1]
        ligne_horizontale[1] = [0.6, 0.3, 0.1]
        slope = [0, 1, -1]
        for i in range(len(ligne_horizontale)):
            ax.axline(xy1=ligne_horizontale[i], slope=slope, color='k', linewidth=1)
        ligne_droite = [0, .1, .9]
        ligne_droite_stop = [0.6, 0.05, 0.35]
        ax.plot([ligne_droite[0], ligne_droite_stop[0]],[ligne_droite[1], ligne_droite_stop[1]],[ligne_droite[2], ligne_droite_stop[2]],color='k', linewidth=1)
        ligne_droite = [0, .9, .1]
        ligne_droite_stop = [0.6, 0.35, 0.05]
        ax.plot([ligne_droite[0], ligne_droite_stop[0]],[ligne_droite[1], ligne_droite_stop[1]],[ligne_droite[2], ligne_droite_stop[2]],color='k', linewidth=1)
        ligne_droite = [0.1, .45, .45]
        ligne_droite_stop = [0.6, 0.2, 0.2]
        ax.plot([ligne_droite[0], ligne_droite_stop[0]],[ligne_droite[1], ligne_droite_stop[1]],[ligne_droite[2], ligne_droite_stop[2]],color='k', linewidth=1)
        ligne_droite = [0, .35, .65]
        ligne_droite_stop = [0.055, 0.1842 , 0.3158]
        ax.plot([ligne_droite[0], ligne_droite_stop[0]],[ligne_droite[1], ligne_droite_stop[1]],[ligne_droite[2], ligne_droite_stop[2]],color='k', linewidth=1)
        ligne_droite = [0,  .65, .35]
        ligne_droite_stop = [0.055 , 0.3158, 0.1842]
        ax.plot([ligne_droite[0], ligne_droite_stop[0]],[ligne_droite[1], ligne_droite_stop[1]],[ligne_droite[2], ligne_droite_stop[2]],color='k', linewidth=1)
        pc = ax.scatter(F/100, A/100, P/100,marker = '+',c='r', s = 5000)
        ax.set_tlabel("Feldspathoid")
        ax.set_llabel("Alkali Feldspar")
        ax.set_rlabel("Plagioclase")
        canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=0)

        root.update()
    print(P_prim)
    return Q,A,P,F
  def_roche = ""
  def afficher_contenu_pdf(def_roche):
      global scrollbar, label
      def_roche = nom_roche.cget("text")

      # Création des balises pour les roches du fichier
      caractfin = "_"
      balise_debut = "DEBUT_"+def_roche+caractfin
      balise_fin = "FIN_"+def_roche+caractfin

      chemin_pdf = "Data\\fiches_roches.pdf"

      try:
          pdf_doc = fitz.open(chemin_pdf)

          texte_complet = ""
          for page_num in range(pdf_doc.page_count):
              page = pdf_doc[page_num]
              texte_complet += page.get_text("text")

          # Filtrer le texte en fonction du nom de la roche et des balises de début/fin
          texte_filtré = filtrer_texte_par_roche(texte_complet, balise_debut, balise_fin)
          text_widget.config(state=tk.NORMAL)
          text_widget.delete("1.0", tk.END)  # Efface le contenu actuel du Text widget
          text_widget.insert(tk.END, texte_filtré)
          text_widget.config(state=tk.DISABLED)

          # Mettre à jour le widget de défilement vertical
          scrollbar.config(command=text_widget.yview)
          text_widget.config(yscrollcommand=scrollbar.set)
          label.config(text="")

      except FileNotFoundError:
          label.config(text="Erreur : Fichier introuvable.")
      except Exception as e:
          label.config(text=f"Erreur : {str(e)}")

  # Fonction pour filtrer le texte entre les balises
  def filtrer_texte_par_roche(texte_complet, balise_debut, balise_fin):
      # Rechercher les balises de début et de fin pour le nom de la roche
      debut_index = texte_complet.find(balise_debut)
      fin_index = texte_complet.find(balise_fin, debut_index + len(balise_debut))

      # Vérifier si les balises ont été trouvées
      if debut_index != -1 and fin_index != -1:
          texte_filtré = texte_complet[debut_index + len(balise_debut):fin_index]
          return texte_filtré.strip()
      else:
          return "Balises introuvables pour", def_roche
  def Afficher_Photo(indexphoto):
      photo2=PhotoImage(file=f'Data\\images\\{indexphoto}.png')
      affichage_photo.itemconfigure(Image_Affichee, image=photo2)
      affichage_photo.image=photo2
  Calcul_Norme()
  afficher_contenu_pdf(nom_roche)
  Afficher_Photo(indexphoto)



def type_pluto(): #fonction pour que la roche affichée au final soit la roche plutonique
    type2.deselect() #décoche le deuxième choix
    global roche_pluto, roche_volca
    roche_pluto=True
    roche_volca=False
def type_volca(): #fonction pour que la roche affichée au final soit la roche plutonique
    type.deselect() #décoche le deuxième choix
    global roche_pluto, roche_volca
    roche_pluto=False
    roche_volca=True
#TABLEAU RESULTATS

#Titre
sous_titre=tk.Label(cadre, borderwidth=1, text="     % Mineraux virtuels     ")
sous_titre.grid(row=17,column=1)
#Apatite
titreApatite=tk.Label(cadre, text="% Apatite:",width=label_width)
titreApatite.grid(row=18,column=1)
pourcApatite=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcApatite.grid(row=18,column=2)
#Ilmenite
titreIlmenite=tk.Label(cadre, text="% Ilmenite:",width=label_width)
titreIlmenite.grid(row=19,column=1)
pourcIlmenite=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcIlmenite.grid(row=19,column=2)
#Orthose
titreOrthose=tk.Label(cadre, text="% Orthose:",width=label_width)
titreOrthose.grid(row=20,column=1)
pourcOrthose=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcOrthose.grid(row=20,column=2)
#Leucite
titreLeucite=tk.Label(cadre, text="% Leucite:",width=label_width)
titreLeucite.grid(row=21,column=1)
pourcLeucite=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcLeucite.grid(row=21,column=2)
#Kalsilite
titreKalsilite=tk.Label(cadre, text="% Kalsilite:",width=label_width)
titreKalsilite.grid(row=22,column=1)
pourcKalsilite=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcKalsilite.grid(row=22,column=2)
#Albite
titreAlbite=tk.Label(cadre, text="% Albite:",width=label_width)
titreAlbite.grid(row=23,column=1)
pourcAlbite=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcAlbite.grid(row=23,column=2)
#Nepheline
titreNepheline=tk.Label(cadre, text="% Nepheline:",width=label_width)
titreNepheline.grid(row=24,column=1)
pourcNepheline=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcNepheline.grid(row=24,column=2)
#Anorthite
titreAnorthite=tk.Label(cadre, text="% Anorthite:")
titreAnorthite.grid(row=25,column=1)
pourcAnorthite=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcAnorthite.grid(row=25,column=2)
#Corindon
titreCorindon=tk.Label(cadre, text="% Corindon:")
titreCorindon.grid(row=26,column=1)
pourcCorindon=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcCorindon.grid(row=26,column=2)
#Aegyrine
titreAegyrine=tk.Label(cadre, text="% Aegyrine:",width=label_width)
titreAegyrine.grid(row=27,column=1)
pourcAegyrine=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcAegyrine.grid(row=27,column=2)
#Magnetite
titreMagnetite=tk.Label(cadre, text="% Magnetite:")
titreMagnetite.grid(row=28,column=1)
pourcMagnetite=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcMagnetite.grid(row=28,column=2)
#Hematite
titreHematite=tk.Label(cadre, text="% Hematite:")
titreHematite.grid(row=29,column=1)
pourcHematite=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcHematite.grid(row=29,column=2)
#Diopside_Wo
titreDiopside_Wo=tk.Label(cadre, text="% Diopside Wo:",width=label_width)
titreDiopside_Wo.grid(row=30,column=1)
pourcDiopside_Wo=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcDiopside_Wo.grid(row=30,column=2)
#Diopside_CEn
titreDiopside_CEn=tk.Label(cadre, text="% Diopside CEn:",width=label_width)
titreDiopside_CEn.grid(row=31,column=1)
pourcDiopside_CEn=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcDiopside_CEn.grid(row=31,column=2)
#Diopside_CFs
titreDiopside_CFs=tk.Label(cadre, text="% Diopside CFs:",width=label_width)
titreDiopside_CFs.grid(row=32,column=1)
pourcDiopside_CFs=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcDiopside_CFs.grid(row=32,column=2)
#Wollastonite
titreWollastonite=tk.Label(cadre, text="% Wollastonite:",width=label_width)
titreWollastonite.grid(row=33,column=1)
pourcWollastonite=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcWollastonite.grid(row=33,column=2)
#Larnite
titreLarnite=tk.Label(cadre, text="% Larnite:",width=label_width)
titreLarnite.grid(row=34,column=1)
pourcLarnite=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcLarnite.grid(row=34,column=2)
#Hypersthene
titreHypersthene=tk.Label(cadre, text="% Hypersthene:",width=label_width)
titreHypersthene.grid(row=35,column=1)
pourcHypersthene=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcHypersthene.grid(row=35,column=2)
#Olivine_Fo
titreOlivine_Fo=tk.Label(cadre, text="% Olivine Fo:",width=label_width)
titreOlivine_Fo.grid(row=36,column=1)
pourcOlivine_Fo=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcOlivine_Fo.grid(row=36,column=2)
#Olivine_Fa
titreOlivine_Fa=tk.Label(cadre, text="% Olivine Fa:",width=label_width)
titreOlivine_Fa.grid(row=37,column=1)
pourcOlivine_Fa=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcOlivine_Fa.grid(row=37,column=2)
#Quartz
titreQuartz=tk.Label(cadre, text="% Quartz:",width=label_width)
titreQuartz.grid(row=38,column=1)
pourcQuartz=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcQuartz.grid(row=38,column=2)
#Total
titreTotal=tk.Label(cadre, text="% Total:",width=label_width)
titreTotal.grid(row=39,column=1)
pourcTotal=tk.Label(cadre, relief="sunken", borderwidth=2, text="",width=label_width)
pourcTotal.grid(row=39,column=2)
#Nom de la roche
nom_roche = tk.Label(cadre,text="Nom de la roche",width=label_width*2,font=("Arial", 18, "bold", "italic"))
nom_roche.grid(row=0, columnspan=3)

#LISTE DES BOUTONS ET TITRES
bouton_calculs = tk.Button(cadre, text="Commencer", command=CIPower, font=("Arial", 13)) #bouton pour lancer les calculs
bouton_calculs.grid(row=1, column=3, padx=5, pady=5)  # Place le bouton à côté du premier tableau
type = Checkbutton(cadre, text="Plutonique", command=type_pluto, font=("Arial", 13)) #case à cocher pour le type de roche
type.grid(row=1, column=1, padx=5, pady=5) #positionne le bouton au dessus de "démarrer"
type2 = Checkbutton(cadre, text="Volcanique", command=type_volca, font=("Arial", 13)) #deuxième case à cocher pour le type de roche
type2.grid(row=1, column=2, padx=5, pady=5) #positionne le bouton à coté du premier
label_titre = tk.Label(cadre_titre, text="CIPoWer", font=("Georgia", 30, "bold"))
label_titre.grid(row=0, column=0, columnspan=14, pady=10)

# LANCEMENT DE LA BOUCLE PRINCIPALE

###Accessoires 
barremenu=Menu(root)
Fichier=Menu(barremenu,tearoff=0)

#Fichier
barremenu.add_cascade(label="Fichier",menu=Fichier)
menuTypeRoche=Menu(barremenu, tearoff=0)

def ChargerExemple(indexroche): #ON VA ICI FAIRE DES UNITTESTS POUR VOIR SI LE FICHIER CHARGE N'A PAS ETE ALTERE
    if indexroche == 1:
      csv_file_path = 'Data\\Exemples\\Granite.csv'
      #Von Eller 1961 : https://www.persee.fr/doc/sgeol_0080-9020_1961_mon_19_1
    elif indexroche == 2:
      csv_file_path = 'Data\\Exemples\\Basalte.csv'
      #Everard 1997 : https://www.researchgate.net/publication/274712082_Geology_of_the_islands_of_southwestern_Bass_Strait
    elif indexroche == 3 :
      csv_file_path = 'Data\\Exemples\\Monzodiorite.csv'
      #Andersen 1993 : https://api.semanticscholar.org/CorpusID:128356243
    elif indexroche == 4 :
      csv_file_path = 'Data\\Exemples\\Monzogabbro.csv'
      #Amaral 2022 : https://doi.org/10.1016/j.chemer.2022.125917
    elif indexroche == 5:
      csv_file_path = 'Data\\Exemples\\Rhyolite.csv'
      # : https://doi.org/10.1590/0001-3765202120201202
    elif indexroche == 6:
      csv_file_path = 'Data\\Exemples\\Hawaiite.csv'
      # Pillard 1980 : https://www.persee.fr/doc/bulmi_0180-9210_1980_num_103_1_7379
    donnees_chargees = pd.read_csv(csv_file_path, delimiter=",")
    for i in range(len(ListeCasesElements)):
      ListeCasesElements[i].delete(0,END)
      ListeCasesElements[i].insert(0, str(donnees_chargees[Liste_des_elements[i]][0]))

Fichier.add_cascade(label="Charger un exemple", menu=menuTypeRoche)
menuTypeRoche.add_command(label="P - Granite", command=lambda: ChargerExemple(1))
menuTypeRoche.add_command(label="V - Basalte", command=lambda: ChargerExemple(2))
menuTypeRoche.add_command(label="P - Monzodiorite", command=lambda: ChargerExemple(3))
menuTypeRoche.add_command(label="P - Monzogabbro", command=lambda: ChargerExemple(4))
menuTypeRoche.add_command(label="V - Rhyolite", command=lambda: ChargerExemple(5))
menuTypeRoche.add_command(label="V - Hawaiite", command=lambda: ChargerExemple(6))


def Charger():
  csv_file_path = askopenfilename()
  donnees_chargees = pd.read_csv(csv_file_path, delimiter=",")
  for i in range(len(ListeCasesElements)):
    ListeCasesElements[i].delete(0,END)
    ListeCasesElements[i].insert(0, str(donnees_chargees[Liste_des_elements[i]][0]))
Fichier.add_command(label="Charger...",command=Charger)

def Sauvegarder():
  data = [("fichier CIPoWer csv(*.csv)","*.csv"),('All tyes(*.*)', '*.*')]
  listeElementswt = [wtSiO2.get(),wtAl2O3.get(), wtFe2O3.get(),wtFeO.get(),wtMgO.get(),wtCaO.get(), wtNa2O.get(), wtK2O.get(), wtTiO2.get(), wtP2O5.get(), wtMnO.get()]
  file = asksaveasfilename(filetypes = data, defaultextension = data)
  if file:
      with open(file, "w", newline='') as f:
          writer = csv.writer(f)
          writer.writerow(Liste_des_elements)
          writer.writerow(listeElementswt)
Fichier.add_command(label="Sauvegarder sous...",command=Sauvegarder)

Fichier.add_separator()

Fichier.add_command(label="Fermer le programme",command=root.destroy)

#Edition
Edition=Menu(barremenu,tearoff=0)
barremenu.add_cascade(label="Edition",menu=Edition)

def Reinitialiser():
  for i in range(len(ListeCasesElements)):
    ListeCasesElements[i].delete(0,END)
Edition.add_command(label="Réinitialiser les valeurs",command=Reinitialiser)
#Aide
Aide=Menu(barremenu,tearoff=0)
barremenu.add_cascade(label="Aide",menu=Aide)

def Manuel_Utilisateur():
  webbrowser.open('Notice_Info.pdf')
Aide.add_command(label="Ouvrir la notice utilisateur",command=Manuel_Utilisateur)
Aide.add_separator()
def Fenetre_Liens():
    # Création de la fenêtre Tkinter
    fen_Liens = Toplevel()
    fen_Liens.geometry("1000x600")
    fen_Liens.title("Liens des images")
    text_box = tk.Text(fen_Liens, height=12800, width=720, font=("Arial", 10), bg='grey94')
    text_box.pack()
    liste_des_liens = [
        "Miracosta (2021) Every Rock Tells A Story, https://gotbooks.miracosta.edu/rocks/igneous%20rocks/43.html",
        "Miracosta (2021) Every Rock Tells A Story, https://gotbooks.miracosta.edu/rocks/igneous%20rocks/39.html",
        "Miracosta (2021) Every Rock Tells A Story, https://gotbooks.miracosta.edu/rocks/igneous%20rocks/36.html",
        "ViaGallica ([...]) Le trachyte, https://viagallica.com/auvergne/trachyte.htm",
        "Alex Strekeizen (2020) Latite, https://www.alexstrekeisen.it/english/vulc/latite.php",
        "GéoForum (2007) Trachyandésite basaltique (Le Mont-Dore / P de D)), https://www.geoforum.fr/gallery/image/415-trachyandésite-basaltique-le-mont-dore-p-de-d/",
        "GéoForum (2006) Trachyandésite (La Bourboule - P de D), https://www.geoforum.fr/gallery/image/270-trachyandésite-la-bourboule-p-de-d/",
        "Virtual Microscope ([...]) Olivine Hawaiite - Isle of Rum, https://www.virtualmicroscope.org/content/olivine-hawaiite-isle-rum",
        "Virtual Microscope ([...]) Mugearite, https://www.virtualmicroscope.org/content/mugearite",
        "Comparer Roches (2024) shoshonite et shoshonite Types et Faits, https://rocks.comparenature.com/fr/shoshonite-et-shoshonite-types-et-faits/comparison-107-107-9",
        "Comparer Roches (2024) Formation de Benmoreite et Grès, https://rocks.comparenature.com/fr/formation-de-benmoreite-et-gres/comparison-114-8-8",
        "Bégénat ([...]) basalte à olivine,https://www.begenat.com/produit/basalte-a-olivine-5/",
        "Collège Colette Sartrouville (2011) L’andésite : une roche volcanique, https://clg-colette-sartrouville.ac-versailles.fr/spip.php?article22",
        "GéoForum (2006) Phonolite (La Roche Tulilière - P de D), https://www.geoforum.fr/gallery/image/215-phonolite-la-roche-tuilière-p-de-d/",
        "Mindat () Tephritic-phonolite, https://www.mindat.org/min-48547.html",
        "GéoForum (2007) Basanite (Cantal), https://www.geoforum.fr/gallery/image/960-basanite-cantal/",
        "Pinterest (([...]) no name provided, https://www.pinterest.fr/pin/274508539772482745/",
        "Mineralienatlas - Fossilienatlas (2006) foidite, https://www.mineralienatlas.de/lexikon/index.php/RockData?lang=en&rock=foidite",
        "Wikipedia (2022) Fichier:Granit (RK 2206 P1890210), https://fr.wikipedia.org/wiki/Fichier:Granit_%28RK_2206_P1890210%29.jpg",
        "Geologysciences (2023) Granodiorite, https://fr.geologyscience.com/roches/roches-ignées/granodiorite/",
        "Wiktionnaire (2023) tonalite, https://fr.wiktionary.org/wiki/tonalite",
        "Virtual Microscope ([...]) Syenite - Ben Loyal, https://www.virtualmicroscope.org/content/syenite-ben-loyal",
        "Alex Strekeisen (2020) Monzonite, https://www.alexstrekeisen.it/english/pluto/monzonite.php",
        "Alex Strekeisen (2020) Diorite, https://www.alexstrekeisen.it/english/pluto/diorite.php",
        "Youtube (2023) Trajet d’un gabbro dans la croûte océanique, https://www.youtube.com/watch?v=d8qIbCKlp-A",
        "Alex Strekeisen (2020) Monzodiorite, https://www.alexstrekeisen.it/english/pluto/monzodiorite.php",
        "Northern Geological Supplies Limited ([...]) Essexite (olivine monzogabbro), https://www.geologysuperstore.com/product/essexite-olivine-monzogabbro/",
        "Science Photo Library (2024) Nepheline monzosyenite igneous rock, https://www.sciencephoto.com/media/169461/view/nepheline-monzosyenite-igneous-rock",
        "Sandatlas ([...]) Rock Types, https://www.sandatlas.org/rock-types/",
        "Fossiliraptor ([...]) Roches et phénomènes ignés 4, http://www.fossiliraptor.be/rochesetphenomenesignes4.htm"
    ]
    for link in liste_des_liens:
        text_box.insert(tk.END, link + "\n\n")
    text_box.config(state=tk.DISABLED)
    fen_Liens.resizable(width=False, height=False)
    fen_Liens.iconphoto(False, logo, logo)
Aide.add_command(label="Liens des images", command=Fenetre_Liens)

def Fenetre_A_Propos():
    fen_Apropos = Toplevel()
    fen_Apropos.title("A propos de CIPoWer")
    canvas_logo = Canvas(fen_Apropos, width = 500, height = 400)
    canvas_logo.pack(expand = YES, fill = BOTH)  
    canvas_logo.create_image(700/2, 200, image = logo)
    canvas_logo.logo = logo
    Noms_apropos = Label(fen_Apropos, text ="CIPoWer est un logiciel open-source développé par l'équipe CIPoWer dépendante de l'Ecole et Observatoire des Sciences de la Terre (EOST)\n Crédit : GAUCHET Noémie, DIROFF Mathis, DESBIN Lou, HAY Nathan, HEYDEL Lilian, ZIMMERLIN Jules. \n\n\n\n CIPoWer 1993-1994")
    Noms_apropos.pack(expand = YES,side=TOP)
    fen_Apropos.iconphoto(False, logo, logo)
    fen_Apropos.resizable(width=False, height=False)
Aide.add_command(label="A propos de CIPoWer", command=Fenetre_A_Propos)


root.config(menu=barremenu)


label = tk.Label(root, text="")
label.pack(pady=10)

scrollbar = tk.Scrollbar(root, orient="vertical")
text_widget = tk.Text(root,font=("Arial", 10),  wrap='word', width=60, height=700, yscrollcommand=scrollbar.set, state=tk.DISABLED)
text_widget.pack(pady=10, padx=50, side=RIGHT)

class TestFonctionsCIPOWER(unittest.TestCase):
  #ON TEST LA FONCTION DE CHARGEMENT DES EXEMPLES - Ici, les fichiers dans le dossier du programme doivent avoir exactement les mêmes valeurs que celles que l'on veut. Ceci permet donc de voir si rien n'a été corrompu.
  def test_ChargerExemples(self):
    valeurs_attendues = [
    [70.83, 14.52, 0.51, 2.5, 0.78, 0.65, 2.48, 5.56, 0.32, 0.14, 0.05],
    [45.65, 10.56, 1.26, 8.26, 17.87, 10.34, 0.48, 0.11, 0.26, 0.10, 0.15],
    [53.45, 17.9, 3.88, 3.16, 1.82, 6.2, 6.23, 2.46, 1.15, 0.47, 0.21],
    [45.45, 12.81, 11.78, 0, 13.52, 10.99, 1.25, 1.81, 1.48, 0.55, 0.17],
    [72.34, 13.25, 1.77, 1.03, 0.35, 0.89, 3.96, 4.89, 0.27, 0.15, 0.09],
    [48.90, 16.70, 4.60, 5.20, 5.80, 7.15, 4.80, 1.70, 2.17, 0.69, 0.17]
    ]
    for i in range(1,6):
       ChargerExemple(i)
       for k in range(len(ListeCasesElements)):
          self.assertEqual(float(ListeCasesElements[k].get()), valeurs_attendues[i-1][k])
  #Test case pour tester la fonction 'calcul_norme()' 
  def test_calcul_norme(self):
      #Test le fonctionnement de la fonction trapz.
      #Liste L = valeur issue du cours de pétrologie magmatique considérée comme valeurs vraies des minéraux pour un granite
      PoidsOxyd = [70.83, 14.52, 0.51, 2.5, 0.78, 0.65, 2.48, 5.56, 0.32, 0.14, 0.05]
      L = [0.336, 0.608, 32.804, 0.0, 0.0, 20.96, 0.0, 2.502, 3.468, 0.0, 0.696, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 3.828, 0.0, 0.0, 31.14]
      Q,A,P,F,PropMin_calcul = calcul_norme(PoidsOxyd)
      self.assertAlmostEqual(PropMin_calcul,L)

unittest.main(argv=[''], verbosity=3, exit=False)


Reinitialiser()
root.mainloop()

