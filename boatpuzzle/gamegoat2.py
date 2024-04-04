import pygame
import sys

pygame.init()
display_width=1280
display_height=650
gameDisplay=pygame.display.set_mode((display_width,display_height))


#setting color values
black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
light_red=(226,110,110)
light_blue=(173,216,230)
green=(60,179,113)

#setting welcome screen and rules
myfont = pygame.font.Font('freesansbold.ttf', 30)
msg = myfont.render("Welcome to Helping Missionaries & Cannibals!",True, green)
gameDisplay.fill(light_blue)
gameDisplay.blit(msg, [310, 300])
pygame.display.flip()
pygame.time.wait(1500)


msg2 = myfont.render("Your challenge is to move all of characters to the right side of the river",True, green)
gameDisplay.fill(light_blue)
gameDisplay.blit(msg2, [170, 300])
pygame.display.flip()
pygame.time.wait(2500)

thefont = pygame.font.Font('freesansbold.ttf', 24)
msg3 = thefont.render("Rules: 1.The boat can carry at most two people", True, green)
msg4 = thefont.render("           2.If cannibals num greater than missionaries then the"+
                                   " cannibals would eat the missionaries", True, green)
msg5 = thefont.render("           3.The boat cannot cross the river by itself with no"+ 
                                  " people on board",True, green)
gameDisplay.fill(light_blue)
gameDisplay.blit(msg3, [100, 300])
gameDisplay.blit(msg4, [100, 350])
gameDisplay.blit(msg5, [100, 400])

pygame.display.flip()
pygame.time.wait(4500)

 
#loading images
boatImg=pygame.image.load('boat.png')
bgImg=pygame.image.load('bg1.png')
mImg=pygame.image.load('missionary.png')
cImg=pygame.image.load('cannibal.png')
c1Img=pygame.image.load('cannibal1.png')
m1Img=pygame.image.load('missionary1.png')
ngImg=pygame.image.load('newgame.png')
ng1Img=pygame.image.load('newgame1.png')
gameoverImg=pygame.image.load('gameover.png')
wonImg=pygame.image.load('winners.png')
goImg=pygame.image.load('go.png')
go1Img=pygame.image.load('go1.png')
soundonImg=pygame.image.load('soundon.png')
soundoffImg=pygame.image.load('soundoff.png')
gameoversd = pygame.mixer.Sound('music_gameover.wav')
wonsd = pygame.mixer.Sound('music_won.wav')


class boat:
    width = 40
    height = 100
    def __init__(self, x, y, pos,image1,image2,gameDisplay):
        self.x = x
        self.y = y
        self.pos = pos  #position of boat 
        self.image1 = image1
        self.image2 = image2
        self.gameDisplay = gameDisplay

    def highlight(self,a,b,c):
        if self.pos==2 or self.pos==3:
            if c=='M':
                self.gameDisplay.blit(self.image1,(a+20,b-50))
            elif c == 'C':
                self.gameDisplay.blit(self.image2,(a+20,b-50))

        elif self.pos==4 or self.pos==5:
            if c=='M':
                self.gameDisplay.blit(self.image1, (a+180,b-50))
            elif c == 'C':
                self.gameDisplay.blit(self.image2, (a + 180, b - 50))
                
class person:
    width=40
    height=100
    #pos indicate position of M and C;
    #  0 and 1 indicates left and right shore respectively
    # 2 and 4 indicates left an right of boat at left shore
    # 3 and 5 indicates left an right of boat at right shore

    def __init__(self, x,y,x_change,pos,char,leftright,image1,image2,gameDisplay):
        self.leftright=leftright
        self.x=x
        self.y=y
        self.x_change=x_change #change in x for movement of missionary or cannibal
        self.pos=pos
        self.char=char #char indicates character (M for Missionary and C for cannibal)
        self.rect_x = self.x+12
        self.rect_y = self.y
        self.image1=image1
        self.image2=image2
        self.gameDisplay=gameDisplay

    def display(self):
            self.gameDisplay.blit(self.image1, (self.x, self.y))

    def highlight(self):
        self.gameDisplay.blit(self.image2, (self.x, self.y))
        
        
#setting default font
font=pygame.font.SysFont(None,25)
def main():
    x = (display_width * 0.1)
    y = (display_height * 0.8)
    x_change, y_change = 0, 0
    
 
    #creating missionaries and cannibals objects
    mc=[]
    mc.insert(0,person(x-135,y-100,0,0,'M','left',mImg,m1Img,gameDisplay))
    mc.insert(1,person(x-90,y-100,0,0,'M','left',mImg,m1Img,gameDisplay))
    mc.insert(2,person(x-45,y-100,0,0,'M','left',mImg,m1Img,gameDisplay))
    mc.insert(3,person(x-135,y-250,0,0,'C','left',cImg,c1Img,gameDisplay))
    mc.insert(4,person(x-90,y-250,0,0,'C','left',cImg,c1Img,gameDisplay))
    mc.insert(5,person(x-45,y-250,0,0,'C','left',cImg,c1Img,gameDisplay))

    #creating boat position objects
    boats=[]
    boats.insert(0,boat(157,478,2,m1Img,c1Img,gameDisplay))
    boats.insert(1,boat(656,478,3,m1Img,c1Img,gameDisplay))
    boats.insert(2,boat(318,478,4,m1Img,c1Img,gameDisplay))
    boats.insert(3,boat(817,478,5,m1Img,c1Img,gameDisplay))

    pygame.display.set_caption('Missionaries and cannibals')
    clock = pygame.time.Clock()
    crashed = False
    boat_position = 0 #indicates boat at left shore
    a, b = 0, 0
    action = [a, b] #indicates no of missionaries and cannibals to move
    m, c, bt = 3, 3, 1 #indicates 3 missionaries, 3 canibals and boat at left shore
    state = [m, c, bt] #indicates state of missionaries, cannibals and boat at left shore

    gameover = False
    gameoverplayed,wonplayed=False,False
    left,right=False,False
    won=False
    moves=0 #for counting the no of moves

    #loading the background music
    pygame.mixer.music.load('music_bgmusic.mp3')
    pygame.mixer.music.play(-1) #play the bg music infinite times
    sound=True
    while not crashed:
        #loading bgimage and new game image
        gameDisplay.blit(bgImg, (0, 0))
        gameDisplay.blit(ngImg, (1000, 45))
        if sound:
            gameDisplay.blit(soundonImg, (1150, 40))
        else:
            gameDisplay.blit(soundoffImg, (1150, 40))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        #loading the missionaries and cannibals image
        for i in range(6):
            mc[i].display()

        #displaying states, actions, moves        
        state_text = font.render("State: " + str(state), True, black)
        gameDisplay.blit(state_text, [20, 20])
        action_text = font.render("Action: " + str(action), True, black)
        gameDisplay.blit(action_text, [20, 50])
        moves_text = font.render("No. of moves: " + str(moves), True, black)
        gameDisplay.blit(moves_text, [20, 80])
        cur = pygame.mouse.get_pos() #getting cursor position

        #click and point actions of sound button
        if 1150 + 50 > cur[0] > 1150 and 40 + 50 > cur[1] > 40:
            if sound:
                gameDisplay.blit(soundoffImg, (1150, 40))
            else:
                gameDisplay.blit(soundonImg, (1150, 40))
            if pygame.mouse.get_pressed() == (1, 0, 0):
                if sound:
                    sound=False
                    pygame.mixer.music.pause()
                else:
                    sound=True
                    pygame.mixer.music.play()

        #click and point actions of new game button
        if 1000 + 119 > cur[0] > 1000 and 45 + 36 > cur[1] > 45:
            gameDisplay.blit(ng1Img, (1000, 20))
            if pygame.mouse.get_pressed() == (1, 0, 0):
                main()
        gameDisplay.blit(boatImg, (x, y))  #display boat

        #checking gameover
        if (state[0] < state[1] and state[0]>0 )or  (state[0] > state[1] and state[0] < 3 ):
            gameDisplay.blit(gameoverImg, (400, 250))
            gameover = True

        #checking game won
        if state==[0,0,0] and action==[0,0]:
            gameDisplay.blit(wonImg, (400, 250))
            won=True

        if not gameover and not won:
            # click and point actions of go button
            if 590+88 > cur[0] > 590 and 300 + 90 > cur[1] > 300 and action != [0, 0]:
                gameDisplay.blit(go1Img, (590, 300))
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    if boat_position == 0:
                        x_change = 10
                        for i in range(6):
                            if mc[i].pos == 2 or mc[i].pos == 4: mc[i].x_change = 10
                    else:
                        x_change = -10
                        for i in range(6):
                            if mc[i].pos == 3 or mc[i].pos == 5: mc[i].x_change = -10
            else:
                gameDisplay.blit(goImg, (590, 300))

            #stopping condition of boat
            if x >= 620 and boat_position == 0:
                x_change = 0
                for i in range(6):
                    mc[i].x_change=0
                boat_position = 1
                moves+=1
                state[0], state[1], state[2] = state[0] - action[0], state[1] - action[1], 0
                for i in range(6):
                    if mc[i].pos == 2:
                        mc[i].pos = 3
                        mc[i].leftright = 'right'
                        mc[i].rect_x+=900
                    if mc[i].pos == 4:
                        mc[i].pos = 5
                        mc[i].leftright = 'right'
                        mc[i].rect_x += 900
            if x <= 128 and boat_position == 1:
                x_change = 0
                for i in range(6):
                    mc[i].x_change=0
                boat_position = 0
                moves+=1
                state[0], state[1], state[2] = state[0] + action[0], state[1] + action[1], 1
                for i in range(6):
                    if mc[i].pos == 3:
                        mc[i].pos = 2
                        mc[i].rect_x -= 900
                        mc[i].leftright = 'left'
                    if mc[i].pos == 5:
                        mc[i].pos = 4
                        mc[i].leftright = 'left'
                        mc[i].rect_x -= 900

            # if boat is not full
            if action != [1, 1] and action != [0, 2] and action != [2, 0]:
                for i in range(6):
                    # click and point actions of missionary or cannibal at ground
                    if mc[i].rect_x+person.width > cur[0] > mc[i].rect_x and mc[i].rect_y+person.height > cur[1] >mc[i].rect_y  :  
                        if mc[i].pos==0 and mc[i].leftright=='left' and boat_position==0:
                            mc[i].highlight()
                            if pygame.mouse.get_pressed() == (1, 0, 0):
                                if mc[i].char=='M':
                                    a+= 1
                                elif mc[i].char=='C':
                                    b+=1
                                if action == [0, 1] or action == [1, 0]:
                                    for k in range(6):
                                        if mc[k].pos == 2:
                                            left = True
                                        if mc[k].pos == 4:
                                            right = True
                                    if left:
                                        mc[i].x, mc[i].y = x + 180, y - 50
                                        mc[i].pos = 4
                                    elif right:
                                        mc[i].x, mc[i].y = x + 20, y - 50
                                        mc[i].pos = 2
                                else:
                                    mc[i].x, mc[i].y = x + 20, y - 50
                                    mc[i].pos = 2

                        elif mc[i].pos==1 and   mc[i].leftright == 'right' and boat_position == 1:
                            mc[i].highlight()
                            if pygame.mouse.get_pressed() == (1, 0, 0):
                                if mc[i].char == 'M':
                                    a += 1
                                elif mc[i].char == 'C':
                                    b += 1
                                if action == [0, 1] or action == [1, 0]:
                                    for k in range(6):
                                        if mc[k].pos == 3:
                                            left = True
                                        if mc[k].pos == 5:
                                            right = True
                                    if left:
                                        mc[i].x, mc[i].y = x + 180, y - 50
                                        mc[i].pos = 5
                                    elif right:
                                        mc[i].x, mc[i].y = x + 20, y - 50
                                        mc[i].pos = 3
                                else:
                                    mc[i].x, mc[i].y = x + 20, y - 50
                                    mc[i].pos = 3
                                print(i, mc[i].x, mc[i].y)

            # if any 1 or more person on boat
            if action != [0, 0]:
                for j in range(4):
                    if boats[j].x + boat.width > cur[0] > boats[j].x and boats[j].y + boat.height > cur[1] > boats[j].y:
                        k = 7
                        for i in range(6):
                            if mc[i].pos == boats[j].pos:
                                k = i
                        if k != 7:
                            boats[j].highlight(x,y,mc[k].char)
                            if pygame.mouse.get_pressed() == (1, 0, 0):
                                if mc[k].char=='M':
                                    a -= 1
                                elif mc[k].char == 'C':
                                    b -= 1
                                if mc[k].leftright=='left':
                                    mc[k].x, mc[k].y = mc[k].rect_x - 12, mc[k].rect_y
                                    mc[k].pos = 0
                                elif mc[k].leftright=='right':
                                    mc[k].x, mc[k].y = mc[k].rect_x - 12, mc[k].rect_y
                                    mc[k].pos = 1
                                if boats[j].pos==2 or boats[j].pos==3:
                                    left = False
                                elif boats[j].pos==4 or boats[j].pos==5:
                                    right = False

            #update boat position for movement
            x = x + x_change

            #update missionary and cannibal position for movement
            for i in range(6):
                mc[i].x += mc[i].x_change
            action = [a, b]

        #actions for gameover
        elif gameover and not gameoverplayed:
            pygame.mixer.music.stop()
            gameoversd.play(0)
            gameoverplayed=True

        #actions for game won
        elif won and not wonplayed:
            pygame.mixer.music.stop()
            wonsd.play(0)
            wonplayed = True

        pygame.display.update()
        clock.tick(25)

    pygame.quit()
    quit()

if __name__=="__main__":
    main()
