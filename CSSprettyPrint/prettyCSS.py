# read in .txt and strip each line
with open('prettyCSS_input.txt', 'r') as f:
    linesInList = f.readlines()
    # lstrip = beginning, rstrip = end, strip = both
# basic new data setup and cleaning
linesInList = [_.rstrip() for _ in linesInList]
newlinesinlist = ' \n'.join(linesInList)
splitList = list(newlinesinlist)

# list where all the operation ranges are places
areaList = []
# splitList will stay unedited with our individual chars
# areaList starts with empty values of '---'
for _ in range(len(splitList)):
    areaList.append('---')

# flags:
inSelectFlag = True
inCurlyFlag = False
inFeatureFlag = False
inDashesFlag = False
inOptionFlag = False
inRgbFlag = False
inStringFlag = False
openn = False

lasti = len(splitList) - 1

# label comment areas
inCommentFlag = False
for i, _ in enumerate(splitList):
    if i+1<=(len(splitList)-1) and inCommentFlag == False and _ == '/' and splitList[i+1] == '*':
        inCommentFlag = True
    elif i>1 and inCommentFlag and splitList[i-2] == '*' and splitList[i-1] == '/':
        inCommentFlag = False
    if inCommentFlag:
        areaList[i] = 'inComment'

# label inString areas
for i, _ in enumerate(splitList):
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    if openn and inStringFlag == False and _ == '"':
        inStringFlag = True
    elif openn and inStringFlag == True and _ == '"':
        inStringFlag = False
    # the or in parens just defines the last " to mark as inString
    if openn and i>0 and inStringFlag == True or (areaList[i-1] == 'inString' and splitList[i-1] != '"' and _ == '"'):
        areaList[i] = 'inString'

# label the bracket start areas
for i, _ in enumerate(splitList):
    # set safe condition for labeling blanks
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    if openn and _ == '{':
        areaList[i] = 'curlyOpen'
    if openn and _ == '}':
        areaList[i] = 'curlyClose'

# label selector areas
inCurlyFlag = False
for i, _ in enumerate(splitList):
    # set safe condition for labeling blanks
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    # set inCurlyFlag flags
    if inCurlyFlag == False and areaList[i] == 'curlyOpen':
        inCurlyFlag = True
    if inCurlyFlag == True and areaList[i] == 'curlyClose':
        inCurlyFlag = False

    # label selector areas
    if openn and inCurlyFlag == False:
        areaList[i] = 'inSelect'

# label dashes areas
inCurlyFlag = False
for i, _ in enumerate(splitList):
    # set safe condition for labeling blanks
    if areaList[i] == '---':
        openn = True
    else:
        openn = False
    # set inCurlyFlag flags
    if inCurlyFlag == False and areaList[i] == 'curlyOpen':
        inCurlyFlag = True
    if inCurlyFlag == True and areaList[i] == 'curlyClose':
        inCurlyFlag = False

    # label inDashes areas
    if i>1 and openn and inCurlyFlag and splitList[i-1] == '-' and _ == '-':
        inDashesFlag = True
        areaList[i-1] = 'inDashes'
    if i>2 and openn and inCurlyFlag and splitList[i-2] == '(' and splitList[i-1] == '-' and _ == '-':
        inDashesFlag = True
        areaList[i-1] = 'inDashes'
        areaList[i-2] = 'inDashes'
    if openn and inCurlyFlag and inDashesFlag and (_ == ':' or _ == ' '):
        inDashesFlag = False
        areaList[i] = 'inDashes'
    if i+1<=lasti and openn and inCurlyFlag and inDashesFlag and _ == ')' and splitList[i+1] == ';':
        inDashesFlag = False
        areaList[i] = 'inDashes'
        areaList[i+1] = 'inDashes'
    if i+1<=lasti and openn and inCurlyFlag and inDashesFlag and _ == ')':
        inDashesFlag = False
        areaList[i] = 'inDashes'
    if openn and inDashesFlag:
        areaList[i] = 'inDashes'

# label feature areas
inCurlyFlag = False
for i, _ in enumerate(splitList):
    # set safe condition for labeling blanks
    if areaList[i] == '---':
        openn = True
    else:
        openn = False
    # set inCurlyFlag flags
    if inCurlyFlag == False and areaList[i] == 'curlyOpen':
        inCurlyFlag = True
    if inCurlyFlag == True and areaList[i] == 'curlyClose':
        inCurlyFlag = False

    if i>1 and openn and inFeatureFlag == False and areaList[i-1] == 'curlyOpen':
        areaList[i] = 'inFeature'
        inFeatureFlag = True
    if i>1 and openn and inFeatureFlag == False and splitList[i-1] == ';':
        areaList[i] = 'inFeature'
        inFeatureFlag = True
    if i>1 and inFeatureFlag and splitList[i-1] == ':':
        inFeatureFlag = False
    if openn and inFeatureFlag:
        areaList[i] = 'inFeature'

# label option areas
inCurlyFlag = False
for i, _ in enumerate(splitList):
    # set safe condition for labeling blanks
    if areaList[i] == '---':
        openn = True
    else:
        openn = False
    # set inCurlyFlag flags
    if inCurlyFlag == False and areaList[i] == 'curlyOpen':
        inCurlyFlag = True
    if inCurlyFlag == True and areaList[i] == 'curlyClose':
        inCurlyFlag = False

    if openn and (areaList[i-1] == 'inFeature' or areaList[i-1] == 'inDashes'):
        inOptionFlag = True
        areaList[i] = 'inOption'
    if openn and inOptionFlag and splitList[i-1] == ';':
        inOptionFlag = False
    if openn and inOptionFlag:
        areaList[i] = 'inOption'

#print('initial areas and item:')
testList = []
for i, _ in enumerate(splitList):
    data = areaList[i] + ' ' + _
    testList.append(data)
# print(testList)

# copy the areaList map (blue and white)
mapList = areaList

# begin finalize stages
# change hex areas on option areas
inHex = False
hexcntr = 0
for i, _ in enumerate(splitList):
    # set safe condition for labeling blanks
    if areaList[i] == 'inOption':
        openn = True
    else:
        openn = False

    if openn and _ == '#':
        inHex = True
        mapList[i] = 'white'
    if openn and inHex and _ != '#' and hexcntr < 7:
        hexcntr += 1
        mapList[i] = 'red'
    if hexcntr == 6:
        hexcntr = 0
        inHex = False


# finalize inSelect area
openn = False
for i, _ in enumerate(splitList):
    # define condition that we change cells in
    # use areaList to find the label condition, and write to mapList
    if areaList[i] == 'inSelect':
        openn = True
    else:
        openn = False

    if openn and _ != '\n' and (_ == ':' or _ == '#' or _ == '@' or _ == '.' or _ == ','):
        mapList[i] = 'white'
    else:
        if openn and _ != '\n':
            mapList[i] = 'blue'

# finalize inFeature area
openn = False
for i, _ in enumerate(splitList):
    # define condition that we change cells in
    # use areaList to find the label condition, and write to mapList
    if areaList[i] == 'inFeature' or areaList[i] == 'inDashes':
        openn = True
    else:
        openn = False

    if openn and _ != '\n' and (_ == ':' or areaList[i] == 'inDashes'):
        mapList[i] = 'white'
    else:
        if openn and _ != '\n':
            mapList[i] = 'green'

# finalize inOption area
openn = False
for i, _ in enumerate(splitList):
    # define condition that we change cells in
    # use areaList to find the label condition, and write to mapList
    if areaList[i] == 'inOption':
        openn = True
    else:
        openn = False

    if (openn and _ != '\n' and (_ == ',' or _ == ';' or _ == ':' or _ == '(' or _ == ')')) or (areaList[i] == 'inDashes'):
        mapList[i] = 'white'
    elif openn and _ != '\n' and _ == '%':
        mapList[i] = 'blue'
    elif i>2 and openn and _ != '\n' and ((splitList[i-1] == 'p' and _ == 'x')or(splitList[i-1] == 'e' and _ == 'm')\
    or(splitList[i-1] == 'e' and _ == 'x')or(splitList[i-1] == 'c' and _ == 'm')or(splitList[i-1] == 'm' and _ == 'm')\
    or(splitList[i-1] == 'i' and _ == 'n')or(splitList[i-1] == 'p' and _ == 't')or(splitList[i-1] == 'p' and _ == 'c')\
    or(splitList[i-1] == 'c' and _ == 'h')or(splitList[i-1] == 'v' and _ == 'h')or(splitList[i-1] == 'v' and _ == 'w'))\
    and (splitList[i-2] == '0' or splitList[i-2] == '1' or splitList[i-2] == '2' or splitList[i-2] == '3'\
    or splitList[i-2] == '4' or splitList[i-2] == '5' or splitList[i-2] == '6' or splitList[i-2] == '7'\
    or splitList[i-2] == '8' or splitList[i-2] == '9'):
        mapList[i] = 'blue'
        mapList[i-1] = 'blue'
    elif i>3 and openn and _ != '\n' and (splitList[i-2] == 'r' and splitList[i-1] == 'e' and _ == 'm')\
        and (splitList[i-3] == '0' or splitList[i-3] == '1' or splitList[i-3] == '2' or splitList[i-3] == '3'\
        or splitList[i-3] == '4' or splitList[i-3] == '5' or splitList[i-3] == '6' or splitList[i-3] == '7'\
        or splitList[i-3] == '8' or splitList[i-3] == '9'):
            mapList[i] = 'blue'
            mapList[i-1] = 'blue'
            mapList[i-2] = 'blue'
    elif i>4 and openn and _ != '\n' and ((splitList[i-3] == 'v' and splitList[i-2] == 'm' and splitList[i-1] == 'i' and _ == 'n')\
    or (splitList[i-3] == 'v' and splitList[i-2] == 'm' and splitList[i-1] == 'a' and _ == 'x'))\
    and (splitList[i-4] == '0' or splitList[i-4] == '1' or splitList[i-4] == '2' or splitList[i-4] == '3'\
    or splitList[i-4] == '4' or splitList[i-4] == '5' or splitList[i-4] == '6' or splitList[i-4] == '7'\
    or splitList[i-4] == '8' or splitList[i-4] == '9'):
        mapList[i] = 'blue'
        mapList[i-1] = 'blue'
        mapList[i-2] = 'blue'
        mapList[i-3] = 'blue'
    elif openn and (_ == '0' or _ == '1' or _ == '2' or _ == '3' or _ == '4' or _ == '5' or _ == '6' or _ == '7' or _ == '8' or \
    _ == '9' or _ == '.'):
        mapList[i] = 'red'
    else:
        if openn and _ != '\n':
            mapList[i] = 'green'

# finalize inString areas
openn = False
for i, _ in enumerate(splitList):
    # define condition that we change cells in
    # use areaList to find the label condition, and write to mapList
    if areaList[i] == 'inString':
        mapList[i] = 'strgrn'

# finalize inComment areas
openn = False
for i, _ in enumerate(splitList):
    # define condition that we change cells in
    # use areaList to find the label condition, and write to mapList
    if areaList[i] == 'inComment':
        mapList[i] = 'gray'

# finalize curlybraces areas
openn = False
for i, _ in enumerate(splitList):
    # define condition that we change cells in
    # use areaList to find the label condition, and write to mapList
    if areaList[i] == 'curlyOpen' or areaList[i] == 'curlyClose':
        mapList[i] = 'white'

# finalize enters
openn = False
for i, _ in enumerate(splitList):
    # define condition that we change cells in
    # use areaList to find the label condition, and write to mapList
    if splitList[i] == '\n':
        mapList[i] = 'enter'

# finalize tabs
enterFlag = False
cntr = 0
for i, _ in enumerate(splitList):
    # define condition that we change cells in
    # use areaList to find the label condition, and write to mapList
    if mapList[i] == 'enter':
        enterFlag = True
        cntr = 0
    elif enterFlag and _ != ' ':
        enterFlag = False
        cntr = 0
    elif enterFlag and _ == ' ':
        cntr += 1
        mapList[i] = ' '

# print()
# print('splitlist:')
# print(splitList)
# print(len(splitList))
# print()
# print('areaList and item:')
testList = []
for i, _ in enumerate(splitList):
    data = areaList[i] + ' ' + _
    testList.append(data)
# print(testList)
# print(len(testList))
# print()
# print("map:")
testList2 = []
for i, _ in enumerate(splitList):
    data = mapList[i] + ' ' + _
    testList2.append(data)
# print(testList2)

# remove the space: [enter space enter]
for i, _ in enumerate(splitList):
    if i>1 and mapList[i-2] == 'enter' and mapList[i-1] == ' ' and mapList[i] == 'enter':
        mapList.pop(i-1)
        splitList.pop(i-1)

# remove the space: [curly space enter]
for i, _ in enumerate(splitList):
    if (splitList[i-2] == '{' and splitList[i-1] == ' ' and splitList[i] == '\n')\
    or (splitList[i-2] == '}' and splitList[i-1] == ' ' and splitList[i] == '\n'):
        mapList.pop(i-1)
        splitList.pop(i-1)

################################################################################################# start original dels
# prepare to remove the unecesary tabs ***********new version***********:
cntr = 1
lasti = len(splitList) -1
flag = False
# just doing index 0 first, other in later loop
for i, _ in enumerate(splitList):
    if i == 0 and flag == False and _ == ' ':
        flag = True
        mapList[i] = 'del'
        splitList[i] = 'del'
    elif i>0 and flag and splitList[i] != ' ':
        flag = False
        mapList[i-1] = str(cntr)
        splitList[i-1] = 'space'
        cntr = 1
    if i>0 and flag:
        mapList[i] = 'del'
        splitList[i] = 'del'
        cntr += 1

cntr = 1
lasti = len(splitList) -1
flag = False
# now doing the other space areas, all others
for i, _ in enumerate(splitList):
    if i>0 and flag == False and splitList[i-1] == ' ' and _ == ' ':
        flag = True
        mapList[i] = 'del'
        splitList[i] = 'del'
        mapList[i-1] = 'del'
        splitList[i-1] = 'del'
    elif i>0 and flag and splitList[i] != ' ':
        flag = False
        mapList[i-1] = str(cntr)
        splitList[i-1] = 'space'
        cntr = 1
    if i>0 and flag:
        mapList[i] = 'del'
        splitList[i] = 'del'
        cntr += 1

# print(len(mapList))
# print(len(splitList))
#
# print()
# print("after dels added")
testList2 = []
for i, _ in enumerate(splitList):
    data = mapList[i] + ' ' + _
    testList2.append(data)
# print(testList2)

#how many to delete
isdel = 0
for i, _ in enumerate(mapList):
    if _ == 'del':
        isdel += 1

# print("dels: "+ str(isdel))

delshene = True
while delshene:
    for i, _ in enumerate(mapList):
        if _ == 'del':
            mapList.pop(i)
            splitList.pop(i)
    isdel = 0
    for i, _ in enumerate(mapList):
        if _ == 'del':
            isdel += 1
    if isdel == 0:
        delshene = False
    else:
        delshene = True

# did we delete them all?
isdel = 0
for i, _ in enumerate(mapList):
    if _ == 'del':
        isdel += 1

# print('dels after del: ' + str(isdel))

######################################################################################## end original dels
# remove the pointless color open that's before line ends: ['color  ', 'enter' ]
for i, _ in enumerate(splitList):
    if (i+1<=(len(splitList)-1) and i>0)and (mapList[i] == 'blue' or mapList[i] == 'white' or mapList[i] == 'red'\
    or mapList[i] == 'green' or mapList[i] == 'strgrn' or mapList[i] == 'gray') and _ == ' ' and mapList[i+1] == 'enter':
        mapList[i] = mapList[i-1]

# print()
# print("after pop:")
testList3 = []
for i, _ in enumerate(splitList):
    data = mapList[i] + ' ' + _
    testList3.append(data)
# print(testList3)

# print()
# print("after new round of dels added:")
testList3 = []
for i, _ in enumerate(splitList):
    data = mapList[i] + ' ' + _
    testList3.append(data)
# print(testList3)

# ################################################################################### end added from prettyPY
# empty list for final ruleset, start and stop style
ruleList = []
for i, _ in enumerate(mapList):
    ruleList.append('---')
# first round of instruction making
for i, _ in enumerate(mapList):
    # for some reason this breaks if we
    # try elfi anywhere
    if i == 0:
        ruleList[i] = 'open'
    if i>0 and _ != mapList[i-1]:
        ruleList[i-1] = 'close'
        ruleList[i] = 'open'
    if i>1 and mapList[i-2] != mapList[i-1] and _ != mapList[i-1]:
        ruleList[i-1] = 'only'
# fix index zero errors
for i, _ in enumerate(mapList):
    # for some reason this breaks if we
    # try elfi anywhere
    if i == 0:
        if i+1<=(len(mapList)-1) and mapList[i] == mapList[i+1]:
            ruleList[i] = 'open'
        else:
            ruleList[i] = 'only'

# fix final spot
############################################################################################## add to prettyCSS
for i, _ in enumerate(mapList):
    if i == len(mapList)-1:
        if mapList[i-1] == mapList[i]:
            ruleList[i] = 'close'
        elif mapList[i-1] != mapList[i]:
            ruleList[i] = 'only'
########################################################################################### end added from prettyPY

# print()
# print("after rules:")
testList4 = []
for i, _ in enumerate(ruleList):
    data = mapList[i] + ' ' + _
    testList4.append(data)
# print(testList4)

# replace <> with &lt; &gt; and &amp;
############################################################################################## add to cssPretty
for i, _ in enumerate(splitList):
    if _ == '<':
        splitList[i] = '&lt;'
    elif _ == '>':
        splitList[i] = '&gt;'

# blue is from next higher div
# this always goes after tab num: '">'
dict = {
    'white-open': '<span class="cw">', 'red-open': '<span class="cn">', 'green-open': '<span class="fg">',
    'strgrn-open': '<span class="sg">', 'red-open': '<span class="cn">', 'green-open': '<span class="fg">',
    'tab': '<p class="t', 'gray-open': '<span class="cg">', 'white': 'cw',  'red': 'cn', 'green': 'fg',
    'strgrn': 'sg', 'gray': 'cg', 'blue': '',
}

# put in the html
htmlList=[]
lasti = len(splitList)-1
for i, _ in enumerate(splitList):
    htmlList.append('---')

for i, _ in enumerate(splitList):
    opens = mapList[i] + '-' + 'open'

    if ruleList[i] == 'open':
        if (mapList[i] == 'white' or mapList[i] == 'red' or mapList[i] == 'green' or mapList[i] == 'strgrn'\
        or mapList[i] == 'gray'):
            htmlList[i] = dict[opens] + _
        else:
            htmlList[i] = _

    elif ruleList[i] == 'close':
        if mapList[i] == 'white' or mapList[i] == 'red' or mapList[i] == 'green' or mapList[i] == 'strgrn'\
        or mapList[i] == 'gray':
            htmlList[i] = _ + '</span>'
        else:
            htmlList[i] = _
    elif ruleList[i] == 'only':
        if mapList[i] == 'white' or mapList[i] == 'red' or mapList[i] == 'green' or mapList[i] == 'strgrn'\
        or mapList[i] == 'gray':
            htmlList[i] = dict[opens] + _ + '</span>'
        else:
            htmlList[i] = _
    elif ruleList[i] == '---':
        htmlList[i] = _
    elif mapList[i] == 'enter':
        htmlList[i] = ' \n'
    #################### this one is just for space areas starting at index 0
    if splitList[i] == 'space' and i==0: #######################################################################  add to prettyCSS (end spaces)
        if i+1 <= lasti and ruleList[i+1] == 'open' or ruleList[i+1] == '---':
            htmlList[i] = '<span class="t' + mapList[i] + ' ' + dict[mapList[i+1]] + '">'
            ruleList[i+1] = '---'
        elif i+1 <= lasti and (ruleList[i+1] == 'close' or ruleList[i+1] == 'only'):
            htmlList[i] = '<span class="t' + mapList[i] + ' ' + dict[mapList[i-1]] + '">'
            ruleList[i+1] = 'close'
    #################### this one is just for space areas after index 0
    elif splitList[i] == 'space' and i>0: #######################################################################  add to prettyCSS (end spaces)
        if i+1 <= lasti and ruleList[i+1] == 'open' or ruleList[i+1] == '---':
            htmlList[i] = '<span class="t' + mapList[i] + ' ' + dict[mapList[i+1]] + '">'
            ruleList[i+1] = '---'
        elif i+1 <= lasti and (ruleList[i+1] == 'close' or ruleList[i+1] == 'only'):
            htmlList[i] = '<span class="t' + mapList[i] + ' ' + dict[mapList[i-1]] + '">'
            ruleList[i+1] = 'close'

# print()
# print(htmlList)

stringsdone = "".join(htmlList).split("\n")

# fix empty lines
newlist2 = []
for _ in stringsdone:
    # normal line
    if _.startswith('<p class="t') == False and _ != '\n':
        _ = '<p>' + _ + '</p>'
    # tab line
    elif _.startswith('<p class="t') == True:
        _ = _ + '</p>'
    # enter line
    if _ == '<p></p>':
        _ = '<p class="hidden">*</p>'
    newlist2.append(_)
#
# save to new file
thing = ['aergafgafa', 'rgafgadfadfa', 'ergafasdgafaf']

# save to new file
with open('prettyCSS_output.txt', 'w') as finalList:
    # this puts each list item as new line
    for _ in newlist2:
        finalList.write(_ + ' \n')
