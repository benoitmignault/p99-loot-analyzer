import csv

# Fonction pour exporter les résultats au format CSV
# Cette fonction sera appeller par le GUI et son bouton "Export to CSV"
def export_csv(results, filename):
    
    # Une liste des colonnes dynamiques pour les items lootés, on va les ajouter après les colonnes fixes
    # set conserve uniquement les valeurs uniques, donc si un item est looté plusieurs fois, 
    # il ne sera ajouté qu'une seule fois à la liste des colonnes dynamiques
    header_item_columns = set()
            
    # Étape 1 — trouver les colonnes d'items
    for monster, data in results["monsters"].items():

        # On va déterminer les colonnes dynamiques pour les items lootés, on va les ajouter après les colonnes fixes
        for item in data["loot"].keys():
            header_item_columns.add(item)            
    
    # Étape 2 - Trier les colonnes d'items pour qu'elles apparaissent dans un ordre cohérent dans le fichier CSV
    header_item_columns = sorted(header_item_columns)
    
    # Étape 3 - Créer les colonnes fixes du CSV
    headers = [
        "Monster",
        "Kills",
        "Platinum",
        "Gold",
        "Silver",
        "Copper",
        # 2026-08-31, on va ajouter le total de l'argent reçu pour chaque monstre tué et la moyenne d'argent reçu par kill pour chaque monstre tué
        "Total Money",
        "Average Money"        
    ]
    
    # Étape 4 - Ajouter les colonnes dynamiques pour les items lootés
    headers.extend(header_item_columns)
    
    # Étape 5 - Écrire les données dans le fichier CSV
    with open(filename, "w", newline="", encoding="utf-8") as file:        
                
        # Création de l'object writer pour écrire dans le fichier CSV
        writer = csv.writer(file)
        
        # Étape 6 - Écrire les en-têtes dans le fichier CSV
        writer.writerow(headers)
        
        # Étape 7 — Créer une ligne pour chaque monstre
        for monster, data in results["monsters"].items():
            
            # Étape 7.1 - On commence par les colonnes fixes pour chaque monstre : Monster, Kills, platinum, gold, silver, copper     
            row = [
                monster,
                data["kills"],
                data["money"]["platinum"],
                data["money"]["gold"],
                data["money"]["silver"],
                data["money"]["copper"]
            ]
            
            # Initialisation des variables total_money et average_money pour chaque monstre tué
            total_money = 0
            average_money = 0
            
            # Étape 7.2 - On va calculer le total de l'argent reçu pour chaque monstre tué et la moyenne d'argent reçu par kill pour chaque monstre tué
            # Les calculs seront effectués en convertissant l'argent reçu en cuivre pour faciliter les calculs
            total_money = (
                data["money"]["platinum"] * 1000 +
                data["money"]["gold"] * 100 +
                data["money"]["silver"] * 10 +
                data["money"]["copper"]
            )
            
            # On va maintenant calculer la moyenne d'argent reçu par kill pour chaque monstre tué si la somme d'argent reçu est supérieure à 0, sinon on mettra la moyenne à 0
            if total_money > 0:                
                # On redivise par 1000 pour avoir l'équivalent de la valeur en platinum avec 3 décimales qui vont représenter les valeurs gold, silver et copper restantes
                average_money = ( total_money / data["kills"] ) / 1000
                
                # On redivise par 1000 la somme d'argent reçu pour avoir l'équivalent de la valeur en platinum avec 3 décimales qui vont représenter les valeurs gold, silver et copper restantes
                total_money = total_money / 1000                
            
            # On va maintenant mettre à jour les colonnes dynamiques pour le total de l'argent reçu et la moyenne d'argent reçu par kill pour chaque monstre tué
            row.append(f"{total_money:.3f}")
            row.append(f"{average_money:.3f}")
            
            # Étape 8 - Pour chaque item looté, on ajoute le nombre de fois qu'il a été looté pour ce monstre, sinon on ajoute 0
            for item in header_item_columns:

                # On va chercher le nombre de fois qu'un item a été looté pour ce monstre, sinon on met 0
                item_data  = data["loot"].get(item, {"count": 0})
                count = item_data["count"]
                row.append(count)
                
            # Étape 9 - Écrire la ligne
            writer.writerow(row)
            