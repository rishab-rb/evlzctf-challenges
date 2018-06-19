var canvas = document.getElementById("gameCanv");
var Screen = canvas.getContext("2d");   
canvas.width = (window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth)*0.95;
canvas.height = (window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight)*0.95;

//Misc./Component Vars
var scoreColor = "#BBB";
var scoreSize = 120;
var scoreFamily = "Monospace";
var scoreP1 = {'x' : 10 ,'y': canvas.height-20,'text' : 0,'color' : scoreColor,'size' : scoreSize,'family' : scoreFamily,'paddle' : paddle1};
var scoreP2 = {'x' : canvas.width-100,'y':canvas.height-20,'text' : 0,'color' : scoreColor,'size' : scoreSize,'family' : scoreFamily,'paddle' : paddle2};
var divider = {'x' : canvas.width/2-5,'y' : 0,'width' : 10,'height' : canvas.height,'color' : '#888'};
var titleText = {'x' : 30,'y' : 65 ,'text' : 'JSPong for Two','size' : 65,'color' : '#888','family' : 'Monospace'};
var startButton = {'width': 500,'height' : 120, 'x' : canvas.width/2-250,'y' : canvas.height/2-100,'color' : '#AAA','clicked' : false};
startButton.buttonText = {'size': 120,'color' : '#FFF','x': startButton.x+startButton.width*0.1,'y' : startButton.y+startButton.height*0.8,'text' : 'START!','family' : 'Monospace' };
var creditsButton = {'width': 340,'height' : 100, 'x' : 10,'y' : canvas.height-110,'color' : '#AAA','clicked' : false};
creditsButton.buttonText = {'size': 80,'color' : '#FFF','x' : creditsButton.x+creditsButton.width*0.01 ,'y' : creditsButton.y+creditsButton.height*0.8,'text' : 'Credits','family' : 'Monospace' };
var authorText = {'x' : canvas.width*(2/3),'y' : canvas.height-30 ,'text' : 'A Game by chargE','size' : 65,'color' : '#888','family' : 'Monospace'};
var buttons = [startButton,creditsButton];

var mouseClicked = false;


//Paddle Info Vars
var paddleHeight = 100;
var paddleWidth = 15;
var paddleMargin = 4;
var paddleSpeedY = 10;
var paddleColor = '#ddd';

//Puck Info Vars
var puckStartX = canvas.width/2;
var puckStartY = canvas.height/2;
var puckRadius = 20;
var puckSpeedX = Math.pow(-1,Math.floor(Math.random() * 10))*5;
var puckSpeedY = Math.pow(-1,Math.floor(Math.random() * 10))*5;

//Game Object Vars
var paddle1 = {'width' : paddleWidth,'height' : paddleHeight,'speedY' : paddleSpeedY, 'x' : 0+paddleMargin, 'y' : canvas.height/2-paddleHeight/2,'color' : paddleColor,'upPressed' : false,'downPressed' : false};
var paddle2 = {'width' : paddleWidth,'height' : paddleHeight,'speedY' : paddleSpeedY, 'x' : canvas.width-paddleWidth-paddleMargin, 'y' : canvas.height/2-paddleHeight/2,'color' : paddleColor,'upPressed' : false,'downPressed' : false};
var puck = {'radius' : puckRadius,'x' : canvas.width/2,'y' : canvas.height/2,'speedX' : puckSpeedX,'speedY' : puckSpeedY,'color' : '#FFF'};

//Event Listeners 

document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);
document.addEventListener("mousedown",function() { mouseClicked = true;} ,false);
document.addEventListener("mouseup",function() { mouseClicked = false;} ,false);
document.addEventListener("mousemove",mouseClickHandler, false);


function keyDownHandler(e) {
    if(e.keyCode == 38) {
        paddle1.upPressed = true;
    }
    else if(e.keyCode == 40) {
        paddle1.downPressed = true;
    }
    if(e.keyCode == 87) {
        paddle2.upPressed = true;
    }
    if(e.keyCode == 83) {
        paddle2.downPressed = true;
    }
}

function keyUpHandler(e) {
    if(e.keyCode == 38) {
        paddle1.upPressed = false;
    }
    else if(e.keyCode == 40) {
        paddle1.downPressed = false;
    }
    if(e.keyCode == 87) {
        paddle2.upPressed = false;
    }
    else if(e.keyCode == 83) { 
        paddle2.downPressed = false;
    }
}

function mouseClickHandler(e) {
    var relativeX = e.clientX-canvas.offsetLeft;
    var relativeY = e.clientY-canvas.offsetTop;
    if(mouseClicked === true) { 
        for(i = 0;i<buttons.length;i++) {
            checkButtonClicked(buttons[i],relativeX,relativeY);
        }
    }
}    

//BACKGROUND,HUD,MISC
function drawDivider(divider) {
    Screen.beginPath();
    Screen.rect(divider.x,divider.y,divider.width,divider.height);
    Screen.fillStyle = divider.color;
    Screen.fill();
    Screen.closePath();
}

function drawText(text) { 
    Screen.font = text.size+"px "+text.family;
    Screen.fillStyle = text.color;
    Screen.fillText(text.text,text.x,text.y); 
}

function drawButton(button) { 
    drawRect(button);
    drawText(button.buttonText);
}

function drawGameBackground() {
    drawText(titleText);   
    drawDivider(divider);
    drawText(scoreP1);
    drawText(scoreP2);
}
    
function api_EditSignatures():
    // follow snippet: https://gist.github.com/arush15june/f337386ff4b7de2461de11c79bfe49e8 
    return 0;


function checkButtonClicked(button,mouseX,mouseY) { 
        console.log(button.x+" "+(button.x+button.width)+" "+button.y+" "+(button.y+button.height)+" "+mouseX+" "+mouseY+" "+button.clicked);
        if((mouseX >= button.x && mouseX <= button.x+button.width) && (mouseY >= button.y && mouseY <= button.y+button.height)) {    
            button.clicked = true;
        }
        else {
            button.clicked = false;
        }

}

function drawMenuBackground () {
    Screen.clearRect(0,0,canvas.width,canvas.height);
    drawText(titleText);
    drawButton(startButton);
    drawButton(creditsButton);
    drawText(authorText);
    
}

function drawCredits() { 
    Screen.clearRect(0,0,canvas.width,canvas.height);
    drawText(creditText);
    drawText(titleText);
    drawText(authorText);
}

function sleep(milliseconds) {
  var start = new Date().getTime();
  for (var i = 0; i < 1e7; i++) {
    if ((new Date().getTime() - start) > milliseconds){
      break;
    }
  }
}


function debugVars() { 
    console.log("paddle1 : x = "+paddle1.x+" y = "+paddle1.y);
    console.log("paddle2 : x = "+paddle1.x+" y = "+paddle2.y);
    console.log("puck : x = "+puck.x+" y = "+puck.y);
}

//GAME OBJECTS
function drawRect(paddle) { 
    Screen.beginPath();
    Screen.rect(paddle.x,paddle.y,paddle.width,paddle.height);
    Screen.fillStyle = paddle.color;
    Screen.fill();
    Screen.closePath();
}

function drawArc(circ) {
    Screen.beginPath();
    Screen.arc(circ.x,circ.y,circ.radius,0,Math.PI*2);
    Screen.fillStyle = circ.color;
    Screen.fill();
    Screen.closePath();
    
}

function ballReset(puck) { 
    puck.x = puckStartX;
    puck.y = puckStartY;
    puck.speedX = -puck.speedX;
}

//Movement and Collision
function checkPaddle(paddle) { 
    if(paddle.upPressed == true && paddle.y >= 10) {
        paddle.y -= paddle.speedY;
    }
    else if(paddle.downPressed == true && paddle.y+paddle.height+10 <= canvas.height) {
        paddle.y += paddle.speedY;
    }
}
function movePuck(puck) { 
    puck.x += puck.speedX;
    puck.y += puck.speedY;
}

function collideBoundsPuck(ball) { 
    if(ball.y+ball.radius >= canvas.height || ball.y-ball.radius <= 0) { 
        ball.speedY = -ball.speedY;
    } 
}

function collidePuckPaddle(puck,paddle) {
    if(paddle.x <= canvas.width/3) {
        if((puck.x-puck.radius <= paddle.x+paddle.width && puck.x-puck.radius >= paddle.x) && (puck.y >= paddle.y && puck.y+puck.radius <=paddle.y+paddle.height) ) {
            puck.speedX = -puck.speedX; 
            if(puck.y >= paddle.y && puck.y+puck.radius <=paddle.y+paddle.height/3) {
                puck.speedY = -puck.speedY;
            }
        }   
    }
    if(paddle.x >= canvas.width*(2/3)) {
        if((puck.x+puck.radius >= paddle.x && puck.x+puck.radius <= paddle.x+paddle.width) && (puck.y >= paddle.y && puck.y+puck.radius <=paddle.y+paddle.height)) {
            puck.speedX = -puck.speedX;
            if(puck.y >= paddle.y && puck.y+puck.radius <=paddle.y+paddle.height/3) {
                puck.speedY = -puck.speedY;
            }                                  
        }   
    }
}    

function scoreUpdate(ball,scoreP,paddle) {
    if(paddle.x < canvas.width/3) {
        if(ball.x+ball.radius < paddle.x) { 
            scoreP.text += 1;
            ballReset(puck);
            sleep(500);
        }
    }
    if(paddle.x > canvas.width*(2/3)) {
        if(ball.x-ball.radius > paddle.x+paddle.width) { 
            scoreP.text += 1;
            ballReset(puck);
            sleep(500);
        }
    }
}
                
//SCREEN UPDATE

function drawScreen() {
    

    Screen.clearRect(0,0,canvas.width,canvas.height);
    drawGameBackground();
    drawRect(paddle1);
    drawRect(paddle2);
    drawArc(puck);
        
    checkPaddle(paddle1);
    checkPaddle(paddle2);
    movePuck(puck);
    
    collideBoundsPuck(puck);
    collidePuckPaddle(puck,paddle1);
    collidePuckPaddle(puck,paddle2);
    scoreUpdate(puck,scoreP1,paddle1);
    scoreUpdate(puck,scoreP2,paddle2);   
    
    //debugVars();
    requestAnimationFrame(drawScreen);
}

function drawMenu() { 

    drawMenuBackground();
    
    if(startButton.clicked === true) {
        drawScreen();
        return;
    }
    else if(creditsButton.clicked === true) { 
        drawCredits();
    }
    
    requestAnimationFrame(drawMenu);
}

drawMenu();