import os

if not os.path.exists('./reverse/records'):
    os.mkdir('./reverse/records')

subdirectories = [x[0] for x in os.walk('./records')]
subdirectories.pop(0)

for subdirectory in subdirectories:
    if not os.path.exists('./reverse' + '/' + subdirectory):
        os.mkdir('./reverse' + subdirectory)
    path = subdirectory + '/index.txt'
    outfile = open(path, 'r', encoding='utf-8')
    infile = open('./reverse' + '/' + path, 'w', encoding='utf-8')
    i = 0
    text = []
    temp = None
    for line in outfile:
        if i == 0:
            infile.write(line)
        elif i % 2 == 1:
            temp = line
        elif i % 2 == 0:
            infile.write(line)
            infile.write(temp)
        i = i + 1
    outfile.close()
    infile.close()
