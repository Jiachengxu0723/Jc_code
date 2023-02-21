import pandas as pd

if __name__ == '__main__':
    df = pd.read_excel(r'C:\\Users\\Administrator\\Desktop\\西安局1.xlsx')
    # f = open('data.txt', mode='r', encoding='utf8')
    with open ('data.txt',mode='r', encoding='utf8') as f:
        data = f.readlines()
        print(data[0].split("\t")[6])


    for i in range(len(data)):
        errNum = int(data[i].split("\t")[6].split('\n')[0])
        joint = int(data[i].split("\t")[5].split('\n')[0])
        bottom = int(data[i].split("\t")[4].split('\n')[0])
        waist = int(data[i].split("\t")[3].split('\n')[0])
        hole = int(data[i].split("\t")[2].split('\n')[0])
        head = int(data[i].split("\t")[1].split('\n')[0])
        matchData = data[i].split("\t")[0]
        df['异常总数'][df['T1K'] == matchData] = errNum
        df['焊缝伤损'][df['T1K'] == matchData] = joint
        df['轨底伤损'][df['T1K'] == matchData] = bottom
        df['轨腰伤损'][df['T1K'] == matchData] = waist
        df['螺孔裂'][df['T1K'] == matchData] = hole
        df['轨头核伤'][df['T1K'] == matchData] = head

    df.to_excel(r'C:\Users\Administrator\Desktop\西安局1.xlsx',
                sheet_name=r"西安局",
                index=False)
