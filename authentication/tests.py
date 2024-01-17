inp = 4
step1 = 1
step2 = inp*2 - 1

for i in range(inp):
    for j in range(i+1):
        print(step1+j,end='')
        if i-j:
            print('*',end='')
    print()
    step1 += i+1
    
for i in range(inp):
    for j in range(inp-i):
        print(step2+j,end='')
        if (inp-i)-(j+1):
            print('*',end='')
    print()
    step2 -= inp-i-1