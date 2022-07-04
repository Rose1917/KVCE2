'''
kernel code and variable processing
'''

import os
import subprocess

def export_config_list(src_dir):
    cmd_str = 'cd %s && git clone https://github.com/Rose1917/Kconfiglib.git && patch -Np1 -i Kconfiglib/makefile.patch' %(src_dir)
    subprocess.run(cmd_str,shell=True,check=True)

    cmd_str = 'cd %s && make scriptconfig SCRIPT=Kconfiglib/example/print_tree.py' %(src_dir)
    run_res = subprocess.run(cmd_str,shell=True,check=True, capture_output=True)

    return run_res.stdout.decode('utf-8')

if __name__ == '__main__':
    res = export_config_list('./linux-5.10.22')
    print(res)
