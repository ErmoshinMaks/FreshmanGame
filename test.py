file=open('Maps/1.txt','r')
for i in range(len(file)):
    for obj in file[i]:
        if obj=="1":
            print(obj)