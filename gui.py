# Import the tkinter library for GUI development
import tkinter as tk

window = tk.Tk()

window.title("P99 Loot Analyzer")
window.geometry("800x600")

label = tk.Label(
    window,
    text="P99 Loot Analyzer",
    font=("Arial", 20)
)

label.pack(pady=20)

window.mainloop()