import os
import tkinter.filedialog as fd
import threading
import time
#spine -i G:\蔚蓝档案files\meng-files\characters\chr\aru_spr\aru_spr.skel -s 0.45 -o ./a.spine -r
root_dir = fd.askdirectory()
spine_list = os.listdir(root_dir)
spine_list.remove('get_chr.py')
for i in spine_list[:]:
    print(i)
    if f'{i}.spine' not in os.listdir(f'{root_dir}/{i}'):
        t = threading.Thread(target=os.system,args=[f'spine.com -i {root_dir}/{i}/{i}.skel -s 0.45 -o {root_dir}/{i}/{i}.spine -r'])
        t.start()
        time.sleep(1)