import re

# Log file to analyze
# On doit modifier le chemin du fichier de log à analyser en fonction du stockage du project dans un dossier .git et l'emplacement du fichier sur votre système
LOG_FILE = "../eqlog_Halfskeleting_P1999Green.txt"


# Fonction pour extraire le nom du monstre tué d'une ligne de log
def extract_slain_monster(line):
    
    if "You have slain " in line:
                
        # rstrip retire les espaces et les characters fournis en paramètres       
        return line.split("You have slain ")[1].strip().rstrip("!")

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
        return item

    # Les items lootés par d'autres joueurs du fichier de log
    elif " has looted " in line:
        item = line.split(" has looted ")[1].strip().rstrip(".--")
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
    
        
# Fonction pour lire le fichier de log et compter le nombre de fois qu'un monstre spécifique est tué et les items lootés et l'argent reçu
def analyze_log_file(log_file):
    
    # On initialise un dictionnaire pour stocker les résultats
    results = {
        "monsters": {} # On va créer des sous objects pour chaque monstre avec le nombre de kills et les items lootés
    }
    
    # On initialise une variable pour garder la trace du monstre actuel
    current_monster = None
    
    # On ouvre le fichier de log en lecture
    with open(log_file, "r", encoding="utf-8") as file:
        
        # On parcourt chaque ligne du fichier de log
        for line in file:
                
            # On vérifie si la ligne contient la situation d'un monstre tué
            monster = extract_slain_monster(line)

            # On ajoute le monstre tué au dictionnaire des résultats, 
            # si le monstre n'existe pas, on le crée et on incrémente le compteur de kills
            if monster:                
                add_monster_kill(results, monster)
                
                # On garde ce monstre comme monstre actuel pour garder l'association avec les items lootés et l'argent reçu
                current_monster = monster
                continue
            
            # On vérifie si la ligne contient un item looté
            item = extract_looted_item(line)
            
            # On ajoute l'item looté au dictionnaire des résultats,
            # si l'item n'existe pas, on le crée et on incrémente le compteur de loot
            if item:
                add_looted_item(results, current_monster, item)
                continue

            # On vérifie si la ligne contient de l'argent reçu et on prépare le dictionnaire money pour l'ajouter au monstre correspondant
            money = extract_money(line)

            # On ajoute l'argent reçu au dictionnaire des résultats si elle information est présente, sinon on ne fait rien
            if money:
                add_money(results, current_monster, money)
                continue
                
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

    results = analyze_log_file(LOG_FILE)    
    print_results(results)