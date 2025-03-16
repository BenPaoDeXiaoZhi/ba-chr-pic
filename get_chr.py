import os
import time
import requests
import json
import threading

loaded_list = []
chr_list = \
    json.load(
        open(r'G:\蔚蓝档案files\meng-files\meng-ccw\ScenarioCharacterNameExcelTable.json', 'r', encoding='utf-8'))[
        'DataList'][:]
url = 'https://yuuka.cdn.diyigemt.com/image/ba-all-data/spine/%s_spr/%s_spr.%s'
for i in chr_list:
    try:
        if len(i['NicknameCN']) > 0:
            print('[log] 名称:%s <- %s' % (i['NameCN'], i['NicknameCN']), flush=True)
        else:
            raise Exception
    except:
        try:
            print('[log] 名称:' + i['NameCN'], flush=True)
        except:
            print('[error]%s' % i, flush=True)
            continue
    if len(i['SpinePrefabName']) > 0:
        print('[log] spine:' + i["SpinePrefabName"])
        spine_name = str(i["SpinePrefabName"].split('CharacterSpine_')[-1]).lower()
        try:
            os.mkdir('./%s_spr'%spine_name)
        except FileExistsError:
            if len(os.listdir('./%s_spr'%spine_name)) >= 3:
                continue
            continue
        print(spine_name, flush=True)
        # for j in ext_names:
        #     spine_url = url % (spine_name, spine_name, j)
        #     if spine_url in loaded_list:
        #         print('[log] %s的数据已进行过加载'%spine_url)
        #         continue
        #     req = requests.get(spine_url)
        #     loaded_list.append(spine_url)
        #     if b'<?xml' in req.content:
        #         print('  [error] %s加载失败，重试' % (spine_url), flush=True)
        #         req = requests.get(spine_url)
        #         if b'<?xml' in req.content or req.status_code != 200:
        #             print('\033[31m  [error] 重试失败\033[0m')
        #     elif req.status_code != 200:
        #         print('  [error] %s加载失败，重试' % (spine_url), flush=True)
        #         req = requests.get(spine_url)
        #         if b'<?xml' in req.content or req.status_code != 200:
        #             print('\033[31m  [error] 重试失败\033[0m')
        #     else:
        #         print('  [log] 已成功加载%s' % spine_url, flush=True)
        #         open('./%s_spr/%s'%(spine_name,'%s_spr.%s'%(spine_name,j)),'wb').write(req.content)
        atlas_url = url % (spine_name, spine_name, 'atlas')
        if atlas_url not in loaded_list:
            loaded_list.append(atlas_url)
            req = requests.get(atlas_url)
            if b'<?xml' in req.content or req.status_code != 200:
                print('\033[31m  [error] atlas文件 %s加载失败\033[0m' % atlas_url)
                continue
            else:
                print('  [log] atlas文件 %s加载成功' % atlas_url)
                open('./%s_spr/%s'%(spine_name,'%s_spr.%s'%(spine_name,'atlas')),'wb').write(req.content)
                req_data = req.content.decode('utf-8')
                img_name = req_data.splitlines()[1].split('_spr')[0]
                img_url = url%(img_name,img_name,'png')
                req = requests.get(img_url)
                if b'<?xml' in req.content or req.status_code != 200:
                    print('\033[31m  [error] png文件 %s加载失败\033[0m' % img_url)
                    continue
                else:
                    print('  [log] png文件 %s加载成功' % img_url)
                    open('./%s_spr/%s' % (spine_name, '%s_spr.%s' % (img_name, 'png')), 'wb').write(req.content)
                    skel_url = url % (spine_name, spine_name, 'skel')
                    req = requests.get(skel_url)
                    if b'<?xml' in req.content or req.status_code != 200:
                        print('\033[31m  [error] skel文件 %s加载失败\033[0m' % img_url)
                        continue
                    else:
                        print('  [log] skel文件 %s加载成功' % img_url)
                        open('./%s_spr/%s' % (spine_name, '%s_spr.%s' % (spine_name, 'skel')), 'wb').write(req.content)
        else:
            print('[log]已完成加载%s'%atlas_url)
    print('-' * 50)

print('下载完成，开始解包')
spine_list = os.listdir('./')
spine_list.remove('get_chr.py')
def extract_atlas(i):
    os.system('spine.com -i %s -o %s -c %s 2>&1> qwe4r, ./temp'%('./%s'%i,'./%s'%i,'./%s/%s.atlas'%(i,i)))
    print('%s完成解包'%i)
for i in spine_list[:]:
    spine_file_list = os.listdir('./%s'%i)
    if len(spine_file_list) != 0 and '%s.atlas'%i in spine_file_list and '%s.png'%i in spine_file_list:
        print('%s包含了纹理图集与纹理图片文件，可以解包'%i)
        try:
            os.mkdir('./%s/export'%i)
        except:
            pass
        t = threading.Thread(target=extract_atlas,args=[i])
        t.start()
        time.sleep(2)
        print('%s纹理正在解包'%i)
        print('-'*50)
# for i in range(os.listdir('./').remove('get_chr.py')):
