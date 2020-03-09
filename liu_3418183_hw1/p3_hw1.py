while True:
    try:
        x = float(input("x = "))
    except ValueError:
        print("Not a number, please enter again.")
    else:
        break
        
result = 2*(x**2) - 3*x + 2
print(result)
