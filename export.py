import csv

# Fonction pour exporter les résultats au format CSV
# Cette fonction sera appeller par le GUI et son bouton "Export to CSV"
# Format groupé : une ligne par item looté ; les informations du monstre (kills, argent)
# apparaissent seulement sur la première ligne de son bloc, les lignes suivantes laissent ces colonnes vides
def export_csv(results, filename):
    
    # Étape 1 - Créer les colonnes du CSV : les informations du monstre, puis le détail de chaque item looté
    headers = [
        "Monster",
        "Kills",
        "Platinum",
        "Gold",
        "Silver",
        "Copper",
        # Le total de l'argent reçu pour chaque monstre tué et la moyenne d'argent reçu par kill
        "Total Money",
        "Average Money",
        # Le détail des items lootés : un item par ligne, avec son nombre de fois looté et son pourcentage de drop
        "Item",
        "Count",
        "Drop %"
    ]
    
    # Étape 2 - Écrire les données dans le fichier CSV
    with open(filename, "w", newline="", encoding="utf-8") as file:        
                
        # Création de l'object writer pour écrire dans le fichier CSV
        writer = csv.writer(file)
        
        # Étape 3 - Écrire les en-têtes dans le fichier CSV
        writer.writerow(headers)
        
        # Étape 4 — Créer les lignes pour chaque monstre
        for monster, data in results["monsters"].items():
            
            # Étape 4.1 - On calcule le total de l'argent reçu pour ce monstre tué et la moyenne d'argent reçu par kill
            # Les calculs seront effectués en convertissant l'argent reçu en cuivre pour faciliter les calculs
            total_money = (
                data["money"]["platinum"] * 1000 +
                data["money"]["gold"] * 100 +
                data["money"]["silver"] * 10 +
                data["money"]["copper"]
            )
            
            # On redivise par 1000 pour avoir l'équivalent de la valeur en platinum avec 3 décimales qui vont représenter les valeurs gold, silver et copper restantes
            total_money = total_money / 1000
            
            # On calcule la moyenne d'argent reçu par kill pour ce monstre, si le nombre de kills est supérieur à 0
            average_money = total_money / data["kills"] if data["kills"] > 0 else 0
            
            # Étape 4.2 - On prépare les informations du monstre, qui iront sur la première ligne de son bloc
            monster_row = [
                monster,
                data["kills"],
                data["money"]["platinum"],
                data["money"]["gold"],
                data["money"]["silver"],
                data["money"]["copper"],
                f"{total_money:.3f}",
                f"{average_money:.3f}"
            ]
            
            # Étape 4.3 - Une ligne par item looté pour ce monstre
            if data["loot"]:
                
                # La première ligne du bloc porte les informations du monstre, les suivantes laissent ces colonnes vides
                first_row = True
                
                for item, item_data in data["loot"].items():
                    
                    count = item_data["count"]
                    
                    # Le pourcentage de drop de l'item pour ce monstre, avec 1 décimale
                    drop_rate = (count / data["kills"]) * 100 if data["kills"] > 0 else 0
                    
                    if first_row:
                        writer.writerow(monster_row + [item, count, f"{drop_rate:.1f}"])
                        first_row = False
                    else:
                        writer.writerow(["", "", "", "", "", "", "", "", item, count, f"{drop_rate:.1f}"])
            
            else:
                # Aucun item looté pour ce monstre : une seule ligne avec ses informations, sans item
                # Correction de l'indentation pour que cette ligne soit écrite correctement dans le CSV
                writer.writerow(monster_row + ["", "", ""])
