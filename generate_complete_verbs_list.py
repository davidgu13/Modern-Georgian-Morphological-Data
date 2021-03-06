import os
import re

def remove_transliteration2(file_name):
    s=''
    with open(file_name,'r',encoding='utf8') as f:
        for line in f:
            line = re.sub('#\d+ - .+ - .+:','',line)
            line = re.sub('Screeve #\d+:\n','',line)
            line = re.sub(' = .+','',line)
            line = re.sub('\n\n','\n',line)
            s += line
    return s

if __name__=='__main__':
    classes = ['Transitive', 'Intransitive', 'Medial', 'Indirect']
    paths = [os.path.join("Clean Paradigms",c) for c in classes]
    with open('Georgian Data.txt','w+',encoding='utf8') as f:
        for p in paths:
            for file_name in os.listdir(p):
                full_path = os.path.join(p,file_name)
                with open(full_path,'r',encoding='utf8') as f_orig:
                    content = remove_transliteration2(full_path)
                    content = content.replace('\n\n\n','\n').replace('\n\n','\n')
                f.write(content)
