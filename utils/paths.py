class Path(object):
    def __init__(self, text):
        self.items=text.split("/")

    def __getitem__(self,i):
        return self.items[i]

    def __len__(self):
        return len(self.items)

    def __str__(self):
        return "/".join(self.items)	

    def replace(self,other_path):
        new_path=self.copy()
        name=other_path.get_name()
        new_path.set_name(name)
        return new_path

    def get_name(self):
        return self.items[-1]

    def set_name(self,name):
        self.items[-1]=nam

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

if __name__ == "__main__":
    data="../dataset2/binary"
    path=Path(data)
    path.add("/abc/aff")
    print(str(path))