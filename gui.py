# Import the tkinter library for GUI development
import tkinter as tk
from tkinter import ttk

# Import the analyze_log function from the main module
from main import analyze_log


LOG_FILE = "../eqlog_Halfskeleting_P1999Green.txt"


# Fonction pour obtenir la couleur associée à chaque type de monnaie
def get_money_color(currency):
    
    if currency == "platinum":
        return "#7f8c8d"  # Gris foncé pour le platine
    
    elif currency == "gold":
        return "gold"
    
    elif currency == "silver":
        return "silver"
    
    elif currency == "copper":
        return "#CD7F32"


# Fonction pour créer une carte pour chaque monstre tué et afficher ses informations dans la GUI
def create_monster_card(monster, data, row, column):
    
    # Création d'un frame pour chaque monstre tué et l'associer à la grille des résultats
    monster_frame = tk.Frame(results_frame, borderwidth=2, relief="groove")

    # Positionnement de la carte dans la grille des résultats
    monster_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

    # Création d'un Frame pour le titre du monstre et le nombre de kills
    title_frame = tk.Frame(monster_frame)
    title_frame.pack(fill="x", padx=5, pady=2)
    
    # Création d'un label pour le nom du montre dans la section de gauche
    monster_label = tk.Label(title_frame, text=f"{monster}")
    monster_label.grid(row=0, column=0, sticky="w")
    
    monster_statut_kills = tk.Label(title_frame, text="Kills : ", font=("TkDefaultFont", 10))
    monster_statut_kills.grid(row=0, column=1, sticky="e")

    # Création d'un label pour le nombre de kills dans la section de droite
    kills_label = tk.Label(title_frame, text=data["kills"], font=("TkDefaultFont", 10, "bold"))
    kills_label.grid(row=0, column=2, sticky="e")
    
    title_frame.grid_columnconfigure(0, weight=1)
    
    # On ajoute un séparateur pour séparer visuellement le nom du monstre et les informations de loot
    separator = ttk.Separator(monster_frame, orient="horizontal")
    separator.pack(fill="x", padx=5, pady=5)
    
    # Affichage des items lootés
    loot_label = tk.Label(monster_frame, text="Looted Items :")
    loot_label.pack(anchor="w", padx=5)
    
    # Création d'un sous-frame pour les items lootés afin de les aligner correctement
    loot_frame = tk.Frame(monster_frame)
    loot_frame.pack(fill="x", padx=5)
    
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
        count_label = tk.Label(loot_frame, text=count, font=("TkDefaultFont", 10, "bold"))
        count_label.grid(row=item_row, column=1, sticky="e")
      
     
    separator = ttk.Separator(monster_frame, orient="horizontal")
    separator.pack(fill="x", padx=5, pady=5)
    
    # Affichage de la monnaie lootée
    if any(amount > 0 for amount in data["money"].values()):
                
        # Affichage de la monnaie lootée
        money_label = tk.Label(monster_frame, text="Money Looted :")
        money_label.pack(anchor="w", padx=5)    
        
        # Création d'un sous-frame pour l'argent looté afin de les aligner correctement
        money_frame = tk.Frame(monster_frame)    
        # Utilisation de fill="x" pour que le frame prenne toute la largeur disponible et de padx=5 pour ajouter un peu d'espace à gauche et à droite
        money_frame.pack(fill="x", padx=5)
        
        # La colonne des noms prend tout l'espace disponible
        money_frame.grid_columnconfigure(0, weight=1)
        
        # Pour chaque type de monnaie lootée, on crée un label pour le nom de la monnaie et un autre pour le montant reçu          
        for money_row, (currency, amount) in enumerate(data["money"].items()):
            
            color = get_money_color(currency)
            
            # On crée un label pour le nom qui va être aligner à gauche
            currency_label = tk.Label(money_frame, text=currency, fg=color, font=("TkDefaultFont", 10, "bold"))
            currency_label.grid(row=money_row, column=0, sticky="w")
            
            # On crée un label pour le montant qui va être aligner à gauche
            amount_label = tk.Label(money_frame, text=amount, font=("TkDefaultFont", 10, "bold"))
            amount_label.grid(row=money_row, column=1, sticky="e")
    
    else:
        # Si aucune monnaie n'a été lootée, on affiche un message indiquant qu'aucune monnaie n'a été lootée
        no_money_label = tk.Label(monster_frame, text="No money looted")
        no_money_label.pack(anchor="w", padx=5, pady=5)
        

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


# Initialisation de la fenêtre principale de l'application
window = tk.Tk()

window.title("P99 Loot Analyzer")

# Plus mince pour avoir deux cartes et peu espace de chaque bord, mais assez pour voir les cartes et les scrollbars si nécessaire
window.geometry("550x600")

# --- Bouton ---
run_button = tk.Button(
    window,
    text="Run Analysis",
    command=run_analysis
)

# Pack the button with some padding
run_button.pack(pady=10)

# --- Conteneur des résultats ---
main_window = tk.Frame(window)
main_window.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

# --- Canvas pour permettre le défilement ---
# Un canvas est une surface sur lequelle on peut placer des choses ou dessiner
canvas = tk.Canvas(main_window)
canvas.pack(
    side="left", 
    fill="both", 
    expand=True
)

# Création de l'object scrollbar et on l'associe au canvas pour permettre le défilement vertical
scrollbar = tk.Scrollbar(
    main_window,
    orient="vertical",
    command=canvas.yview
)

scrollbar.pack(
    side="right",
    fill="y"
)

# On configure le canvas pour qu'il utilise la scrollbar pour le défilement vertical
canvas.configure(
    yscrollcommand=scrollbar.set
)

# --- Frame qui contient les cartes ---
results_frame = tk.Frame(canvas)

canvas.create_window(
    (0, 0),
    window=results_frame,
    anchor="nw"
)

# Chaque fois que results_frame change de dimension, recalcule la zone qui peut être défilée.
results_frame.bind(
    "<Configure>",
    lambda event: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.bind_all(
    "<MouseWheel>",
    lambda event: canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )
)







window.mainloop()