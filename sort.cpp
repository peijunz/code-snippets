#include <iostream>
using namespace std;

template <typename T>
void insertion_sort(T* head, int length){
    int i, j, tmp;
    for (i=1; i<length; i++){
        tmp = head[i];
        for (j=i; j>0 && head[j-1] > head[j]; j--){
            head[j] = head[j-1];
        }
        head[j-1] = tmp;
    }
}

template <typename T>
void sieve_down(T*head, int pos, int length){
    int k;
    while (pos<length/2){
        if (((pos<<1)+2<length) && (head[(pos<<1)+2] > head[(pos<<1)+1])){
            k = (pos<<1) + 2;
        }
        else{
            k = (pos<<1) + 1;
        }
        if (head[pos] < head[k]){
            swap(head[pos], head[k]);
            pos = k;
        }
        else{
            break;
        }
    }
}

template <typename T>
void max_heapify(T*head, int length){
    for(int i = length/2-1; i>=0; i--)
        sieve_down(head, i, length);
}

template <typename T>
void heap_sort(T*head, int length){
    max_heapify(head, length);
    for (int i=length-1;i>0;i--){
        swap(head[i], head[0]);
        sieve_down(head, 0, i);
    }
}

int main(){
    int l[10]={7,2,3,4,8,2,2,9,4,1};
//     insertion_sort(l, 10);
    heap_sort(l, 10);
    for(int i=0; i<10;i++){
        cout << l[i]<<endl;
    }
}
