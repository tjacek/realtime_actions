import re

def extract_number(path):
    name=get_name(path)
    pattern = re.compile(r"\d+")
    raw_digits=re.findall(pattern,name)[0]
    return int(raw_digits)

def extract_sufix(filename):
    return filename.split(".")[-1] 

def replace_sufix(sufix,files):
    return [s.replace(sufix,"") for s in files]

def has_sufix(filename,sufix):
	return extract_sufix(filename)==sufix