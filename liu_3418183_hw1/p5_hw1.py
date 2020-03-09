import numpy as np

#(a)summing in a for loop
sum1 = 0
for i in range(0, 10000):
    if i % 2 == 1:
        sum1+= i
print(sum1)


#(b)summing in a while loop
sum2 = 0
x = 1
while (x<10000):
    sum2 += x
    x += 2
print(sum2)


#(c)summing in numpy array
r = np.arange(1, 10000, 2)
sum3 = np.sum( a = r)
print(sum3)


