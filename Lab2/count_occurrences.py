import re
text = open("a.csv", "r", encoding="utf-8") 
  
d = dict() 
  
for line in text: 
    line = line.strip() 

    line = line.replace(',', ' ')
    line = line.replace('"', ' ')
    line = line.replace(',', ' ')

    line = re.sub(r'(.*wav.*)|(http.*html)', ' ', line)
    line = re.sub("\s\s+", " ", line)

    line = line.lower() 
  
    words = line.split(" ") 
  
    for word in words: 
        word = word.strip()
        if word in d: 
            d[word] = d[word] + 1
        else: 
            d[word] = 1

d = {k: v for k, v in reversed(sorted(d.items(), key=lambda item: item[1]))}

f = open("word_occurrences.csv", "w",  encoding="utf-8")
for key in list(d.keys()): 
    f.write("{},{}\n".format(key, d[key]))
    # print("{},{}\n".format(key, d[key]))

f.close()
