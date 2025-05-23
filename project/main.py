import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from collections import deque


root = tk.Tk()
root.withdraw()

# Elements 
items = ["farmer", "wolf", "goat", "cabbage"]
state = (False, False, False, False)
initial_state = (False, False, False, False)

# Uploading Images 
images = {}
for item in items:
    img = Image.open(f"{item}.png").resize((50, 60))
    images[item] = ImageTk.PhotoImage(img)

bg_img = Image.open("river2.png").resize((600, 500))
images['bg'] = ImageTk.PhotoImage(bg_img)

root.deiconify()

# Elements Position 
custom_positions = {
    "farmer": {False: (80, 310), True: (520, 290)},
    "wolf": {False: (80, 250), True: (420, 250)},
    "goat": {False: (40, 290), True: (490, 260)},
    "cabbage": {False: (40, 340), True: (520, 340)},
}

# Valid or Not 
def is_valid(state):
    if state[0] != state[2]:
        if state[1] == state[2] or state[2] == state[3]:
            return False
    return True

# Upgating andMaking Move 
def move(state, item=None):
    new_state = list(state)
    new_state[0] = not new_state[0]
    if item:
        idx = items.index(item)
        if state[idx] == state[0]:
            new_state[idx] = not new_state[idx]
        else:
            return None
    return tuple(new_state)

#  Possible Moves
def get_possible_moves(state):
    moves = []
    farmer_move = move(state)
    if farmer_move and is_valid(farmer_move):
        moves.append((farmer_move, "Farmer moves alone"))

    for item in ["wolf", "goat", "cabbage"]:
        move_with_item = move(state, item)
        if move_with_item and is_valid(move_with_item):
            moves.append((move_with_item, f"Farmer moves with {item}"))
    return moves

# updating GUI
def update_canvas():
    canvas.delete("all")
    canvas.create_image(0, 0, image=images['bg'], anchor=tk.NW)
    for i, item in enumerate(items):
        side = state[i]
        x, y = custom_positions[item][side]
        canvas.create_image(x, y, image=images[item], anchor=tk.NW)

# Endig
def game_over():
    global state
    answer = messagebox.askquestion("Game Over", "You Failed! Retry?")
    if answer == "yes":
        state = (False, False, False, False)
        update_canvas()
    else:
        root.destroy()

# moves
def make_move(item=None):
    global state
    new_state = move(state, item)
    if new_state and is_valid(new_state):
        state = new_state
        update_canvas()
        if state == (True, True, True, True):
            messagebox.showinfo("Congratulations!", "You Won the game!")
            root.destroy()
    else:
        game_over()

# starting Gui
def start_game():
    start_frame.pack_forget()
    game_frame.pack()
    update_canvas()
    print("Switched to game screen")
    for widget in game_frame.winfo_children():
        print(widget)


#bfs
def show_solution():
    solution_steps = []

    def solve_for_gui(initial_state):
        queue = deque()
        queue.append((initial_state, []))
        visited = set()

        while queue:
            current_state, path = queue.popleft()

            if current_state == (True, True, True, True):
                return path

            visited.add(current_state)

            for next_state, action in get_possible_moves(current_state):
                if next_state not in visited:
                    queue.append((next_state, path + [(next_state, action)]))
        return None

    solution_steps = solve_for_gui(initial_state)

    if not solution_steps:
        messagebox.showerror("Error", "❌ No solution found.")
        return

    def animate_solution(steps, index=0):
        global state
        if index < len(steps):
            new_state, action = steps[index]
            state = new_state
            update_canvas()
            root.after(1000, animate_solution, steps, index + 1)
        else:
            messagebox.showinfo("🎉 Congratulations!", "The solution has been completed!")

    animate_solution(solution_steps)
    
     
root.title("Farmer and the Wolf, Goat, and Cabbage Game")
root.geometry("700x600")
root.configure(bg="#2e2e2e")

# Starting frame
start_frame = tk.Frame(root, width=700, height=800)
start_frame.pack()

start_bg = tk.Label(start_frame, image=images['bg'])
start_bg.place(x=0, y=0, relwidth=1, relheight=1)

welcome_label = tk.Label(start_frame, text="Farmer and the Wolf, Goat, and Cabbage Game", font=("Arial", 20, "bold"))
welcome_label.pack(pady=60)

start_btn = tk.Button(start_frame, text="Start Game", font=("Arial", 14), bg="#2e2e2e", fg="#add8e6", command=start_game, width=15, height=2)
start_btn.pack(pady=20)

exit_btn = tk.Button(start_frame, text="Exit", font=("Arial", 14), bg="#2e2e2e", fg="#add8e6", command=root.destroy, width=15, height=2)
exit_btn.pack(pady=10)

# Game frame 
game_frame = tk.Frame(root)
canvas = tk.Canvas(game_frame, width=600, height=400)
canvas.pack()

# moving buttons  
button_frame = tk.Frame(game_frame)
button_frame.pack(pady=10)

btns = [
    ("Move alone", None),
    ("With wolf", "wolf"),
    ("With goat ", "goat"),
    ("With cabbage", "cabbage")
]

for i, (text, item) in enumerate(btns):
    tk.Button(button_frame, text=text, command=lambda itm=item: make_move(itm), width=15, height=2,  bg="#2e2e2e", fg="#add8e6").grid(row=0, column=i, padx=3)

# Restart Button   
restart_btn = tk.Button(game_frame, text="Restart",  bg="#2e2e2e", fg="#add8e6", command=lambda: [globals().update(state=(False, False, False, False)), update_canvas()], width=20, height=2)
restart_btn.pack(pady=5)

# AI Solvng Button 
solve_btn = tk.Button(game_frame, text="Solve Automatically", bg="#2e2e2e", fg="#add8e6", command=show_solution, width=20, height=2)
solve_btn.pack(pady=20)

root.mainloop()
