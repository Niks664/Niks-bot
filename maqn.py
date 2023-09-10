apple = 10
price = 15
sale = 1
summa = apple*price

if summa >= 200:
    sale = 0.9
if summa >= 500:
    sale = 0.8
    print(summa*sale)
if summa < 200:
    print (summa)