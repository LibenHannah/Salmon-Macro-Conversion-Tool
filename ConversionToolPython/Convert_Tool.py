import tkinter as tk
import tkinter.ttk as ttk
import webbrowser
from tkinter import filedialog, messagebox
from convert_strategy import convert_dataset_v1_to_v2, export_data_v2_as_text
from convert_coordinate import convert_coordinate_v1_to_v2, save_output
import os
import sys


def open_link(url):
    webbrowser.open(url)

def center_window(win):
    win.update_idletasks()
    w = win.winfo_width()
    h = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (w // 2)
    y = (win.winfo_screenheight() // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")


GAMEMODES = [
    "Default", "Boss Rush", "Bounty", "Challenge", "Dungeon", "Event",
    "Infinite", "Legend Stage", "Odyssey", "Portal", "Raid", "Rift", "Story"
]

MAPS = [
    "All", "Blood Red Chamber", "Burning Spirit Tree", "Crystal Chapel",
    "Dark Tainted Tyrant", "Double Dungeon", "Edge of Heaven", "Frozen Volcano",
    "Golden Castle", "Hill of Swords", "Jeju Island", "Jojo", "Jojo 2",
    "Kuinshi Palace", "Lebereo Raid", "Martial Island", "Mountain Shrine",
    "Old Lobby", "Old Namek", "Planet Namek", "Planet Namek Spring",
    "Ruined City", "Rumbling Event", "Sand Village", "Shibuya Aftermath",
    "Shibuya Station", "Shining Castle", "Spider Forest", "Spirit Society",
    "Sun Temble", "The Land of Gods", "Underground Church"
]

MAP_FILTER = {
    "Default": "ALL",
    "Boss Rush": ["Blood Red Chamber", "Dark Tainted Tyrant", "Rumbling Event", "Shibuya Aftermath"],
    "Bounty": ["Burning Spirit Tree", "Crystal Chapel", "Double Dungeon", "Edge of Heaven",
               "Golden Castle", "Hill of Swords", "Kuinshi Palace", "Lebereo Raid", "Martial Island",
               "Planet Namek", "Sand Village", "Shibuya Aftermath", "Shibuya Station",
               "Shining Castle", "Spirit Society", "The Land of Gods", "Underground Church"],
    "Challenge": ["Burning Spirit Tree", "Crystal Chapel", "Double Dungeon", "Edge of Heaven",
                  "Golden Castle", "Hill of Swords", "Kuinshi Palace", "Lebereo Raid", "Martial Island",
                  "Planet Namek", "Sand Village", "Shibuya Aftermath", "Shibuya Station",
                  "Shining Castle", "Spirit Society", "The Land of Gods", "Underground Church"],
    "Dungeon": ["Frozen Volcano", "Jeju Island"],
    "Event": ["Double Dungeon", "Golden Castle", "Kuinshi Palace", "The Land of Gods",
              "Shining Castle", "Crystal Chapel", "Burning Spirit Tree", "Old Lobby", "Old Namek"],
    "Infinite": ["Double Dungeon", "Edge of Heaven", "Hill of Swords", "Lebereo Raid", "Martial Island",
                 "Planet Namek", "Sand Village", "Shibuya Station", "Spirit Society", "Underground Church"],
    "Legend Stage": ["Burning Spirit Tree", "Crystal Chapel", "Double Dungeon", "Golden Castle",
                     "Kuinshi Palace", "Sand Village", "Shibuya Aftermath", "Shining Castle", "The Land of Gods"],
    "Odyssey": ["Double Dungeon", "Planet Namek", "Sand Village", "Shibuya Aftermath", "Shibuya Station"],
    "Portal": ["Edge of Heaven", "Planet Namek Spring", "Sun Temple"],
    "Raid": ["Jojo", "Jojo 2", "Ruined City", "Spider Forest"],
    "Rift": ["Kuinshi Palace", "Mountain Shrine", "Underground Church"],
    "Story": ["Double Dungeon", "Edge of Heaven", "Hill of Swords", "Lebereo Raid", "Martial Island",
              "Planet Namek", "Sand Village", "Shibuya Station", "Spirit Society", "Underground Church"]
}

def update_map_combobox(gamemode, map_combobox):
    allowed = MAP_FILTER.get(gamemode, "ALL")

    if allowed == "ALL":
        map_combobox["values"] = MAPS
    else:
        map_combobox["values"] = allowed

    map_combobox.current(0)


def convert_coordinate_menu():
    popup = tk.Toplevel()
    popup.title("Convert Coordinate")
    popup.geometry("500x430")
    popup.resizable(False, False)
    popup.attributes("-topmost", True)
    popup.configure(bg="#f2f2f2")

    center_window(popup)

    selected_folder = tk.StringVar(value="No folder selected")
    gamemode_var = tk.StringVar(value="Default")
    map_var = tk.StringVar(value="All")

    frame = ttk.Frame(popup, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Convert Coordinate", font=("Segoe UI", 16, "bold")).pack(pady=10)

    ttk.Button(frame, text="Browse Folder", command=lambda: browse_folder(selected_folder)).pack(pady=5)
    ttk.Label(frame, textvariable=selected_folder, foreground="blue").pack(pady=3)

    ttk.Label(frame, text="Select Gamemode:", font=("Segoe UI", 11)).pack(pady=5)
    gamemode_cb = ttk.Combobox(frame, textvariable=gamemode_var, values=GAMEMODES, state="readonly")
    gamemode_cb.pack()

    ttk.Label(frame, text="Select Map:", font=("Segoe UI", 11)).pack(pady=5)
    map_cb = ttk.Combobox(frame, textvariable=map_var, values=MAPS, state="readonly")
    map_cb.pack()

    gamemode_cb.bind("<<ComboboxSelected>>", lambda e: update_map_combobox(gamemode_var.get(), map_cb))

    ttk.Button(
        frame,
        text="Convert Folder",
        command=lambda: convert_coordinate_action(popup, selected_folder, gamemode_var, map_var),
    ).pack(pady=20)


def convert_coordinate_action(popup, selected_folder, gamemode_var, map_var):

    folder_path = selected_folder.get().strip()
    if folder_path in ("", "No folder selected"):
        messagebox.showerror("Error", "Please select a folder.", parent=popup)
        return

    if not os.path.isdir(folder_path):
        messagebox.showerror("Error", "Selected folder does not exist.", parent=popup)
        return

    chosen_gamemode = gamemode_var.get()
    chosen_map = map_var.get()

    gamemode_folder = chosen_gamemode.replace(" ", "")
    map_folder = chosen_map.replace(" ", "_")

    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    output_dir = os.path.join(base_dir, "Data", "Config", gamemode_folder, map_folder)
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{map_folder}_Coordinate.txt")

    try:
        v2_text = convert_coordinate_v1_to_v2(folder_path)
        save_output(v2_text, output_file)

        messagebox.showinfo(
            "Success",
            f"Coordinate conversion complete!\nSaved at:\n\n{output_file}",
            parent=popup
        )

    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed:\n\n{e}", parent=popup)


def convert_strategy_menu():
    popup = tk.Toplevel()
    popup.title("Convert Strategy")
    popup.geometry("500x430")
    popup.resizable(False, False)
    popup.attributes("-topmost", True)
    popup.configure(bg="#f2f2f2")

    center_window(popup)

    selected_file = tk.StringVar(value="No file selected")
    gamemode_var = tk.StringVar(value="Default")
    map_var = tk.StringVar(value="All")

    frame = ttk.Frame(popup, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Convert Strategy", font=("Segoe UI", 16, "bold")).pack(pady=10)

    ttk.Button(frame, text="Browse Data V1 File", command=lambda: browse_file(selected_file)).pack(pady=5)
    ttk.Label(frame, textvariable=selected_file, foreground="blue").pack(pady=3)

    ttk.Label(frame, text="Select Gamemode:", font=("Segoe UI", 11)).pack(pady=5)
    gamemode_cb = ttk.Combobox(frame, textvariable=gamemode_var, values=GAMEMODES, state="readonly")
    gamemode_cb.pack()

    ttk.Label(frame, text="Select Map:", font=("Segoe UI", 11)).pack(pady=5)
    map_cb = ttk.Combobox(frame, textvariable=map_var, values=MAPS, state="readonly")
    map_cb.pack()

    gamemode_cb.bind("<<ComboboxSelected>>", lambda e: update_map_combobox(gamemode_var.get(), map_cb))

    ttk.Button(
        frame,
        text="Convert File",
        command=lambda: convert_strategy_action(popup, selected_file, gamemode_var, map_var),
    ).pack(pady=20)


def convert_strategy_action(popup, selected_file, gamemode_var, map_var):

    file_path = selected_file.get()
    if file_path == "No file selected":
        messagebox.showerror("Error", "Please select a file.", parent=popup)
        return

    if not os.path.exists(file_path):
        messagebox.showerror("Error", "Selected file does not exist.", parent=popup)
        return

    chosen_gamemode = gamemode_var.get()
    chosen_map = map_var.get()

    gamemode_folder = chosen_gamemode.replace(" ", "")
    map_folder = chosen_map.replace(" ", "_")

    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    output_dir = os.path.join(base_dir, "Data", "Config", gamemode_folder, map_folder)
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{map_folder}_Strategy.txt")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_lines = f.readlines()

        data_v2 = convert_dataset_v1_to_v2(raw_lines)
        export_data_v2_as_text(data_v2, output_file)

        messagebox.showinfo(
            "Success",
            f"Strategy conversion complete!\nSaved at:\n\n{output_file}",
            parent=popup
        )

    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed:\n\n{e}", parent=popup)


def browse_folder(var):
    path = filedialog.askdirectory(title="Select Folder")
    if path:
        var.set(path)


def browse_file(var):
    path = filedialog.askopenfilename(title="Select File", filetypes=[("Text Files", "*.txt")])
    if path:
        var.set(path)


def main_gui():

    window = tk.Tk()
    window.title("Conversion Tool")
    window.geometry("400x260")
    window.resizable(False, False)
    window.configure(bg="#f2f2f2")

    center_window(window)

    ttk.Style().theme_use("clam")

    frame = ttk.Frame(window, padding=20)
    frame.pack(fill="both", expand=True)

    ttk.Label(frame, text="Conversion Tool", font=("Segoe UI", 18, "bold")).pack(pady=15)

    ttk.Button(frame, text="Convert Strategy", width=22, command=convert_strategy_menu).pack(pady=8)
    ttk.Button(frame, text="Convert Coordinate", width=22, command=convert_coordinate_menu).pack(pady=8)

    bottom_bar = ttk.Frame(window)
    bottom_bar.pack(fill="x", side="bottom")

    status = ttk.Label(bottom_bar, text="Ready", anchor="w")
    status.pack(side="left", padx=10, pady=5)

    donate_frame = ttk.Frame(bottom_bar)
    donate_frame.pack(side="right", padx=10, pady=5)

    ttk.Label(
        donate_frame,
        text="Support the Developer ♥",
        font=("Segoe UI", 9, "bold")
    ).pack(anchor="e")

    donate_buttons = ttk.Frame(donate_frame)
    donate_buttons.pack(anchor="e")

    ttk.Button(
        donate_buttons,
        text="Robux",
        width=10,
        command=lambda: open_link("https://www.roblox.com/catalog?Category=3&Subcategory=55&CreatorName=PuellaLunae&salesTypeFilter=1")
    ).pack(side="left", padx=2)

    ttk.Button(
        donate_buttons,
        text="PayPal",
        width=10,
        command=lambda: open_link("https://www.paypal.com/paypalme/LunaePuella")
    ).pack(side="left", padx=2)

    status = ttk.Label(window, text="Ready", anchor="w")
    status.pack(fill="x", side="bottom")

    window.mainloop()


if __name__ == "__main__":
    main_gui()
