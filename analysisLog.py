#!/usr/bin/python                                                                                                                                                                                                                                                                
import sys
import re
import subprocess
import os
import shlex
import codecs

ADDR2LINE_BINARY='arm-linux-androideabi-addr2line' # full path to arm-linux-androideabi-addr2line
SYMBOL_FILES_CONFIG = 'symbol_config.txt' # symbol file list config, so->sym

LOG_FILE_INPUT = 'log_input.txt' # log input file
LOG_FILE_OUTPUT = 'log_output.txt' # log output file

def analysisLog(input_file, output_file):

    print ('------------------------')# space line
    print ("-> begin analysis log file : {}".format(input_file))
    print ('')# space line

    symbol_files = {}
    input_lines = []

    with codecs.open(SYMBOL_FILES_CONFIG, mode='r', encoding='UTF-8') as f:
        for item in f.readlines():
            if len(item) > 0 and item.startswith('#') is False:
                split_items = item.split(' ', maxsplit=2)
                if (len(split_items) == 2):
                    k = split_items[0].strip()
                    v = split_items[1].strip()
                    symbol_files[k] = v

    with codecs.open(input_file, mode='r') as f:
        for item in f.readlines():
            if len(item) > 0:
                input_lines.append(item)
    
    infos = []
    addresses = []
    libNames = []
    functions = []
    files = []

    for line in input_lines:
        lib_name, sym_name = get_match_sym(symbol_files, line)
        print (line)
        if sym_name is not None:
            info, address = get_address(line)
            if address is not None:
                source = get_analiysis_line(address, sym_name)
                if source is not None:
                    infos.append(info)
                    addresses.append(address)
                    libNames.append(lib_name)
                    functions.append(source[0])
                    files.append(source[1])
                    continue
        
        # add source line if not match
        infos.append(line.rstrip('\n'))
        addresses.append('')
        libNames.append('')
        functions.append('')
        files.append('')
                

    print ('')# space line

    if len(addresses) == 0 or len(files) == 0:
        print ('No addresses found from symbol files.')
        return

    #longest_address = len(max(addresses, key=len))
    #longest_file = len(max(files, key=len))

    output_lines = []
    for i in range(0, len(addresses)):
        output_line = '{} {} {} {} {}\n'.format(infos[i], addresses[i], libNames[i], functions[i], files[i])
        output_lines.append(output_line)
        print (output_line)
        #print (addresses[i].ljust(longest_address + 1)),
        #print (functions[i].ljust(longest_address + 1)),
        #print (files[i].ljust(longest_file + 1)),
    
    with codecs.open(output_file, mode='w') as f:
        f.writelines(output_lines)

#获取匹配到的符号文件
def get_match_sym(files, line):
    lib_name = None
    sym_name = None
    m = re.match(r".*/(\S*.so).*", line)
    if m is not None:
        lib_name = m.group(1)
        sym_name = files.get(lib_name)
    return (lib_name, sym_name)

#获取地址
def get_address(line):
    search = re.search('(#[0-9]{2} +pc) +([0-9A-Fa-f]{8}) +/data', line)
    if search is None:
        return None
    else:
        return (search.group(1), search.group(2))

#获取地址的解析内容
def get_analiysis_line(address, library):
    cmd_str = "{} -C -f -e {} {}".format(ADDR2LINE_BINARY, library, address)
    args = shlex.split(cmd_str)
    p = subprocess.Popen(args, 
        universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errs = p.communicate()
    if 0 == p.returncode:
        output = outs.split('\n')
        return (output[0], output[1])
    else:
        print (errs)
    return None
    
if __name__ == '__main__': 

    print ('Paste the stack trace in log_input.txt. And the output result at log_output.txt.')

    '''
    while True:
        try:
            line = input()
        except KeyboardInterrupt:
            sys.exit()
        except EOFError:
            break
        if len(line) != 0:
            lines.append(line)
    '''
    analysisLog(LOG_FILE_INPUT, LOG_FILE_OUTPUT)