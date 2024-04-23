import subprocess
import re
from pprint import pprint
from colorama import Fore

def monitoring_error(line,errors,details):
    for e in errors:
        r=re.compile(fr"{e}: (.+)")
        error_match = r.search(line)
        if error_match:
            print(Fore.RED+line+Fore.WHITE)
            if e not in details:
                details[e]=[error_match]
            else:
                details[e].append(error_match)
            return 0
def  monitoring(file_path):
    try:
        details={}
        print(f"Monitoring log file: {file_path}")
        tail_process = subprocess.Popen(['tail', '-F', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        errors=input("Enter The Errors To Monitor : ").split()
        for line in tail_process.stdout:
            flag=monitoring_error(line,errors,details)
            if flag!=0:
                print(line)
    except KeyboardInterrupt: #ctrl+c to exit
        print("\nMonitoring stopped.")
        tail_process.terminate()
        print(f"\n\n{Fore.YELLOW}Summary Report:")
        for i in details:
            print(Fore.RED+i+Fore.WHITE)
            print("Total Count :",len(details[i]))
            pprint(details[i])
if __name__=="__main__":
    file_path=input("Enter File Path : ")
    monitoring(file_path)