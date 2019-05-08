import sys, pygame, random
pygame.init()
pygame.mixer.init()

# Variables
pressed = False
score = 0
bulim = 30
died = False

# Definations
def imp(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    return running

def mobInit2():
    pattern = [3,2,3,2]
    s = w//pattern[0]
    for j in range(0,len(pattern),2):
        for i in range(0,pattern[j]):
            m = badies((s*i)+s//2,30 + (60*j))
            mobs.add(m)
            allSprites.add(m)
    c = 0
    for j in range(1,len(pattern),2):
        c += 1
        for i in range(0,pattern[j]):
            m = badies(s*(i+1),(60*j)+30)
            mobs.add(m)
            allSprites.add(m)

# Iniitialise
size = w,h = 300,600
fps = 30
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pondo Fights Back")
clock = pygame.time.Clock()

# Colors
black = 0,0,0
white = 255,255,255
red = 255,0,0
green = 0,255,0
blue = 0,0,255

# Sprite Classes
class Player(pygame.sprite.Sprite):
    # sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((30,30))
        #self.image.fill(green)
        self.image = pygame.image.load("Spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = w//2,h-50

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
            
        if self.rect.left > w:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = w

        global pressed
        if not(keys[pygame.K_SPACE]):
            pressed = False
            
        if keys[pygame.K_SPACE] and not(pressed) and len(bullets) != bulim :
            pressed = True
            b = bullet(self.rect.center[0],self.rect.top,10,mobs)
            bullets.add(b)
            print("Bullets left :", bulim - len(bullets))
            allSprites.add(b)
            
class badies(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,20))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        self.speed = random.randint(1,8)

    def update(self):
        # Movement 
        self.rect.x += self.speed
        self.rect.y += 1 if random.randint(0,1) else 0
        if self.rect.left > w:
            self.rect.right = 0

        # Firing
        chance = random.randint(0,1000)
        if chance >= 990:
            b = bullet(self.rect.center[0],self.rect.center[1],-10,players)
            allSprites.add(b)

        # Check if crossed player
        global died
        if self.rect.bottom > player.rect.top:
            died = True
        

class bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,speed,target):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((5,5))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        self.speed = speed
        self.target = target

    def update(self):
        self.rect.y -= self.speed

        global score
        for m in self.target:
            if m.rect.bottom >= self.rect.top:
                if m.rect.top <= self.rect.bottom:
                    if m.rect.left <= self.rect.right:
                        if m.rect.right >= self.rect.left:
                            score += 1
                            self.target.remove(m)
                            allSprites.remove(m)
                            allSprites.remove(self)

# Sprite Init Section
allSprites = pygame.sprite.Group()
players = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
players.add(player)
mobInit2()  # Def to init Mobs
allSprites.add(player)

# Game Loop
running = True
start = False
while running:
    # Processing
    clock.tick(fps)
    running = imp(running)
    # Update
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        start = True
    if start:
        allSprites.update()
        if len(mobs) == 0 or died:
            print("You win")
            running = False
        if len(players) == 0 or len(bullets) == bulim:
            score -= 1
            print("You lose")
            running = False
    # Draw
    screen.fill(black)
    allSprites.draw(screen)
    pygame.display.flip()

print("Your score is : ",score)
pygame.quit()
