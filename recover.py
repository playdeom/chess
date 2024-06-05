import pygame

pygame.init()
WIDTH=800
HEIGHT=800
board=pygame.image.load('img/board.png')
board=pygame.transform.scale(board,(800,800))
knight=pygame.image.load('img/black/bn.png')
knight=pygame.transform.scale(knight,(100,100))

white=(255,255,255)
green=(0,255,0)
screen=pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(white)
pygame.display.set_caption("Knight's Tour")
clock = pygame.time.Clock()
fps=60

tour=[[-1 for i in range(8)] for j in range(8)]
dx=[-1,-2,-2,-1,1,2,2,1]
dy=[-2,-1,1,2,2,1,-1,-2]
def check(x, y):
    global tour
    if x<0 or x>=8 or y<0 or y>=8:return 0
    elif tour[x][y]==-1:return 1
    return 0
def move(x, y):
    where_to_go=0
    for i in range(0,8):
        nx=x+dx[i]
        ny=y+dy[i]
        if check(nx,ny):where_to_go+=1
    return where_to_go
def next(x, y):
    m=8
    ans=0
    for i in range(0,8):
        nx=x+dx[i]
        ny=y+dy[i]
        if check(nx,ny) and move(nx,ny)<m:
            ans=i
            m=move(nx,ny)
    return ans
def knight_tour():
    global tour
    run=1
    isclick=0
    while run:
        clock.tick(fps)
        screen.blit(board,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    run=0
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                clicked=pygame.mouse.get_pos()
                get=list(clicked_where(clicked[0],clicked[1]))
                x,y=get[0],get[1]
                
                tour[get[0]][get[1]]=0
                for i in range(1,64):
                    if move(get[0],get[1])==0:
                        noneto_move()
                        pygame.quit()
                    nw=next(get[0],get[1])
                    print(f'nw: {nw}')
                    get[0]+=dx[nw]
                    get[1]+=dy[nw]
                    print(get)
                    tour[get[0]][get[1]]=i
                now=0
                ni=pygame.image.load('img/black/bn.png')
                ni=pygame.transform.scale(ni,(100,100))
                screen.blit(ni,(x*100,y*100))
                pygame.display.flip()
                for i in range(1,8*8):
                    for j in range(8):
                        nx=x+dx[j]
                        ny=y+dy[j]
                        if nx<0 or nx>=8 or ny<0 or ny>=8:continue
                        if tour[nx][ny]==now+1:
                            font=pygame.font.Font(None,100)
                            import random
                            title=font.render(f"{now+1}",True,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
                            title_r=title.get_rect()
                            title_r.center=(400,200)
                            screen.blit(title,(nx*100,ny*100))
                            pygame.display.flip()
                            pygame.time.wait(125)
                            now+=1
                            x,y=nx,ny
                pygame.time.wait(1000)
                tour=[[-1 for i in range(8)] for j in range(8)]

        pygame.display.update()
        
def noneto_move():
    pass
def clicked_where(x:int,y:int)->tuple:
    fix_pos=[100,200,300,400,500,600,700,800]
    for i in fix_pos:
        if x<i:
            for j in fix_pos:
                if y<j:
                    return (i-100)//100,(j-100)//100
def make_screen():
    screen.fill(white)
    font=pygame.font.Font(None,100)
    title=font.render("Knight's Tour",True,(0,0,0))
    title_r=title.get_rect()
    title_r.center=(400,200)
    screen.blit(title,title_r.topleft)
    font=pygame.font.Font(None,70)
    text=font.render("Click To Play",True,(0,0,0))
    text_r=text.get_rect()
    text_r.center=(400,450)
    click=pygame.draw.rect(screen,green,[200,400+2,400,100])
    screen.blit(text,text_r)
    run=1
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=0
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                clicked=pygame.mouse.get_pos()
                get=clicked_where(clicked[0],clicked[1])
                print(get)
                if click.collidepoint(event.pos):
                    knight_tour()
        pygame.display.update()
make=0 # 0: intro, 1: knight tour
make_screen()