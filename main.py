import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from itertools import permutations
import re
import networkx as nx



def is_safe(board, row, col):
    for i in range(col):
        if board[i] == row or board[i] - i == row - col or board[i] + i == row + col:
            return False
    return True


def solve_n_queens_util(board, col, solutions):
    N = len(board)
    if col >= N:
        solutions.append(board[:])
        return

    for row in range(N):
        if is_safe(board, row, col):
            board[col] = row
            solve_n_queens_util(board, col + 1, solutions)
            board[col] = -1


def solve_n_queens(N):
    board = [-1] * N
    solutions = []
    solve_n_queens_util(board, 0, solutions)
    return solutions


def visualize_n_queens_solution(solution, N, step=None):
    board = np.zeros((N, N))
    for col, row in enumerate(solution):
        board[row, col] = 1

    plt.matshow(board, cmap="cool")
    for (i, j), value in np.ndenumerate(board):
        ax_text = '♛' if value else '•'
        plt.text(j, i, ax_text, ha='center', va='center', color='black', fontsize=20)

    if step is not None:
        plt.title(f"N-Queens Solution (Step {step + 1}/{len(solution)})", fontsize=16)
    else:
        plt.title(f"N-Queens Solution (N={N})", fontsize=16)

    plt.xticks([])
    plt.yticks([])
    plt.show()


def show_all_n_queens_solutions(solutions, N):
    max_solutions = 5  # Limit to 5 solutions
    for idx, solution in enumerate(solutions[:max_solutions]):
        visualize_n_queens_solution(solution, N, step=idx)



def parse_cryptarithmetic_input(equation):
    match = re.match(r"(\w+)\s*\+\s*(\w+)\s*=\s*(\w+)", equation.replace(" ", ""))
    if not match:
        raise ValueError("Invalid format. Use the form 'WORD1 + WORD2 = RESULT'.")
    word1, word2, result = match.groups()
    unique_letters = set(word1 + word2 + result)
    if len(unique_letters) > 10:
        raise ValueError("Too many unique letters. Cryptarithmetic must have 10 or fewer unique letters.")
    return word1, word2, result, list(unique_letters)


def solve_cryptarithmetic(word1, word2, result, letters):
    solutions = []
    for perm in permutations(range(10), len(letters)):
        letter_to_digit = dict(zip(letters, perm))
        if letter_to_digit[word1[0]] == 0 or letter_to_digit[word2[0]] == 0 or letter_to_digit[result[0]] == 0:
            continue
        num1 = int("".join(str(letter_to_digit[letter]) for letter in word1))
        num2 = int("".join(str(letter_to_digit[letter]) for letter in word2))
        num_result = int("".join(str(letter_to_digit[letter]) for letter in result))
        if num1 + num2 == num_result:
            solutions.append((num1, num2, num_result))
    return solutions


def visualize_cryptarithmetic_solution(solution, word1, word2, result):
    num1, num2, num_result = solution
    fig, ax = plt.subplots()
    ax.text(0.5, 0.7, f"{word1} = {num1}", ha='center', fontsize=12, color="blue")
    ax.text(0.5, 0.5, f"{word2} = {num2}", ha='center', fontsize=12, color="green")
    ax.text(0.5, 0.3, f"{result} = {num_result}", ha='center', fontsize=12, color="purple")
    plt.axis('off')
    plt.title("Cryptarithmetic Solution", fontsize=16)
    plt.show()


def show_cryptarithmetic_solutions(solutions, word1, word2, result):
    if solutions:
        for solution in solutions:
            visualize_cryptarithmetic_solution(solution, word1, word2, result)
    else:
        messagebox.showinfo("Result", "🔍 No solutions found for the cryptarithmetic.")



def is_color_safe(graph, colors, node, color):
    for neighbor in graph[node]:
        if neighbor in colors and colors[neighbor] == color:
            return False
    return True


def solve_map_coloring(graph, colors, node, color_limit):
    if node == len(graph):
        return True

    for color in range(color_limit):
        if is_color_safe(graph, colors, node, color):
            colors[node] = color
            if solve_map_coloring(graph, colors, node + 1, color_limit):
                return True
            del colors[node]
    return False


def visualize_map_coloring(graph, colors):
    num_colors = max(colors.values()) + 1
    color_map = plt.get_cmap("tab10", num_colors)


    G = nx.Graph()
    for node, neighbors in graph.items():
        G.add_node(node)
        for neighbor in neighbors:
            G.add_edge(node, neighbor)


    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=[color_map(colors[node]) for node in G.nodes()], node_size=700)
    plt.title("Map Coloring Solution", fontsize=16)
    plt.show()


def interactive_map_coloring():
    graph = {
        0: [1, 2],
        1: [0, 2, 3],
        2: [0, 1, 3],
        3: [1, 2]
    }
    colors = {}
    color_limit = 3
    if solve_map_coloring(graph, colors, 0, color_limit):
        visualize_map_coloring(graph, colors)
    else:
        print("🔍 No solution found for map coloring.")



def on_n_queens():
    try:
        N = int(n_queens_entry.get())
        if N <= 0:
            raise ValueError("The board size must be a positive integer.")
        solutions = solve_n_queens(N)
        if solutions:
            show_all_n_queens_solutions(solutions, N)  # Show all solutions, max 5 for N=8
        else:
            messagebox.showinfo("Result", "🔍 No solutions found.")
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def on_cryptarithmetic():
    equation = cryptarithmetic_entry.get()
    try:
        word1, word2, result, letters = parse_cryptarithmetic_input(equation)
        solutions = solve_cryptarithmetic(word1, word2, result, letters)
        if solutions:
            show_cryptarithmetic_solutions(solutions, word1, word2, result)
        else:
            messagebox.showinfo("Result", "🔍 No solutions found for the cryptarithmetic.")
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def on_map_coloring():
    interactive_map_coloring()


def create_advanced_gui():
    root = tk.Tk()
    root.title("Advanced CSP Solver")
    root.geometry("600x400")


    title_label = tk.Label(root, text="Constraint Satisfaction Problem Solver", font=("Arial", 16))
    title_label.pack(pady=10)


    n_queens_frame = tk.Frame(root, padx=10, pady=10)
    n_queens_frame.pack(fill='x')
    tk.Label(n_queens_frame, text="N-Queens Challenge", font=("Arial", 14)).pack(side='left')
    global n_queens_entry
    n_queens_entry = tk.Entry(n_queens_frame)
    n_queens_entry.insert(0, "Enter board size (e.g., 8)")
    n_queens_entry.bind("<FocusIn>", lambda e: n_queens_entry.delete(0,
                                                                     tk.END) if n_queens_entry.get() == "Enter board size (e.g., 8)" else None)
    n_queens_entry.pack(side='left')
    tk.Button(n_queens_frame, text="Solve", command=on_n_queens).pack(side='right')


    cryptarithmetic_frame = tk.Frame(root, padx=10, pady=10)
    cryptarithmetic_frame.pack(fill='x')
    tk.Label(cryptarithmetic_frame, text="Cryptarithmetic Puzzle", font=("Arial", 14)).pack(side='left')
    global cryptarithmetic_entry
    cryptarithmetic_entry = tk.Entry(cryptarithmetic_frame)
    cryptarithmetic_entry.insert(0, "Enter equation")
    cryptarithmetic_entry.bind("<FocusIn>", lambda e: cryptarithmetic_entry.delete(0,
                                                                                   tk.END) if cryptarithmetic_entry.get() == "Enter equation (e.g., SEND + MORE = MONEY)" else None)
    cryptarithmetic_entry.pack(side='left')
    tk.Button(cryptarithmetic_frame, text="Solve", command=on_cryptarithmetic).pack(side='right')


    map_coloring_frame = tk.Frame(root, padx=10, pady=10)
    map_coloring_frame.pack(fill='x')
    tk.Label(map_coloring_frame, text="Map Coloring", font=("Arial", 14)).pack(side='left')
    tk.Button(map_coloring_frame, text="Solve", command=on_map_coloring).pack(side='right')


    quit_button = tk.Button(root, text="Quit", command=root.quit)
    quit_button.pack(pady=20)

    root.mainloop()


if __name__ == "__main__":
    create_advanced_gui()
