"# qa_veeam_test"
To answer the test I used:
1- python>=3.8
2- Install dependencies from requirements.txt <python -m pip install -r requirements.txt>
3- Code instruction are in <python answer.py -h> or <python answer.py --help>
4- To run the code just need <python answer.py --source PATH_SOURCE --replica PATH_REPLICA --logs> 
5- In case of the path to the folders have spaces place the path between ""
6- By defect the synchronization is every 2 seconds by it is changed with the argument --sync <python answer.py --source PATH_SOURCE --replica PATH_REPLICA --logs --sync SECONDS>
7- The code don't show logs and don't write/update the logs.txt file if you don't put the argument --logs.
8- To stop just need press ESC bottom.   