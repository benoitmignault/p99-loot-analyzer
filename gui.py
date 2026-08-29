# Import the tkinter library for GUI development
import tkinter as tk

# Import the analyze_log function from the main module
from main import analyze_log


LOG_FILE = "../eqlog_Halfskeleting_P1999Green.txt"


# Fonction pour créer une carte pour chaque monstre tué et afficher ses informations dans la GUI
def create_monster_card(monster, data, row, column):
    
    # Création d'un frame pour chaque monstre tué
    monster_frame = tk.Frame(
        results_frame,
        borderwidth=2,
        relief="groove"
    )

    # Positionnement de la carte dans la grille des résultats
    monster_frame.grid(
        row=row,
        column=column,
        padx=10,
        pady=10
    )

    # Affichage du nom du monstre et du nombre de kills
    monster_label = tk.Label(monster_frame, text=f"{monster} - Kills: {data['kills']}")
    monster_label.pack(anchor="w", padx=5, pady=2)

    # Affichage des items lootés
    loot_label = tk.Label(monster_frame, text="Looted Items:")
    loot_label.pack(anchor="w", padx=5)

    for item, count in data["loot"].items():
        item_label = tk.Label(monster_frame, text=f"  {item}: {count}")
        item_label.pack(anchor="w", padx=15)
    
    # Affichage de l'argent looté
    money_label = tk.Label(monster_frame, text="Money Looted:")
    money_label.pack(anchor="w", padx=5)
    
    for currency, amount in data["money"].items():
        money_item_label = tk.Label(monster_frame, text=f"  {currency.capitalize()}: {amount}")
        money_item_label.pack(anchor="w", padx=15)
        

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