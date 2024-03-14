# answer_test
> #### This code is designed to answer the following test task:
> Please implement a program that synchronizes two folders: source and replica. The 
program should maintain a full, identical copy of source folder at replica folder.
Solve the test task by writing a program in one of these programming languages: Python, C/C++, C#
> * Synchronization must be one-way: after the synchronization content of the 
replica folder should be modified to exactly match content of the source 
folder;
> * Synchronization should be performed periodically.
> * File creation/copying/removal operations should be logged to a file and to the 
console output;
> * Folder paths, synchronization interval and log file path should be provided 
using the command line arguments;
> * It is undesirable to use third-party libraries that implement folder 
synchronization;
> * It is allowed (and recommended) to use external libraries implementing other 
well-known algorithms. For example, there is no point in implementing yet 
another function that calculates MD5 if you need it for the task – it is 
perfectly acceptable to use a third-party (or built-in) library.



## To answer the test I used the following:

### Programming language:
* python==3.8
### Dependencies:
  * glog==0.3.1
  * keyboard==0.13.5
### Install dependencies from requirements.txt 
```
python -m pip install -r requirements.txt
``` 
### The code instructions are in:
```
python answer.py -h  
```
or 
```
python answer.py --help 
```
### To run the code you only need: 
```
python answer.py --source <PATH_SOURCE> --replica <PATH_REPLICA> --logs
``` 
* In case the path to the folders has spaces, put the path between "PATH SOURCE".
* The code does not display logs and does not write/update the logs.txt file if the --logs argument is not set.
    
### By default synchronization is every two seconds but can be changed with the --sync argument.
```
python answer.py --source <PATH_SOURCE> --replica <PATH_REPLICA> --logs --sync <SECONDS>
```

### To stop, just press the ESC button.   
