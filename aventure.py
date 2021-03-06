# -*- coding:Utf-8 -*-
'''
Un jeu d'aventure texte simple, exploration, interaction avec objets,
-Les fonctionnalités que je souhaite ajouter :
-La possibilité de prendre un objet dans le monde - ok, commande prendre
-La possibilité de regarder les objets du monde ou de l'inventaire - ok, commande regarder
-La possibilité de regarder son inventaire, son status ou la carte du monde - ok, commande info
-La possibilité d'interagir avec un objet - ok, commande utiliser
-La possibilité d'avoir de l'aide, pour connaître les commandes (+ introduction au départ) - ok, commande aide
-Un système de score pour pouvoir finir le jeu (gagner des points en ramassant les objet et en les utilisant) - ok
'''
#bibliothèques

import time
import random
import sys, os

# données

AIDE = '''
=============AIDE=================
Bienvenue dans ce jeu d'aventure !
==================================
Vous pouvez intéragir avec les lieux et les objets à l'aide de commandes textuelles,
Voici les différentes commandes possibles, il peut y avoir soit une commande seule ou 
soit accompagnée d'un objet ou d'un lieu, mais les articles (un, le, les) ne fonctionneront pas.
ex : 'aller chambre'
---
# aller # -- pour déplacer le joueur vers le lieu où l'on souhaite se rendre
# regarder # -- pour avoir une description de ce que vous souhaitez observer
# prendre # -- pour ajouter à son inventaire un objet.
# utiliser # -- pour interagir avec les objets.
# carte # -- permet d'afficher le monde.
# info # -- pour en savoir plus sur le joueur.
# aide # -- pour voir cet aide décrivant les différentes commandes.
---
'''

SCORE_MAX = 8

OBJETS = {
"couteau" : {
"nom" : "Couteau",
"description" : "Il est long et aiguisé, attention à ne pas vous couper.",
"situation" : "Un couteau se trouve sur le lit.",
"points" : 2
}, 
"tomate" : {
"nom" : "Tomate",
"description" : "Elle est bien mûre et elle semble bien juteuse, miam.",
"situation" : "Il y a une tomate sur la petite table.",
"points" : 2
},
"porte" : {
"nom" : "Porte",
"description" : "Une porte en bois vernis simple.",
"situation" : "",
"points" : 0
}
}

LIEUX ={
"chambre" : {
"nom" : "une chambre", 
"description" : "Il s'agit d'une petite salle avec un lit sans draps, tous les meubles sont vides,\
 une porte ouvre sur un couloir.",
"choix_lieu" : ["couloir"],
"choix_objet" : ["porte", "couteau"]
}, 
"salon" : {
"nom" : "un salon", 
"description" : "Il s'agit d'une pièce avec une petite table, les murs frais ont été repeints il n'y a pas longtemps,\
 une porte ouvre sur un couloir.",
"choix_lieu" : ["couloir"],
"choix_objet" : ["porte", "tomate"]
},
"couloir" : {
"nom" : "un couloir",
"description" : "Il s'agit d'un couloir étroit, il y a deux portes, l'une allant vers la chambre, l'autre vers le salon.",
"choix_lieu" : ["chambre", "salon"],
"choix_objet" : ["porte"]
}
}

ACTIONS = ["aller", "regarder", "prendre", "utiliser", "info", "aide", "carte", "quitter"]

PLAN ='''
 _________
|  |      |
|  /   2  |
|  |______|
|1 |      |
|  /   3  |
|__|______|

1 - couloir
2 - chambre
3 - salon

''' 

#classes

class Objet():
    def __init__(self, dicto):
        self.nom = dicto["nom"]
        self.description = dicto["description"]
        self.situation = dicto["situation"]
        self.points = dicto["points"]


class Lieu():
    def __init__(self, dictl):
        self.nom = dictl["nom"]
        self.description = dictl["description"]
        self.choix_lieu = dictl["choix_lieu"]
        self.choix_objet = dictl["choix_objet"]


class Joueur():
    def __init__(self):
        self.nom = input("Quel est votre nom ?")
        self.score = 0
        self.pre_situation = ""
        self.nou_situation = ""
        self.lx_possibles = []
    
        self.inventaire = []
        self.obj_possibles = []

    def ajout_inventaire(self, o):
        self.objet = Objet(OBJETS[o])
        self.inventaire.append(self.objet)
        self.score += self.objet.points

    def control_inventaire(self):
        if len(self.inventaire):
            print("Vous avez dans votre inventaire :")
            for i in self.inventaire:
                print("-", i.nom)
        else:
            print("Vous n'avez rien dans votre inventaire.")

    def changement_situation(self, ns):
        self.pre_situation = self.nou_situation
        self.nou_situation = ns

    def afficher_info(self):
        os.system("cls")
        print("======INFO-JOUEUR=========================")
        print("Vous vous appelez :", self.nom)
        print("Vous vous trouvez dans", self.nou_situation.nom)
        print("Vous avez", self.score, "points sur", SCORE_MAX, end=".\n")
        print("---")
        self.control_inventaire()
        print("==========================================\n")


#fonctions


def decoupage_commande(commande):
    '''découpe l'action du joueur pour produire deux str séparées'''
    c = commande.split()
    c0, c1 = "", ""
    if len(c) == 1:
        c0 = c[0]
        return c0, c1
    elif len(c) == 2:
        c0 = c[0]
        c1 = c[1]
        return c0, c1
    else:
        print("ce n'est pas une commande valide.\n")
        return c0, c1

def verification_action(a):
    if a in ACTIONS:
        return False

    else:
        print("Erreur :", a, "n'est pas une bonne commande.\n")
        return True

def verification_objet(o, j):
    for i in j.inventaire:
        if o == i.nom.lower():
            return False

    if o in j.nou_situation.choix_lieu or o in j.obj_possibles:
        return False

    elif o in j.nou_situation.nom.split():
        return False

    elif len(o) == 0:
        return False
    
    else:
        print("Erreur :", o, "n'est pas un objet ou un lieu possible.\n")
        return True
    
def choix_action(joueur):
    verifa, verifo = True, True
    while verifa or verifo:
        print("\n==========ACTION=========")
        print("Quelle est votre action ?")
        print("Tapez 'aide' si vous avez besoin d'informations sur le jeu.")
        commande = input(">>>").lower()
        action, objet = decoupage_commande(commande)
        verifa = verification_action(action)
        verifo = verification_objet(objet, joueur)
    return action, objet

def utiliser_objet(j, o):
    '''vérifie si l'objet peut être utilisé avec un autre objet et si oui, supprime les objets et ajoute les points de chaque objets'''
    objet = input('>>>')
    avertissement = "\n- Vous ne pouvez pas utiliser cet objet avec lui-même."
    if not verification_objet(objet, j):
        for i in j.inventaire:
            if i.nom.lower() == objet and o == objet:
                print(avertissement)

            if i.nom.lower() == objet and o != objet:
                print("\n- Vous utilisez", o, "avec", objet, end=".\n")
                j.score += 4

        for i in j.obj_possibles:
            if i == objet and o == objet:
                print(avertissement)

            if i == objet and o != objet:
                print("\n- Vous utilisez", o, "avec", objet, end=".\n")
                j.score += 6

def redirection_commande(a, j):
    '''fonction centrale du jeu qui redirigine l'action du joueur vers la fonction correspondante'''
    if a[0] == "aller":
        if a[1] in j.nou_situation.choix_lieu:
            l = Lieu(LIEUX[a[1]]) # une nouvelle instance lieu est créé
            print("\n- Vous ouvrez la porte et entrez dans", l.nom, end=".\n")
            time.sleep(1)
            j.changement_situation(l) # et permet de mettre à jour la situation du joueur

        elif a[1] in j.nou_situation.nom.split():
            print("\n- Vous vous trouvez déjà dans", a[1], end=".\n")

        elif a[1] == "":
            print("\n- Où souhaitez vous aller ?")

    elif a[0] == "regarder":
        if a [1] == "":
            afficher_situation(j)
        
        elif a[1] in j.nou_situation.nom.split():
            print('\n-', j.nou_situation.description)

        elif a[1] in j.obj_possibles:
            print('\n-', OBJETS[a[1]]['description'])

        for i in j.inventaire:
            if a[1] == i.nom.lower():
                print("\n- Vous sortez l'objet de votre inventaire pour l'observer :")
                print(i.description)

    elif a[0] == "prendre":

        for i in j.inventaire:
            if i.nom.lower() == a[1]:
                print("\n- Vous avez déjà", a[1], "dans votre inventaire.")

        for i in j.obj_possibles:
            obj = OBJETS[i]

            #le nombre de points de l'objet permet de distinguer ce que l'on peut prendre ou pas 
            if i == a[1] and obj['points'] > 0:
                print("\n- Vous ramassez", a[1], end=".\n")
                j.ajout_inventaire(a[1])

            elif  i == a[1] and obj['points'] == 0: 
                print("\n- Vous ne pouvez pas prendre", a[1], end=".\n")

        if a[1] == '':
            print("\n- Que souhaitez vous prendre ?")

    elif a[0] == "utiliser":

        if a[1] == "":
            print("\n- Que souhaitez-vous utiliser ?")

        for i in j.inventaire:
            if i.nom.lower() == a[1] :
                print("\n- Avec quoi souhaitez vous utiliser", a[1], "?")
                utiliser_objet(j, a[1])

        for o in j.obj_possibles:
            obj = OBJETS[o]
            if o == a[1] and obj['points'] > 0:
                print("\n- Avec quoi souhaitez vous utiliser", a[1], "?")
                utiliser_objet(j, a[1])

            elif o == a[1] and obj['points'] == 0:
                print("\n- Il n'est pas possible d'utiliser", a[1], end=".\n")
    
    elif a[0] == "quitter":
        os.system("cls")
        print("merci et au revoir !")
        sys.exit()

    elif a[0] == "info":
        j.afficher_info()

    elif a[0] == "aide":
        os.system("cls")
        print(AIDE)

    elif a[0] == "carte":
        print(PLAN)


def afficher_situation(j):
    os.system("cls")
    print('============SITUATION============')
    print("Vous vous trouvez dans", j.nou_situation.nom, end='.\n')
    print(j.nou_situation.description)
    for o in j.obj_possibles:
        if OBJETS[o]["points"] > 0:
            print(OBJETS[o]["situation"])

        

def obj_lex_possibles(j):
    j.obj_possibles = []
    j.lex_possibles = []
    for o in j.nou_situation.choix_objet:
        #print(o)
        j.obj_possibles.append(o)
        #print('flag 1')
    
        for i in j.inventaire:
            #print(i, i.nom, i.nom.lower())
            if o == i.nom.lower():
                j.obj_possibles.remove(o)
                #print("flag 0")

    #print("inventaire :", j.inventaire, 'objets possibles :', j.obj_possibles)
    for l in j.nou_situation.choix_lieu:
        j.lex_possibles.append(l)

def nouvelle_partie():

    # création des objets instances
    joueur = Joueur()

    # situation de départ
    joueur.pre_situation = Lieu(LIEUX["salon"])
    joueur.nou_situation = Lieu(LIEUX["couloir"])

    print("Bonjour %s \nC'est parti !" % joueur.nom)
    time.sleep(1)


    # déroulement du jeu  
    while joueur.score < SCORE_MAX:
        obj_lex_possibles(joueur) #mise à jour du joueur et des objets et lieu avec lesquels il peut entrer en relation
        if joueur.pre_situation != joueur.nou_situation:
            afficher_situation(joueur) #affiche la situation du joueur
            joueur.pre_situation = joueur.nou_situation # un transfert de situation si la situation à changé
        action = choix_action(joueur) 
        redirection_commande(action, joueur)

    print('\n!')
    print('\nVictoire, vous avez mangé un bonne tomate sans vous en mettre partout ! :)\n')
    print('!\n')

def menu():
    #print("\n"*50)
    os.system("cls")
    print(PLAN)
    print("\n===============\nJeux d'aventure\n===============")
    nouvelle_partie()

#programme

if __name__ == '__main__':
    menu()