import pygame

pygame.init()
WIDTH=800
HEIGHT=800
board=pygame.image.load('img/board.png')
board=pygame.transform.scale(board,(800,800))

types=['p','r','n','b','q','k'] #0, 1, 2, 3, 4, 5
white=[pygame.image.load(f'img/white/w{i}.png') for i in types]
black=[pygame.image.load(f'img/black/b{i}.png') for i in types]
for i in range(6):
    white[i]=pygame.transform.scale(white[i],(100,100))
    black[i]=pygame.transform.scale(black[i],(100,100))

screen=pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fps=60

field=dict() # (x -> int, y -> int) : [which -> int, color -> str, moved -> int]
# which is number of pieces in "types" array
for i in range(0,800,100):
    for j in range(0,800,100):
        field[(i,j)]=[-1,'',0]

# preset of pieces 
make_set=[1,2,3,4,5,3,2,1]
for i in range(0,800,100):
    field[(i,100)]=[0,'b',0]
    field[(i,600)]=[0,'w',0]
    field[(i,0)]=[make_set[i//100],'b',0]
    field[(i,700)]=[make_set[i//100],'w',0]

# fix click pos
gray=(150,150,150)
yellow=(255,255,153)
def make_board()->None:
    screen.blit(board,[0,0])
    
    for (x,y),arr in field.items():
        if arr[1]=='w':
            screen.blit(white[arr[0]],[x,y])
        elif arr[1]=='b':
            screen.blit(black[arr[0]],[x,y])
def show_click(get:tuple)->None:
    pygame.draw.rect(screen,yellow,[get[0],get[1]+2,100,100])
    for (x,y),arr in field.items():
        if arr[1]=='w':
            screen.blit(white[arr[0]],[x,y])
        elif arr[1]=='b':
            screen.blit(black[arr[0]],[x,y])
def flip_board()->None:
    global field,white_king_pos,black_king_pos
    for i in range(0,800,100):
        for j in range(0,400,100):
            field[(i,j)],field[(700-i,700-j)]=field[(700-i,700-j)],field[(i,j)]
    white_king_pos=[700-white_king_pos[0],700-white_king_pos[1]]
    black_king_pos=[700-black_king_pos[0],700-black_king_pos[1]]

def clicked_where(x:int,y:int)->tuple:
    fix_pos=[100,200,300,400,500,600,700,800]
    for i in fix_pos:
        if x<i:
            for j in fix_pos:
                if y<j:
                    return i-100,j-100

def print_cant_move(n:list)->bool:
    #print(len(n))
    if len(n)==0:
        font=pygame.font.Font(None,100)
        out=font.render("Can't move",True,(0,0,0))
        out_make=out.get_rect()
        out_make.centerx=400
        out_make.centery=400
        screen.blit(out,out_make)
        pygame.display.update()
        pygame.time.delay(500)
        return 0
    return 1
def mover(run:int,x:int,y:int,can:list,types:int)->int:
    global white_king_pos,black_king_pos,field
    # not for a king
    forbiden=[]
    print(can)
    save=field[(x,y)]
    for i in range(len(can)):
        #print(field[(x,y)],field[(can[i][0],can[i][1])])
        field[(x,y)],field[(can[i][0],can[i][1])]=field[(can[i][0],can[i][1])],field[(x,y)]
        if save[1]=='w':checker=before_check(white_king_pos[0],white_king_pos[1])
        else:checker=before_check(black_king_pos[0],black_king_pos[1])
        field[(x,y)],field[(can[i][0],can[i][1])]=field[(can[i][0],can[i][1])],field[(x,y)]
        if checker:forbiden.append((can[i][0],can[i][1]))
        else:
            pygame.draw.circle(screen,gray,[can[i][0]+50,can[i][1]+50],25)
            pygame.display.update()
        #print(field[(x,y)],field[(can[i][0],can[i][1])])
    moved=0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                clicked=pygame.mouse.get_pos()
                get=clicked_where(clicked[0],clicked[1])
                if (get in can) and not (get in forbiden):
                    field[get]=[types,field[(x,y)][1],1]
                    field[(x,y)]=[-1,'',0]
                    moved=1
                run=0
    return moved
def mover_for_king(run:int,x:int,y:int,can:list,types:int)->int:
    global white_king_pos,black_king_pos
    #here u have to make some funcs enjoy :)
    
    moved=0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                clicked=pygame.mouse.get_pos()
                get=clicked_where(clicked[0],clicked[1])
                if get in can:
                    if types==5 and field[(x,y)][2]==0:
                        if field[(x,y)][1]=='w':
                            if get==(600,700):
                                field[(500,700)]=[1,field[(700,700)][1],1]
                                field[(700,700)]=[-1,'',0]
                            elif get==(200,700):
                                field[(300,700)]=[1,field[(0,700)][1],1]
                                field[(0,700)]=[-1,'',0]
                            white_king_pos=[get[0],get[1]]
                        else:
                            if get==(500,700):
                                field[(400,700)]=[1,field[(700,700)][1],1]
                                field[(700,700)]=[-1,'',0]
                            elif get==(100,700):
                                field[(200,700)]=[1,field[(0,700)][1],1]
                                field[(0,700)]=[-1,'',0]
                            black_king_pos=[get[0],get[1]]
                    field[get]=[types,field[(x,y)][1],1]
                    field[(x,y)]=[-1,'',0]
                    moved=1
                run=0
    return moved

def p_move(x:int,y:int,moved:int)->int:
    #pown guide line two dots when pown moved value is 0 or one dot in front of pown
    global field
    dx=[0,0,-100,100]
    dy=[-100,-200,-100,-100]
    can=[]
    # i have to make ang pa sang rules but i will do it later.
    for i in range(4):
        nx=x+dx[i]
        ny=y+dy[i]
        if nx<0 or ny<0 or nx>700 or ny>700:continue
        if i==1 and moved!=0:continue
        if i in [2,3]:
            if field[(nx,ny)][0]!=-1 and field[(nx,ny)][1]!=field[(x,y)][1]:
                can.append((nx,ny))
                #pygame.draw.circle(screen,gray,[nx+50,ny+50],25)
            continue
        if field[(nx,ny)][0]==-1:
            if i==1 and field[(nx,y-100)][0]!=-1:continue
            can.append((nx,ny))
            #pygame.draw.circle(screen,gray,[nx+50,ny+50],25)
    pygame.display.update()
    run=print_cant_move(can)
    return mover(run,x,y,can,0)

def k_move(x:int,y:int)->int:
    global field
    dx=[100,100,100,-100,-100,-100,0,0]
    dy=[0,-100,100,0,-100,100,-100,100]
    can=[]
    for i in range(8):
        nx,ny=x+dx[i],y+dy[i]
        if nx<0 or ny<0 or nx>700 or ny>700:continue
        if field[(nx,ny)][0]==-1:
            can.append((nx,ny))
            pygame.draw.circle(screen,gray,[nx+50,ny+50],25)
        elif field[(nx,ny)][1]!=field[(x,y)][1]:
            can.append((nx,ny))
            pygame.draw.circle(screen,gray,[nx+50,ny+50],25)
    if field[(x,y)][2]==0:
        c1,c2=1,1
        for i in range(x+100,700,100):
            if field[(i,y)][0]!=-1:
                c1=0
        for i in range(100,x,100):
            if field[(i,y)][0]!=-1:
                c2=0
        if field[(x,y)][1]=='w':
            if c1:can.append((600,700));pygame.draw.circle(screen,gray,[650,750],25)
            if c2:can.append((200,700));pygame.draw.circle(screen,gray,[250,750],25)
        elif field[(x,y)][1]=='b':
            if c1:can.append((500,700));pygame.draw.circle(screen,gray,[550,750],25)
            if c2:can.append((100,700));pygame.draw.circle(screen,gray,[150,750],25)


    pygame.display.update()
    run=print_cant_move(can)
    return mover_for_king(run,x,y,can,5)
def r_move(x:int,y:int)->int:
    dx=[1,-1,0,0]
    dy=[0,0,1,-1]
    can=[]
    for i in range(4):
        #run while cant go
        eat=1
        for j in range(0,800,100):
            nx=x+dx[i]*j
            ny=y+dy[i]*j
            if nx<0 or ny<0 or nx>700 or ny>700:continue
            if field[(nx,ny)][0]==-1 and eat:
                can.append((nx,ny))
                #pygame.draw.circle(screen,gray,[nx+50,ny+50],25)
            else:
                if field[(nx,ny)][1]!=field[(x,y)][1] and eat:
                    can.append((nx,ny))
                    #pygame.draw.circle(screen,gray,[nx+50,ny+50],25)
                    eat=0
                elif field[(nx,ny)][1]==field[(x,y)][1] and j!=0:break
    pygame.display.update()
    run=print_cant_move(can)
    return mover(run,x,y,can,1)
def n_move(x:int,y:int)->int:
    dx=[100,100,200,200,-100,-100,-200,-200]
    dy=[200,-200,100,-100,200,-200,100,-100]
    can=[]
    for i in range(8):
        nx=x+dx[i]
        ny=y+dy[i]
        if nx<0 or ny<0 or nx>700 or ny>700:continue
        if field[(nx,ny)][0]==-1:
            can.append((nx,ny))
            #pygame.draw.circle(screen,gray,[nx+50,ny+50],25)
        elif field[(nx,ny)][1]!=field[(x,y)][1]:
            can.append((nx,ny))
            #pygame.draw.circle(screen,gray,[nx+50,ny+50],25)
    pygame.display.update()
    run=print_cant_move(can)
    return mover(run,x,y,can,2)
def b_move(x:int,y:int)->int:
    dx=[1,1,-1,-1]
    dy=[-1,1,-1,1]
    can=[]
    for i in range(4):
        eat=1
        for j in range(0,800,100):
            nx=x+dx[i]*j
            ny=y+dy[i]*j
            if nx<0 or ny<0 or nx>700 or ny>700:continue
            if field[(nx,ny)][0]==-1 and eat:
                can.append((nx,ny))
                #pygame.draw.circle(screen,gray,[nx+50,ny+50],25)
            else:
                if field[(nx,ny)][1]!=field[(x,y)][1] and eat:
                    can.append((nx,ny))
                    #pygame.draw.circle(screen,gray,[nx+50,ny+50],25)
                    eat=0
                elif field[(nx,ny)][1]==field[(x,y)][1] and j!=0:break
    pygame.display.update()
    run=print_cant_move(can)
    return mover(run,x,y,can,3)
def q_move(x:int,y:int)->int:
    dx=[1,-1,0,0,1,1,-1,-1]
    dy=[0,0,1,-1,-1,1,-1,1]
    can=[]
    for i in range(8):
        eat=1
        for j in range(0,800,100):
            if j==0:continue
            nx=x+dx[i]*j
            ny=y+dy[i]*j
            if nx<0 or ny<0 or nx>700 or ny>700:continue
            if field[(nx,ny)][0]==-1 and eat:
                can.append((nx,ny))
                #pygame.draw.circle(screen,gray,[nx+50,ny+50],25)
            else:
                if field[(nx,ny)][1]!=field[(x,y)][1] and eat:
                    can.append((nx,ny))
                    #pygame.draw.circle(screen,gray,[nx+50,ny+50],25)
                    eat=0
                elif field[(nx,ny)][1]==field[(x,y)][1] and j!=0:break
    pygame.display.update()
    run=print_cant_move(can)
    return mover(run,x,y,can,4)

def before_check(x:int,y:int) -> bool:
    #check when any piece move
    #use king pos
    global field
    dx=[1,-1,0,0,1,1,-1,-1]
    dy=[0,0,1,-1,-1,1,-1,1]
    for i in range(4): # check rook and queen
        for j in range(0,800,100):
            if j==0:continue
            nx=x+dx[i]*j
            ny=y+dy[i]*j
            if nx<0 or ny<0 or nx>700 or ny>700:continue
            if field[(nx,ny)][1]!=field[(x,y)][1]:
                if field[(nx,ny)][0] in [1,4]:
                    #print(f'check by 1 or 4')
                    return 1
            else:break
    for i in range(4,8): # check bisup and queen
        for j in range(0,800,100):
            if j==0:continue
            nx=x+dx[i]*j
            ny=y+dy[i]*j
            if nx<0 or ny<0 or nx>700 or ny>700:continue
            if field[(nx,ny)][1]!=field[(x,y)][1]:
                if field[(nx,ny)][0] in [3,4]:
                    #print(f'check by 3 or 4')
                    return 1
            else:break
    dx=[100,100,200,200,-100,-100,-200,-200]
    dy=[200,-200,100,-100,200,-200,100,-100]
    for i in range(8): # check knight
        nx=x+dx[i]
        ny=y+dy[i]
        if nx<0 or ny<0 or nx>700 or ny>700:continue
        if field[(nx,ny)][0]==2:
            if field[(nx,ny)][1]!=field[(x,y)][1]:
                #print(f'check by 2')
                return 1
    return 0
def now_check(x:int,y:int) -> bool:
    dx=[100,-100]
    dy=[-100,-100]
    for i in range(2): # check pown <- may be this got be error
        nx=x+dx[i]
        ny=y+dy[i]
        if nx<0 or ny<0 or nx>700 or ny>700:continue
        if field[(nx,ny)][0]==0:
            if field[(nx,ny)][1]!=field[(x,y)][1]:
                #print(f'check by 0')
                return 1
    return 0





# under here is main loop

run=1
turn=1 # 1: white, 0: black
#if turn is end, then borad is swaped in 180 degree
white_king_pos,black_king_pos=[400,700],[400,0]
white_king_check,black_king_check=0,0
#to check check where is king 
while run:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=0
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            clicked=pygame.mouse.get_pos()
            get=clicked_where(clicked[0],clicked[1])
            # check empty place
            now_f=field[(get[0],get[1])]
            if turn==1 and now_f[1]=='w':
                moved=0
                show_click(get)
                if now_f[0]==0:
                    moved=p_move(get[0],get[1],now_f[2])
                if now_f[0]==1:
                    moved=r_move(get[0],get[1])
                if now_f[0]==2:
                    moved=n_move(get[0],get[1])
                if now_f[0]==3:
                    moved=b_move(get[0],get[1])
                if now_f[0]==4:
                    moved=q_move(get[0],get[1])
                if now_f[0]==5:
                    moved=k_move(get[0],get[1])
                if moved:turn=0;flip_board()
            elif turn==0 and now_f[1]=='b':
                moved=0
                show_click(get)
                if now_f[0]==0:
                    moved=p_move(get[0],get[1],now_f[2])
                if now_f[0]==1:
                    moved=r_move(get[0],get[1])
                if now_f[0]==2:
                    moved=n_move(get[0],get[1])
                if now_f[0]==3:
                    moved=b_move(get[0],get[1])
                if now_f[0]==4:
                    moved=q_move(get[0],get[1])
                if now_f[0]==5:
                    moved=k_move(get[0],get[1])
                if moved:turn=1;flip_board()
            black_king_check=before_check(black_king_pos[0],black_king_pos[1])
            white_king_check=before_check(white_king_pos[0],white_king_pos[1])
            black_king_check=max(black_king_check,now_check(black_king_pos[0],black_king_pos[1]))
            white_king_check=max(white_king_check,now_check(white_king_pos[0],white_king_pos[1]))
            print(f'clicked: {get}')
            print(f'types: {now_f}')
            print(f'white king: {white_king_pos} ',end='')
            print(f'black king: {black_king_pos}',)
            print(f'ischeck black: {black_king_check}')
            print(f'ischeck white: {white_king_check}\n')
    make_board()
    pygame.display.update()
pygame.quit()