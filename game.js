// 2D Marioland Spaceship Destroyer Game

const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game objects
const player = {
    x: 100,
    y: canvas.height - 100,
    width: 30,
    height: 50,
    velocityY: 0,
    jumping: false,
    speed: 5,
    health: 100
};

let bullets = [];
let spaceships = [];
let marios = [];
let score = 0;
let gameRunning = true;
let chantFrame = 0;

const keys = {};

// Initialize Marios and Luigis
function initializeMarios() {
    marios = [];
    for (let i = 0; i < 5; i++) {
        marios.push({
            x: 50 + i * 150,
            y: canvas.height - 100,
            width: 24,
            height: 36,
            animationFrame: i * 10,
            direction: Math.random() > 0.5 ? 1 : -1,
            isLuigi: i % 2 === 0  // Alternate between Mario and Luigi
        });
    }
}

// Event listeners
document.addEventListener('keydown', (e) => {
    keys[e.key] = true;
    if (e.key === ' ') {
        shoot();
    }
});

document.addEventListener('keyup', (e) => {
    keys[e.key] = false;
});

// Shooting function
function shoot() {
    bullets.push({
        x: player.x + player.width / 2,
        y: player.y - 10,
        velocityX: 8,
        width: 5,
        height: 10
    });
}

// Create spaceships
function spawnSpaceship() {
    const ship = {
        x: Math.random() * canvas.width,
        y: Math.random() * 150 + 20,
        width: 40,
        height: 30,
        velocityX: (Math.random() - 0.5) * 4,
        health: 2
    };
    spaceships.push(ship);
}

// Draw Mario character
function drawMario(x, y, width, height, isLuigi = false) {
    // Body
    const bodyColor = isLuigi ? '#00AA00' : '#FF0000';
    const hatColor = isLuigi ? '#228B22' : '#CC0000';
    
    ctx.fillStyle = bodyColor;
    ctx.fillRect(x + 3, y + 15, width - 6, 16);
    
    // Head (skin tone)
    ctx.fillStyle = '#FFDBAC';
    ctx.beginPath();
    ctx.arc(x + width / 2, y + 8, 7, 0, Math.PI * 2);
    ctx.fill();
    
    // Eyes (creepy)
    ctx.fillStyle = '#FFFFFF';
    ctx.beginPath();
    ctx.arc(x + width / 2 - 3, y + 6, 2, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(x + width / 2 + 3, y + 6, 2, 0, Math.PI * 2);
    ctx.fill();
    
    // Pupils (creepy black)
    ctx.fillStyle = '#000000';
    ctx.beginPath();
    ctx.arc(x + width / 2 - 3, y + 6, 1, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(x + width / 2 + 3, y + 6, 1, 0, Math.PI * 2);
    ctx.fill();
    
    // Creepy mouth
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.arc(x + width / 2, y + 11, 2, 0, Math.PI);
    ctx.stroke();
    
    // Mustache
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.arc(x + width / 2, y + 10, 2.5, 0, Math.PI);
    ctx.stroke();
    
    // Hat
    ctx.fillStyle = hatColor;
    ctx.fillRect(x + 2, y - 2, width - 4, 8);
    
    // Pants (blue or green)
    const pantsColor = isLuigi ? '#0000AA' : '#0000FF';
    ctx.fillStyle = pantsColor;
    ctx.fillRect(x + 5, y + 31, width - 10, 5);
}

// Draw creepy chant text
function drawCreepyChant() {
    const chants = [
        "wahhhhh...",
        "mamma mia...",
        "it's-a-me...",
        "luigi...",
        "wahoooooo...",
        "mama mia...",
        "let's-a-go...",
        "yippeeee..."
    ];
    
    return chants;
}

// Draw function
function draw() {
    // Clear canvas
    ctx.fillStyle = '#87CEEB';
    ctx.fillRect(0, 0, canvas.width, canvas.height * 0.7);
    
    // Draw ground
    ctx.fillStyle = '#228B22';
    ctx.fillRect(0, canvas.height * 0.7, canvas.width, canvas.height * 0.3);
    
    // Draw Marios & Luigis (chanting around the player)
    marios.forEach((mario, index) => {
        const bobAmount = Math.sin(chantFrame / 10 + index) * 3;
        const bounce = Math.abs(Math.sin(chantFrame / 20 + index * 0.5)) * 5;
        drawMario(mario.x + bounce * mario.direction, mario.y - bobAmount, mario.width, mario.height, mario.isLuigi);
        
        // Draw creepy chant bubbles
        const chantCycle = Math.floor((chantFrame + index * 20) / 15) % 8;
        const chants = drawCreepyChant();
        ctx.fillStyle = '#222';
        ctx.font = 'bold 8px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(chants[chantCycle], mario.x + mario.width / 2, mario.y - 15);
    });
    
    // Draw player (hero character)
    ctx.fillStyle = '#FF0000';
    ctx.fillRect(player.x, player.y, player.width, player.height);
    
    // Draw player face
    ctx.fillStyle = '#FFDBAC';
    ctx.fillRect(player.x + 5, player.y + 5, 20, 20);
    
    // Draw eyes
    ctx.fillStyle = '#000';
    ctx.fillRect(player.x + 8, player.y + 8, 4, 4);
    ctx.fillRect(player.x + 18, player.y + 8, 4, 4);
    
    // Draw gun (bazooka weapon)
    ctx.fillStyle = '#444';
    ctx.fillRect(player.x + player.width - 8, player.y + 12, 10, 8);
    // Barrel
    ctx.fillStyle = '#333';
    ctx.fillRect(player.x + player.width + 2, player.y + 14, 6, 4);
    
    // Draw bullets (Lesotho flags)
    bullets.forEach(bullet => {
        // Lesotho flag colors: White, Blue, Green
        // Draw flag as a small rectangle
        const flagWidth = 8;
        const flagHeight = 6;
        
        // White stripe
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(bullet.x, bullet.y, flagWidth, flagHeight / 3);
        
        // Blue stripe
        ctx.fillStyle = '#0052CC';
        ctx.fillRect(bullet.x, bullet.y + flagHeight / 3, flagWidth, flagHeight / 3);
        
        // Green stripe
        ctx.fillStyle = '#007A5E';
        ctx.fillRect(bullet.x, bullet.y + (flagHeight * 2) / 3, flagWidth, flagHeight / 3);
        
        // Border
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 0.5;
        ctx.strokeRect(bullet.x, bullet.y, flagWidth, flagHeight);
    });
    
    // Draw spaceships (actual ships)
    spaceships.forEach(ship => {
        // Ship hull (brown/gray)
        ctx.fillStyle = '#8B7355';
        ctx.beginPath();
        ctx.moveTo(ship.x + 5, ship.y + 10);
        ctx.lineTo(ship.x + ship.width - 5, ship.y + 10);
        ctx.lineTo(ship.x + ship.width - 8, ship.y + ship.height);
        ctx.lineTo(ship.x + 8, ship.y + ship.height);
        ctx.closePath();
        ctx.fill();
        
        // Ship mast
        ctx.fillStyle = '#8B4513';
        ctx.fillRect(ship.x + ship.width / 2 - 2, ship.y + 2, 4, 10);
        
        // Ship sail
        ctx.fillStyle = '#FFFACD';
        ctx.beginPath();
        ctx.moveTo(ship.x + ship.width / 2, ship.y + 5);
        ctx.lineTo(ship.x + ship.width / 2 + 12, ship.y + 8);
        ctx.lineTo(ship.x + ship.width / 2 + 10, ship.y + 15);
        ctx.closePath();
        ctx.fill();
        
        // Sail border
        ctx.strokeStyle = '#8B4513';
        ctx.lineWidth = 1;
        ctx.stroke();
        
        // Ship windows (portholes)
        ctx.fillStyle = '#FFD700';
        ctx.beginPath();
        ctx.arc(ship.x + 12, ship.y + ship.height - 5, 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.arc(ship.x + ship.width - 12, ship.y + ship.height - 5, 2, 0, Math.PI * 2);
        ctx.fill();
        
        // Health indicator
        if (ship.health === 1) {
            ctx.fillStyle = '#FF0000';
            ctx.font = 'bold 12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('!', ship.x + ship.width / 2, ship.y - 5);
        }
    });
}

// Update function
function update() {
    // Player movement
    if (keys['ArrowLeft'] || keys['a']) {
        player.x = Math.max(0, player.x - player.speed);
    }
    if (keys['ArrowRight'] || keys['d']) {
        player.x = Math.min(canvas.width - player.width, player.x + player.speed);
    }
    
    // Jumping
    if ((keys['ArrowUp'] || keys['w'] || keys[' ']) && !player.jumping) {
        player.velocityY = -15;
        player.jumping = true;
    }
    
    // Gravity
    player.velocityY += 0.6;
    player.y += player.velocityY;
    
    // Ground collision
    if (player.y >= canvas.height - 100) {
        player.y = canvas.height - 100;
        player.velocityY = 0;
        player.jumping = false;
    }
    
    // Update bullets
    bullets = bullets.filter(bullet => {
        bullet.x += bullet.velocityX;
        return bullet.x < canvas.width;
    });
    
    // Update spaceships
    spaceships.forEach(ship => {
        ship.x += ship.velocityX;
        
        // Wrap around edges
        if (ship.x < 0) ship.x = canvas.width;
        if (ship.x > canvas.width) ship.x = 0;
        
        // Player collision
        if (checkCollision(player, ship)) {
            player.health -= 10;
        }
    });
    
    // Check bullet-spaceship collision
    for (let i = bullets.length - 1; i >= 0; i--) {
        for (let j = spaceships.length - 1; j >= 0; j--) {
            if (checkCollision(bullets[i], spaceships[j])) {
                spaceships[j].health--;
                bullets.splice(i, 1);
                
                if (spaceships[j].health <= 0) {
                    spaceships.splice(j, 1);
                    score += 100;
                }
                break;
            }
        }
    }
    
    // Update HUD
    document.getElementById('score').textContent = score;
    document.getElementById('health').textContent = player.health;
    
    // Game over check
    if (player.health <= 0) {
        gameRunning = false;
        ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#fff';
        ctx.font = 'bold 40px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('GAME OVER', canvas.width / 2, canvas.height / 2);
        ctx.font = 'bold 20px Arial';
        ctx.fillText('Final Score: ' + score, canvas.width / 2, canvas.height / 2 + 40);
    }
}

// Collision detection
function checkCollision(obj1, obj2) {
    return obj1.x < obj2.x + obj2.width &&
           obj1.x + obj1.width > obj2.x &&
           obj1.y < obj2.y + obj2.height &&
           obj1.y + obj1.height > obj2.y;
}

// Game loop
let spawnTimer = 0;
function gameLoop() {
    draw();
    
    if (gameRunning) {
        update();
        
        // Spawn spaceships
        spawnTimer++;
        if (spawnTimer > 60) {
            spawnSpaceship();
            spawnTimer = 0;
        }
        
        // Update chant animation
        chantFrame++;
    }
    
    requestAnimationFrame(gameLoop);
}

// Start game
initializeMarios();
gameLoop();
