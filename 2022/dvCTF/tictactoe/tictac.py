from shutil import move
from time import sleep
from pandas import array
import pwn

ROW = 1
COL = 3
DIAG = 4
RDIAG = 2

DIRS = [
    (0,ROW),(0,COL),(0,DIAG),
    (1, COL), (2, COL),(2,RDIAG),
    (3, ROW),
    (6, ROW)
]
I=[ 0, 1, 2,
    3, 4, 5,
    6, 7, 8]

conn = pwn.remote('challs.dvc.tf',6666)
conn.recvlines(3)

def parse(b:bytes) -> int:
    if b == ord(b'X'):
        return 1
    if b == ord(b'O'):
        return -1
    return 0

def readBoard(input: array) -> array:
    board = [0]*9
    for row in range(3):
        board[row*3+0] = parse(input[row][0])
        board[row*3+1] = parse(input[row][2])
        board[row*3+2] = parse(input[row][4])
    return board

def checkDir(board: array, start:int, dir: int, target: int) -> int:
    sum = 0
    mul = 1
    s = start
    resultProposition = None
    for i in range(3):
        v = board[s]
        if v == 0:
            resultProposition = s
        sum += v
        mul *= v
        s += dir
    
    if sum == target and mul == 0:
        return resultProposition
    else:
        return None

def blockEnemy(board: array) -> int:
    for start, dir in DIRS:
        result = checkDir(board, start, dir, -2)
        if result is not None:
            return result
    corn = [(0,1,3),(8,5,7),(2,5,1),(6,3,7)]
    for p,p1,p2 in corn:
        if (board[p] == 0 and 
                (board[p1] == -1 or board[p2] == -1)):
            return p
    return None

def findWinInOneMove(board: array) -> int:
    for start, dir in DIRS:
        result = checkDir(board, start, dir, 2)
        if result is not None:
            return result
    return None

def findRandomMove(board: array) -> int:
    pos  = [1,7,3,5,0,8,2,6]
    opos = [7,1,5,3,8,0,6,2]
    for i in range(len(pos)):
        if board[pos[i]] == 0 and board[opos[i]] == 0:
            return pos[i]
    pos = [0,8,2,6,1,7,3,5]
    for p in pos:
        if board[p] == 0:
            return p
    return None

def countMoves(board: array) -> int:
    count = 0
    for i in range(9):
        if board[i] != 0:
            count += 1
    return count

def makeDecision(board: array) -> tuple:
    moves = countMoves(board)
    if moves == 0:
        return (0,0, False)
    elif moves == 1:
        if board[4] == 0:
            return (1,1, False)
        else:
            return (0,0, False)
    elif moves == 2:
        if board[4] == 0:
            return (1,1, False)
        elif board[8] == 0:
            return (2,2,False)

    winMove = findWinInOneMove(board)
    if winMove is not None:
        return (winMove//3, winMove%3, True)
    block = blockEnemy(board)
    if block is not None:
        return (block//3, block%3, False)
    random = findRandomMove(board)
    if random is not None:
        return (random//3, random%3, False)

    return (-1,-1,False)

games = 0
while games < 250:
    line1 = conn.recvline()
    if b'Match Draw' in line1:
        print(line1)
        line1 = conn.recvline()
    line2 = conn.recvline()
    line3 = conn.recvline()
    [print(l) for l in [line1, line2, line3]]
    board = readBoard([line1, line2, line3])
    r, c, win = makeDecision(board)
    print(f"{r+1} {c+1}".encode('utf8'))
    if c >= 0 and r >= 0:
        conn.send(f"{r+1} {c+1}\n".encode('utf8'))
    
    sol = conn.recvline()
    print(sol)
    if win:
        print(conn.recvlines(3))
        sol = conn.recvline()
        print(sol)
    if b'Well done' in sol:
        games += 1
        sol = conn.recvline()
        print(sol)
    elif sol != b'\n':
        print(conn.recvall())
        

print(conn.recvall())
#conn.interactive()