import struct
import sys,os
import threading
import time
import socket


class client(object):
    def __init__(self,IP,m1,m2,m3,ip1,port1,ip2,port2,ip3,port3):
        self.IP = IP
        self.m2 = m2
        self.m3 = m3
        self.m1 = m1
        self.ip1 = ip1
        self.ip2 = ip2
        self.ip3 = ip3
        self.port1 = port1
        self.port2 = port2
        self.port3 = port3
        global dir
        dir = r'C:\Users\kvd\Desktop\20210607' #计算节点所在目录


    def sendfile(self,s,f_path,f_size):
        # 发送文件到计算节点
        # f_path    文件路径及名
        # f_size    文件大小

        file_head = struct.pack('128sl', f_path.encode('utf-8'), f_size)
        s.send(file_head)   #发送文件头


        fp = open(f_path, 'rb')
        file = fp.read(1024)
        while file:
            s.send(file)
            file = fp.read(1024)

        fp.close()

    def max_list(self,c):
        # 用于任务三计算最大值
        # c 文件名
        # 返回为文件数据由大到小排列的列表
        f = open(c)
        txt = f.readlines()
        txt1 = []
        b = len(txt)

        for m in range(0, b):
            txt1.append(eval(txt[m].strip('\n')))
        txt1.sort(reverse=True)

        f.close()
        return txt1  # return max value

    def maxzhishu(self,list, data):
        #用于计算列表list中与data互质的最大值  即求与最大值互质的次大值
        # list 传入列表
        # data 传入的最大值
        for i in range(len(list)):
            if data % list[i] != 0:
                return list[i]  # return max value
        else:
            return 0  # return 0 : if  no number can huzhi



        # 实现任务1
    def connection(self):
        # 创建三个线程分别实现与三个计算节点通信
        s = []
        ip = [self.ip1,self.ip2,self.ip3] # 计算节点的IP地址列表
        port = [self.port1,self.port2,self.port3] # 计算节点的端口号列表
        for i in range(3):
            s.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

        for i in range(3):
            try:
                s[i].connect((ip[i], port[i]))
            except Exception as e:
                print('server not find or not open')
                sys.exit()
            print('-----------------------------')
            print('Connect Sever successfully')
            t1 = threading.Thread(target=self.tcplink1,name='Thread_0',args=(s[i],i))
            t1.start()# 线程开启

    def tcplink1(self,s,i):
        # 线程内：实现与计算节点通信

        data = s.recv(1024).decode('utf-8')
        print(data)   # 1.接受 Welcome 消息

        i = str(i)
        role=i+' and task1'
        s.send(role.encode('utf-8'))
        s.send('setup1.txt'.encode('utf-8'))   # 2.发送Role 和 Taski

        data = s.recv(1024).decode('utf-8')
        print(data)   # 3.接受：节点i接受信息成功.

        name = 'setup1.txt'
        s.send(name.encode('utf-8'))   # 3.1 发送Task 数据文件信息
        f_path = os.path.join(dir, name)
        f_size = os.path.getsize(f_path)
        self.sendfile(s,f_path,f_size)   # 3.2 发送 Task 数据文件

        name = 'task1.py'
        # s.send(name.encode('utf-8'))
        f1_path = os.path.join(dir, name)
        f1_size = os.path.getsize(f1_path)
        self.sendfile(s,f1_path,f1_size)   #3.3 发送Task 执行文件

        data = s.recv(1024).decode('utf-8')
        print(data)
        data = s.recv(1024).decode('utf-8')
        print('-----------------------------')
        print('The Thread '+i+' result is '+data)  # 4.接受各线程局部最大值

        if i == '1':
            self.m2 = int(data)
        if i == '2':
            self.m3 = int(data)
        if i == '0':
            self.m1 = int(data)

            while(self.m2==-1 or self.m3==-1):  #在线程0内规约最大值
                continue

            # 比较各线程局部最大值
            print('-----------------------------')

            print('The max value is %s.'% max(self.m1,self.m2,self.m3))
            #输出最大值 任务完成！
            print('Task 1 is completed ！ ')
            print('-----------------------------')
        s.close()


        # 实现任务2
    def connection1(self):
        # 创建三个线程分别实现与三个计算节点通信
        global starttime
        starttime = time.time() #记录程序开始时间
        for i in range(3):
            t = threading.Thread(target=self.tcplink2,args=(i,0))
            t.start()# 线程开启

    def tcplink2(self,i,p):
        # 线程内：实现与计算节点通信

        ip = [self.ip1, self.ip2, self.ip3]  # 计算节点的IP地址列表
        port = [self.port1, self.port2, self.port3]  # 计算节点的端口号列表
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((ip[i], port[i]))
        except Exception as e:
            print('server not find or not open')
            sys.exit()
        print('-----------------------------')
        print('Connect Sever successfully')

        data = s.recv(1024).decode('utf-8')
        print(data)  # 1.接受 Welcome 信息.

        i = str(i)
        role = i + ' and task2'
        s.send(role.encode('utf-8'))
        s.send('setup2.txt'.encode('utf-8'))  # 2.发送Role 和 Taski

        data = s.recv(1024).decode('utf-8')
        print(data)  # 3.3.接受：节点i接受信息成功.

        s.send('100000'.encode('utf-8'))  # 3.1 发送 num值

        name = 'task2.py'
        # s.send(name.encode('utf-8'))
        f1_path = os.path.join(dir, name)
        f1_size = os.path.getsize(f1_path)
        self.sendfile(s, f1_path, f1_size)  # 3.2 发送执行文件

        data = s.recv(1024).decode('utf-8')
        print(data)

        data = s.recv(1024).decode('utf-8')
        print('-----------------------------')
        print('The Thread ' + i + ' result is ' + data)  # 4.接受局部 sum值.

        if i == '1':
            self.m2 = data
        if i == '2':
            self.m3 = data
        if i == '0':
            self.m1 = data
            while (self.m2 == -1 or self.m3 == -1):
                continue


            sum = int(self.m1) +int(self.m2)+int(self.m3)
            # 在线程0中进行规约求和，得到质数个数和
            end_time = time.time()


            print('-----------------------------')
            print('The zhihsu sum is %s.' % sum)
            print('The Task2 is completed.')
            t1 = end_time-starttime
            print(t1)
            print('-----------------------------')


            sum_1=0
            start_1 = time.time()
            for k in range(2, 100000):
                for i in range(2, k):
                    if k % i == 0:
                        break
                else:
                    sum_1 += 1  # sum for zhihshu
            end_1 = time.time()
            print(sum_1)
            t2 = end_1-start_1
            print(t2)

            print('-----------------------------')
            print('加速比：'+str(t2/t1))
        s.close()

    # 实现Task3
    def connection2(self):
        # 创建三个线程分别实现与三个计算节点通信
        global starttime1
        starttime1 = time.time()  # 记录程序开始时间

        s = []
        ip = [self.ip1,self.ip2,self.ip3]
        port = [self.port1,self.port2,self.port3]
        for i in range(3):
            s.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

        for i in range(3):
            try:
                s[i].connect((ip[i], port[i]))
            except Exception as e:
                print('server not find or not open')
                sys.exit()
            print('-----------------------------')
            print('Connect Sever successfully')
            t1 = threading.Thread(target=self.tcplink3,name='Thread_0',args=(s[i],i))
            t1.start()# 线程开启

    def tcplink3(self,s,i):
        # 线程内：实现与计算节点通信
        global maxvalue,m4,m5,m6 #maxvalue 保存最大值  m4 m5 m6 保存局部互质次大值
        global mutex #用于同步最大值 以便向下执行求互质的次大值
        maxvalue = 0
        mutex = 0
        m4=-1
        m5=-1
        m6=-1

        data = s.recv(1024).decode('utf-8')
        print(data)# 1.接收 Welcome 消息.

        i = str(i)
        role = i + ' and task3'
        s.send(role.encode('utf-8'))
        s.send('setup3.txt'.encode('utf-8'))  # 2.发送Role 和 Taski

        data = s.recv(1024).decode('utf-8')
        print(data)    # 3.接收 计算节点接收Role 和Task成功.


        name = 'setup3.txt'
        s.send(name.encode('utf-8'))  # 3.1 发送Task 数据文件信息
        f_path = os.path.join(dir, name)
        f_size = os.path.getsize(f_path)
        self.sendfile(s, f_path, f_size)  # 3.2 发送 Task 数据文件

        name = 'task3.py'
        # s.send(name.encode('utf-8'))
        f1_path = os.path.join(dir, name)
        f1_size = os.path.getsize(f1_path)
        self.sendfile(s, f1_path, f1_size)  # 3.3 发送Task 执行文件

        data = s.recv(1024).decode('utf-8')
        print(data)
        data = s.recv(1024).decode('utf-8')
        print('-----------------------------')
        print('The Thread '+i+' max value is '+data)  # 4.接收局部最大值.
        if i == '1':
            self.m2 = data
            print('-----------------------------')
            while mutex==0:
                continue
            s.send('The max value is calculated.'.encode('utf-8'))  #
            s.send(('%s' % str(maxvalue)).encode('utf-8'))  # 5. 发送全局最大值

            data = s.recv(1024).decode('utf-8')
            print(data)
            data = s.recv(1024).decode('utf-8')

            print('-----------------------------')
            print('The Thread ' + i + ' max huzhishu is ' + data)  # 6.接收局部互质最大值
            m5 = data


        if i == '2':
            self.m3 = data
            print('-----------------------------')
            while mutex == 0:
                continue
            s.send('The max value is calculated.'.encode('utf-8'))  #
            s.send(('%s' % str(maxvalue)).encode('utf-8'))  # 5. 发送全局最大值

            data = s.recv(1024).decode('utf-8')
            print(data)
            data = s.recv(1024).decode('utf-8')

            print('-----------------------------')
            print('The Thread ' + i + ' max huzhishu is ' + data)  # 6.接收局部互质最大值
            m6 = data

        if i == '0':
            guiyuenum = 0
            self.m1 = data
            while (self.m2 == -1 or self.m3 == -1):
                continue

            maxvalue = max(self.m2,self.m1,self.m3)

            print('-----------------------------')
            print('The max value is ' + maxvalue)
            guiyuenum +=1

            mutex  =  1    #mutex改变 以实现线程0与线程1、线程2同步
            print('-----------------------------')
            s.send('The max value is calculated.'.encode('utf-8'))  #
            s.send(('%s'%str(maxvalue)).encode('utf-8'))  #5. 发送最大值max

            data = s.recv(1024).decode('utf-8')
            print(data)
            data = s.recv(1024).decode('utf-8')

            print('-----------------------------')
            print('The Thread ' + i + ' max huzhishu is ' + data)  # 6.接收局部互质次大值
            m4 = data

            while m5==-1 or m6==-1:
                continue

            maxzhi_value = max(m4,m5,m6)
            guiyuenum += 1
            print('-----------------------------')
            print('The max zhishu value is ' + maxzhi_value)
            print('The task3  is  completed.')
            print('-----------------------------')
            end_time1 = time.time()
            k = end_time1 - starttime1;
            print('分布式运行时间为：',k)

            start_time2 = time.time()
            list = self.max_list('setup3.txt')

            zhishu = self.maxzhishu(list,list[0])
            end_time2 = time.time()
            k1 = end_time2 -start_time2
            print('单机结果为：',zhishu)
            print('单机运行时间：',k1)
            print('规约轮次为： ',guiyuenum)

            print('-----------------------------')
            print('加速比为：',k1/k)

        s.close()



if __name__=='__main__':

    a = eval(input("Please input task number(1 、2 or 3):"))
    # 选择需要执行的任务i
    # 根据要执行的任务选择启动不同任务的控制节点
    if a == 1:
        cli = client('192.168.158.109', -1, -1, -1, '192.168.158.108', 5001, '192.168.158.107', 5002, '192.168.158.106', 5003)
        cli.connection()

    if a == 2:
        cli = client('192.168.158.109', -1,-1,-1, '192.168.158.108', 5001, '192.168.158.107', 5002, '192.168.158.106', 5003)
        cli.connection1()

    if a == 3:
        cli = client('192.168.158.109', -1, -1, -1, '192.168.158.108', 5001, '192.168.158.107', 5002, '192.168.158.106', 5003)
        cli.connection2()

