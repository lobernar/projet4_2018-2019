"""
Auteur: Loïc Bernard
Date: 20/11/2018
Matricule ULB: 000469510
Etudes: BA1 Info
But: Le but est de créer une prison dans laquelle on peut enfermer des super villains. Il
faut cependant faire attention que la sécurité soit assez élevée et qu'il ait assez de place dans
la prison
Entrées: la taille de la prison, les ailes ainsi que leurs niveaux de sécurité et le fichier contenant
les criminels
Sorties: le menu de la prison avec lequel il est possible d'effectuer plusieurs opérations
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
        if sys.argv[2] not in gender or int(sys.argv[1]) <= 0:
            raise
        prison = {}
        i = 2
        aile = 1
        while i < len(sys.argv) - 1:
            if sys.argv[i] in gender:
                selected_gender = sys.argv[i]
                gender.remove(sys.argv[i])
                int(sys.argv[i + 1])
                if int(sys.argv[i + 1]) < 0:
                    raise
                aile = 1
                prison[selected_gender] = {aile:{}}
            elif int(sys.argv[i]):
                prison[selected_gender][aile] = {"prisonniers": [], "sécurité": int(sys.argv[i])}
                aile += 1
            i += 1

    except Exception:
         print("Votre prison n'est pas construite selon les règles !\n"
                 "Veuillez relancer le programme avec une prison adéquate !")
         return False
    else:
        prison["taille"] = int(sys.argv[1])
        print("Votre prison sait accueillir", prison["taille"], "prisonniers.")
        for gender in prison:
            if gender != "taille":
                secu = []
                i = 1
                while i <= len(prison[gender]):
                    secu.append(str(prison[gender][i]["sécurité"]))
                    i += 1
                if gender == "M":
                    print("La prison possède une aile pour hommes, composée de", max(prison[gender]), "divison(s) \n"
                            "de sécurité", ",".join(secu) + ".")
                elif gender == "F":
                    print("La prison possède une aile pour femmes, composée de", max(prison[gender]), "divison(s) \n"
                        "de sécurité", ",".join(secu) + ".")
    print(prison)
    return prison


def print_villain(villain):
    """Cette fonction imprime les caractéristiques du criminel choisi"""

    print("-", str(villain["nom"]) + ", ID", str(villain["ID"]) + ", unviers", villain["univers"])
    print("     Niveau de danger :", villain["danger"])
    crimes = ["- " + i for i in villain["crimes"]]
    print("     Crimes commis : \n        " + "\n        ".join(crimes))


def taille(prison):
    """Cette fonction vérifie si la prison possède la taille appropriée pour accueillir les criminels"""

    with open(sys.argv[-1], "rb") as f:
        pickle_file = pickle.load(f)
        taille = 0
        for gender in pickle_file:
            for j in pickle_file[gender]:
                taille += 1
        return taille <= prison["taille"]


def fill_prison(prison):
    """Cette fonction ajoute les prisonniers du fichier à la prison construite"""

    with open(sys.argv[-1], "rb") as f:
        pickle_file = pickle.load(f)
        print("Maintenant, remplissons la prison de prisonniers...")
        res = True
        for gender in pickle_file:
            if gender not in prison:
                print("Votre prison ne possède pas la division du sexe approprié pour certains de vos \n"
                      "prisonniers ! \nVeuillez construire une prison adéquate pour votre population carcérale !")
                res = False
                break
            elif not taille(prison):
                print("Vous possédez trop de prisonniers pour la taille de votre prison ! \n"
                      "Débarassez-vous de quelques-uns de vos prisonniers avant de revenir, on ne dira rien, promis."
                      " Ils ne manqueront à peronne... \nOu construisez une prison plus grande !")
                res = False
                break
            else:
                i = 0
                while i < len(pickle_file[gender]) and res:
                    res = put_in_jail(prison, pickle_file[gender][i], gender)
                    i += 1
                if res is False:
                    print("Vous êtes priés de construire une prison plus protégée si vous ne voulez pas"
                            "qu'ils s'enfuient. Encore.")
                    return res
        return res


def put_in_jail(prison, villain, gender):
    """Cette fonction ajoute à la prison le criminel donné en argument"""
    secu = {"M": [], "F": []}
    for i in prison:
        if i != "taille":
            for j in range(1, len(prison[i]) + 1):
                secu[i].append(prison[i][j]["sécurité"])
    secu["M"].sort()
    secu["F"].sort()
    res = True
    if villain["danger"] > max(secu[gender]):
        print("Votre prison n'était pas suffisamment sécurisée pour le/la prisonnier/ère :")
        print_villain(villain)
        res = False
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
    return res


def lst_prisonniers(prison):
    lst = []
    for gender in prison:
        if gender != "taille":
            for i in prison[gender]:
                for j in range(len(prison[gender][i]["prisonniers"])):
                    lst.append(prison[gender][i]["prisonniers"][j]["nom"])
    return lst


def access_prison(prison, s):
    lst = []
    for gender in prison:
        if gender != "taille":
            for i in prison[gender]:
                for j in range(len(prison[gender][i]["prisonniers"])):
                    lst.append(prison[gender][i]["prisonniers"][j][s])
    return lst


def add_villain(prison):
    """Cette fonction permer à l'utilisateur d'ajouter un prisonnier dans sa prison"""

    new_pris = {}
    nom = input("Quel est le nom du prisonnier à ajouter à la prison ? \n>")
    while nom in access_prison(prison, "nom"):
        nom = input("Ce prisonnier existe déjà \n>")
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
        while crimes == "":
            print("Entrez des crimes valables")
            crimes = input(">")
        if crimes != "Fini":
            lst_crimes.append(crimes)
            crimes = input(">")
    lst_id = []
    ID = [lst_id.append(str(random.randint(0, 6))) for i in range(6)]
    ID = int("".join(lst_id))
    while ID in access_prison(prison, "ID"):
        ID = [lst_id.append(str(random.randint(0, 6))) for i in range(6)]
    ID = int("".join(lst_id))
    new_pris.update({"nom": nom, "crimes": lst_crimes, "univers": univers, "ID": ID, "danger": danger})
    put_in_jail(prison, new_pris, genre)
    if len(lst_prisonniers(prison)) > prison["taille"]:
        print("Votre prison possède trop de prisonniers ! Un de vos prisonniers a "
              "réussi à s'échapper dans la confusion !")
        prisonniers = lst_prisonniers(prison)
        random_flee = random.randint(0, len(prisonniers) - 1)
        for gender in prison:
            if gender != "taille":
                for i in prison[gender]:
                    for j in range(len(prison[gender][i]["prisonniers"]) - 1):
                        if prison[gender][i]["prisonniers"][j]["nom"] == str(prisonniers[random_flee]):
                            print("Le/la prisonnier/ère", prison[gender][i]["prisonniers"][j].pop("nom"),
                                  "s'est enfui(e) !")
                            del prison[gender][i]["prisonniers"][j]
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
    if choice == 1: # l'utilisateur souhaite filtrer la prison en fonction du genre
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

    elif choice == 2: # l'utilisateur souhaite filtrer la prison en fonction de l'univers
        print("Veuillez entrer l'univers dont vous cherchez le vilain.")
        univ = input(">")
        compteur = 0
        prisonniers = []
        for gender in prison:
            if gender != "taille":
                for i in prison[gender]:
                    for j in range(len(prison[gender][i]["prisonniers"])):
                        if prison[gender][i]["prisonniers"][j]["univers"] == univ:
                            prisonniers.append(prison[gender][i]["prisonniers"][j])
                            compteur += 1
        if compteur == 0:
            print("Nous n'avons trouvé aucun super vilain de cet univers !")
        else:
            print("Vous avez", compteur, "prisonniers de cet univers")
            i = 0
            while i < len(prisonniers):
                print_villain(prisonniers[i])
                i += 1

    elif choice == 3: # l'utilisateur souhaite filtrer la prison selon le niveau de danger
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
        prisonniers_danger = []
        for gender in prison:
            if gender != "taille":
                for i in prison[gender]:
                    for j in range(len(prison[gender][i]["prisonniers"])):
                        if prison[gender][i]["prisonniers"][j]["danger"] >= niv_danger:
                            prisonniers_danger.append(prison[gender][i]["prisonniers"][j])
                            compteur += 1
        if compteur == 0:
            print("Nous n'avons trouvé aucun super vilain avec ce niveau de danger ! \n"
                  "(J'imagine que c'est une bonne chose...)")
        else:
            print("Vous avez", compteur, "prisonniers qui ont un niveau de danger supérieur ou égal à", niv_danger)
            i = 0
            while i < len(prisonniers_danger):
                print_villain(prisonniers_danger[i])
                i += 1
    elif choice == 4:
            print("Toute la prison")
            print(prison)


def menu():
    prison = build_prison()


    if prison is not False:
        fill = fill_prison(prison)
        if fill is True:
            print("Ok, votre prison a su être construite et est maintenant remplie de prisonniers !")
            cond = True
            while cond:

                print("Comment pouvons-nous vous aider ? Voulez-vous :\n"
                    "1) Consulter les statistiques de notre prison ?\n"
                    "2) Ajouter un Super Vilain à notre prison ?\n"
                    "3) Sauvegarder les prisonniers dans un fichier ?\n"
                    "4) Quitter notre programme ?")
                choice = input(">")
                ok = True
                while ok:
                    try:
                        int(choice)
                        choice = int(choice)
                        if choice <= 4:
                            ok = False
                        else:
                            raise
                    except Exception:
                        print("Veuillez choisir un nobre entier !")
                        choice = input(">")
                if choice == 1:
                    filter_prison(prison)
                elif choice == 2:
                    add_villain(prison)
                elif choice == 3:
                    with open("liste_prisonniers.pkl", "wb") as f:
                        pickle.dump(prison, f)
                elif choice == 4:
                    print("Merci d'avoir utilisé notre programme !\n"
                      "Nous allons nous efforcer de garder les super vilains enfermés d'ici votre "
                      "prochaine visite.\n"
                      "En cas de problèmes, n'hésitez pas à consulter notre programme d'annuaire de "
                      "super-hérosTM !")
                    cond = False


menu_choice = menu()



"""
comments!!!!!!!!!!!!!!!!
test si taille de prison est ok
taille too small!!!!!!!!!!
function for try and except 
"""