import json
import requests

stack = []
dictMap = {}
opposites = {}
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
print(x1)
s = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token=' + x1
r2 = requests.get(s)
print(r2.text)
x2 = json.loads(r2.text)
if(x2["status"] == "FINISHED"):
    exit()
y2 = x2["levels_completed"]
y3 = x2["total_levels"]
length = x2["maze_size"][1]
width = x2["maze_size"][0]
stat = x2["status"]
for i in range(0, width):
    for j in range(0, length):
        dictMap[(i*length)+j] = False
end = False
success = False
while(stat != "FINISHED"):
    currPos = x2["current_location"]
    currPosX = currPos[0];
    currPosY = currPos[1];
    #print("X: ", currPosX)
    #print(",Y: ", currPosY)
    pos = currPosX * length + currPosY
    dictMap[pos] = True
  
    moveURL = 'http://ec2-34-216-8-43.us-west-2.compute.amazonaws.com/game?token='+x1
    str = ""
    for i in range(0, 4):
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

        if(str != ""):
            payload2 = {"action": str}
            #print(stack)
            r3 = requests.post(moveURL, data=payload2, headers=headers)
            x3 = json.loads(r3.text)
            if(x3["result"] == "SUCCESS"):
                success = True
                stack.append(opposites[str])
                break
            elif(x3["result"] == "END"):
                end = True
                break
            else:
                str = ""
            dictMap[pos] = True
    if( not success and  (not end)):
        #print("Oh no!")
        if(len(stack) == 0):
            exit()
        else:
            payload2 = {"action": stack.pop()}
            r3 = requests.post(moveURL, data=payload2, headers=headers)
    success = False
    if(end):
        for i in range(0, width):
            for j in range(0, length):
                dictMap[(i*length)+j] = False
        stack = []
    r2 = requests.get(s)
    x2 = json.loads(r2.text)
    stat = x2["status"]
    if(stat == "FINISHED"):
        print(x2)
        print("Finished the maze!")
        exit()

    if(end):
        print(x2)
        length = x2["maze_size"][1]
        width = x2["maze_size"][0]
        for i in range(0, width):
            for j in range(0, length):
                dictMap[(i*length)+j] = False
        
    end = False




