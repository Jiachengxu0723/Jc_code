import os
jpg_lst = os.listdir("C:\\Users\\byb\\Desktop\\1_json")

jpg_lst_new = []
for item in jpg_lst:
    jpg_lst_new.append(item.split(".")[0])

count = 0
for root, dirs, files in os.walk("C:\\Users\\byb\\Desktop\\1"):
    for i, file in enumerate(files):
        if file.split(".")[0] not in jpg_lst_new:
            files_path = os.path.join(root, files[i])
            os.remove(files_path)
            print(file)
            count += 1
print(count)

