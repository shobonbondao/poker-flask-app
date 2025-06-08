from flask import Flask, render_template, request, jsonify
from treys import Card, Deck, Evaluator

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    my_cards = data.get('my_cards', [])
    opp_cards = data.get('opp_cards', [])
    board_cards = data.get('board_cards', [])

    evaluator = Evaluator()
    my = [Card.new(c) for c in my_cards]
    opp = [Card.new(c) for c in opp_cards]
    board = [Card.new(c) for c in board_cards]

    wins = 0
    sims = 1000
    for _ in range(sims):
        deck = Deck()
        for c in my + opp + board:
            if c in deck.cards:
                deck.cards.remove(c)
        full_board = board[:]
        while len(full_board) < 5:
            full_board.append(deck.draw(1)[0])
        my_score = evaluator.evaluate(full_board, my)
        opp_score = evaluator.evaluate(full_board, opp)
        if my_score < opp_score:
            wins += 1
        elif my_score == opp_score:
            wins += 0.5
    return jsonify({'winrate': round(wins / sims * 100, 2)})

if __name__ == '__main__':
    app.run(debug=True)
