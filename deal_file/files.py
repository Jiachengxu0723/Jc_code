from file_deal import file_deal as fd

class files():
    def __init__(self,file_path,save_path):
        self.file_path = file_path
        self.save_path = save_path

    def file(self):
        f = fd(self.file_path, self.save_path)
        f.file_move()



if __name__ == '__main__':
    file_path = (r'C:/Users/Administrator/Desktop/picture2')
    save_path = (r'C:/Users/Administrator/Desktop/save_path')
    f = files(file_path,save_path)
    f.file()