# take-backup

## Algo
source; destination; archive
skip: nkishlay_od, OneDrive/Pictures
1. If source file is present in destination
   1. If source file is different from destination
      1. Copy destination file to archive
      2. Copy source file to destination
2. If source file is NOT present in destination
   1. copy source file to destination


## Sample Commands

* python main.py -s "C:/_NK/Cloudy/OneDrive" -d "S:/Backup_Cloudy/OneDrive" -a "S:/Backup_Cloudy/OneDrive_Archive" 
* python main.py -s "C:/_NK/Cloudy/OneDrive" -d "C:/_NK/Cloudy/OneDrive/nkishlay_od/Backup_Cloudy/OneDrive" -a "C:/_NK/Cloudy/OneDrive/nkishlay_od/Backup_Cloudy/OneDrive_Archive" 
* python main.py -s "C:/_NK/Cloudy/GoogleDrive" -d "S:/Backup_Cloudy/GoogleDrive" -a "S:/Backup_Cloudy/GoogleDrive_Archive" 

skip folder
nkishlay_od