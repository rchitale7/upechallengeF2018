#UPE Coding Challenge for Fall 2018 - Maze Solver


import json
import requests

stack = []
dictMap = {}
opposites = {}

# populating dictionary for opposite moves
# will be used for backtracking
opposites["LEFT"] = "RIGHT"
opposites["RIGHT"] = "LEFT"
opposites["UP"] = "DOWN"
opposites["DOWN"] = "UP"

headers= {'Content-Type': 'application/x-www-form-urlencoded'}
u1 = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/session'
payload1 = {'uid': '704924773'}
r1 = requests.post(u1, data=payload1, headers=headers) #getting token
x1 = json.loads(r1.text)
x1 = x1["token"]
print("Game Token: ", x1)

s = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + x1
r2 = requests.get(s)
x2 = json.loads(r2.text)
print("Initial Maze: ", x2)
if(x2["status"] == "FINISHED"): #checking to see if we got the same token from a previous game
    exit()

y2 = x2["levels_completed"]
y3 = x2["total_levels"]
length = x2["maze_size"][1]
width = x2["maze_size"][0]
stat = x2["status"]

#populating dictionary that keeps track of visited items
for i in range(0, width):
    for j in range(0, length):
        dictMap[(i*length)+j] = False

end = False
success = False

#while the game status is not finished
while(stat != "FINISHED"):

    if(stat == "NONE" or stat == "GAME_OVER"):
        print("Error, game quit prematurely")
        exit()
    currPos = x2["current_location"]
    currPosX = currPos[0];
    currPosY = currPos[1];
    #print("X: ", currPosX)
    #print(",Y: ", currPosY)
    pos = currPosX * length + currPosY #indexing into the dictionary
    dictMap[pos] = True # position is visited
  
    moveURL = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token='+x1
    str = ""
    for i in range(0, 4):
        
        #checking if we can move up, down left, or right to an unvisited position
        
        if(i == 0 and currPosY > 0 and dictMap[(currPosX)*length + currPosY-1] ==  False):
            str = "UP"
            #print("errorUP")
            pos = (currPosX)*length + currPosY-1
        elif(i == 1 and currPosY < length - 1 and dictMap[(currPosX)*length + currPosY+1] == False):
            str = "DOWN"
            #print("errordown")
            pos = (currPosX)*length + currPosY+1
        elif(i == 2 and currPosX < width - 1 and dictMap[(currPosX+1)*(length) + currPosY] ==  False):
            str= "RIGHT"
            #print("erroright")
            pos = (currPosX+1)*(length) + currPosY
        elif(i == 3 and currPosX > 0 and dictMap[(currPosX-1)*(length)+ currPosY] ==  False):
            #print("errorleft")
            str= "LEFT"
            pos = (currPosX-1)*(length)+ currPosY

        # if we can move to an unvisited position, then we make a post request
        # and see if we make a successful move or end the maze
        if(str != ""):
            payload2 = {"action": str}
            #print(stack)
            r3 = requests.post(moveURL, data=payload2, headers=headers)
            x3 = json.loads(r3.text)
            if(x3["result"] == "SUCCESS"): #if we successfully moved to the location
                success = True
                stack.append(opposites[str]) #push the opposite move so that we can backtrack
                break
            elif(x3["result"] == "END"):
                end = True
                break
            else:
                str = ""
            dictMap[pos] = True # marking the position as visited

    # backtrack
    if( not success and  (not end)):
        if(len(stack) == 0):
            exit()
        else:
            payload2 = {"action": stack.pop()}
            r3 = requests.post(moveURL, data=payload2, headers=headers)

    success = False
    #if we reached the end
    if(end):
        for i in range(0, width):
            for j in range(0, length):
                dictMap[(i*length)+j] = False
        stack = []

    # get the new game state
    r2 = requests.get(s)
    x2 = json.loads(r2.text)
    stat = x2["status"]

    if(stat == "FINISHED"):  #we finished all levels
        print(x2)
        print("Finished the maze!")
        exit()

    # we repopulate dictionary that keeps track of visited items for a new level
    if(end):
        print("Finished level, here is the new maze: " , x2)
        length = x2["maze_size"][1]
        width = x2["maze_size"][0]
        for i in range(0, width):
            for j in range(0, length):
                dictMap[(i*length)+j] = False
        
    end = False




