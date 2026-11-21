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
            
            # On va maintenant calculer la moyenne d'argent reçu par kill pour chaque monstre tué si la somme d'argent reçu est supérieure à 0, sinon on mettra la moyenne à 0
            if total_money > 0:                
                # On redivise par 1000 pour avoir l'équivalent de la valeur en platinum avec 3 décimales qui vont représenter les valeurs gold, silver et copper restantes
                average_money = ( total_money / data["kills"] ) / 1000
                
                # On redivise par 1000 la somme d'argent reçu pour avoir l'équivalent de la valeur en platinum avec 3 décimales qui vont représenter les valeurs gold, silver et copper restantes
                total_money = total_money / 1000                
            
            # On va maintenant mettre à jour les colonnes fixes pour le total de l'argent reçu et la moyenne d'argent reçu par kill pour chaque monstre tué
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
            