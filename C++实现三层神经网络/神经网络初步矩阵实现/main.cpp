//作者：mingkwind
//三层神经网络
//单例模式
#include <iostream>
#include <fstream>
#include <time.h>
#include <iomanip>
#include <Eigen/Dense>//导入矩阵库
#include<cstdlib>
#include<ctime>
clock_t start,end;
using namespace Eigen;//使用Eigen命名空间
using namespace std;

#define INPUT_NUM 4//输入层数目
#define HIDDEN_NUM 14//隐藏层数目
#define OUTPUT_NUM 3 //输出层数目
#define dataMaxNum 200

string specie1="Iris-setosa";
string specie2="Iris-versicolor";
string specie3="Iris-virginica";
int dataNum=0;
int testNum=0;
MatrixXd data(INPUT_NUM,dataMaxNum);
MatrixXd allOutput(OUTPUT_NUM,dataMaxNum);

MatrixXd testData(INPUT_NUM,dataMaxNum);
MatrixXd testOutput(OUTPUT_NUM,dataMaxNum);

class NeuralNetwork
{
private:

    MatrixXd W1,W2;//注意：不能在此处直接定义矩阵大小，而应该在构造函数声明大小
    VectorXd B1,B2;
    VectorXd x_max,x_min;

    //singleton（单例模式）
    static NeuralNetwork *instance;
    NeuralNetwork()//此处我们对矩阵大小进行初始化
       :W1(HIDDEN_NUM,INPUT_NUM),W2(OUTPUT_NUM,HIDDEN_NUM),B1(HIDDEN_NUM),B2(OUTPUT_NUM),x_max(INPUT_NUM),x_min(INPUT_NUM)
    {
        //构建正态分布随机网络
        for(int i=0;i<HIDDEN_NUM;i++)
        {
            for(int j=0;j<INPUT_NUM;j++)
            {
                W1(i,j)=gaussrand();
            }
            B1(i)=gaussrand();
        }
        for(int i=0;i<OUTPUT_NUM;i++)
        {
            for(int j=0;j<HIDDEN_NUM;j++)
            {
                W2(i,j)=gaussrand();
            }
            B2(i)=gaussrand();
        }
        for(int i=0;i<INPUT_NUM;i++)
        {
            x_max(i)=x_min(i)=0;//初始化
        }
    }

    bool have_train(void)//判断是否进行过有效训练
    {
        bool judge=true;

        for(int i=0;i<INPUT_NUM;i++)
        {
            if(x_max(i)==x_min(i))
            {
                judge=false;
                break;
            }
        }
        return judge;
    }

    template <typename Derived>
    void normalization(MatrixBase<Derived>& data,int dataNum)//归一化处理
    {
        x_max=data.col(0);x_min=data.col(0);
        for(int i=1;i<dataNum;i++)
        {
            for(int j=0;j<INPUT_NUM;j++)
            {
                x_max(j)=max(x_max(j),data(j,i));
                x_min(j)=min(x_min(j),data(j,i));
            }
        }
        for(int i=0;i<dataNum;i++)
        {
            for(int j=0;j<INPUT_NUM;j++)
            {
                data(j,i)=(data(j,i)-x_min(j))/(x_max(j)-x_min(j));
            }
        }
    }

    double gaussrand()//高斯(正态)分布
    {
        static double V1, V2, S;
        static int phase = 0;
        double X;
        if(phase==0)
        {
            do
            {
                double U1 = (double)rand() / RAND_MAX;
                double U2 = (double)rand() / RAND_MAX;
                V1=2*U1-1;
                V2=2*U2-1;
                S=V1*V1+V2*V2;
            }while(S>=1||S==0);
            X=V1*sqrt(-2*log(S)/S);
        }
        else
        {
            X=V2*sqrt(-2*log(S)/S);
        }
        phase=1-phase;
        return X;
    }

    double sigmoid(double x)//激活函数sigmoid
    {
        return 1/(1+exp(-x));
    }

    double deriv_sigmoid(double x)//激活函数sigmoid的导数
    {
        double fx=sigmoid(x);
        return fx*(1-fx);
    }


    template <typename Derived>
    void feedforward(MatrixBase<Derived>& x,MatrixBase<Derived>& y)//前向反馈函数
    {
        VectorXd h(HIDDEN_NUM);
        h=W1*x+B1;
        for(int i=0;i<HIDDEN_NUM;i++)
        {
            h(i)=sigmoid(h(i));
        }
        y=W2*h+B2;
        for(int i=0;i<OUTPUT_NUM;i++)
        {
            y(i)=sigmoid(y(i));
        }
    }

    template <typename Derived>
    double mse_loss(MatrixBase<Derived>& y_true,MatrixBase<Derived>& y_pred,int dataNum)//损失函数：均方差函数J=1/2*(Y'-Y)^2
    {
        double sum=0;
        MatrixXd D_y;
        D_y=y_true-y_pred;
        for(int i=0;i<dataNum;i++)
        {
            sum+=0.5*(D_y.col(i)).dot(D_y.col(i));//单样本损失函数
        }
        return sum/dataNum;
    }

public:

    static NeuralNetwork* getinstance()
    {
        if(instance==NULL)
        {
            instance=new NeuralNetwork();
        }
        return instance;
    }

    template <typename Derived>
    void train(MatrixBase<Derived>& data,MatrixBase<Derived>& y_true,int dataNum)//训练函数
    {
        normalization(data,dataNum);//归一化数据
        double learn_rate=0.1;//学习率(步长)初始为0.1
        double loss=1;//初始loss
        double lossed=2;
        int epoch=0;//整个数据集的训练次数

        //计算预测值{
        VectorXd h(HIDDEN_NUM);
        VectorXd o(OUTPUT_NUM);
        VectorXd sum_h(HIDDEN_NUM);
        VectorXd sum_o(OUTPUT_NUM);
        VectorXd y_pred(OUTPUT_NUM);//单样本预测值
        MatrixXd y_preds(OUTPUT_NUM,dataMaxNum);//所有样本预测值
        //}

        //损失函数J对y_pred偏导
        VectorXd d_J_d_ypred(OUTPUT_NUM);

        //输出层神经元{
        MatrixXd d_ypred_d_w2(OUTPUT_NUM,HIDDEN_NUM);
        VectorXd d_ypred_d_b2(OUTPUT_NUM);
        MatrixXd d_ypred_d_h(OUTPUT_NUM,HIDDEN_NUM);
        //}

        //隐藏层神经元{
        MatrixXd d_h_d_w1(HIDDEN_NUM,INPUT_NUM);
        VectorXd d_h_d_b1(HIDDEN_NUM);
        //}

        //计算J(X,Y,W1,B1,W2,B2)中W1,B1,W2,B2的偏导值{
        VectorXd d_J_d_h(HIDDEN_NUM);
        MatrixXd d_J_d_w1(HIDDEN_NUM,INPUT_NUM);
        VectorXd d_J_d_b1(HIDDEN_NUM);
        MatrixXd d_J_d_w2(OUTPUT_NUM,HIDDEN_NUM);
        VectorXd d_J_d_b2(OUTPUT_NUM);
        //}

        while(abs(lossed-loss)>=0.00001)
        {

            for(int k=0;k<dataNum;k++)
            {
            //**************计算预测值y_pred***********************************************************
                sum_h=W1*data.col(k)+B1;
                for(int i=0;i<HIDDEN_NUM;i++)
                {
                    h(i)=sigmoid(sum_h(i));
                }//h=sigmoid(sum_h)=sig_moid(W1*x+B1)

                sum_o=W2*h+B2;
                for(int i=0;i<OUTPUT_NUM;i++)
                {
                    o(i)=sigmoid(sum_o(i));
                }//o=sigmoid(sum_o)=sig_moid(W2*h+B2)

                y_pred=o;//当前反馈输出
            //*******************************************************************************************

            //*************损失函数J对y_pred的偏导*******************************************************
            //单样本损失函数J=0.5*(y_pred-y_true)^2,所以d_J_d_ypred=y_pred-y_true
                d_J_d_ypred=y_pred-y_true.col(k);
            //*******************************************************************************************


            //*************输出层神经元OUTPUT************************************************************
            //y_pred=o=sigmoid(sum_o)=sig_moid(W2*h+B2),所以d_ypred_d_h=sigmoid’(sum_o)*W2
            //d_y_pred_d_w2=sigmoid’(sum_o)*h,d_y_pred_d_b2=sigmoid’(sum_o)

                for(int i=0;i<OUTPUT_NUM;i++)
                {
                    sum_o(i)=deriv_sigmoid(sum_o(i));
                }//将sum_o映射为sigmoid'(sum_o)

                for(int i=0;i<OUTPUT_NUM;i++)
                {
                    d_ypred_d_h.row(i)=sum_o(i)*W2.row(i);
                    d_ypred_d_w2.row(i)=sum_o(i)*(h.transpose());
                }//d_ypred_d_h=sigmoid’(sum_o)*W2,d_y_pred_d_w2=sigmoid’(sum_o)*h

                d_ypred_d_b2=sum_o;//d_y_pred_d_b2=sigmoid’(sum_o)
            //********************************************************************************************

            //*************隐藏层神经元HIDDEN*************************************************************
            //h=sigmoid(sum_h)=sigmoid(W1*x+B1),所以d_h_d_w1=sigmoid'(sum_h)*x
            //d_h_d_b1=sigmoid'(sum_h)

                for(int i=0;i<HIDDEN_NUM;i++)
                {
                    sum_h(i)=deriv_sigmoid(sum_h(i));
                }//将sum_h映射为sigmoid'(sum_h)

                for(int i=0;i<HIDDEN_NUM;i++)
                {
                    d_h_d_w1.row(i)=sum_h(i)*(data.col(k)).transpose();
                }//d_h_d_w1=sigmoid'(sum_h)*x

                d_h_d_b1=sum_h;//d_h_d_b1=sigmoid'(sum_h)
             //*******************************************************************************************

             //************计算J(X,Y,W1,B1,W2,B2)中W1,B1,W2,B2的偏导值************************************
                d_J_d_h=d_ypred_d_h.transpose()*d_J_d_ypred;//(a^T*B)^T=B^T*a
                for(int i=0;i<HIDDEN_NUM;i++)
                {
                    d_J_d_w1.row(i)=d_J_d_h(i)*d_h_d_w1.row(i);//对应项相乘
                }
                d_J_d_b1=(d_J_d_h.array()*d_h_d_b1.array()).matrix();//实现对应元素相乘

                for(int i=0;i<OUTPUT_NUM;i++)
                {
                    d_J_d_w2.row(i)=d_J_d_ypred(i)*d_ypred_d_w2.row(i);//对应项相乘
                }
                d_J_d_b2=(d_J_d_ypred.array()*d_ypred_d_b2.array()).matrix();//实现对应元素相乘
             //********************************************************************************************

             //***********误差反向传播，更新神经网络*******************************************************
                W1=W1-learn_rate*d_J_d_w1;
                B1=B1-learn_rate*d_J_d_b1;
                W2=W2-learn_rate*d_J_d_w2;
                B2=B2-learn_rate*d_J_d_b2;
             //********************************************************************************************

            }

            //*******每十轮更新一次损失函数值(误差）*******************************************************
            if(epoch%10==0)
            {
                lossed=loss;
                for(int i=0;i<dataNum;i++)
                {
                    VectorXd x(INPUT_NUM);
                    VectorXd y(OUTPUT_NUM);
                    x=data.col(i);
                    feedforward(x,y);
                    y_preds.col(i)=y;
                }
                loss=mse_loss(y_true,y_preds,dataNum);
                //printf("Epoch %d loss %lf\n",epoch,loss);
                printf("%d  %lf\n",epoch,loss);

                learn_rate=exp(-epoch*0.0004);//学习率函数
            }
            //*********************************************************************************************

            epoch++;

        }
    }

    template <typename Derived>
    void getOutput(MatrixBase<Derived>& input,MatrixBase<Derived>& y)
    {
        if(!have_train())
        {
            cout<<"No train,no gain."<<endl;
            return;
        }
        for(int j=0;j<INPUT_NUM;j++)
        {
            input(j)=(input(j)-x_min(j))/(x_max(j)-x_min(j));
        }
        VectorXd x(INPUT_NUM);x=input;
        VectorXd h(HIDDEN_NUM);
        for(int i=0;i<INPUT_NUM;i++)
        h=W1*x+B1;
        for(int i=0;i<HIDDEN_NUM;i++)
        {
            h(i)=sigmoid(h(i));
        }
        y=W2*h+B2;
        for(int i=0;i<OUTPUT_NUM;i++)
        {
            y(i)=sigmoid(y(i));
        }
    }

    template <typename Derived>
    void decode(MatrixBase<Derived>& Y,MatrixBase<Derived>& output)
    {
        VectorXd code1(3);code1<<1,0,0;
        VectorXd code2(3);code2<<0,1,0;
        VectorXd code3(3);code3<<0,0,1;
        bool s1=true,s2=true,s3=true;
        VectorXd y(OUTPUT_NUM);
        int MaxI=0;
        for(int i=1;i<OUTPUT_NUM;i++)
        {
            if(Y(i)>Y(MaxI)) MaxI=i;
        }
        y(MaxI)=1;
        for(int i=0;i<OUTPUT_NUM;i++)
        {
            if(i==MaxI) continue;
            y(i)=0;
        }
        for(int i=0;i<OUTPUT_NUM;i++)
        {
            if(y(i)!=code1(i)) s1=false;
            if(y(i)!=code2(i)) s2=false;
            if(y(i)!=code3(i)) s3=false;
        }
        if(s1&&!s2&&!s3)
        {
            cout<<specie1<<endl;
            output=code1;
        }
        else if(!s1&&s2&&!s3)
        {
            cout<<specie2<<endl;
            output=code2;
        }
        else if(!s1&&!s2&&s3)
        {
            cout<<specie3<<endl;
            output=code3;
        }
        else
        {
            cout<<"Be unable to identify!"<<endl;
        }
    }

    void print(void)//打印神经网络
    {
        cout<<"W1:"<<endl;
        cout<<W1<<endl;
        cout<<"B1:"<<endl;
        cout<<B1.transpose()<<endl;
        cout<<"W2:"<<endl;
        cout<<W2<<endl;
        cout<<"B2:"<<endl;
        cout<<B2.transpose()<<endl;
    }

    ~NeuralNetwork()//析构函数
    {
        cout<<"\nNeuralNetwork has been destructed!"<<endl;
    }

};
NeuralNetwork* NeuralNetwork::instance=NULL;//初始化静态成员

int main()
{
    srand(time(NULL));//随机数种子

    VectorXd code1(3);code1<<1,0,0;
    VectorXd code2(3);code2<<0,1,0;
    VectorXd code3(3);code3<<0,0,1;

    //读入文件数据
    ifstream infile;
    infile.open("iris.data");
    cout << "Reading from the file:iris.data" << endl;
    char comma;
    string s;
    while(infile>>data(0,dataNum)>>comma>>data(1,dataNum)>>comma>>data(2,dataNum)>>comma>>data(3,dataNum)>>comma>>s&&dataNum<dataMaxNum)
    {
        if(s==specie1) allOutput.col(dataNum)=code1;
        if(s==specie2) allOutput.col(dataNum)=code2;
        if(s==specie3) allOutput.col(dataNum)=code3;
        dataNum++;
    }
    infile.close();

    infile.open("test.data");
    cout << "Reading from the file:test.data" << endl;
    while(infile>>testData(0,testNum)>>comma>>testData(1,testNum)>>comma>>testData(2,testNum)>>comma>>testData(3,testNum)>>comma>>s&&testNum<dataMaxNum)
    {
        if(s==specie1) testOutput.col(testNum)=code1;
        if(s==specie2) testOutput.col(testNum)=code2;
        if(s==specie3) testOutput.col(testNum)=code3;
        testNum++;
    }
    infile.close();

    //开始实现一个神经网络
    NeuralNetwork* network=NeuralNetwork::getinstance();

    start=clock();
    network->train(data,allOutput,dataNum);
    end=clock();		//程序结束用时
	double endtime=(double)(end-start)/CLOCKS_PER_SEC;
	cout<<"Total time:"<<endtime<<endl;		//s为单位
	network->print();//输出网络

	int matchNum=0;
    MatrixXd y_preds(OUTPUT_NUM,dataMaxNum);
    VectorXd x(INPUT_NUM),y(OUTPUT_NUM);
    for(int i=0;i<testNum;i++)
    {
        x=testData.col(i);
        network->getOutput(x,y);
        y_preds.col(i)=y;
    }
    VectorXd pr(OUTPUT_NUM);
    VectorXd output(OUTPUT_NUM);
    for(int i=0;i<testNum;i++)
    {
        for(int j=0;j<OUTPUT_NUM;j++)
        {
            pr(j)=y_preds(j,i);
        }
        network->decode(pr,output);
        bool flag=true;
        for(int j=0;j<OUTPUT_NUM;j++)
        {
            if(output(j)!=testOutput(j,i))
            {
                flag=false;
                break;
            }
        }
        if(flag==true) matchNum++;
    }//输出测试集拟合效果
    cout<<"测试集匹配率："<<double(matchNum)/testNum*100<<"%"<<endl;

    //利用这个训练后的网络识别实例
    VectorXd a(INPUT_NUM),b(INPUT_NUM),c(OUTPUT_NUM);
    a<<5.0,3.5,1.3,0.3;
    b<<7,7,7,7;
    network->getOutput(a,c);
    cout<<"\na输出预测值"<<endl;
    network->decode(c,output);
    network->getOutput(b,c);
    cout<<"b输出预测值"<<endl;
    network->decode(c,output);

    delete network;

    return 0;
}
