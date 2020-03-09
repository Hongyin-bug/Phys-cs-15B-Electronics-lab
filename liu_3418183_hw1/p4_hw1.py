while True:
    try:
        x = float(input("x = "))
        y = float(input("y = "))
    except ValueError:
        print("Not a number, please try again.")
    else:
        break
        
while y == 0:
    print("Please select a different y (divisor) as to not make your primary school teacher unhappy :D")
    while True:
        try:
            y = float(input("y = "))
        except ValueError:
            print("Not a number, please enter again.")
        else:
            break
            
result1 = x - y
result2 = x/y

print("x - y = ", '{0:.4f}'.format(result1))
print("x/y = ", '{0:.4f}'.format(result2))
