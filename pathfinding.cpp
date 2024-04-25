#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<math.h>
#define TURN 1//转90度的权值
#define NRUT 1.7//转180度的权值
#define LEN 4//节点字符串的 最大长度=LEN-2
#define DEA 88888//尚未到达的节点用DEA标记, death
#define FROM to
#define PRE FROM->to//简化程序，寻找最短路径时到达该点的前一个节点
struct point;
typedef struct road{//路径结构体
        double length;//路径长度
        point* to;//路径去向
        road* next;//下一条路径
}*rlink;//路径指针
typedef struct point{//节点结构体。可以通过增加节点的一个方向变量来改进程序
        char name[LEN];//节点名字
        double x;//节点坐标
        double y;
        int dir;//direction
        double dis;//distance出发点到该点的最短距离的值
        point* next;//下一个节点
        rlink to;//to代表路径簇。FROM借用to的头结点，存储最短路径时的来向。
}*plink;
rlink newroad(){//生成空的道路
        rlink p=(road*)malloc(sizeof(road));
        p->length=0.;
        p->to=0;
        p->next=0;
        return p;
}
plink newpoint(char* s, double x, double y){//生成名为s，坐标为x,y的节点
        plink p=(point*)malloc(sizeof(point));
        strcpy(p->name,s);
        p->x=x;
        p->y=y;
        p->dir=0;
        p->next=NULL;
        p->to=newroad();
        return p;
}
void addpoint(plink p,plink q){//在图p中增加一个节点q
        plink pre=p;
        p=p->next;
        while(p!=NULL){
            if(strcmp(p->name,q->name)<0){
                pre=p;
                p=p->next;
            }
            else if(strcmp(p->name,q->name)==0) return;
            else break;
        }
        q->next=p;
        pre->next=q;
        return;
}
void addjoin(plink p, plink q,double length){//在增加由点p指向点q的路径
        rlink pre=p->to,rp=pre->next,rq=NULL;
        while(rp!=NULL){
            if(strcmp(rp->to->name,q->name)<0){
                pre=rp;
                rp=rp->next;
            }
            else if(strcmp(rp->to->name,q->name)==0) return;
            else break;
        }
        rq=newroad();
        rq->to=q;
        rq->length=length;
        rq->next=rp;
        pre->next=rq;
        return;
}
void addroad(plink p, char*a, char*b, double length){//在图p中，找到名为a,b的两个节点，并增加一条从a指向长度为length的道路。
        if(p==NULL) return;
        plink pa=p->next,pb=p->next;
        while(pa!=NULL){
            if(strcmp(pa->name,a)<0)
                pa=pa->next;
            else if(strcmp(pa->name,a)>0)
                return;
            else break;
        }
        while(pb!=NULL){
            if(strcmp(pb->name,b)<0)
                pb=pb->next;
            else if(strcmp(pb->name,b)>0)
                return;
            else break;
        }
        addjoin(pa,pb,length);
}
double dist(plink p, char*a, char*b, int* t){//测量图p中名为a,b的两个节点的距离dis以及位置关系（上下左右分别用1203表示，存储在t中）
        if(p==NULL) return 0;
        plink pa=p->next,pb=p->next;
        while(pa!=NULL){
            if(strcmp(pa->name,a)<0)
                pa=pa->next;
            else if(strcmp(pa->name,a)>0)
                return 0;
            else break;
        }
        while(pb!=NULL){
            if(strcmp(pb->name,b)<0)
                pb=pb->next;
            else if(strcmp(pb->name,b)>0)
                return 0;
            else break;
        }
        if((pa->x==pb->x||pa->y==pb->y)){
            if(pa->x>pb->x) *t=0;
            else if(pa->x<pb->x) *t=3;
            else if(pa->y<pb->y) *t=1;
            else *t=2;
        }
        return sqrt((pa->x-pb->x)*(pa->x-pb->x)+(pa->y-pb->y)*(pa->y-pb->y));
}
double interjoin(char*sx,char*sy,plink p){//将名为sx,sy的两个节点进行名称扩展后。进行连接
        char l[2]="l",r[2]="u",u[2]="d",d[2]="r",ls[LEN],rs[LEN];//,us[LEN],ds[LEN];
        char*ts[4]={l,r,u,d};//,*ss[4]={ls,rs,us,ds};
        double dis;
        int i=0,j=0;
        strcpy(ls,sx);
        strcat(ls,l);
        strcpy(rs,sy);
        strcat(rs,r);
        dis=dist(p,ls,rs,&j);
        i=3-j;
        strcpy(ls,sx);
        strcpy(rs,sy);
//           printf("j=%d",j);
        strcat(ls,ts[j]);
        strcat(rs,ts[j]);
        addroad(p,ls,rs,dis);
        strcpy(ls,sx);
        strcpy(rs,sy);
        strcat(ls,ts[i]);
        strcat(rs,ts[i]);
        addroad(p,rs,ls,dis);
        return dis;
}
void open(plink p,plink tp){//打开文件
        FILE *fp;
        char a[50]="data.map",s[LEN]="";
//        double x,y;
        char sx[20],sy[20],c='a',l[2]="l",r[2]="u",u[2]="d",d[2]="r",ls[LEN],rs[LEN],us[LEN],ds[LEN];
        char*ts[4]={l,r,u,d},*ss[4]={ls,rs,us,ds};
        int i,j;
        double dis;
        plink np;//newpoint
        printf("请输入数据文件的文件名:\n");
        scanf("%s",a);
        if((fp=fopen(a,"r"))==NULL){
                printf("打开失败！\n");
                return;
        }
        do{
            fscanf(fp,"%s %s %s",s,sx,sy);
//            printf("%s %s %s\n",s,sx,sy);
            np=newpoint(s,atof(sx),atof(sy));
            addpoint(tp,np);
            for(i=0;i<4;i++){
                strcpy(ss[i],s);
                strcat(ss[i],ts[i]);
                np=newpoint(ss[i],atof(sx),atof(sy));
                addpoint(p,np);
                for(j=0;j<i;j++){
                    if((i+j)==3){
                        addroad(p,ss[i],ss[j],NRUT);
                        addroad(p,ss[j],ss[i],NRUT);
                    }
                    else{
                        addroad(p,ss[i],ss[j],TURN);
                        addroad(p,ss[j],ss[i],TURN);
                    }
                }
            }
        }while((c=fgetc(fp))=='\n');
        np=p;
        while((c=fgetc(fp))=='\n'){
            fscanf(fp,"%s %s",sx,sy);
            dis=interjoin(sx,sy,p);
            addroad(tp,sx,sy,dis);
            addroad(tp,sy,sx,dis);
        }
        fclose(fp);
}
void print(plink np){//输出数据结构
        rlink rp=0;
        while((np=np->next)!=NULL){
            rp=np->to;
            printf("%s:",np->name);
            while((rp=rp->next)!=NULL){
                printf("%s %lf\t",rp->to->name,rp->length);
            }
            putchar('\n');
        }
}
void save(plink p){//保存为扩展前的简单图
        FILE* fp;
        plink q=p;
        rlink rp;
        char a[50];
        printf("请输入文件名:\n");
        scanf("%s",a);
        if((fp=fopen(a,"w"))==NULL){
                printf("打开失败！\n");
                return;
        }
        while((q=q->next)!=NULL)
            fprintf(fp,"\n%s %lf %lf",q->name,q->x,q->y);
        fputc(' ',fp);
        q=p;
        while((q=q->next)!=NULL){
            rp=q->to;
            while((rp=rp->next)!=NULL){
                if(strcmp(rp->to->name,q->name)>0)
                fprintf(fp,"\n%s %s",rp->to->name,q->name);
            }
        }
        fputc(' ',fp);
        fclose(fp);
}
void gentex(plink p){//生成该图的TeX代码，用Linux系统中的xelatex编译后，用okular打开生成的pdf文件
        plink q=p;
        rlink rq;
        FILE* fp;
        if((fp=fopen("tes.tex","w"))==NULL){
                printf("打开失败！\n");
                return;
        }
        fprintf(fp,"\\documentclass{article}\n\\usepackage{tikz}\n\\begin{document}\n\\begin{tikzpicture}\n");
        while((q=q->next)!=NULL){
            fprintf(fp,"\\filldraw (%lf,%lf) circle(0.03) (%lf+0.15,%lf+0.15)node{%s};\n",q->x,q->y,q->x,q->y,q->name);
            rq=q->to;
            while((rq=rq->next)!=NULL){
                if(strcmp(rq->to->name,q->name)>0)
                fprintf(fp,"\\draw[gray,very thin] (%lf,%lf)--(%lf,%lf);\n",q->x,q->y,rq->to->x,rq->to->y);
            }
        }
        fprintf(fp,"\\end{tikzpicture}\n\\end{document}");
        fclose(fp);
        system("xelatex ./tes.tex 1> /dev/null 2> /dev/null");
        system("okular ./tes.pdf 1> /dev/null 2> /dev/null");
}
void findpath(plink p,plink tp){//寻找最短路径，并在图形化界面中予以表示
        char from[LEN]="ar",to[LEN]="hr";
        plink q=p,np=0,tq=0;
        rlink rp=0,rq=0;
        double mi=DEA;
        printf("请输入初始点与目的地：\n初始点:");
        scanf("%s",from);
        printf("目的地:");
        scanf("%s",to);
        FILE* fp;
        if((fp=fopen("tes.tex","w"))==NULL){
                printf("打开失败！\n");
                return;
        }
        while((q=q->next)!=NULL){
            if(strcmp(q->name,from)){
                q->dis=DEA;
                q->FROM->length=DEA;
            }
            else{
                q->dis=0;
                np=q;
            }
            if((strcmp(q->name,to)==0)) tq=q;
        }
        while((np!=tq)){
            q=p;
            while((q=q->next)!=NULL){
                if(q->dis==DEA) continue;
                else{
                    rp=q->to;
                    while((rp=rp->next)!=NULL){
                        if(rp->length+q->dis<rp->to->dis){
                            rp->to->PRE=q;
                            rp->to->FROM->length=rp->length+q->dis;
                        }
                    }
                }
            }
            q=p;
            mi=DEA;
            while((q=q->next)!=NULL){
                if((q->dis==DEA)&&(q->FROM->length<mi)){
                    mi=q->FROM->length;
                    np=q;
                }
            }
            np->dis=mi;
        }
        tq=np->PRE;
        np->PRE=0;
        if(tq==NULL) return;
        while((tq->dis!=0)){
            q=tq->PRE;
            tq->PRE=np;
            np=tq;
            tq=q;
        }
        tq->PRE=np;
        q=p;
        printf("每个点的最短权");
        while((q=q->next)){
            printf("%s\t%lf\n",q->name,q->dis);
        }
        np=tq;
        q=tp;
        printf("最短路径:");
        fprintf(fp,"\\documentclass{ctexart}\n\\usepackage{tikz}\n\\begin{document}\n");
        do{
            printf("%s",tq->name);
            fprintf(fp,"%s",tq->name);
            if((tq=tq->PRE)!=NULL){
                fprintf(fp,"$\\rightarrow$");
                printf("->");
            }
            else break;
        }while(1);
        fprintf(fp,"\n\n\\begin{tikzpicture}\n");
        while((q=q->next)!=NULL){
            fprintf(fp,"\\filldraw (%lf,%lf) circle(0.03) (%lf+0.15,%lf+0.15)node{%s};\n",q->x,q->y,q->x,q->y,q->name);
            rq=q->to;
            while((rq=rq->next)!=NULL){
                if(strcmp(rq->to->name,q->name)>0)
                fprintf(fp,"\\draw[gray,very thin] (%lf,%lf)--(%lf,%lf);\n",q->x,q->y,rq->to->x,rq->to->y);
            }
        }
        q=np;
        do{
            if((q->PRE->x!=q->x)||(q->PRE->y!=q->y)){
                fprintf(fp,"\\draw[->,blue] (%lf,%lf)--(%lf,%lf);\n",q->x,q->y,q->PRE->x,q->PRE->y);
            }
        }while(((q=q->PRE)!=NULL)&&q->PRE);
        fprintf(fp,"\\end{tikzpicture}\n\\end{document}");
        fclose(fp);
        system("xelatex ./tes.tex 1> /dev/null 2> /dev/null");
        system("okular ./tes.pdf 1> /dev/null 2> /dev/null");
}
int main(){
        char s[50]="",c=0;
        plink p=newpoint(s,0,0),tp=newpoint(s,0,0);//所有的链表都是采用带头节点的链表存储的。p为扩展图。tp为简单图，保存和作图时候需要用到。
        do{//主菜单循环
            printf("1.读取\n2.保存\n3.生成图\n4.最短路径\n5.打印初始数据结构\n6.打印变换后的数据结构\n0.退出\n请输入您要进行的操作：\n");
            do c=getchar();
            while(c=='\n');
            getchar();
            if(c=='1') open(p,tp);
            else if(c=='2') save(tp);
            else if(c=='3') gentex(tp);
            else if(c=='4') findpath(p,tp);
            else if(c=='5') print(tp);
            else if(c=='6') print(p);
        }while(c!='0');
        return 0;
}
