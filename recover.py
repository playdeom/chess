import pygame

pygame.init()
WIDTH=800
HEIGHT=800
board=pygame.image.load('img/board.png')
board=pygame.transform.scale(board,(800,800))
knight=pygame.image.load('img/black/bn.png')
knight=pygame.transform.scale(knight,(100,100))

white=(255,255,255)
screen=pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(white)
pygame.display.set_caption("Knight's Tour")
clock = pygame.time.Clock()
fps=60

tour=[[-1 for i in range(8)] for j in range(8)]
dx=[-1,-2,-2,-1,1,2,2,1]
dy=[-2,-1,1,2,2,1,-1,-2]
def check(x, y, n):
    global tour
    if x<0 or x>=n or y<0 or y>=n:return 0
    elif tour[x][y]==-1:return 1
    return 0
def move(x, y, n):
    where_to_go=0
    for i in range(0,8):
        nx=x+dx[i]
        ny=y+dy[i]
        if check(x,y,n):where_to_go+=1
    return where_to_go
def next(x, y, n):
    m=8
    ans=0
    for i in range(0,8):
        nx=x+dx[i]
        ny=y+dy[i]
        if check(nx,ny,n) and move(nx,ny,n)<m:
            m=move(nx,ny,n)
            ans=i
    return ans

def clicked_where(x:int,y:int)->tuple:
    fix_pos=[100,200,300,400,500,600,700,800]
    for i in fix_pos:
        if x<i:
            for j in fix_pos:
                if y<j:
                    return (i-100)//100,(j-100)//100
def make_screen():
    font=pygame.font.Font(None,100)
    title=font.render("Knight's Tour",True,(0,0,0))
    title_r=title.get_rect()
    title_r.center=(400,200)
    screen.blit(title,title_r.topleft)
    font=pygame.font.Font(None,70)
    text=font.render("Click To Play",True,(0,0,0))
    text_r=text.get_rect()
    text_r.center=(400,450)
    screen.blit(text,text_r)
    pygame.draw.rect(screen,green,[get[0],get[1]+2,100,100])
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
        
        pygame.display.update()
make=0 # 0: intro, 1: knight tour
make_screen()