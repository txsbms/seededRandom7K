from tkinter import filedialog as fd

# Checks to see if user-inputted seed is a valid permutation
# of columns given keycount.
def isSeedValid(inp, keycount):
    tmpA = ''
    for i in range(1, keycount + 1):
        tmpA = tmpA + str(i)
    tmpB = ''.join(sorted(inp))
    if (tmpA == tmpB):
        return True
    else:
        return False
    return False

# Returns gamemode given the input is a valid .osu file.
def getMode(fileName):
    f = open(fileName, "r", encoding='utf-8')
    currLine = ''
    while ('Mode:' not in currLine):
        currLine = f.readline()
        if (currLine == ''):
            return ''
    f.close()
    return int(currLine[-2])

# Returns CircleSize of .osu file.
def getKeycount(fileName):
    f = open(fileName, "r", encoding='utf-8')
    currLine = ''
    while ('CircleSize:' not in currLine):
        currLine = f.readline()
        if (currLine == ''):
            return ''
    f.close()
    return int(currLine[-2])

# Returns the difficulty name given regular .osu naming convention.
def getDiffName(fileName):
    for i in range(1, len(fileName)):
        if (fileName[-i] == ']'):
            rightLimit = len(fileName) - i
        if (fileName[-i] == '['):
            leftLimit = len(fileName) - i + 1
            break
    return fileName[leftLimit:rightLimit]

# Translates regular column numbers (FOR 7K ONLY)
# to osu coordinates because osu is a really good game
def numToColVal(num):
    if (num == 1):
        return 36
    if (num == 2):
        return 109
    if (num == 3):
        return 182
    if (num == 4):
        return 256
    if (num == 5):
        return 329
    if (num == 6):
        return 402
    if (num == 7):
        return 475
    return 0

# Returns string to insert below [HitObjects] in the newly generated .osu file.
def createHitObjects(fileName, seed):
    hitObjString = ''
    colA = []
    colB = []
    colC = []
    colD = []
    colE = []
    colF = []
    colG = []
    keycount = getKeycount(fileName)
    currLine = ''
    f = open(fileName, "r", encoding='utf-8')
    while currLine != '[HitObjects]\n':
        currLine = f.readline()

    while currLine != '':
        currLine = f.readline()
        if currLine == '':
            break
        colVal = int(currLine.split(',')[0])
        if colVal == 36:
            colA.append(currLine)
            continue
        elif colVal == 109:
            colB.append(currLine)
            continue
        elif colVal == 182:
            colC.append(currLine)
            continue
        elif colVal == 256:
            colD.append(currLine)
            continue
        elif colVal == 329:
            colE.append(currLine)
            continue
        elif colVal == 402:
            colF.append(currLine)
            continue
        elif colVal == 475:
            colG.append(currLine)
            continue
        else:
            print('Error in HitObject generation. (1)')
            continue

    for i in range(7):
        newCol = numToColVal(seed.index(str(i + 1)) + 1)
        if i == 0:
            for j in range(len(colA)):
                hitObjString = hitObjString + str(newCol) + colA[j][2:]
        elif i == 1:
            for j in range(len(colB)):
                hitObjString = hitObjString + str(newCol) + colB[j][3:]
        elif i == 2:
            for j in range(len(colC)):
                hitObjString = hitObjString + str(newCol) + colC[j][3:]
        elif i == 3:
            for j in range(len(colD)):
                hitObjString = hitObjString + str(newCol) + colD[j][3:]
        elif i == 4:
            for j in range(len(colE)):
                hitObjString = hitObjString + str(newCol) + colE[j][3:]
        elif i == 5:
            for j in range(len(colF)):
                hitObjString = hitObjString + str(newCol) + colF[j][3:]
        elif i == 6:
            for j in range(len(colG)):
                hitObjString = hitObjString + str(newCol) + colG[j][3:]
        else:
            print('Error in HitObject generation. (2)')

    f.close()
    return hitObjString

# Creates and formats new .osu file.
def createNewFile(fileName, newHitObj, seed):
    currLine = '0'
    f = open(fileName, "r", encoding='utf-8')

    newName = fileName[:-5] + ' (RAN ' + seed + ')].osu'
    ranFile = open(newName, "w", encoding='utf-8')
    while currLine != '':
        currLine = f.readline()
        if ('Version:' in currLine):
            ranFile.write('Version:' + getDiffName(newName) + '\n')
            continue
        if ('BeatmapID:' in currLine):
            ranFile.write('BeatmapID:0\n')
            continue
        if ('BeatmapSetID:' in currLine):
            ranFile.write('BeatmapSetID:-1\n')
            continue
        if (currLine == '[HitObjects]\n'):
            ranFile.write(currLine)
            break
        ranFile.write(currLine)
    ranFile.write(newHitObj)

    print("Created new file at " + newName)
    ranFile.close()
    f.close()

# Main Function

# Opens file and checks if gamemode and keycount are correct.
# Later on if other keymodes are implemented the keycount check should be
# removed and the getKeycount function should be implemented elsewhere.
while True:
    fileName = fd.askopenfilename()
    tmpA = fileName[-4:]
    if (tmpA != '.osu'):
        print('Invalid file type! Please use a .osu file.')
        continue
    else:
        if (getMode(fileName) == 3):
            if (getKeycount(fileName) == 7):
                print('Loaded ' + fileName)
                keycount = 7
                break
            else:
                print('This script currently only supports 7-key osu!mania files.')
                continue
        else:
            print('Invalid game mode and/or file! Please use an osu!mania-specific map.')
            continue

# Checks seed for validity and outputs new file
while True:
    seed = input('Enter seed: ')
    if (isSeedValid(seed, keycount) == True):
        createNewFile(fileName, createHitObjects(fileName, seed), seed)
        break
    else:
        print('Invalid input!')

# End of program
input('Press ENTER to exit script.')
