import tkinter as tk
from tkinter import messagebox

# Initial State: (Farmer, Wolf, Goat, Cabbage) positions
items = ["farmer", "wolf", "goat", "cabbage"]
state = (False, False, False, False)

# Check if the current state is valid
def is_valid(state):
    if state[0] != state[2]:
        if state[1] == state[2]:
            return False
        elif state[2] == state[3]:
            return False
    return True

# Attempt to move the farmer and optionally an item
def move(state, item=None):
    new_state = list(state)
    new_state[0] = not new_state[0]  # Move farmer

    if item:
        idx = items.index(item)
        if state[idx] == state[0]:  # Must be on the same side
            new_state[idx] = not new_state[idx]
        else:
            return None  # Invalid move
    return tuple(new_state)

# Update the label to show current game state
def update_state_label():
    sides = {True: "Right", False: "Left"}
    text = (f"Farmer: {sides[state[0]]}, "
            f"Wolf: {sides[state[1]]}, "
            f"Goat: {sides[state[2]]}, "
            f"Cabbage: {sides[state[3]]}")
    dynamic_state_label.config(text=text)

# Game over popup
def game_over():
    global state
    answer = messagebox.askquestion("Game Over", "You failed! Retry?")
    if answer == "yes":
        state = (False, False, False, False)
        update_state_label()
    else:
        root.destroy()

# Handling moves
def make_move(item=None):
    global state
    new_state = move(state, item)
    if new_state and is_valid(new_state):
        state = new_state
        update_state_label()
        if state == (True, True, True, True):
            messagebox.showinfo("Congratulations!", "You won the game!")
            root.destroy()
    else:
        game_over()

# GUI Setup
root = tk.Tk()
root.title("Farmer and the Wolf, Goat, and Cabbage Game")
root.geometry("700x400")  # Increased height to accommodate the new label
root.configure(bg="#2e2e2e")  # Dark background

# Static label
static_state_label = tk.Label(root, text="Current state:", font=("Arial", 14), bg="#2e2e2e", fg="white")
static_state_label.pack(pady=(20, 5))  # Add some padding

# Dynamic label to show the real-time state
dynamic_state_label = tk.Label(root, text="", font=("Arial", 14, "bold"), bg="#2e2e2e", fg="#add8e6")  # Light blue for emphasis
dynamic_state_label.pack(pady=(0, 15))

# Frame for buttons
button_frame = tk.Frame(root, bg="#2e2e2e")
button_frame.pack(pady=10)

# Movement buttons
tk.Button(button_frame, text="Move Alone", command=lambda: make_move(), width=15, height=2).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Move with Wolf", command=lambda: make_move("wolf"), width=15, height=2).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Move with Goat", command=lambda: make_move("goat"), width=15, height=2).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Move with Cabbage", command=lambda: make_move("cabbage"), width=15, height=2).grid(row=0, column=3, padx=5)

# Quit button
tk.Button(root, text="Quit Game", command=root.destroy, width=20, height=2).pack(pady=20)

# Initialize state label
update_state_label()

# Start the GUI event loop
root.mainloop()