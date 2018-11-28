"""
Auteur: Loïc Bernard
Date: 20/11/2018
Matricule ULB: 000469510
Etudes: BA1 Info
But: Le but est de créer une prison dans laquelle on peut enfermer des super villains. Il
faut cependant faire attention que la sécurité soit assez élevée et qu'il ait assez de place dans
la prison
Entrées:
Sprties:
"""
import random, pickle, sys


def build_prison():
    """Cette fonction construit la prison et vérifie que les entrées de l'utilisateur soient
    valides"""

    print("Bienvenue dans notre programme de gestion de la prison pour Super Vilains ! \n"
          "Tout d'abord, construisons la prison selon les paramètres reçus...")
    try:
        f = open(sys.argv[-1])
        int(sys.argv[1])
        gender = ["M", "F"]
        if sys.argv[2] not in gender:
            assert False
        prison = {}
        i = 2
        num = 1
        d = {}
        while i < len(sys.argv) - 1:
            if (sys.argv[i] not in gender) and (not int(sys.argv[i])):
                assert False
            if sys.argv[i] in gender:
                num = 0
                int(sys.argv[i + 1])
                gender.remove(sys.argv[i])
                gender1 = sys.argv[i]
                d = {}
            else:
                detail = {"prisonniers": [], "sécurité": int(sys.argv[i])}
                d[num] = detail
                prison[gender1] = d
            num += 1
            i += 1
    except Exception:
        print("Votre prison n'est pas construite selon les règles ! \n"
              "Veuillez relancer le programme avec une prison adéquate !")
    else:
# for i in prison:... !!!!!!!!!!!!
        prison["taille"] = int(sys.argv[1])
        print("Votre prison sait accueillir", prison["taille"], "prisonniers.")
        if "F" in prison:
            secu = ""
            i = 1
            while i <= len(prison["F"]):
                secu += str(prison["F"][i]["sécurité"]) + ","
                i += 1
            print("La prison possède une aile pour femmes, composée de", max(prison["F"]), "divison(s) \n"
                  "de sécurité", secu + ".")
        if "M" in prison:
            secu = ""
            i = 1
            while i <= len(prison["M"]):
                secu += "," + str(prison["M"][i]["sécurité"])
                i += 1
            print("La prison possède une aile pour hommes, composée de", max(prison["M"]), "division(s) \n"
                  "de sécurité", secu + ".")
        return prison


def print_villain(villain):
    """Cette fonction imprime les caractéristiques du criminel choisi"""

    print("-", str(villain["nom"]) + ", ID", str(villain["ID"]) + ", unviers", villain["univers"])
    print("     Niveau de danger :", villain["danger"])
    crimes = ["- " + i for i in villain["crimes"]]
    print("     Crimes commis : \n        " + "\n        ".join(crimes))



def put_in_jail(prison, villain, gender):
    """Cette fonction ajoute à la prison le criminel donné en argument"""

    secu = {"M": [], "F": []}
    for i in prison:
        if i != "taille":
            for j in range(1, len(prison[i]) + 1):
                secu[i].append(prison[i][j]["sécurité"])
    secu["M"].sort()
    secu["F"].sort()
    if villain["danger"] > max(secu[gender]):
        print("Votre prison n'était pas suffisamment sécurisée pour le/la prisonnier/ère :")
        print_villain(villain)
        res = "Vous êtes priés de construire une prison plus protégée si vous ne voulez pas qu'ils "
        "s'enfuient. Encore."
    else:
        save = []
        i = 0
        while i < len(secu[gender]):
            if secu[gender][i] >= villain["danger"]:
                save.append(secu[gender][i])
            i += 1
        for key in prison[gender]:
            if prison[gender][key]["sécurité"] == min(save):
                prison[gender][key]["prisonniers"].append(villain)
        res = "Ok, votre prison a su être construite et est maintenant remplie de prisonniers !"
    return res


def fill_prison(prison):
    """Cette fonction ajoute les prisonniers du fichier à la prison construite"""

    with open(sys.argv[-1], "rb") as f:
        pickle_file = pickle.load(f)
        print("Maintenant, remplissons la prison de prisonniers...")
        res = 0
        for gender in pickle_file:
            res += len(pickle_file[gender])
            if gender not in prison:
                print("Votre prison ne possède pas la division du sexe approprié pour certains de vos \n"
                      "prisonniers ! \nVeuillez construire une prison adéquate pour votre population carcérale !")
                break
            elif res > prison["taille"]:
                print("Vous possédez trop de prisonniers pour la taille de votre prison ! \n"
                      "Débarassez-vous de quelques-uns de vos prisonniers avant de revenir, on ne dira rien, promis."
                      " Ils ne manqueront à peronne... \nOu construisez une prison plus grande !")
                break
            else:
                i = 0
                while i < len(pickle_file[gender]):
                    put_in_jail(prison, pickle_file[gender][i], gender)
                    i += 1
    return prison

def add_villain(prison):
    """Cette fonction permer à l'utilisateur d'ajouter un prisonnier dans sa prison"""

    new_pris = {}
    nom = input("Quel est le nom du prisonnier à ajouter à la prison ? \n>")
    while type(nom) != str:
        print("Quel est le nom du prisonnier à ajouter à la prison ?")
        nom = input(">")
    genre = input("Quel est son genre ?")
    while genre != "M" and genre != "F":
        print("Vous devez choisir homme ou femme (M ou F) !")
        genre = input(">")
    univers = input("À quel univers appartient-il/elle ? \n>")
    ok = True
    danger = input("Quel est son niveau de danger ? \n>")
    while ok:
        try:
            int(danger)
            ok = False
        except Exception:
            print("Vous devez saisir un nombre entier !")
            danger = input(">")
    danger = int(danger)
    lst_crimes = []
    crimes = input("Quel(s) crime(s) a-t-il/elle commis ? Entrez-les l'un après l'autre en appuyant sur "
                   "Enter après chaque entrée. Entrez 'Fini' lorsque vous avez terminé d'encoder. \n>")
    while crimes != "Fini":
        lst_crimes.append(crimes)
        crimes = input(">")
    lst_id = []
    for i in range(1, 7):
        lst_id.append(str(random.randint(0, 6)))
# same ID as other prisoner
    ID = int("".join(lst_id))
    new_pris.update({"nom": nom, "crimes": lst_crimes, "univers": univers, "ID": ID, "danger": danger})
    put_in_jail(prison, new_pris, genre)
# taille depassée ----> random flee!!!!!!!!!!!!
    return new_pris


def filter_prison(prison):
    """Cette fonction filtre les prisonniers selon le choix de l'utilisateur"""

    print("Quelle statistique voulez-vous obtenir ?\n"
          "1) Les prisonniers par genre\n"
          "2) Les prisonniers par univers\n"
          "3) Les prisonniers par niveau de danger\n"
          "4) Toute la prison")
    choice = input(">")
    ok = True
    while ok:
        try:
            int(choice)
            choice = int(choice)
            if int(choice) > 4:
                raise
            else:
                ok = False
        except Exception:
            print("Vous devez choisir un nombre entre 1 et 4 compris !")
            choice = input(">")
    if choice == 1: # le joueur souhaite filtrer la prison en fonction du genre
        print("Quelle est l'aile que vous voulez investiguer ?")
        gender = input(">")
        while gender != "M" and gender != "F":
            print("Vous devez choisir homme ou femme (M ou F) !")
            gender = input(">")
        res = 0
        for i in prison[gender]:
            res += len(prison[gender][i]["prisonniers"])
        print("Vous avez", res, "prisonnier(s) dans cette aile. \n"
                "Voici la liste des prisonniers dans cette aile:")
        for i in prison[gender]:
            for j in range(0, len(prison[gender][i]["prisonniers"])):
                print_villain(prison[gender][i]["prisonniers"][j])
                print()

    elif choice == 2:
        print("Veuillez entrer l'univers dont vous cherchez le vilain.")
        univ = input(">")
        compteur = 0
        for gender in prison:
            if gender != "taille":
                for i in prison[gender]:
                    for j in range(len(prison[gender][i]["prisonniers"])):
                        if prison[gender][i]["prisonniers"][j]["univers"] == univ:
                            print_villain(prison[gender][i]["prisonniers"][j])
                            compteur += 1
# print number of villains in this universe!!!!!!!!!!
        if compteur == 0:
            print("Nous n'avons trouvé aucun super vilain de cet univers !")

    elif choice == 3:
        print("Veuillez entrer le niveau de danger minimum du super vilain.")
        niv_danger = input(">")
        ok = True
        while ok:
            try:
                int(niv_danger)
                niv_danger = int(niv_danger)
                ok = False
            except Exception:
                print("Le niveau de danger doit être un nombre entier!")
                niv_danger = input(">")
        compteur = 0
        for gender in prison:
            if gender != "taille":
                for i in prison[gender]:
                    for j in range(len(prison[gender][i]["prisonniers"])):
                        if prison[gender][i]["prisonniers"][j]["danger"] > niv_danger:
                            print_villain(prison[gender][i]["prisonniers"][j])
                            compteur += 1
# print number of criminals with this danger!!!!!!!!!!!!!!!!
        if compteur == 0:
            print("Nous n'avons trouvé aucun super vilain avec ce niveau de danger ! \n"
                  "(J'imagine que c'est une bonne chose...)")
    elif choice == 4:
        print("Toute la prison")
        print(prison)


def menu():
    prison = build_prison()
    fill_prison(prison)





#villain = {'nom': 'Ursula', 'crimes': ['Sorcière de la mer', "A volé la voix d'Ariel", 'Tentative de vol de prince'], 'univers': 'Disney', 'ID': 336542, 'danger': 26}
print(menu())
"""
comments!!!!!!!!!!!!!!!!
docstring debut!!!!!!
test si taille de prison est ok
"""