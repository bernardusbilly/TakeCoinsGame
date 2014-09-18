import pygame, sys, random, time
from pygame.locals import *
from time import sleep

clock = pygame.time.Clock()
pixel_per_second = 250

class Main(object):
    def __init__(self, width = 640, height = 320, bit=32):
        pygame.init()
        self.width = width 
        self.height = height
        self.screen = pygame.display.set_mode((width, height), 0, bit)
        
        self.bg_music = pygame.mixer.Sound("bg_music.wav")
        self.bg_music.set_volume(0.05)
        self.sound_effect_1 = pygame.mixer.Sound("button_pushed.wav")
        self.sound_effect_1.set_volume(0.1)
        self.sound_effect_2 = pygame.mixer.Sound("lose.wav")
        self.sound_effect_2.set_volume(0.1)
        self.sound_effect_3 = pygame.mixer.Sound("win.wav")
        self.sound_effect_3.set_volume(0.1)
        self.sound_effect_4 = pygame.mixer.Sound("button_2.wav")
        self.sound_effect_4.set_volume(0.1)
        
        self.bg = pygame.image.load("bg.jpg").convert()
        self.billy = pygame.image.load("billy.png").convert_alpha()
        self.win = pygame.image.load("win.png").convert_alpha()
        self.lose = pygame.image.load("lose.png").convert_alpha()
        
        self.ai_1 = pygame.image.load("ai_1.png").convert_alpha()
        self.ai_2 = pygame.image.load("ai_2.png").convert_alpha()
        self.ai_3 = pygame.image.load("ai_3.png").convert_alpha()
        
        self.start_again = pygame.image.load("start_again.png").convert_alpha()
        self.start_again_pushed = pygame.image.load("start_again_pushed.png").convert_alpha()
        self.exit_game = pygame.image.load("exit_game.png").convert_alpha()
        self.exit_game_pushed = pygame.image.load("exit_game_pushed.png").convert_alpha()
        
    def turn(self, coins_left, button):
        coins_left = coins_left - button
        if coins_left <= 0:
            winner = "player"
            self.sound_effect_3.play()
            return coins_left, winner
        alg = Algorithm()
        self.score = alg.score(self.screen, coins_left)
        ai = AI(coins_left)
        coins_left, self.pick = ai.AI_turn()
        if coins_left <= 0:
            winner = "ai"
            self.sound_effect_2.play()
            return coins_left, winner
        return coins_left, None
    
    def MainLoop(self):
        #initialize
        cursor_unclicked = pygame.image.load("cursor.png").convert_alpha()
        cursor_clicked = pygame.image.load("cursor_clicked.png").convert_alpha()
        cursor = cursor_unclicked
        pygame.mouse.set_visible(False)
        self.bg_music.play(loops=-1)
        
        button_1_unpushed = pygame.image.load("button_1.png").convert_alpha()
        button_1_pushed = pygame.image.load("button_1_pushed.png").convert_alpha()
        button_2_unpushed = pygame.image.load("button_2.png").convert_alpha()
        button_2_pushed = pygame.image.load("button_2_pushed.png").convert_alpha()
        button_3_unpushed = pygame.image.load("button_3.png").convert_alpha()
        button_3_pushed = pygame.image.load("button_3_pushed.png").convert_alpha()
        button1 = button_1_unpushed 
        button2 = button_2_unpushed
        button3 = button_3_unpushed
        
        start_button = self.start_again
        exit_button = self.exit_game
        
        alg = Algorithm()
        coins_left = alg.coin
        ai = AI(coins_left)
        winner = None
        self.pick = None
        self.start = int(time.time())
        
        while True:
            #mouse
            x, y = pygame.mouse.get_pos()
            x -= cursor.get_width()-33
            y -= cursor.get_height()-28
            
            #coins always positive integer
            if coins_left <= 0:
                coins_left = 0
            
            #screen
            self.screen.blit(self.bg, (0,0))
            self.score = alg.score(self.screen, coins_left)
            self.screen.blit(button1, (100,200))
            self.screen.blit(button2, (250,200))
            self.screen.blit(button3, (400,200))
            self.screen.blit(self.billy, (220,300))
            self.screen.blit(cursor, (x, y))
            
            if self.pick != None:
                aiLib = {1: self.ai_1, 2: self.ai_2, 3: self.ai_3}
                ai_pick = aiLib[self.pick]
                self.screen.blit(ai_pick, (0,0))
            
            #end game condition
            if coins_left <= 0:
                if winner == "player": 
                    self.screen.blit(self.win, (160,120))
                    self.screen.blit(start_button, (500,50))
                    self.screen.blit(exit_button, (500,100))
                elif winner == "ai": 
                    self.screen.blit(self.lose, (160,120))
                    self.screen.blit(start_button, (500,50))
                    self.screen.blit(exit_button, (500,100))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                #when game is not over
                if winner == None:
                    if event.type == MOUSEBUTTONDOWN:
                        cursor = cursor_clicked
                        if x in range(100,200) and y in range(200,300):
                            button1 = button_1_pushed
                            self.sound_effect_1.play()
                        elif x in range(250,350) and y in range(200,300):
                            button2 = button_2_pushed
                            self.sound_effect_1.play()
                        elif x in range(400,500) and y in range(200,300):
                            button3 = button_3_pushed
                            self.sound_effect_1.play()
                        
                    if event.type == MOUSEBUTTONUP:
                        if button1 == button_1_pushed and x in range(100,200) and y in range(200,300):
                            coins_left, winner = self.turn(coins_left, 1)
                        elif button2 == button_2_pushed and x in range(250,350) and y in range(200,300):
                            coins_left, winner = self.turn(coins_left, 2)
                        elif button3 == button_3_pushed and x in range(400,500) and y in range(200,300):
                            coins_left, winner = self.turn(coins_left, 3)
                        
                        cursor = cursor_unclicked
                        button1 = button_1_unpushed
                        button2 = button_2_unpushed
                        button3 = button_3_unpushed
                        
                    if event.type == KEYDOWN:
                        if event.key == K_1:
                            button1 = button_1_pushed
                            self.sound_effect_1.play()
                        if event.key == K_2:
                            button2 = button_2_pushed
                            self.sound_effect_1.play()
                        if event.key == K_3:
                            button3 = button_3_pushed
                            self.sound_effect_1.play()
                        
                    if event.type == KEYUP:
                        if event.key == K_1:
                            button1 = button_1_unpushed
                            coins_left, winner = self.turn(coins_left, 1)
                        elif event.key == K_2:
                            button2 = button_2_unpushed
                            coins_left, winner = self.turn(coins_left, 2)
                        elif event.key == K_3:
                            button3 = button_3_unpushed
                            coins_left, winner = self.turn(coins_left, 3)
                    
                #when game is over
                else:
                    #measure end time
                    self.end = int(time.time())
                    
                    if event.type == MOUSEBUTTONDOWN:
                        cursor = cursor_clicked
                        if x in range(500,600) and y in range(50,80):
                            start_button = self.start_again_pushed
                        elif x in range(500,600) and y in range(100,130):
                            exit_button = self.exit_game_pushed
                            
                    if event.type == MOUSEBUTTONUP:
                        if start_button == self.start_again_pushed and x in range(500,600) and y in range(50,80):
                            coins_left = (alg.coin + (self.end**2 - self.start)) % 40
                            winner = None
                        elif exit_button == self.exit_game_pushed and x in range(500,600) and y in range(100,130):
                            sys.exit()
                        
                        cursor = cursor_unclicked
                        start_button = self.start_again
                        exit_button = self.exit_game
                    
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            start_button = self.start_again_pushed
                            self.sound_effect_4.play()
                        elif event.key == K_ESCAPE:
                            self.sound_effect_4.play()
                            exit_button = self.exit_game_pushed
                            
                    if event.type == KEYUP:
                        if event.key == K_SPACE:
                            coins_left = (alg.coin + (self.end**2 - self.start)) % 40
                            winner = None
                        elif event.key == K_ESCAPE:
                            sys.exit()
                            
                        start_button = self.start_again
                        exit_button = self.exit_game
                        
            pygame.display.update()
            
                
class Algorithm(object):
    def __init__ (self, coin=random.randrange(1,30)):
        self.coin = coin
    
    def score(self, screen, coin):
        numLib = {0:"0.png", 1:"1.png", 2:"2.png", 3:"3.png", 4:"4.png", 5:"5.png", 6:"6.png", 7:"7.png", 8:"8.png", 9:"9.png"}
        self.digit1 = pygame.image.load(numLib[coin//10]).convert_alpha()
        self.digit2 = pygame.image.load(numLib[coin%10]).convert_alpha()
        screen.blit(self.digit1, (250,50))
        screen.blit(self.digit2, (300,50))
        
class AI(object):
    def __init__(self, coins_left):
        self.coins_left = coins_left
        self.ai_1 = pygame.image.load("ai_1.png").convert_alpha()
        self.ai_2 = pygame.image.load("ai_2.png").convert_alpha()
        self.ai_3 = pygame.image.load("ai_3.png").convert_alpha()
    
    def updateAI(self, screen, pick):
        if pick == 1:
            screen.blit(self.ai_1, (0,0))
        elif pick == 2:
            screen.blit(self.ai_2, (0,0))
        elif pick == 3:
            screen.blit(self.ai_3, (0,0))
            
    def AI_turn(self):
        if self.coins_left < 4:
            pick = self.coins_left
            return self.coins_left - pick, pick
        elif self.coins_left%4 == 0:
            pick = random.randrange(1,4)
            return self.coins_left - pick, pick
        else:
            n = self.coins_left // 4
            pick = self.coins_left - 4*n
            return self.coins_left - pick, pick

if __name__ == "__main__":
    MainWindow = Main()
    MainWindow.MainLoop()
    
    