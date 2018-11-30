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
        int(sys.argv[1])  # vérifie que la taille soit un entier
        gender = ["M", "F"]
        if sys.argv[2] not in gender or int(sys.argv[1]) <= 0:
            raise Exception
        prison = {}
        i = 2
        aile = 1
        selected_gender = None
        while i < len(sys.argv) - 1:
            if sys.argv[i] in gender:
                selected_gender = sys.argv[i]
                gender.remove(sys.argv[i])
                int(sys.argv[i + 1]) # si l'element est un genre, l'element suivant doit être un entier
                if int(sys.argv[i + 1]) <= 0:  # analyse si l'entier suivant le genre est positif
                    raise Exception
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
    return prison


def print_villain(villain):
    """Cette fonction imprime les caractéristiques du criminel choisi"""

    print("-", str(villain["nom"]) + ", ID", str(villain["ID"]) + ", unviers", villain["univers"])
    print("     Niveau de danger :", villain["danger"])
    crimes = ["- " + i for i in villain["crimes"]]
    print("     Crimes commis : \n        " + "\n        ".join(crimes))


def fill_prison(prison):
    """Cette fonction ajoute les prisonniers du fichier à la prison construite"""

    with open(sys.argv[-1], "rb") as f:
        pickle_file = pickle.load(f)
        print("Maintenant, remplissons la prison de prisonniers...")
        res = True
        nb_pris = 0
        print(pickle_file)
        # Analyse le nombre de prisonniers dans le fichier
        for gender in pickle_file:
            for j in pickle_file[gender]:
                nb_pris += 1

        for gender in pickle_file:
            if gender not in prison:  # analyse si la prison possède l'aile adéquate
                print("Votre prison ne possède pas la division du sexe approprié pour certains de vos \n"
                      "prisonniers ! \nVeuillez construire une prison adéquate pour votre population carcérale !")
                res = False
                break
            elif nb_pris > prison["taille"]:  # analyse si la prison est assez grande
                print("Vous possédez trop de prisonniers pour la taille de votre prison ! \n"
                      "Débarassez-vous de quelques-uns de vos prisonniers avant de revenir, on ne dira rien, promis."
                      " Ils ne manqueront à peronne... \nOu construisez une prison plus grande !")
                res = False
                break
            else:  # si la prison correspond aux critères, les prisonniers y sont ajoutés
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
            # analyse la sécurité minimum et ajoute le criminel à l'aile correspondante
            if prison[gender][key]["sécurité"] == min(save):
                prison[gender][key]["prisonniers"].append(villain)
    return res


def access_prison(prison, value, search):
    """Cette fonction permet d'accéder aux elements le la prison afin de les comparer
    à la valeur cherchée et renvoie les indexes nécessaires"""

    res = False
    lst = [res]
    for gender in prison:
        if gender != "taille":
            for i in prison[gender]:
                for j in range(len(prison[gender][i]["prisonniers"])):
                    if prison[gender][i]["prisonniers"][j][value] == search:
                        res = True
                        lst = [gender, i, j, res]
    return lst


def add_villain(prison):
    """Cette fonction permer à l'utilisateur d'ajouter un prisonnier dans sa prison"""

    new_pris = {}
    nom = input("Quel est le nom du prisonnier à ajouter à la prison ?\n>")  # nom du nouveau prisonnier
    a = access_prison(prison, "nom", nom)
    while a[-1]:  # vérifie qu'il n'y ait pas déjà un prisonnier avec le même nom
        nom = input("Ce prisonnier existe déjà \n>")
        a = access_prison(prison, "nom", nom)

    genre = input("Quel est son genre ?\n>")  # genre du nouveau prisonnier
    while genre != "M" and genre != "F":
        genre = input("Vous devez choisir homme ou femme (M ou F) !\n>")
    univers = input("À quel univers appartient-il/elle ?\n>")
    ok = True

    danger = input("Quel est son niveau de danger ? \n>")  # niveau de danger du criminel
    while ok:
        try:
            int(danger)
            ok = False
        except Exception:
            danger = input("Vous devez saisir un nombre entier !\n>")
    danger = int(danger)

    lst_crimes = []  # crimes commis par le nouveau prisonnier
    crimes = input("Quel(s) crime(s) a-t-il/elle commis ? Entrez-les l'un après l'autre en appuyant sur "
                   "Enter après chaque entrée. Entrez 'Fini' lorsque vous avez terminé d'encoder. \n>")
    while crimes != "Fini":
        while crimes == "":
            crimes = input("Entrez des crimes valables\n>")
        if crimes != "Fini":
            lst_crimes.append(crimes)
            crimes = input(">")

    lst_id = []  # crée une ID aléatoire pour le prisonnier
    ID = [lst_id.append(str(random.randint(0, 6))) for i in range(6)]
    ID = int("".join(lst_id))
    a = access_prison(prison, "ID", ID)
    while a[-1]:  # vérifie que l'ID choisie aléatoirement ne soit pas déjà prise
        ID = [lst_id.append(str(random.randint(0, 6))) for i in range(6)]
        a = access_prison(prison, "ID", ID)
    ID = int("".join(lst_id))

    new_pris.update({"nom": nom, "crimes": lst_crimes, "univers": univers, "ID": ID, "danger": danger})
    put_in_jail(prison, new_pris, genre)  # ajoute le criminel crée à la prison
    prisonniers = []
    # on ajoute les prisonniers de la prison dans une liste
    for gender in prison:
        if gender != "taille":
            for i in prison[gender]:
                for j in range(len(prison[gender][i]["prisonniers"])):
                    prisonniers.append(prison[gender][i]["prisonniers"][j]["nom"])
    # vérifie qu'il n y ait pas trop de prisonniers pour la prison
    if len(prisonniers) > prison["taille"]:
        print("Votre prison possède trop de prisonniers ! Un de vos prisonniers a "
              "réussi à s'échapper dans la confusion !")
        random_flee = random.randint(0, len(prisonniers) - 1)
        while str(prisonniers[random_flee]) == new_pris["nom"]:
            random_flee = random.randint(0, len(prisonniers) - 1)
        a = access_prison(prison, "nom", str(prisonniers[random_flee]))
        if a[-1]:
            print("Le/la prisonnier/ère", prison[a[0]][a[1]]["prisonniers"][a[2]].pop("nom"),
                  "s'est enfui(e) !")
            del prison[a[0]][a[1]]["prisonniers"][a[2]]  # supprime le prisonnier qui s'est enfui
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
                raise Exception
            else:
                ok = False
        except Exception:
            print("Vous devez choisir un nombre entre 1 et 4 compris !")
            choice = input(">")

    if choice == 1:  # l'utilisateur souhaite filtrer la prison en fonction du genre
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

    elif choice == 2:  # l'utilisateur souhaite filtrer la prison en fonction de l'univers
        print("Veuillez entrer l'univers dont vous cherchez le vilain.")
        univ = input(">")
        prisonniers = []
        for gender in prison:
            if gender != "taille":
                for i in prison[gender]:
                    for j in range(len(prison[gender][i]["prisonniers"])):
                        if prison[gender][i]["prisonniers"][j]["univers"] == univ:
                            prisonniers.append(prison[gender][i]["prisonniers"][j])
        if len(prisonniers) == 0:
            print("Nous n'avons trouvé aucun super vilain de cet univers !")
        else:
            print("Vous avez", len(prisonniers), "prisonniers de cet univers")
            i = 0
            while i < len(prisonniers):
                print_villain(prisonniers[i])
                i += 1

    elif choice == 3:  # l'utilisateur souhaite filtrer la prison selon le niveau de danger
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
        prisonniers_danger = []
        for gender in prison:
            if gender != "taille":
                for i in prison[gender]:
                    for j in range(len(prison[gender][i]["prisonniers"])):
                        if prison[gender][i]["prisonniers"][j]["danger"] >= niv_danger:
                            prisonniers_danger.append(prison[gender][i]["prisonniers"][j])
        if len(prisonniers_danger) == 0:
            print("Nous n'avons trouvé aucun super vilain avec ce niveau de danger ! \n"
                  "(J'imagine que c'est une bonne chose...)")
        else:
            print("Vous avez", len(prisonniers_danger), "prisonniers qui ont un niveau de danger supérieur ou égal à"
                  , niv_danger)
            i = 0
            while i < len(prisonniers_danger):
                print_villain(prisonniers_danger[i])
                i += 1
    elif choice == 4:  # l'utilisateur souhaite afficher toute la prison
            print("Toute la prison")
            print(prison)


def menu():
    """Cette fonction affiche le menu avec les différentes opérations possibles"""

    prison = build_prison()
    if prison is not False:  # vérifie que la prison soit valable
        fill = fill_prison(prison)
        if fill is True:  # vérifie que tous les criminels du fichier peuvent être ajoutés à la prison
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
                            raise Exception
                    except Exception:
                        print("Veuillez choisir un nobre entier !")
                        choice = input(">")
                if choice == 1:  # l'utilisateur souhaite filtrer la prsion
                    filter_prison(prison)
                elif choice == 2:  # l'utilisateur souhaite ajouter un prisonier à la prison
                    add_villain(prison)
                elif choice == 3:  # l'utilisateur souhaite sauvegarder la prison dans un fichier
                    file = input("Comment voulez-vous nommer le ficher?\n>")
                    while file[-1] != "p" and file[-2] != ".": # vérifie que le fichier a l'extension .p
                        print("Votre fichier doit terminer pas l'extension .p !")
                        file = input(">")
                    with open(str(file), "wb") as f:  # ouvre en mode écriture le fichier donné en input
                        prisonniers = {}
                        for gender in prison:
                            if gender != "taille":
                                for i in prison[gender]:
                                    for j in range(len(prison[gender][i]["prisonniers"])):
                                        prisonniers[gender] = prison[gender][i]["prisonniers"]
                        pickle.dump(prisonniers, f)

                        print("Sauvegarde effectuée !")
                elif choice == 4:  # l'utilisateur souhaite quitter le programme
                    print("Merci d'avoir utilisé notre programme !\n"
                          "Nous allons nous efforcer de garder les super vilains enfermés d'ici votre "
                          "prochaine visite.\n"
                          "En cas de problèmes, n'hésitez pas à consulter notre programme d'annuaire de "
                          "super-hérosTM !")
                    cond = False


menu_choice = menu()


"""
comments!!!!!!!!!!!!!!!!
function for try and except 
remove breaks !!!!!!!!!!
"""