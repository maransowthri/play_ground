x = -3987
#arr = [-3,9,8,7]

if x < 0:
     arr = [int(i) for i in str(x)[1:]]
     arr[0] *= -1
else:
    arr = [int(i) for i in str(x)]

print (arr)