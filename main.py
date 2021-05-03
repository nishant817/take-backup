import datetime
import filecmp
import getopt, sys
import logging
import os
import queue
import shutil

# constants
today = datetime.date.today()
now = datetime.datetime.now()
formattedTime = now.strftime("%Y-%m-%d-%H-%M-%S")

argsList = sys.argv[1:]

options = "s:d:a:h"
long_options = ["source = ", "destination = ", "archive = ", "help"]

archPrefix = "_archived_" + formattedTime
archBaseDir = ""
errMsg = ""
report = "Backup Summary"

# define logging
logFilePath = os.getcwd() + "/take-backup-logs/Log_" + today.strftime("%Y-%m-%d") + ".log"
logging.basicConfig(filename=logFilePath, format='%(levelname)s %(asctime)s %(message)s', filemode='a', level=logging.DEBUG)
logging.info("=========================================================================")
logging.info("===================== LOG START " + formattedTime + " =====================")
logging.info("=========================================================================")

# Read arguments
try:
   args, vals = getopt.getopt(argsList, options, long_options)

   # checking each argument
   for currArg, currVal in args:
      if currArg in ("-s", "--source"):
         srcBaseDir = currVal
         print("Source: ", currVal)
      elif currArg in ("-d", "--destination"):
         destBaseDir = currVal
         print("Destination: ", currVal)
      elif currArg in ("-a", "--archive"):
         archBaseDir = currVal
         print("Archive: ", currVal)
      elif currArg in ("-h", "--help"):
         print("Printing Help")
except getopt.error as err:
   print ("Got Error", str(err))
   logging.exception(err)
   sys.exit()

# Check arguments validity
if not srcBaseDir or os.path.isdir(srcBaseDir) == False:
   errMsg = "Got Error: Source directory doesn't exist"
if not destBaseDir: # or os.path.isdir(destBaseDir) == False:
   errMsg += "\nGot Error: destination directory not specified"
if not archBaseDir:
   errMsg += "\nGot Error: Archive directory not specified"
if errMsg:
   print(errMsg)
   sys.exit()

# Log inputs
logging.info("Source: " + currVal)
logging.info("Destination: " + currVal)
logging.info("Archive: " + currVal)


dirStack = queue.LifoQueue(9999) #collections.deque()

def backup_file(srcFilePath):
   global report
   print("Backing up File: ", srcFilePath)
   destFilePath = srcFilePath.replace(srcBaseDir, destBaseDir, 1)
   print("Backup Path: ", destFilePath)

   if os.path.exists(destFilePath):
      isSame = filecmp.cmp(srcFilePath, destFilePath, shallow=True)
      if isSame == False:
         # Move destFile to archive file
         tmpFilePath = srcFilePath.replace(srcBaseDir, archBaseDir, 1)
         tmpFileSplit = os.path.splitext(tmpFilePath)         
         archFilePath = tmpFileSplit[0] + archPrefix + tmpFileSplit[1]
         archDir = os.path.dirname(archFilePath)
         if not os.path.exists(archDir):
            os.makedirs(archDir)
         logmsg = "Archiving:: FROM: " + destFilePath + "; TO: " + archFilePath
         logging.info(logmsg)
         report += "\n" + logmsg
         shutil.copy2(destFilePath, archFilePath)

         # copy the file to destination
         logmsg = "Copying:: FROM: " + srcFilePath + "; TO: " + destFilePath
         logging.info(logmsg)
         report += "\n" + logmsg
         shutil.copy2(srcFilePath, destFilePath)
   else:
      # If directory doesn't exist then create it      
      srcDir = os.path.dirname(srcFilePath)
      destDir = srcDir.replace(srcBaseDir, destBaseDir, 1)
      if not os.path.exists(destDir):
         os.makedirs(destDir)
      logmsg = "Copying:: FROM: " + srcFilePath + "; TO: " + destFilePath
      logging.info(logmsg)
      report += "\n" + logmsg
      shutil.copy2(srcFilePath, destFilePath)
#end def backup_file

def backup_dir(dirPath):
   print("Backing up Directory: ", dirPath)
   currDirPath, dirNames, fileNames = next(os.walk(dirPath))
   print("currDirPath: ", currDirPath)
   print("Sub-directories: ", dirNames)
   print("Files: ", fileNames)

   for dir in dirNames:
      print("Add to Stack: ", dirPath + "/" + dir)
      dirStack.put(dirPath + "/" + dir)

   for fl in fileNames:
      backup_file(dirPath + "/" + fl)
#end def backup_dir

# Add base directory to stack
dirStack.put(srcBaseDir)

# Itirate through stack and perform backup
while dirStack.qsize() > 0:
   currDir = dirStack.get_nowait()
   backup_dir(currDir)

logging.info("=========================================================================")
logging.info("====================== LOG END " + formattedTime + " ======================")
logging.info("=========================================================================")   
print("\n\n")
print(report)
print ("=============== Backup Complete ===============")