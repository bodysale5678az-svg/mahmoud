#problem 7
size = int(input("Enter size of list: "))
Numbers = []

for i in range(size):
    Num = int(input("Enter items of list: "))
    

for i in range(size-1):
    if (Numbers[i] > 0 and Numbers[i+1] > 0) or (Numbers[i] < 0 and Numbers[i+1] < 0):
        print(Numbers[i], " ", Numbers[i+1])
        break
