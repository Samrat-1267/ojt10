num = int(input("Enter a num: "))
n = len(str(num)) 
temp = int(num)
sum = 0

while temp != 0:
  digit = temp %10
  sum =sum+pow(digit,n)
  temp = temp//10

if sum == num :
  print("Armstrong number")
else:
  print("Not armstrong number")
