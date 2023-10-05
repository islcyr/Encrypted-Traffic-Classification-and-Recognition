import os

def get_proc_by_port(port):
    cmd = "netstat -ano|findstr \":"+port+"\""
    pids = os.popen(cmd).read()
    if pids.strip()=="":
        return None, None
    pid = pids.split()[-1]

    cmd = "tasklist /NH /FI \"PID eq "+pid+"\""
    proc_name = os.popen(cmd).read().split()[0]
    return pid, proc_name