import re

# Log file to analyze
# On doit modifier le chemin du fichier de log à analyser en fonction du stockage du project dans un dossier .git et l'emplacement du fichier sur votre système
# Ce chemin est hardocodé à des fins de tests, il faut executer l'interface graphique pour choisir le fichier de log à analyser ou l'executable créé via la distribution
LOG_FILE = "../eqlog_Halfskeleting_P1999Green.txt"


# Fonction pour extraire le nom du monstre tué d'une ligne de log
def extract_slain_monster(line):

    # Situation où le joueur qui roule le script kill le monstre
    if "You have slain " in line:
                
        # rstrip retire les espaces et les characters fournis en paramètres       
        return line.split("You have slain ")[1].strip().rstrip("!")

    # Il va arriver que le joueur ne soit pas celui qui a tué le monstre, mais un autre joueur ou un animal charmé si le joueur est assez proche pour voir le message de monstre tué, on va donc vérifier si la ligne contient " has been slain by " et extraire le nom du monstre tué
    elif " has been slain by " in line:     
        return line.split("] ", 1)[1].split(" has been slain by ", 1)[0].strip()

    return None


# Fonction pour vérifier si le monstre est déjà dans le dictionnaire, sinon on crée sa structure et on incrémente le compteur de kills
def add_monster_kill(results, monster):
    
    # Vérification si le monstre est déjà dans le dictionnaire,
    # sinon on crée sa structure
    if monster not in results["monsters"]:

        results["monsters"][monster] = {
            "kills": 0,
            "loot": {},
            "money": {
                "platinum": 0,
                "gold": 0,
                "silver": 0,            
                "copper": 0
            }
        }

    # On incrémente toujours le compteur de kills
    results["monsters"][monster]["kills"] += 1

   
# Fonction pour extraire l'item looté d'une ligne de log
def extract_looted_item(line):

    # Les items lootés par le joueur du fichier de log
    if "You have looted " in line:
        item = line.split("You have looted ")[1].strip().rstrip(".--")
        
        # Finalement, on va retirer le "a " ou "an " devant le nom de l'item pour ne garder que le nom de l'item
        if item.startswith("a "):
            item = item[2:]
        elif item.startswith("an "):
            item = item[3:]        
        
        return item

    # Les items lootés par d'autres joueurs du fichier de log
    elif " has looted " in line:
        item = line.split(" has looted ")[1].strip().rstrip(".--")
        
        # Finalement, on va retirer le "a " ou "an " devant le nom de l'item pour ne garder que le nom de l'item
        if item.startswith("a "):
            item = item[2:]
        elif item.startswith("an "):
            item = item[3:]
        return item
    
    # Si la ligne ne contient aucun item looté, on retourne None
    return None   
   

# Fonction pour ajouter un item looté au dictionnaire des résultats
def add_looted_item(results, monster, item):

    # Vérification si l'item existe déjà dans la liste de loot du monstre
    if item not in results["monsters"][monster]["loot"]:

        # Création du sous-objet pour le nouvel item
        results["monsters"][monster]["loot"][item] = {
            "count": 0
        }

    # On incrémente toujours le compteur de cet item
    results["monsters"][monster]["loot"][item]["count"] += 1


# Fonction pour extraire si nous avons une ligne contenant de l'argent reçu à partir d'une ligne de log
def extract_money(line):
    
    # On initialise un dictionnaire pour stocker les montants d'argent reçus
    money = {}
    
    # On vérifie si la ligne contient de l'argent reçu d'un cadavre et non d'un vendeur ou d'une autre source
    if "You receive " in line and " from the corpse" in line:
        
        # On définit les différentes monnaies que nous voulons extraire
        currencies = [
            "platinum",
            "gold",
            "silver",
            "copper"
        ]
        
        # On initialise un dictionnaire pour stocker les montants d'argent reçus
        money = {
            "platinum": 0,
            "gold": 0,
            "silver": 0,            
            "copper": 0
        }
        
        # Pour chaque 
        for currency in currencies:

            match = re.search(rf"(\d+) {currency}", line)

            if match:
                money[currency] = int(match.group(1))
    
    # On va retourne le dictionnaire vide ou avec des valeurs
    return money

 
# Fonction pour ajouter l'argent reçu au dictionnaire des résultats au montre correspondant
def add_money(results, monster, money):
    
    # On ajoute l'argent reçu au monstre correspondant dans le dictionnaire des résultats
    for currency, amount in money.items():
        results["monsters"][monster]["money"][currency] += amount
    
  
# Fonction pour trier les résultats de manière décroissante pour chaque monstre tué, en fonction du nombre de kills et du nombre d'items lootés
def sort_results(results):
    
    # On va faire un triage des résultats de manière décroissante pour chaque monstre tué, en fonction du nombre de kills
    results["monsters"] = dict(
        sorted(
            results["monsters"].items(), 
            key=lambda x: x[1]["kills"], 
            reverse=True
        )
    )
    
    # On va maintenant faire un triage des items lootés pour chaque monstre tué, en fonction du nombre de loot pour chaque item
    for monster, data in results["monsters"].items():
        data["loot"] = dict(
            sorted(
                data["loot"].items(), 
                # Pour chaque élément, regarde cette valeur et utilise-la pour faire le tri.
                # x    -> ("a Bear Meat", {"count": 6})
                # x[0] -> "a Bear Meat"
                # x[1] -> {"count": 6}
                # x[1]["count"] -> 6
                # lambda veut dire -> Pour chaque loot : regarde son count et utilise ce count pour déterminer son ordre
                key=lambda x: x[1]["count"], 
                reverse=True
            )
        )

    
# Fonction pour lire le fichier de log et compter le nombre de fois qu'un monstre spécifique est tué et les items lootés et l'argent reçu
def analyze_log(log_file):
    
    # On initialise un dictionnaire pour stocker les résultats
    results = {
        "monsters": {} # On va créer des sous objects pour chaque monstre avec le nombre de kills et les items lootés
    }
    
    # On initialise une variable pour garder la trace du monstre actuel
    current_monster = None
    
    # Variable pour la gestion si un pet fait la job ou en partie
    pet_active = False
    pet_target = None
    
    print("DEBUG : analyze_log() a commencé", flush=True)
    
    # On ouvre le fichier de log en lecture
    with open(log_file, "r", encoding="utf-8") as file:
        
        # On parcourt chaque ligne du fichier de log
        for line in file:
            
            # 2026-09-05, une situation que je n'avais pas encore prise en compte, c'est lorsque le monstre est tué par un pet charmé
            # On vérifie si la ligne contient l'information sur un animal charmé dans un premier temps
            if " tells you, 'Attacking " in line and " Master.'" in line:
                #print(f"DEBUG : Ligne de log avec un pet actif détectée : {line.strip()}", flush=True)
                                                
                # Si nous avons le message, on doit resetter les variables du pet car on garde le principe que le pet va tuer un monstre à la fois, 
                # donc si nous avons un message de pet actif, on va resetter les variables du pet pour le prochain monstre tué
                if pet_active or pet_target:
                    pet_active = False
                    pet_target = None
                    current_monster = None # Je dois remettre current_monster à None car le pet a tué un monstre et nous devons attendre le prochain message de pet actif pour savoir quel monstre il va tuer ensuite
                
                # On extrait le nom de l'attaquant
                # On extrait le nom de l'attaquant
                # attacker = line.split(" tells you, 'Attacking ", 1)[0].strip()
                # On commence par spliter en deux [.....] et le rester de la ligne, puis on split encore une fois pour obtenir le nom de l'attaquant
                attacker = line.split("] ", 1)[1].split(" tells you, 'Attacking ", 1)[0].strip()
                #print(f"DEBUG : Attacker: {attacker}", flush=True)   
                # Seulement un animal charmé, pas le pet d'un joueur qui aura un prénom avec une majuscule, on va vérifier si le premier caractère du nom de l'attaquant est en minuscule
                if attacker and attacker[0].islower():
                    pet_active = True
                    pet_target = line.split(" tells you, 'Attacking ")[1].split(" Master.'")[0].strip()
                    #print(f"DEBUG : Pet actif détecté : {attacker} avec la cible : {pet_target}", flush=True)            
            
            # On vérifie si la ligne contient la situation d'un monstre tué par un joueur ou l'autre ou un animal charmé qu'on est à proximité
            monster = extract_slain_monster(line)

            # On ajoute le monstre tué au dictionnaire des résultats, 
            # si le monstre n'existe pas, on le crée et on incrémente le compteur de kills
            if monster:
                
                # TODO : 2026-09-05, on doit trouver une maniere ajouter le monstre tué par le animal charmé, si nous sommes trop loin
                add_monster_kill(results, monster)
                
                # On garde ce monstre comme monstre actuel pour garder l'association avec les items lootés et l'argent reçu
                current_monster = monster
                continue
            
            # On va valider si la ligne contient de l'argent reçu ou un item looté.                        
            # On vérifie si la ligne contient de l'argent reçu
            money = extract_money(line)
                        
            # On vérifie si la ligne contient un item looté
            item = extract_looted_item(line)
            
            # Si nous avons un item looté ou de l'argent reçu, on va les ajouter au dictionnaire des résultats pour le monstre actuel
            if item or money:
                
                # Situation où le monstre tué est inconnu, mais que le pet est actif et qu'il a un target, on va utiliser le target du pet comme monstre actuel
                if current_monster is None and pet_active and pet_target:
                    current_monster = pet_target
                    
                    # On doit passer la fonction add_monster_kill pour créer le monstre dans le dictionnaire des résultats, sinon nous allons avoir une erreur car le monstre n'existe pas encore
                    add_monster_kill(results, current_monster)

                # On ajoute l'argent reçu au dictionnaire des résultats si elle information est présente, sinon on ne fait rien
                if money:
                    add_money(results, current_monster, money)
                    continue
                
                # On ajoute l'item looté au dictionnaire des résultats,
                # si l'item n'existe pas, on le crée et on incrémente le compteur de loot
                if item:
                    add_looted_item(results, current_monster, item)
                    continue        
                
            # Il reste la situation où nous avons un monstre tué, mais aucun item looté ou argent reçu, mais qu'on doit ajouter +1 au kill du monstres
            # TODO : 2026-09-05, on doit trouver une maniere ajouter le monstre tué par le animal charmé, 
            # si nous sommes trop loin, mais que nous avons un message de pet actif, on va utiliser le target du pet comme monstre actuel
            
    # On va trier les résultats de manière décroissante pour chaque monstre tué, en fonction du nombre de kills et du nombre d'items lootés
    sort_results(results)   
         
    return results


# Fonction pour afficher les résultats de l'analyse du fichier de log
def print_results(results):

    print("\n========== P99 LOOT ANALYZER ==========")

    for monster, data in results["monsters"].items():
        
        # Affichage du montre et du nombre de kills
        print(f"\nMonster: {monster}")
        print(f"Kills: {data['kills']}")

        # Affichage de l'argent looté
        print("\n--- Money ---")
        if any(amount > 0 for amount in data["money"].values()):
            
            print(f"Platinum: {data['money']['platinum']}")
            print(f"Gold: {data['money']['gold']}")
            print(f"Silver: {data['money']['silver']}")
            print(f"Copper: {data['money']['copper']}")
        else:
            print("No money looted")
           
        # Affichage des items lootés 
        print("\n--- Loot ---")

        if data["loot"]:

            for item, item_data in data["loot"].items():
                print(f"{item}: {item_data['count']}")

        else:
            print("No items looted")

        print("\n----------------------------------------")
        
        
# Main execution
if __name__ == "__main__":

    results = analyze_log(LOG_FILE) 
    sort_results(results)
    print_results(results)