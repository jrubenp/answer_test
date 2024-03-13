import os, shutil 
import platform
import sys 
import argparse
from datetime import datetime
import threading
import keyboard
import glog as log 

def arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, help='source path (Mandatory)')
    parser.add_argument('--replica', type=str, help='replica path (Mandatory)')
    parser.add_argument('--sync', type=int, default=2.0, help='synchronization interval seconds 2.0 by dafault')
    parser.add_argument('--logs', action='store_true', help='show logs in console True by default') 
    
    if len(sys.argv) == 1:
        parser.print_help()
        print("\n\n press ESC to exit. \n")
        sys.exit(2) 
    if not parser.parse_args().replica: 
        log.error("You need a REPLICA folder path to work")
        parser.print_help()
        sys.exit(2)
    if not parser.parse_args().source:
        log.error("You need a SOURCE folder path to work")
        parser.print_help()
        sys.exit(2) 
        
    return parser.parse_args() 

def create_logs(): 
    
    try:    
        f = open(f"logs.txt", "x") 
        log.info(f"Create: Logs file {f.name}") 
    except:
        f = open(f"logs.txt", "a")  
    
    return f 
    
def inside_folder(path, files):
    content = os.listdir(path) 
    for item in content:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):  
            {"path": item_path,
             "isFolder": True}
            files.append({"path": item_path,
                        "isFolder": True})
            inside_folder(item_path,files)
        elif os.path.isfile(item_path): 
            files.append({"path": item_path,
                        "isFolder": False}) 
    return
     
def create(files_source, args, doc_logs=None):  
    for file in files_source:
        newFile = file['path'].replace(args.source, args.replica) 
        if file['isFolder']:
            if not os.path.exists(newFile):  
                os.makedirs(newFile) 
                if args.logs: 
                    doc_logs.write(f'[{datetime.now().strftime("%Y-%M-%d %H:%M:%S")}] Create: {newFile} \n')
                    log.info(f"Create: {newFile}")
        else:
            path = file['path']
            try:
                if(platform.system() == "Windows"):
                    if not os.path.isfile(newFile):
                        os.system(f'copy "{path}" "{newFile}" > nul 2>&1')
                        if args.logs: 
                            doc_logs.write(f'[{datetime.now().strftime("%Y-%M-%d %H:%M:%S")}] Create: {newFile} \n')
                            log.info(f"Create: {newFile}")
                else:
                    if not os.path.isfile(newFile):
                        os.system(f'cp "{path}" "{newFile}" > /dev/null 2>&1') 
                        if args.logs: 
                            doc_logs.write(f'[{datetime.now().strftime("%Y-%M-%d %H:%M:%S")}] Create: {newFile} \n')
                            log.info(f"Create: {newFile}")
            except OSError as error:
                log.error(error)

def compare_to_delete(files_source, files_replica, args):
    source_list = list()
    replica_list = list()  
    for file in files_source: 
        source_list.append( file['path'].replace(args.source, ""))
    for file in files_replica: 
        replica_list.append( file['path'].replace(args.replica, ""))   
    
    return list(set(replica_list) - set(source_list))  

def compare_to_update(files_source, files_replica, args):  
    update_source_list = list()
    update_replica_list = list()
    
    for file in files_source:
        update_source_list.append(os.stat(file['path']).st_size) 
    for file in files_replica:
        update_replica_list.append(os.stat(file['path']).st_size) 
     
    update_index = [i for i, (x, y) in enumerate(zip(update_source_list, update_replica_list)) if x != y] 
    
    return update_index

def delete_files(delete_replica_list, args, doc_logs=None):
    for values in delete_replica_list: 
        if os.path.isdir(args.replica + values): 
            try:
                os.rmdir(args.replica + values)  
            except:  
                shutil.rmtree(args.replica + values)
                if args.logs:
                    doc_logs.write(f'[{datetime.now().strftime("%Y-%M-%d %H:%M:%S")}] Deleted Folder: {args.replica + values}. \n')
                    log.info(f"Deleted Folder: {args.replica + values}.")
        else:
            try:
                os.remove(args.replica + values)
                if args.logs:
                    doc_logs.write(f'[{datetime.now().strftime("%Y-%M-%d %H:%M:%S")}] Deleted File: {args.replica + values}. \n')
                    log.info(f"Deleted File: {args.replica + values}")
            except:
                if args.logs:
                    #SAME MESSAGE BECAUSE BELONG TO A EARLY DELETED FOLDER BY SHUTIL
                    doc_logs.write(f'[{datetime.now().strftime("%Y-%M-%d %H:%M:%S")}] Deleted File: {args.replica + values}. \n')
                    log.info(f"Deleted File: {args.replica + values}")
            
def update(filesInSource, filesInReplica, update_replica_files, args, doc_logs=None):
    for idx in update_replica_files:
        try:
            if(platform.system() == "Windows"): 
                os.system(f'copy "{filesInSource[idx]["path"]}" "{filesInReplica[idx]["path"]}" > nul 2>&1')
                if args.logs: 
                    doc_logs.write(f'[{datetime.now().strftime("%Y-%M-%d %H:%M:%S")}] Updated: {filesInReplica[idx]["path"]} \n')
                    log.info(f"Updated: {filesInReplica[idx]['path']}")
            else: 
                os.system(f'cp "{filesInSource[idx]["path"]}" "{filesInReplica[idx]["path"]}" > /dev/null 2>&1') 
                if args.logs: 
                    doc_logs.write(f'[{datetime.now().strftime("%Y-%M-%d %H:%M:%S")}] Updated: {filesInReplica[idx]["path"]} \n')
                    log.info(f"Updated: {filesInReplica[idx]['path']}")
        except OSError as error:
            log.error(error)
        
def main(args):  
    if args.logs:
        doc_logs = create_logs()
         
    if not os.path.isdir(args.source):
        log.error(f"The folder source: {args.source} not exist")
        return
    if not os.path.isdir(args.replica):
        os.makedirs(args.replica) 
        if args.logs: log.info(f"Create Replica: {args.replica}") 
     
    filesInSource = list()
    filesInReplica = list()
    inside_folder(args.source, filesInSource)
    inside_folder(args.replica, filesInReplica)
    delete_replica_list = compare_to_delete(filesInSource, filesInReplica, args) 
     
    if args.logs:
        create(filesInSource, args, doc_logs)
        if len(delete_replica_list) > 0:
            delete_files(delete_replica_list,args,doc_logs)
        else:
            filesInSource = list()
            filesInReplica = list()
            inside_folder(args.source, filesInSource)
            inside_folder(args.replica, filesInReplica)
            update_replica_files = compare_to_update(filesInSource, filesInReplica, args)  
            update(filesInSource, filesInReplica, update_replica_files, args, doc_logs)
        doc_logs.close()
    else: 
        create(filesInSource, args)  
        if len(delete_replica_list) > 0:
            delete_files(delete_replica_list,args)
        else: 
            filesInSource = list()
            filesInReplica = list()
            inside_folder(args.source, filesInSource)
            inside_folder(args.replica, filesInReplica)
            update_replica_files = compare_to_update(filesInSource, filesInReplica, args)  
            update(filesInSource, filesInReplica, update_replica_files, args, doc_logs)
    
    timer = threading.Timer(args.sync, main, args=[args]) 
    timer.start()  
    while True:
        if keyboard.is_pressed('esc'):
            break 
    timer.cancel() 

if __name__ == '__main__': 
    args = arguments()  
    main(args)  