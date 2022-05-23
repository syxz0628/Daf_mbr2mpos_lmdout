import datetime
st=datetime.datetime.now()
n=11952734475

i=0
for i in range(0,int(n)):
    if (i>n):
        print(i)
pt=datetime.datetime.now()
print("time is:",(pt-st).seconds)

