# Import the tkinter library for GUI development
import tkinter as tk

# Import the analyze_log function from the main module
from main import analyze_log


LOG_FILE = "../eqlog_Halfskeleting_P1999Green.txt"


def run_analysis():
    results = analyze_log(LOG_FILE)

    # On efface les anciens résultats
    output.delete("1.0", tk.END)

    # On parcourt chaque monstre
    for monster, data in results["monsters"].items():

        output.insert(tk.END, f"Monster: {monster}\n")
        output.insert(tk.END, f"Kills: {data['kills']}\n\n")

        # Money
        output.insert(tk.END, "--- Money ---\n")

        if any(amount > 0 for amount in data["money"].values()):
            output.insert(
                tk.END,
                f"Platinum: {data['money']['platinum']}\n"
            )
            
            output.insert(
                tk.END,
                f"Gold: {data['money']['gold']}\n"
            )
            
            output.insert(
                tk.END,
                f"Silver: {data['money']['silver']}\n"
            )
            
            output.insert(
                tk.END,
                f"Copper: {data['money']['copper']}\n"
            )
        else:
            output.insert(tk.END, "No money looted\n")

        # Loot
        output.insert(tk.END, "\n--- Loot ---\n")

        if data["loot"]:
            for item, item_data in data["loot"].items():
                output.insert(
                    tk.END,
                    f"{item}: {item_data['count']}\n"
                )
        else:
            output.insert(tk.END, "No items looted\n")

        output.insert(tk.END, "\n----------------------------------------\n\n")


window = tk.Tk()

window.title("P99 Loot Analyzer")
window.geometry("800x600")

run_button = tk.Button(
    window,
    text="Run Analysis",
    command=run_analysis
)

run_button.pack(pady=10)

output = tk.Text(
    window,
    wrap="none"
)

output.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

window.mainloop()