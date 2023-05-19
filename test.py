sql_ex = [" ' or 1=1 # ", " ' or 1=1 or ''=' ", " ' or '1'='1' #"]
for s in sql_ex:
    print(s)
    print("{}".format(s))


def test():
    global a
    a=1
    b=1
    c=1
test()
print(a)

print("test :",a)