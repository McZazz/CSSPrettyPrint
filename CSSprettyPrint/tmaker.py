#######################################################################################
# change the increment to adjust to different monospace fonts with different font sizes,
# run this .py and copy paste out of the prettyPY_output.txt into the css
#######################################################################################
increment = 12
#######################################################################################
start = increment
total = 40

result = []

for i in range(total):
    classNum = i + 1
    result.append('.t' + str(classNum) + ' {')
    result.append('    margin-left: ' + str(start) + 'px;')
    result.append('}')
    start += increment

# save to new file
with open('prettyCSS_output.txt', 'w') as finalList:
    # this puts each list item as new line
    for _ in result:
        finalList.write(_ + ' \n')
