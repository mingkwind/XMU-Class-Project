'''
石材切割问题(可重复和不可重复)
问题：给定一个矩形块，用其切割出样本块，给出一个切割方案，使矩形块利用率达到最高
约束条件：1.只能一刀切
          2.样本块的切割长高方向与原样本块方向相同
'''
#作者:Aurther
import copy
from MainWindow import * # 继承至界面文件的主窗口类
class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.timer = QTimer(self)#初始化计时器
        self.spinBox.setMinimum(1)#设置样本数下界
        self.spinBox.setMaximum(10)#设置样本数上界
        self.horizontalSlider.setMaximum(200)#设置演示速度上界
        self.horizontalSlider.setMinimum(10)#设置演示速度上界
        self.horizontalSlider.valueChanged.connect(self.displaySpeed)#显示速度
        self.number=0
        self.Board=[]
        self.getSamplesNumber=[]
        self.row,self.col=0,0
        self.pushButton.clicked.connect(self.valChange)
        self.pushButton_2.clicked.connect(self.timerControl)#启动计时器
        self.timer.timeout.connect(self.tick)#计时器结束就调用self.tick()
    def displaySpeed(self):
        self.timer.setInterval(5000/ self.horizontalSlider.value())
        self.label_2.setNum(self.horizontalSlider.value())
    def Perm(self,m,li,res): #递归全排列,解空间为(N!)
        if m == len(li) - 1:
            res.append(li)
        else:
            for j in range(m,len(li)):
                li[j], li[m] = li[m], li[j]
                self.Perm(m + 1,li,res)
                li = copy.copy(li)
                li[j], li[m] = li[m], li[j]
    def valChange(self):
        if self.comboBox.currentIndex()==0:
            self.repSolve()
        else:
            self.notRepSolve()
    '''可重复的解决方法'''
    def repSolve(self):
        if not self.lineEdit.text() or not self.textEdit.toPlainText():
            msgBox = QMessageBox(self)
            msgBox.information(self, "警告", "请输入正确的数据", QMessageBox.Yes)
            print('wrong1')
            return
        judgeStone=(self.lineEdit.text()).split()
        judgeNum=int(self.spinBox.value())
        judgeStr=(self.textEdit.toPlainText()).strip()
        judgeSamples = (judgeStr).split('\n')
        if len(judgeSamples)!=judgeNum:
            msgBox = QMessageBox(self)
            msgBox.information(self, "警告", "请输入正确的数据", QMessageBox.Yes)
            print('wrong4')
            return
        for i in range(judgeNum):
            judgeSamples[i]=list(judgeSamples[i].split())
        if len(judgeStone)!=2 or '0' in judgeStone:
            msgBox = QMessageBox(self)
            msgBox.information(self, "警告", "请输入正确的数据", QMessageBox.Yes)
            print('wrong2')
            return
        if (''.join(map(str,judgeStone))).isdigit()==False:
            msgBox = QMessageBox(self)
            msgBox.information(self, "警告", "请输入正确的数据", QMessageBox.Yes)
            print('wrong3')
            return
        for item in judgeSamples:
            if len(item)!=2 or (''.join(map(str,item))).isdigit()==False or ('0' in item):
                msgBox = QMessageBox(self)
                msgBox.information(self, "警告", "请输入正确的数据", QMessageBox.Yes)
                print('wrong5')
                return
        Stone = list(map(int, (self.lineEdit.text()).split()))
        self.col=Stone[0]
        self.row=Stone[1]
        ratio = int(min(921 / Stone[0], 511/ Stone[1]))
        self.label_6.setGeometry(20, 160, ratio * Stone[0], ratio * Stone[1])
        Num = int(self.spinBox.value())
        Str = (self.textEdit.toPlainText()).strip()
        samples = (Str).split('\n')
        for i in range(Num):
            samples[i]=list(map(int,samples[i].split()))
        Samples=[]
        for item in samples:
            if not (item in Samples):
                Samples.append(item)
        Num=len(Samples)
        self.getSamplesNumber=[0 for i in range(Num)]
        print("石砖长和宽为%d，%d"%(Stone[0],Stone[1]))
        print("样本数量:%d"%Num)
        print("样本为",Samples)
        self.Board = [[-1 for col in range(Stone[0])] for row in range(Stone[1])]
        li = Samples
        res=[]
        self.Perm(0,li,res)
        Rate = []
        self.number = 0
        for cl in res:
            heng=self.repHengPosRate(Stone[0],Stone[1],0,cl)
            Rate.append(heng)
            if heng==1:
                break
            shu=self.repShuPosRate(Stone[0],Stone[1],0,cl)
            Rate.append(shu)
            if shu==1:
                break
        MaxRate = max(Rate)
        print('最大利用率为：', '%.2f' % (100 * MaxRate), '%')
        self.label_8.setText('%.2f%%' % (100 * MaxRate))
        Index = Rate.index(MaxRate)
        if Index & 1 == 0:
            self.repHengPos(0, 0, Stone[0] - 1, Stone[1] - 1, 0, res[Index // 2])
            print(self.getSamplesNumber)
            tempStr=[]
            for i in range(Num):
                if self.getSamplesNumber[i] != 0:
                    tempStr.append(str(res[Index//2][i])+":"+str(self.getSamplesNumber[i])+"个\n")
            strings="方案如下:\n"
            for item in tempStr:
                strings+=item
            self.label_9.setText(strings)
        else:
            self.repShuPos(0, 0, Stone[0] - 1, Stone[1] - 1, 0, res[Index // 2])
            print(self.getSamplesNumber)
            tempStr = []
            for i in range(Num):
                if self.getSamplesNumber[i]!=0:
                    tempStr.append(str(res[Index // 2][i]) + ":" + str(self.getSamplesNumber[i]) + "个\n")
            strings = "方案如下:\n"
            for item in tempStr:
                strings += item
            self.label_9.setText(strings)
    def repHengPosRate(self,W,H,i,cloth):#第一刀横切，W是横向,H是纵向
        if i>=len(cloth):
            return 0
        flag=0
        if W*H!=0:
            for x in cloth:
                if W%x[0]==0 and H%x[1]==0:
                    flag=1
                    break
            if 1==flag:#如果存在一种块使(W,H)可以完全被切割,利用率为100%
                return 1
        if W==0 or H==0:#避免除数为0
            return 0
        elif(cloth[i][0]>W or cloth[i][1]>H):
            return self.repHengPosRate(W,H,i+1,cloth)
        else:
            m=(cloth[i][0]*cloth[i][1]+W*(H-cloth[i][1])*self.repHengPosRate(W,H-cloth[i][1],i,cloth)+cloth[i][1]*(W-cloth[i][0])*self.repHengPosRate(W-cloth[i][0],cloth[i][1],i,cloth))/(W*H)
            return m
    def repShuPosRate(self,W,H,i,cloth):#第一刀竖切
        if i>=len(cloth):
            return 0
        flag=0
        if W*H!=0:
            for x in cloth:
                if W%x[0]==0 and H%x[1]==0:
                    flag=1
            if 1==flag:#如果存在一种块可以完全切割(W,H),利用率为100%
                return 1
        if W==0 or H==0:#避免除数为0
            return 0
        elif(cloth[i][0]>W or cloth[i][1]>H):
            return self.repShuPosRate(W,H,i+1,cloth)
        else:
            m=(cloth[i][0]*cloth[i][1]+H*(W-cloth[i][0])*self.repShuPosRate(W-cloth[i][0],H,i,cloth)+cloth[i][0]*(H-cloth[i][1])*self.repShuPosRate(cloth[i][0],H-cloth[i][1],i,cloth))/(W*H)
            return m
    def repHengPos(self,x1, y1, x2, y2, i,samples):  # 第一刀横切，W是横向,H是纵向
        if i >= len(samples):
            return
        flag = 0
        W = x2 - x1 + 1
        H = y2 - y1 + 1
        if W * H != 0:
            for x in samples:
                if W % x[0] == 0 and H % x[1] == 0:
                    flag = 1
                    self.getSamplesNumber[samples.index(x)] += W // x[0] * H // x[1]
                    break
            if 1 == flag:  # 如果存在一种块使(W,H)可以完全被切割,利用率为100%
                for nr in range(W // x[0]):
                    for nc in range(H // x[1]):
                        self.number += 1
                        for r in range(x1 + nr * x[0], x1 + (nr + 1) * x[0]):
                            for c in range(y1 + nc * x[1], y1 + (nc + 1) * x[1]):
                                self.Board[c][r] = self.number
                return
        if W == 0 or H == 0:  # 避免除数为0
            return
        elif (samples[i][0] > W or samples[i][1] > H):
            self.repHengPos(x1, y1, x2, y2, i + 1, samples)
            return
        else:
            self.number += 1
            self.getSamplesNumber[i] += 1
            for r in range(x1, x1 + samples[i][0]):
                for c in range(y1, y1 + samples[i][1]):
                    self.Board[c][r] = self.number
            self.repHengPos(x1 + samples[i][0], y1, x2, y1 + samples[i][1] - 1, i, samples)
            self.repHengPos(x1, y1 + samples[i][1], x2, y2, i, samples)
            return
    def repShuPos(self,x1, y1, x2, y2, i, samples):  # 第一刀横切，W是横向,H是纵向
        if i >= len(samples):
            return
        flag = 0
        W = x2 - x1 + 1
        H = y2 - y1 + 1
        if W * H != 0:
            for x in samples:
                if W % x[0] == 0 and H % x[1] == 0:
                    flag = 1
                    self.getSamplesNumber[samples.index(x)] += W // x[0] * H // x[1]
                    break
            if 1 == flag:  # 如果存在一种块使(W,H)可以完全被切割,利用率为100%
                for nr in range(W // x[0]):
                    for nc in range(H // x[1]):
                        self.number += 1
                        for r in range(x1 + nr * x[0], x1 + (nr + 1) * x[0]):
                            for c in range(y1 + nc * x[1], y1 + (nc + 1) * x[1]):
                                self.Board[c][r] = self.number
                return
        if W == 0 or H == 0:  # 避免除数为0
            return
        elif (samples[i][0] > W or samples[i][1] > H):
            self.repShuPos(x1, y1, x2, y2, i + 1, samples)
            return
        else:
            self.number += 1
            self.getSamplesNumber[i] += 1
            for r in range(x1, x1 + samples[i][0]):
                for c in range(y1, y1 + samples[i][1]):
                    self.Board[c][r] = self.number
            self.repShuPos(x1, y1 + samples[i][1], x1 + samples[i][0] - 1, y2, i, samples)
            self.repShuPos(x1 + samples[i][0], y1, x2, y2, i,samples)
            return
    '''不可重复的解决方法'''
    def notRepSolve(self):
        if not self.lineEdit.text() or not self.textEdit.toPlainText():
            msgBox = QMessageBox(self)
            msgBox.information(self, "警告", "请输入正确的数据", QMessageBox.Yes)
            print('wrong1')
            return
        judgeStone = (self.lineEdit.text()).split()
        judgeNum = int(self.spinBox.value())
        judgeStr = (self.textEdit.toPlainText()).strip()
        judgeSamples = (judgeStr).split('\n')
        if len(judgeSamples) != judgeNum:
            msgBox = QMessageBox(self)
            msgBox.information(self, "警告", "请输入正确的数据", QMessageBox.Yes)
            print('wrong4')
            return
        for i in range(judgeNum):
            judgeSamples[i] = list(judgeSamples[i].split())
        if len(judgeStone) != 2 or '0' in judgeStone:
            msgBox = QMessageBox(self)
            msgBox.information(self, "警告", "请输入正确的数据", QMessageBox.Yes)
            print('wrong2')
            return
        if (''.join(map(str, judgeStone))).isdigit() == False:
            msgBox = QMessageBox(self)
            msgBox.information(self, "警告", "请输入正确的数据", QMessageBox.Yes)
            print('wrong3')
            return
        for item in judgeSamples:
            if len(item) != 2 or (''.join(map(str, item))).isdigit() == False or ('0' in item):
                msgBox = QMessageBox(self)
                msgBox.information(self, "警告", "请输入正确的数据", QMessageBox.Yes)
                print('wrong5')
                return
        Stone = list(map(int, (self.lineEdit.text()).split()))
        self.col = Stone[0]
        self.row = Stone[1]
        ratio = int(min(921 / Stone[0], 511 / Stone[1]))
        self.label_6.setGeometry(20, 160, ratio * Stone[0], ratio * Stone[1])
        Num = int(self.spinBox.value())
        Str = (self.textEdit.toPlainText()).strip()
        samples = (Str).split('\n')
        for i in range(Num):
            samples[i] = list(map(int, samples[i].split()))
        Samples = []
        for item in samples:
            Samples.append(item)
        Num = len(Samples)
        self.getSamplesNumber = [0 for i in range(Num)]
        print("石砖长和宽为%d，%d" % (Stone[0], Stone[1]))
        print("样本数量:%d" % Num)
        print("样本为", Samples)
        self.Board = [[-1 for col in range(Stone[0])] for row in range(Stone[1])]
        li = Samples
        res = []
        self.Perm(0,li,res)
        Rate = []
        self.number = 0
        Smax = 0
        for item in Samples:
            Smax += item[0] * item[1]
        Smax = Smax / (Stone[0] * Stone[1])
        for cl in res:
            heng=self.notRepHengPosRate(Stone[0], Stone[1], 0, cl)[0]
            Rate.append(heng)
            if heng == 1 or heng == Smax:
                break
            shu = self.notRepShuPosRate(Stone[0], Stone[1], 0, cl)[0]
            Rate.append(shu)
            if shu == 1 or shu == Smax:
                break
        MaxRate = max(Rate)
        print('最大利用率为：', '%.2f' % (100 * MaxRate), '%')
        self.label_8.setText('%.2f%%' % (100 * MaxRate))
        Index = Rate.index(MaxRate)
        if Index & 1 == 0:
            self.notRepHengPos(0, 0, Stone[0] - 1, Stone[1] - 1, 0, res[Index // 2])
            print(self.getSamplesNumber)
            tempStr = []
            for i in range(Num):
                if self.getSamplesNumber[i] != 0:
                    tempStr.append(str(res[Index // 2][i]) + ":" + str(self.getSamplesNumber[i]) + "个\n")
            strings = "方案如下:\n"
            for item in tempStr:
                strings += item
            self.label_9.setText(strings)
        else:
            self.notRepShuPos(0, 0, Stone[0] - 1, Stone[1] - 1, 0, res[Index // 2])
            print(self.getSamplesNumber)
            tempStr = []
            for i in range(Num):
                if self.getSamplesNumber[i] != 0:
                    tempStr.append(str(res[Index // 2][i]) + ":" + str(self.getSamplesNumber[i]) + "个\n")
            strings = "方案如下:\n"
            for item in tempStr:
                strings += item
            self.label_9.setText(strings)
    def notRepHengPosRate(self,W, H, i, cloth):  # 第一刀横切，W是横向,H是纵向
        if i >= len(cloth) or (cloth[i][0] > W or cloth[i][1] > H):
            return 0, i
        else:
            m1, i1 = self.notRepHengPosRate(W, H - cloth[i][1], i + 1, cloth)
            m2, i2 = self.notRepHengPosRate(W - cloth[i][0], cloth[i][1], i1, cloth)
            return (cloth[i][0] * cloth[i][1] + W * (H - cloth[i][1]) * m1 + (cloth[i][1] * (W - cloth[i][0]) * m2)) / (W * H), i2
    def notRepShuPosRate(self,W, H, i, cloth):  # 第一刀竖切
        if i >= len(cloth) or (cloth[i][0] > W or cloth[i][1] > H):
            return 0, i
        else:
            m1, i1 =self.notRepShuPosRate(W - cloth[i][0], H, i + 1, cloth)
            m2, i2 =self.notRepShuPosRate(cloth[i][0], H - cloth[i][1], i1, cloth)
            return (cloth[i][0] * cloth[i][1] + H * (W - cloth[i][0]) * m1 + cloth[i][0] * (H - cloth[i][1]) * m2) / (W * H), i2
    def notRepHengPos(self, x1, y1, x2, y2, i, samples):  # 第一刀横切，W是横向,H是纵向
        W = x2 - x1 + 1
        H = y2 - y1 + 1
        if i >= len(samples) or (samples[i][0] > W or samples[i][1] > H):
            return i
        else:
            self.number += 1
            self.getSamplesNumber[i] += 1
            for r in range(x1, x1 + samples[i][0]):
                for c in range(y1, y1 + samples[i][1]):
                    self.Board[c][r] = self.number
            i1 = self.notRepHengPos(x1 + samples[i][0], y1, x2, y1 + samples[i][1] - 1, i + 1, samples)
            i2 = self.notRepHengPos(x1, y1 + samples[i][1], x2, y2, i1, samples)
            return i2
    def notRepShuPos(self, x1, y1, x2, y2, i, samples):  # 第一刀横切，W是横向,H是纵向
        W = x2 - x1 + 1
        H = y2 - y1 + 1
        if i >= len(samples) or (samples[i][0] > W or samples[i][1] > H):
            return i
        else:
            self.number += 1
            self.getSamplesNumber[i] += 1
            for r in range(x1, x1 + samples[i][0]):
                for c in range(y1, y1 + samples[i][1]):
                    self.Board[c][r] = self.number
            i1 = self.notRepShuPos(x1, y1 + samples[i][1], x1 + samples[i][0] - 1, y2, i + 1, samples)
            i2 = self.notRepShuPos(x1 + samples[i][0], y1, x2, y2, i1, samples)
            return i2
    '''图形演示'''
    def timerControl(self):
        if not self.Board:
            msgBox = QMessageBox(self)
            msgBox.information(self, "警告", "请先点击解决问题", QMessageBox.Yes)
            return
        self.timer.start(5000/self.horizontalSlider.value())
        self.ticks = 0
    def tick(self):
        ratio=int(min(921/self.col,511/self.row))#此处务必要有int，否则会产生无名黑线
        pix = QPixmap(ratio * self.col, ratio * self.row)
        pix = self.drawImg(pix, self.Board, self.ticks,ratio)
        self.label_6.setPixmap(pix)
        self.ticks += 1
        if self.ticks >= self.number+1:
            self.timer.stop()
    def drawImg(self, pix, _board,idx,ratio):
        myPainter = QPainter()
        myPainter.begin(pix)
        colorList = [QColor.fromRgb(255, 0, 0), QColor.fromRgb(255, 125, 0), QColor.fromRgb(255, 255, 0),
                      QColor.fromRgb(0, 255, 0), QColor.fromRgb(0, 0, 255),QColor.fromRgb(0,255,255),
                      QColor.fromRgb(255, 0, 255),QColor.fromRgb(230, 28, 100),QColor.fromRgb(240,145, 146),
                      QColor.fromRgb(220, 91,111),QColor.fromRgb(200, 8, 82),QColor.fromRgb(238,134,154),
                      QColor.fromRgb(215,0,64)]
        for _r in range(self.row):
            for _c in range(self.col):
                cubeType = _board[_r][_c]
                if cubeType <= idx and cubeType>=0:
                    color = colorList[(cubeType*5)%13]
                    myPainter.fillRect(_c * ratio, _r * ratio, ratio, ratio, color)
                else:
                    myPainter.fillRect(_c * ratio, _r * ratio, ratio, ratio, QColor(255, 255, 255))
        myPainter.end()
        return pix
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())
