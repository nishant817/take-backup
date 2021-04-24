import sys

n = len(sys.argv)
print("Number of args: ", n)

print("\nName of script: ", sys.argv[0])

for i in range(1, n):
   print(sys.argv[i], end = "\n")