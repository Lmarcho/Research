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
for i in range(1,4):
    x=myfamily.get("child"+str(i)).get("name")
    y=myfamily.get("child"+str(i)).get("year")
    print (x)
    print(y)