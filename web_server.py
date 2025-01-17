from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from tunk.game import Game
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

games = {}  # Store active games

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('create_game')
def on_create_game():
    game_id = len(games)
    games[game_id] = Game()
    join_room(game_id)
    emit('game_created', {'game_id': game_id})

@socketio.on('join_game')
def on_join_game(data):
    game_id = data['game_id']
    if game_id in games:
        game = games[game_id]
        join_room(game_id)
        # Send initial game state
        emit('game_joined', {
            'game_id': game_id,
            'numPlayers': len(game.players),
            'gameState': {
                'players': [{'name': p.name, 'hand': p.hand} for p in game.players],
                'discardTop': game.show_last_discard()
            }
        }, room=game_id)
    else:
        emit('error', {'message': 'Game not found'})

@socketio.on('play_card')
def on_play_card(data):
    game_id = data['game_id']
    card = data['card']
    player_id = data['player_id']
    if game_id in games:
        game = games[game_id]
        # Handle card play logic here
        emit('card_played', {'card': card, 'player_id': player_id}, room=game_id)

@socketio.on('draw_card')
def on_draw_card(data):
    game_id = data['game_id']
    draw_type = data.get('type', 'deck')  # 'deck' or 'discard'
    if game_id in games:
        game = games[game_id]
        if draw_type == 'deck':
            card = game.deck.deal(1)[0]  # Deal one card from deck
        else:
            card = game.get_last_discard()  # Get card from discard pile
            
        emit('card_drawn', {
            'card': card,
            'source': draw_type,
            'gameState': {
                'players': [{'name': p.name, 'hand': p.hand} for p in game.players],
                'discardTop': game.show_last_discard(),
                'deckCount': len(game.deck)
            }
        }, room=game_id)

if __name__ == '__main__':
    socketio.run(app, debug=True)
