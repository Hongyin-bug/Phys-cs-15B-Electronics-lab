while True:
    try:
        c_temp0 = float(input("What is the temperature in Celsius? "))
    except ValueError:
        print("Not a number, please enter again.")
    else:
        break
        
while c_temp0 < -273.15:
    while True:
        try:
            c_temp0 = float(input("Temperature too low, can't be below absolute zero 0k!!! Reenter please:"))
        except ValueError:
            print("Not a number, please enter again.")
        else:
            break
            
f_temp = round(1.8 * c_temp0 + 32, 2)
print("The temperature in Fahrenheit is: ", f_temp)

