from os import listdir

network_files_folder = '../Networks'

for net_fname in listdir(network_files_folder):
    if net_fname.endswith('.txt'):
        cmd = 'python3 ../QueryScripts/EnqueueAscending.py ComputationsAscending ../Networks/' + net_fname + ' X0 X2'
        print(cmd)
