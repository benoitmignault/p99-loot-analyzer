# Import the tkinter library for GUI development
import tkinter as tk

# Import the analyze_log function from the main module
from main import analyze_log


LOG_FILE = "../eqlog_Halfskeleting_P1999Green.txt"


# Fonction pour créer une carte pour chaque monstre tué et afficher ses informations dans la GUI
def create_monster_card(monster, data, row, column):
    
    # Création d'un frame pour chaque monstre tué et l'associer à la grille des résultats
    monster_frame = tk.Frame(results_frame, borderwidth=2, relief="groove")

    # Positionnement de la carte dans la grille des résultats
    monster_frame.grid(row=row, column=column, padx=10, pady=10)

    # Affichage du nom du monstre et du nombre de kills
    monster_label = tk.Label(monster_frame, text=f"{monster} - Kills : {data['kills']}")    
    # .pack est utilisé pour empiller les widgets les uns sur les autres, ici on l'utilise pour afficher le nom du monstre et le nombre de kills
    monster_label.pack(anchor="w", padx=5, pady=2)

    # Affichage des items lootés
    loot_label = tk.Label(monster_frame, text="Looted Items :")
    loot_label.pack(anchor="w", padx=5)
    
    # Création d'un sous-frame pour les items lootés afin de les aligner correctement
    loot_frame = tk.Frame(monster_frame)
    loot_frame.pack(anchor="w", padx=5)
    
    # La colonne des noms prend tout l'espace disponible
    loot_frame.grid_columnconfigure(0, weight=1)

    # Pour chaque item looté, on crée un label pour le nom de l'item et un autre pour le nombre de fois qu'il a été looté
    for item_row, (item, count) in enumerate(data["loot"].items()):
        
        count = count["count"]        
        # Utilisation de ancre="w" pour aligner le texte à gauche dans le label
        item_label = tk.Label(loot_frame, text=item)
        # Utilisation de sticky="w" pour aligner le label à gauche dans la grille
        item_label.grid(row=item_row, column=0, sticky="w")
        
        # Utilisation de ancre="e" pour aligner le texte à droite dans le label
        count_label = tk.Label(loot_frame, text=count)
        count_label.grid(row=item_row, column=1, sticky="e")
      
            
    # Affichage de la monnaie lootée
    money_label = tk.Label(monster_frame, text="Money Looted :")
    money_label.pack(anchor="w", padx=5)    
    
    # Création d'un sous-frame pour l'argent looté afin de les aligner correctement
    money_frame = tk.Frame(monster_frame)
    money_frame.pack(anchor="w", padx=5)
    
    # Pour chaque type de monnaie lootée, on crée un label pour le nom de la monnaie et un autre pour le montant reçu          
    for money_row, (currency, amount) in enumerate(data["money"].items()):
       
        # On crée un label pour le nom qui va être aligner à gauche
        currency_label = tk.Label(money_frame, text=currency.capitalize())
        currency_label.grid(row=money_row, column=0)
        
        amount_label = tk.Label(money_frame, text=amount)
        amount_label.grid(row=money_row, column=1)
        

# Function to run the analysis and display results in the GUI
def run_analysis():
    results = analyze_log(LOG_FILE)

    # Efface les résultats précédents
    for widget in results_frame.winfo_children():
        widget.destroy()

    # Le positionnement des cartes dans la grille au départ est en haut à gauche (0, 0)
    row = 0
    column = 0
    
    # Pour chaque montre tué, on va crééer une grid pour afficher le montre et ses loot
    for monster, data in results["monsters"].items():
        
        # On crée une carte pour chaque monstre tué et on l'affiche dans la grille
        create_monster_card(monster, data, row, column)

        # On incrémente la colonne pour la prochaine carte
        column += 1
        
        # Si on a atteint 2 colonnes, on passe à la ligne suivante et on réinitialise la colonne à 0
        if column == 2:
            column = 0
            row += 1 # ligne suivante
                

    # Pour l'instant, on va juste vérifier qu'on reçoit bien results
    print(results)


window = tk.Tk()

window.title("P99 Loot Analyzer")
window.geometry("800x600")

# --- Bouton ---
run_button = tk.Button(
    window,
    text="Run Analysis",
    command=run_analysis
)

# Pack the button with some padding
run_button.pack(pady=10)

# --- Conteneur des résultats ---
results_frame = tk.Frame(window)

results_frame.pack(
    # Étends results_frame horizontalement ET verticalement.
    fill="both", 
    expand=True,
    padx=10,
    pady=10
)

window.mainloop()