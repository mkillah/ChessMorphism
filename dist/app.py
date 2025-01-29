import pandas as pd
from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

df = pd.read_csv("C:/Users/marko/PycharmProjects/ChessMorphism//dist/alternated_preserved_motif_positions.csv")

# MOTIFS and ALTERNATE_MOTIFS dictionaries (storing both FENs as pairs)
MOTIFS = {}

# Populate the MOTIFS dictionary with pairs of FENs
def load_motifs():
    for index, row in df.iterrows():
        if row["correct_classification"]:
            motif = row['Motif']
            motif_fen = row['newFen']
            alternate_fen = row['alternated_fen']
            correct_move_main = row["newMove"]  # Correct move for main puzzle (e.g., 'e2e4')
            correct_move_alternate = row["alteredMove"]  # Correct move for alternate puzzle
            n_moves_main = len(correct_move_main.split(" "))
            n_moves_alternate = len(correct_move_alternate.split(" "))
            MOTIFS[motif] = {
                "main": motif_fen,
                "alternate": alternate_fen,
                "correct_move_main": correct_move_main,
                "correct_move_alternate": correct_move_alternate,
                "n_moves_main": n_moves_main,
                "n_moves_alternate": n_moves_alternate,
                "turn": "w"  # Initialize with white's turn
            }

# Load the motifs from the DataFrame
load_motifs()

@app.route('/')
def index():
    return render_template('index.html', motifs=MOTIFS)

@app.route('/generate_fen', methods=['POST'])
def generate_fen():
    motif = request.json.get('motif')  # Get the motif name
    alternate = request.json.get('alternate', False)  # Get the alternate flag (default is False)

    # Handle random motif selection
    if motif == "random":  # If the user requests a random motif
        motif = random.choice(list(MOTIFS.keys()))  # Select a random motif name from the keys

    # Check if the motif exists in the dictionary
    if motif in MOTIFS:
        # If alternate is true, return the alternate FEN and move, otherwise the main FEN and move
        if alternate:
            fen = MOTIFS[motif]["alternate"]  # Get the alternate FEN
            correct_move = MOTIFS[motif]["correct_move_alternate"]
            n_moves = MOTIFS[motif]["n_moves_alternate"]
        else:
            fen = MOTIFS[motif]["main"]  # Get the main FEN
            correct_move = MOTIFS[motif]["correct_move_main"]
            n_moves = MOTIFS[motif]["n_moves_main"]
    else:
        # Fallback to a default position if motif is not found
        fen = "startpos"  # Example FEN for a new game
        correct_move = ""  # No move
        n_moves = 0

    return jsonify({"fen": fen, "correct_move": correct_move, "n_moves": n_moves})

if __name__ == '__main__':
    app.run(debug=True)

# https://www.youtube.com/watch?v=_u-VAFwY95U
