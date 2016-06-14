"""
Program: FINAL ASSIGNMENT
Created By: Rohit Terry Kisto
Purpose: Make a full functioning game
DATE: 11/03/2016
REVISION: 16
NOTES: 
-Disabled gravity(There's no gravity in space..)
-Made projectile rotate once fired
-Started setting up 'levels'
-Cleaned up level code and made it more efficent
-Set up enemy health system
-Added hit detection between the missile and the player
-Added in asteroid
-Enabled enemy to start from different parts of the screen
    top of the screen is 1, right is 2, bottom is 3 and left is 4,
    uses random generator to determine spots and set velocities
    depending on the starting spot
-Added explosion when enemy hits the player
-Added image to enemy projectile
-Changed enemy missile velocity from 10,10 to 30,30
-Added hit detection between player and enemy missile
-Changed enemy bounce counter to 1
-Corrected asteroids spawn to make it move
-Added a random x or y velocity to the asteroids movement
    Uses the same spawn system as the enemy
-Added hit detection between the missile and the asteroid
-Added hit detection between the asteroid and the player
-Added hit detection between asteroid and the enemy 
-Gave level pass condition
-Added explosion images for the asteroid
-Added shield image
-Added hit detection between entites and shield

   
TO-DO:
-Add hit detection between enemy and player DONE
-Give enemy a weapon DONE
-Add hit detection between asteroid and all other entities DONE
-Enable level pass/conditions DONE
-Give loss condition
-Add shield that will nullify damage DONE
-Give win condition DONE 
"""

add_library('minim') #add sound library
minim = Minim(this)

#what's run on the opening of the program
def setup():
    size(1280, 720)
    init()

#initializes variables
def init():
    
    #globals for ints
    global sclMissle, sclEnem, sclExp, sclPlayer, sclMissleEnem
    global missleRad, bCounter, ebCounter, score, timer, timerRand, expTimer, rotateCounter, level, armour, sclAst
    global enemArmour, player_weapon_dmg, enem_weapon_dmg, ast_dmg, enemStart
    global timerAst, expAstTimer, sclShield, totalScore, velSetEnem, shieldPower
    sclPlayer = 1
    sclMissle = .3
    sclEnem = .3 #scale of the enemy
    sclExp = .6 #scale of the explosion
    sclAst = .6
    sclShield = 0
    sclMissleEnem = .3
    bCounter = 0 #bounce counter
    ebCounter = 0 #enemies bounce counter
    missleRad = 100 #missiles diameter
    score = 0 #score for player
    timer = 120
    timerAst = 120
    expTimer = 120
    expAstTimer = 120
    rotateCounter = 0
    level = 1
    armour = 100
    enemArmour = 30
    player_weapon_dmg = 30
    enem_weapon_dmg = 10
    ast_dmg = 20
    enemStart = 0
    astStart = 0
    totalScore = 0
    velSetEnem = 10
    shieldPower = 100
    
    #global for PVectors
    global posMissle, posPlayer, posEnem, posExp, posEnemMissle
    global velMissle, velEnem, velAst, grav, enemRad, enemAim, playerRad, posAst, velEnemMissle, enemMissleRad, astRad, posAstExp
    global colDis, colDis_player, colDis_enem_player, colDis_enemMissle_player, colDis_missle_ast, colDis_player_ast, colDis_enem_ast
    global posShield, shieldRad, colDis_shield_enem, colDis_shield_enemMissle, colDis_shield_ast
    posPlayer = PVector(width/2, height/2) #places player in the middle of screen
    posMissle = PVector(width/2, height/2) #places missle off the screen
    posExp = PVector(width/2, height/2) #places the explosion to the middle of the screen
    posAstExp = PVector(width*2, height*2) #position of the asteroid explosion
    posShield = PVector(posPlayer.x, posPlayer.y)
    playerRad = PVector(125, 125) #players diameter
    enemRad = PVector(210, 300)
    shieldRad = PVector(200, 200)
    enemMissleRad = PVector(100, 100)
    astRad = PVector(100, 100)
    posEnem = PVector(0-enemRad.x, random(enemRad.y/2, height-enemRad.y/2)) #inits the position of the enemy at a random location on the screen
    posEnemMissle = PVector(posEnem.x, posEnem.y)
    posAst = PVector(random(0, width), 0-enemRad.y)
    velMissle = PVector() #sets missles velocity
    velAst = PVector(0, 10)
    velEnem = PVector(velSetEnem, 0)
    velEnemMissle = PVector()
    grav = PVector() #sets gravities velocity
    colDis = PVector() #distance of collision
    colDis_player = PVector() #distance of collision between player and missile
    colDis_enem_player = PVector() #distance of collision between player and enemy
    colDis_enemMissle_player = PVector()
    colDis_missle_ast = PVector()
    colDis_player_ast = PVector()
    colDis_enem_ast = PVector()
    colDis_shield_enem = PVector()
    colDis_shield_enemMissle = PVector()
    colDis_shield_ast = PVector()
    enemAim = PVector()
    
    #globals for booleans
    global launchMissle, launchEnemMissle, gameState, explode, asteroidExplode, win, lose, keyHeld
    launchMissle = False #controls the users ability to spam the missile
    launchEnemMissle = True
    gameState = False #current state of the 'game'
    explode = False
    asteroidExplode = False
    lose = False
    win = False
    keyHeld = False
    
    #globals for images
    global startscreen, bg, expAnim, playerImageN, enemyImage, playerMissle, enemMissle, astImage, expAnimAst, shieldAnim
    startscreen = loadImage("startscreen.png")
    bg = loadImage("background_0.jpg")
    expAnim = loadImage("explosion.png")
    playerImageN = loadImage("ship_normal_scaled.png")
    enemyImage = loadImage("enemy_normal.png")
    playerMissle = loadImage("proj_1_orange.png")
    enemMissle = loadImage("proj_1_blue.png")
    astImage = loadImage("asteroid_0.png")
    expAnimAst = loadImage("asteroid_1.png")
    shieldAnim = loadImage("shield.png")
    
    #globals for sounds
    global shoot_sound, shoot_sound_enem
    shoot_sound = minim.loadFile("proj_1_sound.mp3")
    shoot_sound_enem = minim.loadFile("proj_2_sound.mp3")
    
    backTrack = minim.loadFile("backingtrack.mp3")
    backTrack.loop()
    
#initializes the game
def initGame():
    global counterText, bg, score, scoreText, armour, armourText, win, lose, shieldPower, shieldText

    frameRate(60)
    
    if(win == False and lose == False):
        initLevels()
        scoreText = "SCORE: " + str(score)
        armourText = "ARMOUR: " +str(armour)
        shieldText = "SHIELD POWER: " + str(shieldPower)
    
        drawExplosion()
        drawAsteroidExplosion()
        
        drawMissle()
        shieldPlayer()
        drawPlayer() #draws the player
        moveMissle() #moves the missle
        drawStrings() #draws the strings to the screen
    
        drawEnemMissle()
        moveEnemMissle()
        
        drawEnem()
        moveEnem()
        
        drawAsteroid()
        moveAsteroid()
    elif(win == True):
        initWinScreen()
    else:
        initLoseScreen()
    
    #print(bCounter, posMissle.x, posMissle.y)    
    
def initStartScreen():
    global startscreen, gameState, keyHeld
    
    background(startscreen)
    fill(0, 0, 0)
    noStroke()
    rect(0, height/2-50, width/2+200, height/2)
    textSize(50)
    textAlign(CENTER)
    fill(150, 0, 77)
    text("Press any key to play!", width/2+300, height/2-150)
    textSize(35)
    text("Instructions", width/2-240, height/2)
    textSize(20)
    text("Use your mouse to pullback your missile\nUse LMB to fire to hit the enemy ship by bouncing your missile off of the edge\nof the screen otherwise you won't be able to hit the enemy\nBe careful because there enemy will be shooting its own missile at you\nHe can also suicide by running into you\nWatch out for the asteroid, it does damage too\nYou can press SPACEBAR to activate a shield that nulifies all damage\nexcept YOUR missiles\nYour goal is a total score of 150\nWhich is gained over 5 levels, your score goes up for every enemy killed\nWith each level, it gets harder...\nGood Luck!", width/2-240, height/2+20)
    
    if(keyPressed and keyHeld == False):
        keyHeld = True
        gameState = True

def initWinScreen():
    global startscreen, win, keyHeld
    background(startscreen)
    
    textAlign(CENTER)
    textSize(35)
    fill(150, 0, 77)
    text("Congratulations\nYou have beaten Spaceflyer X\nThanks for playing!\nPress any key to return to menu", width/2-300, height/2+75)
    
    if(keyPressed and keyHeld == False):
        keyHeld = True
        init()
        
def initLoseScreen():
    global startscreen, lose, keyHeld, totalScore
    
    background(startscreen)
    
    textAlign(CENTER)
    textSize(35)
    fill(150, 0, 77)
    text("Unfortunately\nYour ship was destoryed\nYou got a total score of " + str(totalScore) +"\nBetter luck next time!\nThanks for playing\nPress any key to return to menu", width/2-300, height/2+75)
    
    if(keyPressed and keyHeld == False):
        keyHeld = True
        init()

def initLevels():
    
    if(level == 1):
        initLevel1()
    elif(level == 2):
        initLevel2()
    elif(level == 3):
        initLevel3()
    elif(level == 4):
        initLevel4()
    elif(level == 5):
        initLevel5()
    else:
        print("Level could not be loaded")

def initLevel1():
    global bg, level, score, totalScore, velSetEnem
    bg = loadImage("background_" + str(level) + ".jpg")
    background(bg)
    
    velSetEnem *= level
    
    if(score > (level*10)-1):
        level += 1
        totalScore += score
        score = 0

def initLevel2():
    global bg, level, score, totalScore, velSetEnem
    bg = loadImage("background_" + str(level) + ".jpg")
    background(bg)

    velSetEnem = 15

    if(score > (level*10)-1):
        level += 1
        totalScore += score
        score = 0
        
def initLevel3():
    global bg, level, score, totalScore, velSetEnem
    bg = loadImage("background_" + str(level) + ".jpg")
    background(bg)
    
    velSetEnem *= level
    
    if(score > (level*10)-1):
        level += 1
        totalScore += score
        score = 0
        
def initLevel4():
    global bg, level, score, totalScore, velSetEnem
    bg = loadImage("background_" + str(level) + ".jpg")
    background(bg)

    velSetEnem = 25

    if(score > (level*10)-1):
        level += 1
        totalScore += score
        score = 0
        
def initLevel5():
    global bg, level, score, totalScore, win, velSetEnem
    bg = loadImage("background_" + str(level) + ".jpg")
    background(bg)

    velSetEnem = 30

    if(score > (level*10)-1):
        totalScore += score
        win = True
        
#draws the player
def drawPlayer():
    global posPlayer, playerImage, lose, armour

    if(armour < 1):
        lose = True

    pushMatrix()
    translate(posPlayer.x, posPlayer.y)
    scale(1)
    
    imageMode(CENTER)
    strokeWeight(2)
    stroke(0, 255, 0)
    line(0, 0, mouseX-width/2, mouseY-height/2) #LINE FOR AIMING
    #line(0, 0, mouseX-width/2, 0)
    #line(0, 0, 0, mouseY-height/2)
    
    #print(mouseX, mouseY)

    #makes the ship rotate
    angle = atan2(mouseX-width/2, mouseY-height/2)
    rotate(-angle)
    
    image(playerImageN, 0, 0)
    
    popMatrix()
    
#draws the missile
def drawMissle():
    global posMissle, sclMissle, missleRad, playerMissle, rotateCounter
    
    pushMatrix()
    translate(posMissle.x, posMissle.y)
    scale(sclMissle)
    ###
    strokeWeight(1)
    stroke(0, 0, 0)
    fill(0, 255, 255)
    #ellipse(0, 0, missleRad, missleRad)
    
    imageMode(CENTER)
    
    rotateCounter += .5
    
    if(rotateCounter > 378):
        rotateCounter = 0  
    rotate(rotateCounter)
    image(playerMissle, 0, 0)
    ###
    popMatrix()
    
#moves the missile 
def moveMissle():
    global posPlayer, posMissle, velMissle, sclMissle, sclEnem, grav, bCounter, posEnem, colDis, missleRad, enemRad, posExp, score, explode, armour, enemArmour, sclPlayer
    global colDis_missle_ast, posAst, sclAst, posAstExp, asteroidExplode
    
    #velMissle.add(grav) #applies gravity to the velocity
    posMissle.add(velMissle) #adds the velocity to the position
    
    #COLLISION DETECTION
    colDis = posEnem.dist(posMissle)
    if(colDis < ((missleRad/2)*sclMissle+(enemRad.x/2)*sclEnem or colDis < ((missleRad/2)*sclMissle+(enemRad.y/2)*sclEnem)) #checks to make sure that their is a collision between the object and the missile
    and bCounter > 0 and bCounter < 2):  #and if the bounce counter is greater than 0 and less than 2, only 1 bounce will accepted!
        
        enemArmour -= player_weapon_dmg
        if(enemArmour < 1):
            explode = True
            posExp.set(posEnem)
            spawnEnem()
            bCounter = 0
            score += 1
            enemArmour = 30
        resetMissleVals() #resets the missles values so once it hits the circle, it will return to it's starting point
        
    colDis_player = posPlayer.dist(posMissle)
    if(colDis_player < ((missleRad/2)*sclMissle+(playerRad.x/2)*sclPlayer or colDis_player < ((missleRad/2)*sclMissle+(playerRad.y/2)*sclPlayer)) #checks to make sure that their is a collision between the object and the missile
    and bCounter > 0 and bCounter < 2):
        armour -= player_weapon_dmg
        bCounter = 0
        resetMissleVals() #resets the missles values so once it hits the circle, it will return to it's starting point
    
    colDis_missle_ast = posAst.dist(posMissle)
    if(colDis_missle_ast < ((missleRad/2)*sclMissle+(astRad.x/2)*sclAst or colDis < ((missleRad/2)*sclMissle+(astRad.y/2)*sclAst)) #checks to make sure that their is a collision between the object and the missile
    and bCounter > 0 and bCounter < 2):
        asteroidExplode = True
        posAstExp.set(posAst)
        spawnAsteroid()
    
    if(posMissle.x > width-50*abs(sclMissle) or posMissle.x < 50+abs(sclMissle)): #scale is always positive, used absolute value
        velMissle.x *= -1
        if(bCounter > 0): 
            resetMissleVals()
            bCounter = 0
        else:
            bCounter += 1
    if(posMissle.y > height-50*abs(sclMissle) or posMissle.y < 50+abs(sclMissle)): #scale is always positive, used absolute value
        velMissle.y *= -1
        if(bCounter > 0): 
            resetMissleVals()
            bCounter = 0
        else:
            bCounter += 1
            
#resets the values of the missle
def resetMissleVals():
    global posMissle, velMissle, launchMissle
    posMissle.x = width/2
    posMissle.y = height/2
    velMissle.set(0, 0)
    launchMissle = False
            
#draws the "enemy"
def drawEnem():
    global posEnem, enemRad, sclEnem, enemyImage, posPlayer, enemAim
    
    pushMatrix()
    translate(posEnem.x, posEnem.y)
    #scale(sclEnem)
    scale(1)
    
    noFill()
    strokeWeight(5)
    stroke(255, 0, 0)
    imageMode(CENTER)
    
    enemAim.set(posPlayer.x,posPlayer.y) 
    enemAim.sub(posEnem)
    #enenAim.normalize();
    #enemAim.mult(speed)
    rotate(enemAim.heading()-PI/2.)
    
    image(enemyImage, 0, 0)
    
    scale(sclEnem)
    #ellipse(0, 0, enemRad.x, enemRad.y)
    
    popMatrix()

#moves the enemy and handles collision detection    
def moveEnem():
    global playerRad, posEnem, posPlayer, playerRad, enemRad, sclEnem, timer, timerRand, velEnem, sclEnem, colDis_enem_player, armour, explode, colDis_enem_ast
    global posAst, astRad, asteroidExplode, posShield, colDis_shield_enem, shieldPower
    
    posEnem.add(velEnem)
    #posEnem.sub(velEnem)
    
    colDis_enem_player = posEnem.dist(posPlayer)
    if(colDis_enem_player < ((playerRad.x/2)*sclMissle+(enemRad.x/2)*sclEnem) or colDis_enem_player < ((playerRad.y/2)*sclMissle+(enemRad.y/2)*sclEnem)):
        armour -= 50
        explode = True
        posExp.set(posEnem)
        spawnEnem()
    
    colDis_enem_ast = posAst.dist(posEnem)
    if(colDis_enem_ast < ((enemRad.x/2)*sclEnem+(astRad.x/2)*sclAst or colDis < ((enemRad.y/2)*sclMissle+(astRad.y/2)*sclAst))):
        spawnEnem()
        asteroidExplode = True
        posAstExp.set(posAst)
        spawnAsteroid()
        
    colDis_shield_enem = posEnem.dist(posShield)
    if(colDis_shield_enem < ((shieldRad.x/2)*sclShield+(enemRad.x/2)*sclEnem) or colDis_shield_enem < ((shieldRad.y/2)*sclShield+(enemRad.y/2)*sclEnem)):
        spawnEnem()
        shieldPower -= 10
    
    if((posEnem.x > width+enemRad.x) or (posEnem.x < 0-enemRad.x)):
        spawnEnem()
    elif((posEnem.y > height+enemRad.y) or (posEnem.y < 0-enemRad.y)):
        spawnEnem()
    
#spawns the enemy      
def spawnEnem():
    global playerRad, posEnem, enemRad, sclEnem, timer, timerRand, velEnem, sclEnem, enemStart, velSetEnem
    
    enemStart = int(random(1, 4))
    #print(enemStart)
    
    #top
    if(enemStart == 1):
        posEnem.set(random(enemRad.x/2*sclEnem, width-enemRad.x/2*sclEnem), 0-enemRad.y/2*sclEnem)
        velEnem.x = 0
        velEnem.y = velSetEnem
    #right
    elif(enemStart == 2):
        posEnem.set(width+enemRad.x, random((enemRad.y/2*sclEnem), (height-enemRad.y/2*sclEnem)))    
        velEnem.x = -velSetEnem
        velEnem.y = 0
    elif(enemStart == 3):
        posEnem.set(random(enemRad.x/2*sclEnem, width-enemRad.x/2*sclEnem), height+enemRad.y/2*sclEnem)
        velEnem.x = 0
        velEnem.y = -velSetEnem
    elif(enemStart == 4):
        posEnem.set(0-enemRad.x*sclEnem, random((enemRad.y/2*sclEnem), (height-enemRad.y/2*sclEnem)))
        velEnem.x = velSetEnem
        velEnem.y = 0
    else:
        print("Unable to set velocity of enemy")

#draws the enemy missile
def drawEnemMissle():
    global posEnem, colDis_enemMissle_player, posEnemMissle, enemMissleRad, enemMissle, rotateCounter
    
    pushMatrix()
    translate(posEnemMissle.x, posEnemMissle.y)
    scale(sclMissleEnem)
    rotate(rotateCounter)
    """
    fill(255, 0, 0)
    stroke(0, 255, 0)
    strokeWeight(2)
    ellipse(0, 0, enemMissleRad.x, enemMissleRad.y)
    """
    imageMode(CENTER)
    image(enemMissle, 0, 0)
    popMatrix()

#handles the movement and collision for the enemy missile
def moveEnemMissle():
    global velEnemMissle, posEnemMissle, enemMissleRad, colDis_enemMissle_player, posEnem, launchEnemMissle, ebCounter, sclMissleEnem, sclPlayer
    global armour, enem_weapon_dmg, colDis_enemMissle_player, sclShield, colDis_shield_enemMissle, shieldRad, posShield, shieldPower
    
    colDis_enemMissle_player = posEnemMissle.dist(posPlayer)
    
    if(colDis_enemMissle_player < ((playerRad.x/2)*sclPlayer+(enemMissleRad.x/2)*sclMissleEnem) or colDis_enemMissle_player < ((playerRad.y/2)*sclPlayer+(enemMissleRad.y/2)*sclMissleEnem)):
        armour -= enem_weapon_dmg
        posEnemMissle.set(posEnem) #resets where the missile is
    
    colDis_shield_enemMissle = posEnemMissle.dist(posShield)
    if(colDis_shield_enemMissle < ((shieldRad.x/2)*sclShield+(enemMissleRad.x/2)*sclMissleEnem) or colDis_shield_enemMissle < ((shieldRad.y/2)*sclShield+(enemMissleRad.y/2)*sclMissleEnem)):
        posEnemMissle.set(posEnem)
        shieldPower -= 10
    
    #launchEnemMissle = True
    if(launchEnemMissle == True):    
        velEnemMissle.set(30, 30)
        #velEnemMissle.add()
        launchEnemMissle = False
        
    posEnemMissle.add(velEnemMissle)
    
    if(posEnemMissle.x > width-50*abs(sclMissleEnem) or posEnemMissle.x < 25+abs(sclMissleEnem)):
        velEnemMissle.x *= -1
        if(ebCounter > 2): 
            posEnemMissle.set(posEnem)
            ebCounter = 0
        else:
            ebCounter += 1
    elif(posEnemMissle.y > height-50*abs(sclMissleEnem) or posEnemMissle.y < 25+abs(sclMissleEnem)):
        velEnemMissle.y *= -1
        if(ebCounter > 2): 
            posEnemMissle.set(posEnem)
            ebCounter = 0
        else:
            ebCounter += 1
    
    #posEnemMissle.add(1)

#draws the explosion
def drawExplosion():
    global posEnem, posExp, sclExp, expAnim, expTimer, explode
    
    if(explode == True):
        pushMatrix()
        translate(posExp.x, posExp.y)
        scale(sclExp)
    
        imageMode(CENTER)
        image(expAnim, 0, 0)    
        
        expTimer -= 1
        if(expTimer < 1):
            explode = False
            expTimer = 120
        popMatrix()
        
#will handle everything to do with drawing text to the screen
def drawStrings():
    global counterText, armourText, shieldText
    
    pushMatrix()
    translate(0, 0)
    scale(1)
    
    textAlign(LEFT)
    textSize(15)
    fill(255, 255, 255)
    #text(counterText, 10, 30)
    textAlign(RIGHT)
    textSize(20)
    text(armourText, width, 50)
    text(scoreText, width, 20)
    text(shieldText, width, 80)
    textAlign(LEFT)
    
    popMatrix()
    
#draws the asteroid to the screen
def drawAsteroid():
    global astImage, astRad, posAst, sclAst
    
    pushMatrix()
    translate(posAst.x, posAst.y)
    scale(sclAst)
 
    imageMode(CENTER)
    image(astImage, 0, 0)
    
    popMatrix()
    
#handles moving and collision detection for the asteroid
def moveAsteroid():
    global posPlayer, playerRad, sclPlayer, astRad, posAst, sclAst, velAst, colDis_player_ast, ast_dmg, armour, asteroidExplode, colDis_enem_ast, shieldRad, sclShield, shieldPower
    
    colDis_player_ast = posAst.dist(posPlayer)
    
    #checks to make sure that their is a collision between the object and the missile
    if(colDis_player_ast < ((playerRad.x/2)*sclPlayer+(astRad.x/2)*sclAst or colDis_player_ast < ((playerRad.y/2)*sclPlayer+(astRad.y/2)*sclAst))): 
        armour -= ast_dmg
        asteroidExplode = True
        posAstExp.set(posAst)
        spawnAsteroid()
        
    colDis_shield_ast = posAst.dist(posShield)
    if(colDis_shield_ast < ((shieldRad.x/2)*sclShield+(astRad.x/2)*sclAst) or colDis_shield_ast < ((shieldRad.y/2)*sclShield+(astRad.y/2)*sclAst)):
        shieldPower -= 10
        spawnAsteroid()
    
    posAst.add(velAst)
    
    if((posAst.x > width+astRad.x) or (posAst.x < 0-astRad.x)):
        spawnAsteroid()
    elif((posAst.y > height+astRad.y) or (posAst.y < 0-astRad.y)):
        spawnAsteroid()
    
#spawns the asteroid
def spawnAsteroid():
    global astStart, posAst, astRad, sclAst
 
    astStart = int(random(1, 4))
    
    #top
    if(astStart == 1):
        posAst.set(random(astRad.x/2*sclAst, width-astRad.x/2*sclAst), 0-astRad.y/2*sclAst)
        velAst.x = int(random(-10, 10))
        velAst.y = 10
    #right
    elif(astStart == 2):
        posAst.set(width+astRad.x, random((astRad.y/2*sclAst), (height-astRad.y/2*sclAst)))    
        velAst.x = -10
        velAst.y = int(random(-10, 10))
    #bottom
    elif(astStart == 3):
        posAst.set(random(astRad.x/2*sclAst, width-astRad.x/2*sclAst), height+astRad.y/2*sclAst)
        velAst.x = int(random(-10, 10))
        velAst.y = -10
    #left
    elif(enemStart == 4):
        posAst.set(0-astRad.x*sclAst, random((astRad.y/2*sclAst), (height-astRad.y/2*sclAst)))
        velAst.x = 10
        velAst.y = int(random(-10, 10))
    else:
        print("Unable to set velocity of asteroid")
    
#draws the explosion of the asteroid
def drawAsteroidExplosion():
    global posAst, posAstExp, sclExp, expAnimAst, expAstTimer, asteroidExplode, expAstTimer
    
    if(asteroidExplode == True):
        pushMatrix()
        translate(posAstExp.x, posAstExp.y)
        scale(sclExp*2)
    
        imageMode(CENTER)
        image(expAnimAst, 0, 0)    
        
        expAstTimer -= 1
        if(expAstTimer < 1):
            asteroidExplode = False
            expAstTimer = 120
        popMatrix()
    
#makes the shield for the player
def shieldPlayer():
    global posPlayer, posShield, sclShield, shieldRad, colDis_shield_enem, colDis_shield_enemMissle, colDis_shield_ast, shieldAnim, shieldPower
    
    if(keyPressed == True and key == ' '):
        if(shieldPower > 1):
            sclShield = 1 
        else:
            shieldPower = 0
    
    pushMatrix()
    translate(posShield.x, posShield.y)
    scale(sclShield)
    
    image(shieldAnim, 0, 0)
    
    popMatrix()
    
#when key is released, do the following
def keyReleased():
    global sclShield, keyHeld
    sclShield = 0
    keyHeld = False
    
#runs automatically when the mouse is clicked
def mouseClicked():
    global posMissle, posPlayer, velMissle, launchMissle, gameState, shoot_sound
    
    if(gameState == True and mouseButton == LEFT):
        if(launchMissle == False):
            shoot_sound.play()
            posMissle.x = mouseX #sets the missle at the mouse x
            posMissle.y = mouseY #sets the missle at the mouse y
            velMissle.set(posPlayer.x, posPlayer.y) #sets the velocity to the position (results in the speed of the projectile)
            velMissle.sub(posMissle) 
            velMissle.mult(.15) #makes the speed slower  
            launchMissle = True
            shoot_sound.rewind()
    
#main draw loop
def draw():
    global bCounter, counterText, launchMissle, posMissle
    
    if(gameState == False):
        initStartScreen()
    else:
        initGame() #mainly used for bypassing the start screen to make it easier to code the game!