child1 = {
  "name" : "Emil",
  "year" : 2004
}
child2 = {
  "name" : "Tobias",
  "year" : 2007
}
child3 = {
  "name" : "Linus",
  "year" : 2011
}

myfamily = {
  "child1" : child1,
  "child2" : child2,
  "child3" : child3
}
# for i in range (1,len(myfamily)+1):
#     print(i)
#     x=myfamily.get("child"+str(i)).get("name")
#     y=myfamily.get("child"+str(i)).get("year")
#     print (x)
#     print(y)
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "melon", "mango"]
for x in range(1,len(thislist)):
  for y in range(1,len(thislist)):
    if x!=y:
      print(thislist[x]+"---"+thislist[y])

