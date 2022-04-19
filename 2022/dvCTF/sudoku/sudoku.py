from tokenize import group
from pandas import array
import requests
import re

def printSudoku(sudo):
    for l in range(9):
        if l%3==0:
            print('-'*65)
        for c in range(9):
            if c%3 == 0:
                print('|', end='')
            print(f"{sudo[l*9+c]}", end='\t')
        
        print("")

def clearRow(tmp: array, ind: int):
    row = ind//9
    for off in range(9):
        tmp[9*row+off] = -1
    
def clearCol(tmp: array, ind: int):
    col = ind%9
    for off in range(9):
        tmp[9*off+col] = -1

def calculateIndex(boxRow:int, boxCol:int, r: int, c:int) -> int:
    return (boxCol*3)+c+((boxRow*3+r)*9)

def clearBox(tmp: array, ind: int):
    col = (ind%9)//3
    row = (ind//9)//3
    #print(f"{row}x{col}")
    for coff in range(3):
        for roff in range(3):
            tmp[calculateIndex(row, col, roff, coff)] = -1

def clear(tmp: array, val: int):
    for ind in range(len(tmp)):
        v = tmp[ind]
        if v == val:
            clearRow(tmp, ind)
            clearCol(tmp, ind)
            clearBox(tmp, ind)

def fillOnlyZeroInBox(sud: array, mask: array, val: int, r: int, c: int) -> bool:
    ind = []
    for co in range(3):
        for ro in range(3):
            i = calculateIndex(r, c, ro, co)
            if mask[i] == 0:
                ind.append(i)
    
    if len(ind) > 1:
        return False
    
    if len(ind) == 1:
        sud[ind[0]] = val
        clearRow(mask, ind[0])
        clearCol(mask, ind[0])

    return True

def check(sud: array, val: int) -> bool:
    mask = sud.copy()
    clear(mask, val)
    tasks = []
    for r in range(3):
        for c in range(3):
            tasks.append((r,c))
    
    anyChange = True
    while anyChange:
        anyChange = False
        reTasks = []
        while len(tasks) > 0:
            r,c = tasks.pop()
            res = fillOnlyZeroInBox(sud, mask, val, r, c)
            anyChange |= res
            if not res:
                reTasks.append((r,c))
        tasks = reTasks.copy()

    return len(tasks) == 0

def fill(sud: array, task: array) -> array:
    for i in range(9):
        retry = []
        while len(task) > 0:
            val = task.pop()
            if not check(sud, val):
                retry.append(val)
        task = retry.copy()
    return task
    

def sol(sud: array) -> array:
    task = []
    for i in range(9):
        task.append(i+1)
    task = fill(sud, task)
    
    if len(task) > 0:
        v = task[0]
        for i in range(len(sud)):
            if sud[i] == 0:
                sud[i] = v
                break
        fill(sud, task)


    printSudoku(sud)
    return sud

url = "http://challs.dvc.tf:6002/home?"
solUrl = "http://challs.dvc.tf:6002/flag"
sudoku = [0]*81

session = requests.Session()
chall = session.get(url)

reg = re.compile(r'<input .+ name\s*=\s*(?P<name>\d+)\s+(value\s*=\s*(?P<val>\d+))?')
for i in reg.finditer(chall.text):
    val = i.group('val')
    ind = i.group('name')
    if(val == None):
        continue

    index = int(ind)-1
    value = int(val)
    sudoku[index] = value

orig = sudoku.copy()
printSudoku(sudoku)
print("\nSOL:\n")
sol(sudoku)

d = {}
for i in range(len(sudoku)):
    d[str(i+1)] = sudoku[i]

r = session.post(solUrl, data=d)
print("\n\n")
print(r.text)
print(r.status_code)