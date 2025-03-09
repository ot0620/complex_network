//ベース　longループ
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <float.h>
#include "MT.h"

//bpパラメータ
#define x 7

int *get_mem_int1(int size){
        int *var=(int*)calloc(size,sizeof(int));
        if(var==NULL) { printf("mem over\n"); exit(1); }
        return var;
}

double *get_mem_double1(int size){
        double *var=(double*)calloc(size,sizeof(double));
        if(var==NULL) { printf("mem over\n"); exit(1); }
        return var;
}

int **get_mem_int2(int size1,int size2){
        int i;
        int **var=(int**)calloc(size1,sizeof(int*));
        if(var==NULL) { printf("mem over %d %d\n",size1,size2); exit(1); }
        for(i=0; i<size1; i++) {
                var[i]=(int*)calloc(size2,sizeof(int));
                if(var[i]==NULL) { printf("mem over %d %d\n",size1,size2); exit(1); }
        }
        return var;
}


//エッジ追加時のデータ更新
int connect_func(int a,int b,int node_size,int edges_size,int edges_count,int *kn,int **edges_index,int **ad){
        int i;
        //次数
        kn[a]++;
        kn[b]++;
        //エッジ
        edges_index[a][b]=edges_count;
        edges_count++;

        edges_index[b][a]=edges_count;
        edges_count++;

        if(a>node_size || b>node_size) { printf("error\n"); exit(1); }
        if(edges_count>edges_size) { printf("error\n"); exit(1); }

        //隣接リスト
        i=0;
        while(1) { if(ad[a][i]==0) { ad[a][i]=b; break; } i++; }
        i=0;
        while(1) { if(ad[b][i]==0) { ad[b][i]=a; break; } i++; }

        return edges_count;
}

void net_update_func(int N,int remove_node,int **ad_f,int *kn_f){
        int i,j,k;
        //隣接リスト更新
        for(i=1; i<=N; i++) {
                if(i==remove_node) {
                        for(j=0; j<=N; j++) { ad_f[i][j]=0; }
                }else{
                        for(j=0; ad_f[i][j]!=0; j++) {
                                if(ad_f[i][j]==remove_node) {
                                        for(k=j; ad_f[i][k]!=0; k++) { ad_f[i][k]=ad_f[i][k+1]; }
                                        break;
                                }
                        }
                }
        }

        //次数更新
        for(i=1; i<=N; i++) {
                kn_f[i]=0;
                for(j=0; j<N; j++) {
                        if(ad_f[i][j]==0) { break; }
                        kn_f[i]++;
                }
        }
}

//LCC計算用
int c_size;
int dft(int **ad_f,int *vis,int *dead,int n){
        int i;
        for(i=0; ad_f[n][i]!=0; i++) {
                if(dead[ad_f[n][i]]) { printf("error\n"); }
                if(!vis[ad_f[n][i]] && !dead[ad_f[n][i]]) {
                        vis[ad_f[n][i]]=1;
                        c_size++;
                        dft(ad_f,vis,dead,ad_f[n][i]);
                }
        }
        return c_size;
}

//最大連結成分計算
int get_LLC_max_func(int node_count,int *dead,int **ad_f){
        int i;
        int LCC_count=0;
        int LCC_max;
        int *vis=get_mem_int1(node_count+10);
        int *LCC=get_mem_int1(node_count+10);

        for(i=0; i<=node_count; i++) { vis[i]=0; LCC[i]=0; }
        for(i=1; i<=node_count; i++) {
                if(!vis[i] && !dead[i]) {
                        vis[i]=1;
                        c_size=1;         //クラスタサイズ初期化
                        LCC[LCC_count]=dft(ad_f,vis,dead,i);

                        LCC_count++;
                }
        }

        LCC_max=0;
        for(i=0; i<LCC_count; i++) { if(LCC_max<LCC[i]) { LCC_max=LCC[i]; } }
        free(vis);
        free(LCC);

        return LCC_max;
}

//bp**********************************************************************************

void shuffle(int array[], int size) {
        int i;
        for(i = 0; i < size; i++) {
                int j = genrand_int32()%size;
                int t = array[i];
                array[i] = array[j];
                array[j] = t;
        }
}

//規格化定数の計算
double z_ij_func(double *qij_0,double *qij_i,int **edges,int **ad_f,int node_i,int node_j){
        int k;
        int neighbor;
        double PAI=1.0;
        double SIG=0.0;
        double z_ij;

        for( k = 0; (neighbor = ad_f[ node_i ][k]) != 0; k++ ) {
                if(neighbor!=node_j) {
                        PAI=PAI*( qij_0[ edges[ neighbor ][ node_i ] ] + qij_i[ edges[ neighbor ][ node_i ] ] );
                        SIG=SIG+(1.0 - qij_0[ edges[ neighbor ][ node_i ] ])/(qij_0[ edges[ neighbor ][ node_i ] ] + qij_i[ edges[ neighbor ][ node_i ] ]);
                }
        }

        z_ij=1.0+exp(x)*PAI*(1.0+SIG);

        return z_ij;

}

//qij_i分子計算
double qij_i_numerator_func(double *qij_0,double *qij_i,int **edges,int **ad_f,int node_i,int node_j){
        int k;
        int neighbor;
        double PAI=1.0;
        double qi_numerator;

        for( k = 0; (neighbor = ad_f[ node_i ][k]) != 0; k++ ) {
                if(neighbor!=node_j) {
                        PAI=PAI*( qij_0[ edges[ neighbor ][ node_i ] ] + qij_i[ edges[ neighbor ][ node_i ] ] );
                }
        }
        qi_numerator=exp(x)*PAI;
        return qi_numerator;
}

//node_iの隣接jへのoutメッセージqij_0,qij_iの更新
void qij_update_func(double *qij_0,double *qij_i,int **edges,int **ad_f,int node_i){
        int k;
        int neighbor;
        double z_ij;
        double qi_numerator;

        for( k = 0; (neighbor = ad_f[ node_i ][k]) != 0; k++ ) {

                //neighborシャッフル必要？

                z_ij=z_ij_func(qij_0,qij_i,edges,ad_f,node_i,neighbor);
                qi_numerator=qij_i_numerator_func(qij_0,qij_i,edges,ad_f,node_i,neighbor);
                qij_0[ edges[ node_i ][ neighbor ] ] = 1.0/z_ij;
                qij_i[ edges[ node_i ][ neighbor ] ] = qi_numerator/z_ij;
        }
}

double qi_calc_func(double *qij_0,double *qij_i,int **edges,int **ad_f,int node_i){
        int k;
        int neighbor;
        double qi;
        double PAI=1.0;
        double SIG=0.0;

        for( k = 0; (neighbor = ad_f[ node_i ][k]) != 0; k++ ) {
                PAI=PAI*( qij_0[ edges[ neighbor ][ node_i ] ] + qij_i[ edges[ neighbor ][ node_i ] ] );
                SIG=SIG+(1.0 - qij_0[ edges[ neighbor ][ node_i ] ])/(qij_0[ edges[ neighbor ][ node_i ] ] + qij_i[ edges[ neighbor ][ node_i ] ]);
        }
        qi=1.0/(1.0+exp(x)*(1.0+SIG)*PAI);
        return qi;
}

int node_list_update_func(int remove_node,int *node_list,int node_count){
        int j;

        //node_list更新
        for(j=0; j<node_count-1; j++) {
                if(node_list[j]>=remove_node) {
                        node_list[j]=node_list[j+1];
                }
        }
        node_count--;

        return node_count;

}

int get_gamma_list_func(int node_size,int edges_size,int *kn,int **ad,int **edges_index,int *gamma){
        int i,j;
        int flag;
        int T=100;
        int node_count=node_size;
        int reiteration_count=0;
        int fN;
        int gamma_count;
        int candidate_count;
        int selection;
        double qi_max;

        //ノード除去率を指定する場合
        // double f=0.001;
        // fN=(int)(f*node_size); //1ステップでのノード除去数を計算
        // if(fN==0) { fN=1; }

        fN=1;

        int *kn_f=get_mem_int1(node_size+1);
        int **ad_f=get_mem_int2(node_size+1,node_size+1);
        int *node_list=get_mem_int1(node_size+1);
        int *shuffled_node_list=get_mem_int1(node_size+1);
        int *candidate=get_mem_int1(node_size+1);
        int *dead_f=get_mem_int1(node_size+1);
        double *qij_0=get_mem_double1(edges_size+1);
        double *qij_i=get_mem_double1(edges_size+1);
        double *qi=get_mem_double1(node_size+1);

        //ノードリスト初期化　番号順
        for(i=0; i<node_size; i++) { node_list[i]=i+1; }

        //初期化
        for(i=0; i<edges_size; i++) { qij_0[i]=genrand_real1(); qij_i[i]=genrand_real1(); }
        for(i=0; i<node_size+1; i++) { kn_f[i]=kn[i]; for(j=0; j<node_size+1; j++) { ad_f[i][j]=ad[i][j]; } }

        //ガンマリスト生成
        do {
                //ステップ1//
                //outメッセージの計算
                for(i=0; i<T; i++) {
                        //ランダムノード列の生成
                        for(j=0; j<node_count; j++) { shuffled_node_list[j]=node_list[j]; }
                        shuffle(shuffled_node_list, node_count);

                        //ランダムノード列順にoutメッセージ更新
                        for(j=0; j<node_count; j++) {
                                qij_update_func(qij_0,qij_i,edges_index,ad_f,shuffled_node_list[j]);
                        }
                }

                //qiの計算
                for(i=0; i<node_count; i++) {
                        if(dead_f[node_list[i]]) { printf("node_list error\n"); exit(1); }
                        qi[ node_list[i] ]=qi_calc_func(qij_0,qij_i,edges_index,ad_f,node_list[i]);
                }

                //qi上位fN個取り出し
                if(node_count<fN) { gamma_count=(fN*reiteration_count)+node_count; }
                else{ gamma_count=fN*reiteration_count+fN; }
                for(i=(fN*reiteration_count); i<gamma_count; i++) {

                        qi_max=-1.0;
                        for(j=0; j<node_count; j++) {
                                if(!dead_f[node_list[j]]) {
                                        if(qi[ node_list[j] ]>qi_max) {
                                                qi_max=qi[ node_list[j] ];
                                                candidate_count=0;
                                                candidate[candidate_count]=node_list[j];
                                        }else if(fabs(qi[ node_list[j] ]-qi_max)<=DBL_EPSILON) {
                                                candidate_count++;
                                                candidate[candidate_count]=node_list[j];
                                        }
                                }
                        }

                        selection=candidate[ genrand_int32()%(candidate_count+1) ];

                        gamma[i]=selection;
                        dead_f[selection]=1;
                }

                //ノード除去
                for(i=(fN*reiteration_count); i<gamma_count; i++) {
                        //隣接リスト,次数更新
                        net_update_func(node_size,gamma[i],ad_f,kn_f);
                        node_count=node_list_update_func(gamma[i],node_list,node_count);
                }

                //ステップ２//
                do {
                        flag=0;
                        for(i=0; i<node_count; i++ ) {
                                if(kn_f[ node_list[i] ]<=1 && dead_f[ node_list[i] ]!=1) {
                                        flag=1;
                                        dead_f[ node_list[i] ]=1;
                                        net_update_func(node_size,node_list[i],ad_f,kn_f);
                                        node_count=node_list_update_func(node_list[i],node_list,node_count);
                                }
                        }
                } while(flag==1);
                reiteration_count++;

        } while( node_count > 0);

        //メモリの開放
        for(i=0; i<node_size+1; i++) { free(ad_f[i]); }
        free(ad_f);
        free(kn_f);
        free(node_list);
        free(shuffled_node_list);
        free(dead_f);
        free(candidate);
        free(qij_0);
        free(qij_i);
        free(qi);

        return gamma_count;
}

double bp_attack_func(int node_size,int edges_size,int **edges_index,int *kn,int **ad,double *sn){
        int i,j;
        int candidate_count;
        int LCC_max;
        int remove_node;
        int kc_max;
        int gamma_count;
        double Rob=0.0;

        int *kn_f=get_mem_int1(node_size+1);
        int **ad_f=get_mem_int2(node_size+1,node_size+1);
        int *candidate=get_mem_int1(node_size+1);
        int *gamma=get_mem_int1(node_size+1);
        int *vis=get_mem_int1(node_size+1);
        int *LCC=get_mem_int1(node_size+1);
        int *dead=get_mem_int1(node_size+1);

        //初期化
        Rob=0.0;
        //kn,adコピー
        for(i=0; i<node_size+1; i++) { kn_f[i]=kn[i]; for(j=0; j<node_size+1; j++) { ad_f[i][j]= ad[i][j]; }  }

        gamma_count=get_gamma_list_func(node_size,edges_size,kn,ad,edges_index,gamma);

        //ノード除去プロセス
        for(i=1; i<=node_size; i++) {
                //LCC計算
                LCC_max=get_LLC_max_func(node_size,dead,ad_f);

                if(i>1) { Rob=Rob+(double)LCC_max/(double)node_size; }
                sn[i-1]+=(double)LCC_max/(double)node_size;

                if(gamma_count>=i) { //bp攻撃
                        remove_node=gamma[i-1];
                }else{ //ハブ攻撃
                        kc_max=-1;
                        for(j=1; j<=node_size; j++) {
                                if(kn_f[j]>kc_max && dead[j]!=1) {
                                        kc_max=kn_f[j];
                                        candidate_count=0;
                                        candidate[candidate_count]=j;
                                }else if(kn_f[j]==kc_max && dead[j]!=1) {
                                        candidate_count++;
                                        candidate[candidate_count]=j;
                                }
                        }
                        remove_node=candidate[ genrand_int32()%(candidate_count+1) ];
                }

                if(dead[remove_node]==1) { printf("dead_node error\n"); exit(1); }
                dead[ remove_node ]=1;
                //ネットワーク更新
                net_update_func(node_size,remove_node,ad_f,kn_f);

        }

        //メモリの開放
        for(i=0; i<node_size+1; i++) { free(ad_f[i]); }
        free(ad_f);
        free(kn_f);
        free(candidate);
        free(gamma);
        free(vis);
        free(LCC);
        free(dead);

        Rob=Rob/(double)node_size;

        return Rob;
}

//bp**********************************************************************************

int  get_network(int net_count,int node_size,int edges_size,int *kn,int **edges_index,int **ad){
        FILE *inputf;
        int flag;
        int x1,x2;
        int edges_count=0;
        char filename[20];
        char buf[30];
        char *tok;

        //ファイルからネットワーク取得
        sprintf(filename,"link%d.net",net_count+1);
        flag=0;
        inputf=fopen(filename,"r");
        while( NULL != fgets( buf, 30, inputf ) ) {
                if(flag==1) {
                        tok = strtok( buf, " " ); x1 = atoi( tok );
                        tok = strtok( NULL, " " ); x2 = atoi( tok );

                        edges_count=connect_func(x1,x2,node_size,edges_size,edges_count,kn,edges_index,ad);

                }else if(strstr(buf,"*Edges")!=NULL) { flag=1; }

        }
        fclose(inputf);

        return edges_count;
}

int main(void){
        init_genrand((unsigned)time(NULL));
        int i,j;
        int N0;
        int m;
        int node_size;
        int edges_size;
        int edges_count;
        int loop_size;
        int net_count;
        int net_size;

        printf("node_size >>\n");
        scanf("%d", &node_size);
        printf("m >>\n");
        scanf("%d", &m);
        printf("network_size >>\n");
        scanf("%d",&net_size);
        printf("loop_size >>\n");
        scanf("%d",&loop_size);

        N0=5;
        edges_size=((node_size-N0)*m+10)*2;  //最終エッジ数

        int **ad=get_mem_int2(node_size+1,node_size+1);
        int *kn=get_mem_int1(node_size+1);
        int **edges_index=get_mem_int2(node_size+1,node_size+1);
        double *sn=get_mem_double1(node_size+1);
        double *R=get_mem_double1(net_size+1);

        //ネットワーク生成ループ//
        for(net_count=0; net_count<net_size; net_count++) {

                //初期化
                edges_count=0;
                for(i=0; i<node_size+1; i++) { kn[i]=0; for(j=0; j<node_size+1; j++) { ad[i][j]=0; } }
                for(i=0; i<node_size+1; i++) { for(j=0; j<node_size+1; j++) { edges_index[i][j]=-1; } }                 //エッジがない場合はインデックスは-1

                //ファイルからネットワーク取得
                edges_count=get_network(net_count,node_size,edges_size,kn,edges_index,ad);
                if(edges_count!=edges_size) { printf("edges_count error\n"); exit(1); }

                R[net_count]=bp_attack_func(node_size,edges_count,edges_index,kn,ad,sn);
                printf("%d done! R:%lf\n",net_count+1,R[net_count]);
        }

        FILE *fout;
        char filename[20];
        sprintf(filename,"Rbp_kminl%d.txt",loop_size);
        fout=fopen(filename,"w");
        double sum_R=0.0;
        for(i=0; i<net_size; i++) {
                fprintf(fout,"%d %lf\n",i+1,R[i]);
                sum_R+=R[i];
        }
        fprintf(fout,"mean_R %lf\n",sum_R/net_size);
        fclose(fout);
        printf("mean_R %lf\n",sum_R/net_size);

        sprintf(filename,"SN_bp_kminl%d.txt",loop_size);
        fout=fopen(filename,"w");
        for(i=0; i<=node_size; i++) {
                fprintf(fout,"%lf %lf\n",(double)i/node_size,sn[i]/net_size);
        }
        fclose(fout);

        //メモリ開放
        for(i=0; i<node_size+1; i++) { free(ad[i]); free(edges_index[i]); }
        free(edges_index);
        free(ad);
        free(kn);

        return 0;
}
