'''
kernel code and variable processing
'''

import os
import subprocess
import re


rules_str = ['[mM]akefile', '[\w-]+\.c', '[\w-]+\.h', '[\w-]+\.py', '[\w-]+\.S', '[\w-]+\.sh', '[\w-]+\.rst', '[\w-]+\.txt', 'Kconfig', 'config', '[\w-]*defconfig', '[\w-]+']
rules_res = ['makefile', 'source', 'header', 'python', 'assembly', 'bash', 'rst', 'text', 'kconfig', 'config', 'defconfig', 'others']
rules_re = map(re.compile, rules_str)
rules = dict(zip(rules_re, rules_res))


'''
src_dir : the linux source folder
'''

# unpatch the source folder of makefile and remove the Kconfiglib
def post_config_list(src_dir):
    cmd_str = 'cd %s && patch -p1 -R -i Kconfiglib/makefile.patch' %(src_dir)
    subprocess.run(cmd_str,shell=True,check=True)

    cmd_str = 'cd %s && rm -rf Kconfiglib' %(src_dir)
    subprocess.run(cmd_str,shell=True,check=True)

# get the config list variables
def export_config_list(src_dir):
    cmd_str = 'cd %s && rm -rf %s && git clone https://github.com/Rose1917/Kconfiglib.git && patch -Np1 -i Kconfiglib/makefile.patch' %(src_dir,src_dir)
    os.system(cmd_str)

    cmd_str = 'cd %s && make scriptconfig SCRIPT=Kconfiglib/examples/print_tree.py' %(src_dir)
    run_res = subprocess.run(cmd_str,shell=True, capture_output=True)

    # remove the patch
    post_config_list(src_dir)

    res_str = run_res.stdout.decode('utf-8')
    return list(res_str.splitlines())


# get the blocks of the search file
# one block is a config search result
def get_blocks(file_name):
    blocks = []
    with open(file_name, 'r') as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        block_no = 1
        cur_block = []
        for line in lines:
            # next block begins
            if line == str(block_no+1):
                blocks.append(cur_block.copy())
                cur_block.clear()
                cur_block.append(line)
                block_no += 1
            else:  # add the current line to the block
                cur_block.append(line)
        blocks.append(cur_block)
    return blocks 

def decide_extend(file_name):
    for i, (rule, res) in enumerate((rules.items())):
        if rule.match(file_name):
            return rules_res[i]

def block_to_json(block):
    cur_config = {}

    # extract the config name
    config_name = block[1].split('::')[1]
    cur_config['config_name'] = config_name

    # print(config_name)

    file_blocks = []
    cur_block = []

    for line in block[2:]:
        # print(line)
        if line == '':
            if len(cur_block) > 0:
                if cur_block != []:
                    file_blocks.append(cur_block.copy())
                    cur_block.clear()
        else:  # push it cur_block
            cur_block.append(line)
    if cur_block != []:
        file_blocks.append(cur_block)
    # print(file_blocks)

    file_blocks_json = []
    single_block_json = {}
    for file_block in file_blocks:  # file_block
        single_block_json['path'] = file_block[0]
        single_block_json['extend'] = decide_extend(os.path.basename(file_block[0]))
        single_block_json['hits'] = []
        for hit in file_block[1:]:
            # print('hit:' + hit)
            line_no = int(hit.split(':')[0])
            content = hit[len(hit.split(':')[0])+1:]
            cur_hit = {
                    "line_no": line_no,
                    "content": content
                    }

            single_block_json['hits'].append(cur_hit.copy())
            cur_hit.clear()

        file_blocks_json.append(single_block_json.copy())
        single_block_json.clear()

    cur_config["search_res"] = file_blocks_json
    return cur_config


# this function search the result of the linux source of variables
def search_source(src_dir, variables):
    # make a tmp folder the store the search result
    if not os.path.exists('./build'):
        os.mkdir('./build')

    with open('./build/config_list.txt','w') as f:
        f.writelines('\n'.join(variables))
        f.close()

    with open('./build/search_res.txt', 'w') as f:
        subprocess.run('./scripts/final.sh <./build/config_list.txt %s' %(src_dir),shell=True,stdout=f)
        f.close()

    # parse the search result
    blocks = get_blocks('./build/search_res.txt')
    print(blocks)

    # from block to json
    json_blocks = map(block_to_json, blocks)

    return json_blocks

if __name__ == '__main__':
    variable_list = export_config_list('./linux-5.10.22')
    res = search_source('./linux-5.10.22', variable_list[0:3])
    print(list(res))
