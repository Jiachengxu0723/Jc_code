import threading
import time
def test(p):
    time.sleep(0.001)
    print(p)

ts = []

for i in range(15):
    # target指定线程要执⾏的代码，args指定该代码的参数
    th = threading.Thread(target=test, args=[i])
    ts.append(th)
for i in ts:
    i.start()
print("it is end !")
