import pandas as pd
import math


class watermalon:
    '''
    color=[]    #色泽
    root=[]     #根蒂
    knock=[]    #敲声
    texture=[]      #纹理
    umbilical=[]    #脐部
    touch=[]       #触感
    density=[]  #密度
    sugar=[]    #含糖
    '''
    num = 0  # 属性数量
    numbers = 0  # 数据个数
    attributes = []  # 属性值
    attributes_list = []  # 全部属性值列表
    attributes_p = []  # 各个属性取值的好坏瓜概率
    good_num = 0  # 好瓜个数
    good_p = 0.0  # 好瓜概率
    bad_p = 0.0  # 坏瓜概率

    def __init__(self, num):
        self.num = num
        self.numbers = 0
        for i in range(num):
            self.attributes.append([])
            self.attributes_list.append([])
            self.attributes_p.append([])

    def add_data(self, *args):
        # print(args)
        for i in range(self.num):
            self.attributes[i].append(args[i])
            if not isinstance(args[i], str):
                continue
            elif args[i] not in self.attributes_list[i]:
                self.attributes_list[i].append(args[i])
                self.attributes_p.append([])

        self.numbers += 1

    def show_data(self):
        print("属性数量:" + str(self.num))
        print("数据个数:" + str(self.numbers))
        for i in range(self.numbers):
            for j in range(self.num):
                print(self.attributes[j][i], end=" ")
            print('')
        print("属性值:")

        for i in range(self.num):
            print("第%d个属性的取值：" % (i + 1), end=' ')
            print(self.attributes_list[i])

    def priori_probability(self):  # 计算有拉普拉斯修正的先验概率

        self.good_num = 0
        for i in range(self.numbers):
            if self.attributes[self.num - 1][i] == "是":
                self.good_num += 1
        self.good_p = (self.good_num + 1) / (self.numbers + 2)
        self.bad_p = (self.numbers - self.good_num + 1) / (self.numbers + 2)

        for i in range(self.num - 1):
            if self.attributes_list[i]:  # 离散数据
                for j in range(len(self.attributes_list[i])):  # 每个属性取值
                    temp_good = 0
                    temp_bad = 0
                    temp_all = 0
                    for t in range(len(self.attributes[i])):  # 遍历每条数据的该属性
                        if self.attributes[self.num - 1][t] == "是":  # 好瓜的个数
                            temp_all += 1

                        if self.attributes[i][t] == self.attributes_list[i][j]:  # 该属性取值为此时，好瓜的个数
                            if self.attributes[self.num - 1][t] == "是":
                                temp_good += 1
                            else:
                                temp_bad += 1

                    good_p = (temp_good + 1) / (temp_all + len(self.attributes_list[i]))
                    bad_p = (temp_good + 1) / (self.numbers - temp_all + len(self.attributes_list[i]))

                    #good_p = temp_good / temp_all
                    #bad_p = temp_bad / (self.numbers - temp_all)

                    self.attributes_p[i].append((good_p, bad_p))
                    # print(self.attributes_list[i][j] + ":" + str(
                    #    (temp_good + 1) / (temp_all + len(self.attributes_list[i]))))
                    #print(self.attributes_list[i][j],"是",good_p,"否",bad_p)
                    # self.attributes_p[i][j].append()
            else:
                #print(self.attributes[i])
                good_num=0
                bad_num=0
                good_sum=0
                bad_sum=0
                for j in range(len(self.attributes[i])):
                    if self.attributes[self.num - 1][j] == "是":
                        good_num+=1
                        good_sum+=self.attributes[i][j]
                    else:
                        bad_num+=1
                        bad_sum+=self.attributes[i][j]
                good_avg=good_sum/good_num
                bad_avg=bad_sum/bad_num
                good_variance=0
                bad_variance=0

                for j in range(len(self.attributes[i])):
                    if self.attributes[self.num - 1][j] == "是":
                        good_variance+=(self.attributes[i][j]-good_avg)**2
                    else:
                        bad_variance+=(self.attributes[i][j]-bad_avg)**2

                good_variance=(good_variance/(good_num-1))**0.5
                bad_variance=(bad_variance/(bad_num-1))**0.5

                self.attributes_p[i].append((good_avg,good_variance,bad_avg,bad_variance))
        #print(self.attributes_p)

    def start_train(self):
        self.priori_probability(self)

    def test_data(self, *args):
        p_good=self.good_p
        p_bad=self.bad_p
        for i in range(self.num-1):
            if not isinstance(args[i], str):    #连续属性
                good_avg=self.attributes_p[i][0][0]
                bad_avg=self.attributes_p[i][0][2]
                good_variance=self.attributes_p[i][0][1]
                bad_variance=self.attributes_p[i][0][3]

                p_good*=(1 / ((2 * math.pi)**0.5*good_variance)) * math.exp(-(args[i]-good_avg)**2/(2*good_variance**2))
                p_bad*=(1 / ((2 * math.pi)**0.5*bad_variance)) * math.exp(-(args[i]-bad_avg)**2/(2*bad_variance**2))
            else:    #离散属性
                t=0
                for t in range(len(self.attributes_list[i])):
                    if args[i]==self.attributes_list[i][t]:
                        break
                p_good*=self.attributes_p[i][t][0]
                p_bad*=self.attributes_p[i][t][1]
                #print(self.attributes_p[i][t][1])

        print("好瓜概率:%f,坏瓜概率:%f" % (p_good,p_bad))
        if p_good>p_bad:
            print("该瓜是好瓜")
        else:
            print("该瓜是坏瓜")


if __name__ == '__main__':
    data = pd.read_csv('watermelon3_0_Ch.csv', index_col=0)
    w = watermalon(data.shape[1])
    for i in range(data.shape[0]):
        temp_data = []
        for j in data.columns:
            temp_data.append(data[j][i + 1])
        w.add_data(*tuple(temp_data))
    w.priori_probability()
    w.test_data("青绿","蜷缩","浊响","清晰","凹陷","硬滑",0.697,0.46)
    w.test_data("乌黑","硬挺","沉闷","稍糊","平坦","软粘",0.123,0.13)
    w.test_data("乌黑","稍蜷","浊响","稍糊","稍凹","软粘",0.002,0.42)
    w.test_data("浅白","蜷缩","沉闷","稍糊","平坦","硬滑",0.321,0.88)
    w.test_data("青绿","蜷缩","浊响","清晰","凹陷","软粘",0.397,0.63)
    w.test_data("浅白","硬挺","沉闷","清晰","稍凹","硬滑",0.617,0.02)
    w.show_data()
    # print(data)
    # print(data.columns)
