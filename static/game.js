const socket = io();
let gameId = null;

function createGame() {
    socket.emit('create_game');
}

function joinGame() {
    const gameIdInput = document.getElementById('game-id-input');
    gameId = gameIdInput.value;
    socket.emit('join_game', { game_id: gameId });
}

function showGameArea() {
    document.getElementById('game-area').style.display = 'block';
}

socket.on('game_created', function(data) {
    gameId = data.game_id;
    showGameArea();
    alert(`Game created! Share this ID: ${gameId}`);
});

socket.on('game_joined', function(data) {
    showGameArea();
    positionPlayers(data.numPlayers);
    alert('Successfully joined game!');
});

socket.on('card_played', function(data) {
    // Update the game state when cards are played
    updateGameDisplay(data);
});

function createCard(card) {
    const cardDiv = document.createElement('div');
    cardDiv.className = `card ${getCardColor(card[1])}`;
    cardDiv.innerHTML = `
        <div style="position: absolute; top: 5px; left: 5px;">${card[0]}${getCardSymbol(card[1])}</div>
        <div style="position: absolute; bottom: 5px; right: 5px;">${card[0]}${getCardSymbol(card[1])}</div>
    `;
    cardDiv.draggable = true;
    cardDiv.addEventListener('dragstart', handleDragStart);
    return cardDiv;
}

function getCardColor(suit) {
    return ['♥', '♦'].includes(suit) ? 'red' : 'black';
}

function getCardSymbol(suit) {
    return suit;
}

function positionPlayers(numPlayers) {
    const gameTable = document.querySelector('.game-table');
    const radius = 300; // Adjust based on table size
    const angleStep = (2 * Math.PI) / numPlayers;

    // Clear existing positions
    const existingPositions = document.querySelectorAll('.player-position');
    existingPositions.forEach(pos => pos.remove());

    // Create new positions
    for (let i = 0; i < numPlayers; i++) {
        const angle = angleStep * i - Math.PI / 2; // Start from top
        const x = radius * Math.cos(angle) + 400; // Center x
        const y = radius * Math.sin(angle) + 400; // Center y

        const position = document.createElement('div');
        position.className = 'player-position';
        position.id = `player-${i}`;
        position.style.left = `${x - 100}px`; // Adjust for element width
        position.style.top = `${y - 75}px`;  // Adjust for element height
        
        const nameDiv = document.createElement('div');
        nameDiv.className = 'player-name';
        nameDiv.textContent = `Player ${i + 1}`;
        position.appendChild(nameDiv);

        const handDiv = document.createElement('div');
        handDiv.className = 'player-hand';
        position.appendChild(handDiv);

        gameTable.appendChild(position);
    }
}

function updateGameDisplay(gameState) {
    if (!gameState) return;

    // Update deck count
    document.getElementById('deck-count').textContent = gameState.deckCount;
    
    // Update discard pile
    const discardPile = document.getElementById('discard-pile');
    discardPile.innerHTML = '';
    if (gameState.discardTop) {
        discardPile.appendChild(createCard(gameState.discardTop));
    }
    
    // Update player hands
    gameState.players.forEach((player, index) => {
        const playerHand = document.querySelector(`#player-${index} .player-hand`);
        if (playerHand) {
            playerHand.innerHTML = '';
            player.hand.forEach(card => {
                playerHand.appendChild(createCard(card));
            });
        }
    });
}

// Game action functions
function drawCard() {
    socket.emit('draw_card', { game_id: gameId });
}

function drawFromDeck() {
    socket.emit('draw_card', { game_id: gameId, type: 'deck' });
}

function drawFromDiscard() {
    socket.emit('draw_card', { game_id: gameId, type: 'discard' });
}

socket.on('card_drawn', function(data) {
    updateGameDisplay(data.gameState);
    
    // Show the drawn card
    const card = data.card;
    const cardElement = createCard(card);
    
    // Add animation for drawn card
    cardElement.style.position = 'absolute';
    cardElement.style.zIndex = '1000';
    
    if (data.source === 'deck') {
        document.getElementById('deck-count').textContent = data.gameState.deckCount;
    }
    
    // Update player's hand
    const playerHand = document.querySelector('.player-hand');
    playerHand.appendChild(cardElement);
});

function spread() {
    socket.emit('spread', { game_id: gameId });
}

function knock() {
    socket.emit('knock', { game_id: gameId });
}

function drop() {
    socket.emit('drop', { game_id: gameId });
}
