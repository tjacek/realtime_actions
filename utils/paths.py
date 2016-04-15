class Path(object):
    def __init__(self, text):
        #if(type(text)==Path):
        #    self.items=str(text).split("/")
        self.items=[]
        raw_items=str(text).split("/")
        for item_i in raw_items:
            self.append(item_i)

    def __getitem__(self,i):
        return self.items[i]

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return "/".join(self.items)	

    def replace(self,other_path):
        new_path=self.copy()
        name=other_path.get_name()
        new_path.append(name)
        return new_path

    def get_name(self):
        return self.items[-1]

    def set_name(self,name):
        self.items[-1]=name

    def add(self,str_path):
        strs=str_path.split("/")
        for str_i in strs:
            if(str_i!=''):
                self.append(str_i)

    def append(self,item):
    	item=item.replace("/","")
        self.items.append(item)

    def copy(self):	
        str_path=str(self)
        return Path(str_path)

    def first(self,k):
        new_path=self.copy()
        new_path.items=self.items[0:len(self)-k]
        return new_path

def get_paths(path,filename):
    if(type(path)==str):
        path=Path(path)
    path=path.copy()
    path.add(filename)
    return path

def path_args(func):
    def path_fun(in_str,out_str): 
        in_path=Path(in_str)
        out_path=Path(out_str)
        return func(in_path,out_path)
    return path_fun        

def str_arg(func):
    def inner_fun(in_path):
        in_str=str(in_path)
        return func(in_str)
    return inner_fun

def to_paths(files):
    return [Path(file_i) for file_i in files]

def print_paths(paths):
    print("Length of paths " +str(len(paths)))
    for path_i in paths:
        print(str(path_i))

if __name__ == "__main__":
    data="../dataset2/binary"
    path=Path(data)
    path.add("/abc/aff")
    print(str(path))