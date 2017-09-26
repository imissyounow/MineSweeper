import pygame
from pygame.locals import *
import random
import sys
import traceback
import time

pygame.init()

bg_size = width,height = 495,495
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('扫雷')

#载入图片
bomb_image = pygame.image.load('material/bomb.png').convert()
current_bomb_image = pygame.image.load('material/current_bomb.png').convert()
normal_grid_image = pygame.image.load('material/grid.png').convert()
num0_image = pygame.image.load('material/0.png').convert()
num_image = []
num_image.extend([\
    pygame.image.load('material/1.png').convert(),\
    pygame.image.load('material/2.png').convert(),\
    pygame.image.load('material/3.png').convert(),\
    pygame.image.load('material/4.png').convert(),\
    pygame.image.load('material/5.png').convert(),\
    pygame.image.load('material/6.png').convert(),\
    pygame.image.load('material/7.png').convert(),\
    pygame.image.load('material/8.png').convert()\
    ])
light_grid_image = pygame.image.load('material/new.png').convert()
normal_flag_image = pygame.image.load('material/normal_flag.png').convert()
light_flag_image = pygame.image.load('material/light_flag.png').convert()
background_image = pygame.image.load('material/background.png').convert()
game_start_image = pygame.image.load('material/game_start.png').convert_alpha()
game_start_rect = game_start_image.get_rect()
game_start_rect.left,game_start_rect.top = (width-game_start_rect.width)//2,150
game_reagain_image = pygame.image.load('material/game_Reagain.png').convert_alpha()
game_reagain_rect = game_reagain_image.get_rect()
game_reagain_rect.left,game_reagain_rect.top = (width-game_reagain_rect.width)//2,150
game_over_image = pygame.image.load('material/game_over.png').convert_alpha()
game_over_rect = game_over_image.get_rect()
game_over_rect.left,game_over_rect.top = (width-game_over_rect.width)//2,250
gameover_font = pygame.font.Font('material/a.ttf',60)

def count_bomb(data,i,j):
    count = 0
    if ((data[i-1][j-1] == -1) if i>0 and j>0 else False):
        count+=1
    if ((data[i-1][j] == -1) if i>0 else False):
        count+=1
    if ((data[i-1][j+1]) == -1 if i>0 and j<8 else False):
        count+=1
    if ((data[i][j-1]) == -1 if j>0 else False):
        count+=1
    if ((data[i][j+1]) == -1 if j<8 else False):
        count+=1
    if ((data[i+1][j-1]) == -1 if i<8 and j>0 else False):
        count+=1
    if ((data[i+1][j]) == -1 if i<8 else False):
        count+=1
    if ((data[i+1][j+1]) == -1 if i<8 and j<8 else False):
        count+=1
    return count

BOMB_TOTAL = 10
bomb_index = []
bomb_pos=[]
clock = pygame.time.Clock()
WHITE = (255,255,255)



def spread(data,i,j,used,solved):
    used[i][j]=1
    solved[i][j]=1
    if data[i][j] == 0:
        screen.blit(num0_image,(i*55,j*55))

        if i>0 and j>0 and not used[i-1][j-1] and data[i-1][j-1]>0:
            screen.blit(num_image[data[i-1][j-1]-1],((i-1)*55,(j-1)*55))
            solved[i-1][j-1] = 1
            used[i-1][j-1] = 1
        if i>0 and j<8 and not used[i-1][j+1] and data[i-1][j+1]>0:
            screen.blit(num_image[data[i-1][j+1]-1],((i-1)*55,(j+1)*55))
            used[i-1][j+1] = 1
            solved[i-1][j+1] = 1
        if i<8 and j>0 and not used[i+1][j-1] and data[i+1][j-1]>0:
            screen.blit(num_image[data[i+1][j-1]-1],((i+1)*55,(j-1)*55))
            used[i+1][j-1] = 1
            solved[i+1][j-1] = 1
        if i<8 and j<8 and not used[i+1][j+1] and data[i+1][j+1]>0:
            screen.blit(num_image[data[i+1][j+1]-1],((i+1)*55,(j+1)*55))
            used[i+1][j+1] = 1
            solved[i+1][j+1] = 1
            
        if i>0 and not used[i-1][j]:
            spread(data,i-1,j,used,solved)
        if i<8 and not used[i+1][j]:
            spread(data,i+1,j,used,solved)
        if j>0 and not used[i][j-1]:
            spread(data,i,j-1,used,solved)
        if j<8 and not used[i][j+1]:
            spread(data,i,j+1,used,solved)

        if i>0 and j>0 and not used[i-1][j-1] and data[i-1][j-1]==0:
            spread(data,i-1,j-1,used,solved)
        if i>0 and j<8 and not used[i-1][j+1] and data[i-1][j+1]==0:
            spread(data,i-1,j+1,used,solved)
        if i<8 and j>0 and not used[i+1][j-1] and data[i+1][j-1]==0:
            spread(data,i+1,j-1,used,solved)
        if i<8 and j<8 and not used[i+1][j+1] and data[i+1][j+1]==0:
            spread(data,i+1,j+1,used,solved)
                
    elif data[i][j] > 0:
        screen.blit(num_image[data[i][j]-1],(i*55,j*55))

def main():
    active = False
    need_refresh = True
    start = True
    end = False
    success = False

    screen.blit(background_image,(0,0))
    screen.blit(game_start_image,game_start_rect)
    screen.blit(game_over_image,game_over_rect)
    pygame.display.flip()
    
    while True:
        
        if need_refresh:
            end = False
            need_refresh = False
            data = [[0 for i in range(9)]for i in range(9)]
            solved = [[0 for i in range(9)]for i in range(9)]
            flaged = [[0 for i in range(9)]for i in range(9)]
            used = [[0 for i in range(9)]for i in range(9)]
            while len(bomb_index) < BOMB_TOTAL:
                a = random.randint(0,80)
                if a not in bomb_index:
                    bomb_index.append(a)
        
            count = 0
            for i in range(9):
                for j in range(9):
                    if count in bomb_index:
                        data[i][j] = -1
                        bomb_pos.append((i,j))
                    count += 1

            for i in range(9):
                for j in range(9):
                    if data[i][j] != -1:
                        data[i][j] = count_bomb(data,i,j)

        if not active:
            if end:
                screen.blit(background_image,(0,0))
                screen.blit(game_reagain_image,game_reagain_rect)
                screen.blit(game_over_image,game_over_rect)

                if success:
                    success_text = gameover_font.render('YOU WIN!',True,WHITE)
                    success_rect = success_text.get_rect()
                    success_rect.left,success_rect.top = (width - success_rect.width)//2, 50
                    screen.blit(success_text,success_rect)
                    
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and game_start_rect.collidepoint(event.pos):
                        active = True
                        need_refresh = True

                    if event.button == 1 and game_over_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        
        if active and not end:         
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    a = event.pos[0]//55
                    b = event.pos[1]//55
                    if not solved[a][b]:
                        if event.button == 1:
                            if data[a][b] > 0:
                                screen.blit(num_image[data[a][b]-1],(a*55,b*55))
                                solved[a][b]=1
                            elif data[a][b] == -1:
                                for pos in bomb_pos:
                                    screen.blit(bomb_image,(pos[0]*55,pos[1]*55))
                                    solved[pos[0]][pos[1]]=1
                                screen.blit(current_bomb_image,(a*55,b*55))
                                pygame.display.flip()
                                active = False
                                end = True
                                
                                
                            else:
                                spread(data,a,b,used,solved)

                        else:
                            screen.blit(normal_flag_image,(a*55,b*55))
                            flaged[a][b]=1
        
            for i in range(9):
                for j in range(9):
                    if (not solved[i][j]) and (not flaged[i][j]):
                        screen.blit(normal_grid_image,(i*55,j*55))

            sweeper_num = 0
            for i in range(9):
                sweeper_num += solved[i].count(1)
            if sweeper_num == 81 - BOMB_TOTAL:
                active = False
                end = True
                success = True
    
 
            pygame.display.flip()

            clock.tick(60)
                        
        

if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
