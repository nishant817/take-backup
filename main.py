import getopt, sys
import os

argsList = sys.argv[1:]

options = "s:d:h"
long_options = ["source = ", "destination = ", "help"]

try:
   args, vals = getopt.getopt(argsList, options, long_options)

   # checking each argument
   for currArg, currVal in args:
      if currArg in ("-s", "--source"):
         source = currVal
         print("Source: ", currVal)
         if os.path.isdir(source) == False:
            print("Got Error: Source directory doesn't exist")
            sys.exit()
      elif currArg in ("-d", "--destination"):
         destination = currVal
         print("Destination: ", currVal)
         if os.path.isdir(destination) == False:
            print("Got Error: destination directory doesn't exist")
            sys.exit()
      elif currArg in ("-h", "--help"):
         print("Printing Help")
except getopt.error as err:
   print ("Got Error", str(err))
   sys.exit()

print ("This is the last line")