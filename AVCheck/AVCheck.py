#!/usr/bin/env python3

banner = '''
                                                  .--,-``-.     
    ,----..                    ,----,            /   /     '.   
   /   /   \                 .'   .' \     ,---,/ ../        ;  
  /   .     :              ,----,'    |  ,---.'|\ ``\  .`-    ' 
 .   /   ;.  \,--,  ,--,   |    :  .  ;  |   | : \___\/   \   : 
.   ;   /  ` ;|'. \/ .`|   ;    |.'  /   |   | |      \   :   | 
;   |  ; \ ; |'  \/  / ;   `----'/  ;  ,--.__| |      /  /   /  
|   :  | ; | ' \  \.' /      /  ;  /  /   ,'   |      \  \   \  
.   |  ' ' ' :  \  ;  ;     ;  /  /-,.   '  /  |  ___ /   :   | 
'   ;  \; /  | / \  \  \   /  /  /.`|'   ; |:  | /   /\   /   : 
 \   \  ',  /./__;   ;  \./__;      :|   | '/  '/ ,,/  ',-    . 
  ;   :    / |   :/\  \ ;|   :    .' |   :    :|\ ''\        ;  
   \   \ .'  `---'  `--` ;   | .'     \   \  /   \   \     .'   
    `---`                `---'         `----'     `--`-,,-'     
'''

print(banner)

# 读取杀软识别.txt 只需要一次，而不是每次都读取
with open('杀软识别.txt', 'r', encoding='utf-8') as f:
    antivirus_list = [line.strip('\n').split('\"') for line in f.readlines()]

# 读取 tasklist.txt 并进行处理
with open('tasklist.txt', 'r', encoding='utf-8') as file:
    for line in file.readlines():
        line = line.strip('\n')
        # 提取进程名称
        target = line.split(' ')[0]
        
        # 比对任务列表中的进程名与杀软识别列表
        for antivirus in antivirus_list:
            if target == antivirus[1]:  # 假设进程名是第二项
                result = antivirus[3] if len(antivirus) > 3 else ""
                if result:
                    print(f"自己看___---___: {result}")
                else:
                    print("放心日")
                break  # 找到匹配后不再继续检查其他杀软
