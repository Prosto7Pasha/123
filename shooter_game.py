from  pygame import *
from random import *
from time import time as timer

font.init()

mixer.init()
mixer.music.load('strar wars music.mp3')
mixer.music.set_volume(0.05)
mixer.music.play(-1)
fire_sound = mixer.Sound('fire_sound.ogg')

font.init()
font = font.SysFont('lucidasans',35)
win = font.render('You win!',True,(255,255,255))
lose = font.render('You lose!',True,(255,255,255))

score = 0
lost = 0
life = 5
rel_time = False
num_fire = 0


class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed,width,height):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w ] and self.rect.y >0:
            self.rect.y -=  self.speed
        if keys_pressed[K_s] and self.rect.y < 1050:
            self.rect.y +=  self.speed
        if keys_pressed[K_a] and self.rect.x  >0:
            self.rect.x -=  self.speed
        if keys_pressed[K_d]  and self.rect.x < 1600:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx,self.rect.top, 20, 15, 50)
        bullets.add(bullet)
    


lost = 0
class Vilian(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 1050:
            self.rect.y = 0
            self.rect.x = randint(50,1600-50)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <0:
            self.kill()




hero = Player('player.png',800,950,25,100,100)      

bullets = sprite.Group()        


vilians = sprite.Group()
for i in range(15):
    vilian =  Vilian('vilian.png',randint(150,1600), - 50,randint(5, 10),100,100)
    vilians.add(vilian)

vil_buls = sprite.Group()
for i in range(5):
    vil_bul =  Vilian('vil_bul.png',randint(150,1600), - 50,randint(10, 20),27,100)
    vil_buls.add(vil_bul)




window = display.set_mode((1600,1050))
display.set_caption('2D Star Wars')

background = transform.scale(image.load('background.jpg'), (1600,1050))


game = True
finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN and e.key == K_SPACE:
            if num_fire < 15 and rel_time == False:
                fire_sound.play()
                hero.fire()
                num_fire += 1

            if num_fire >= 15 and rel_time == False:
                last_time = timer()
                rel_time = True

    if not finish:
        hero.update()    
        vilians.update()
        bullets.update()
        vil_buls.update()
        window.blit(background,(0,0))

        text = font.render('Очки: ' + str(score),True,(255,255,255))
        text_lose = font.render('Пропущенно : ' +str(lost),True,(255,255,255))
        window.blit(text,(10,20))
        window.blit(text_lose,(10,50))

        hero.reset()
        vilians.draw(window)
        bullets.draw(window)
        vil_buls.draw(window)

        if rel_time:
            now_time = timer()
            if now_time - last_time < 5:
                rel = font.render('Пергрев', True,(200,0,0))
                window.blit(rel,(250,450))

            else:
                num_fire = 0
                rel_time = False

        
        sprites_list = sprite.groupcollide(vilians,bullets,True,True)
        for c in sprites_list:
            vilian =  Vilian('vilian.png',randint(150,1600), - 50,randint(5, 10),100,100)
            score +=1
            vilians.add(vilian)

        if sprite.spritecollide(hero,vilians,False) :
            finish = True
            window.blit(lose,(950,540))

        if sprite.spritecollide(hero,vil_buls,True):
            vil_bul =  Vilian('vil_bul.png',randint(150,1600), - 50,randint(10, 20),35,100)
            vil_buls.add(vil_bul)
            life -=1
        if life < 1:
            finish = True
            window.blit(lose,(950,540))

        if score > 30:
            finish = True
            window.blit(win,(950,540))

        if life == 5 or 4:
            life_color = (0,255,0)

        if life == 3 or 2:
            life_color = (150,150,0)

        if life == 1 or 0 :
            life_color = (150,0,0)

        teext_life = font.render(str(life),True,life_color)
        window.blit(teext_life,(650,10))
        display.update()



        display.update()

    else:
        finish = False
        score = 0
        lost=0
        for b in bullets:
            b.kill()
        for v in vilians:
            v.kill()
        for a in vil_buls:
            a.kill()
        time.delay(2000)
        
        for i in range(20):
            vilian =  Vilian('vilian.png',randint(150,1600), - 50,randint(5, 10),100,100)
            vilians.add(vilian)

        for i in range(5):
            vil_bul =  Vilian('vil_bul.png',randint(150,1600), - 50,randint(10, 20),35,100)

    time.delay(3)





