import os
import re
# 获取文件夹列表
def get_filelists(file_dir = '.'):
	list_directory = os.listdir(file_dir)
	filelists = []
	for directory in list_directory:
		#
		if(os.path.isfile(directory)):
			filelists.append(directory)
	return filelists
def ReplaceNote(str):
    """ 查找文件中的\\注释 并将其替换成/**/格数 """
    global workmode
    exce_1 = str.find(r"/*")
    exce_2 = str.find(r"*/")    
    if (exce_1>=0) and (workmode == 0):
        workmode = 1


    if (exce_2>=0) and (workmode == 1):
        workmode = 0  
        

    if workmode == 0:
        if(exce_1>=0):
            return (str)
        match_obj = re.search(r"^(\s*//)(.*)",str)
        if match_obj:
            result = re.sub(r"//",r"/* ",match_obj.group(),1)
            result = result +r" */"+"\n"
            # print (result)
            new_line = result
            return (new_line)
        else:
            exce_3 = str.find(r"//")
            if exce_3 >=0:
                new_line = str.replace(r"//",r"/* ")
                new_line = new_line.replace("\n",r"*/ ")
                new_line = new_line +"\n"
                return (new_line)    
            else:
                return (str)
    else:
        return (str)
def ReplaceConstU(str):
    """ Rule7.2 “u”或“u”后缀应应用于以无符号类型表示的所有整数常量。 """
    f_obj0 = re.search(r"\d\)|0x.*[A-F]\)",str)    
    if f_obj0:
        
        result0 = re.sub(r"(\W\d+|0x\d+)(\))",r"\1U\2",str)
        result0 = re.sub(r"(0x.*[A-F])(\))",r"\1U\2",result0)
        str_tmp = result0
    else:
        str_tmp = str
    f_obj1 = re.search(r"[\dA-F](;|\])",str_tmp)
    if f_obj1:
        result = re.sub(r"(\W\d+|0x\d+)(;|\])",r"\1U\2",str_tmp)
        result = re.sub(r"(0x.*[A-F]+)(;|\])",r"\1U\2",result)
        # print (result)
        new_line = result
        return (new_line)
    else:    
        return str_tmp

    
# 处理文件数据
def deal_message(op_file):
    m_path = os.getcwd()
    new_path = m_path + "./new"
    if not os.path.exists(new_path):
        os.mkdir(new_path)                  
    with open(op_file,'r',encoding="ansi")as f:
        lines = f.readlines()
        new_file = new_path + "/" + op_file
        # os.chdir(new_path)
        with open(new_file,"w",encoding="ansi") as l:
            # 遍历所有行数
            for line in lines: 
                # 替换 
                write_line = ReplaceNote(line)
                write_line = ReplaceConstU(write_line)
                l.writelines(write_line)

        # os.chdir(m_path)

    

if __name__ == "__main__":
    m_file = get_filelists() 
    workmode = 0
    replacefile = 0
    for x in m_file:
        if x.endswith(".py"):
            break
        else:
            replacefile +=1
            deal_message(x)
    print(f"共处理{replacefile}个文档")
    print("文档替换只是简单文本替换，请仔细核对。根据需求进行进一步修改")

    
