/**
 * Answer to https://www.zhihu.com/question/54157667
 */

#include <iostream>
using namespace std;
//基类base_vector
template <class T, int N>
struct base_vector{
    static_assert(N>1, "Dimension should be positive!\n");
    char a[N];
};

template <class T>
struct base_vector<T,2>{
    union{
        struct{T x,y;};
        T a[2];
    };
};
template <class T>
struct base_vector<T,3>{
    union{
        struct{T x,y,z;};
        T a[3];
    };
};
template <class T>
struct base_vector<T,4>{
    union{
        struct{T x,y,z,w;};
        T a[4];
    };
};

//子类Vector
template <class T, int N>
class Vector:public base_vector<T,N>{
public:
    Vector()=default;
    explicit Vector(initializer_list<T> l){
        copy(begin(l), end(l), a);
    }
    using base_vector<T,N>::a;
    T norm(){
        T _norm=0;
        for(int i=0;i<N;i++){
            _norm+=a[i]*a[i];
        }
        return _norm;
    }
    void show_elements(){
        switch (N) {//Fall through
        case 4: cout<<"w="<<a[3]<<endl;
        case 3: cout<<"z="<<a[2]<<endl;
        case 2: cout<<"y="<<a[1]<<endl;
        default:cout<<"x="<<a[0]<<endl;
        }
    }
    T& operator[](int i){
        return a[i];
    }
    Vector& operator+=(Vector &rhs){
        for(int i=0;i<N;i++){
            a[i]+=rhs[i];
        }
        return *this;
    }
    Vector operator+(Vector &rhs){
        Vector ret{*this};
        ret+=rhs;
        return ret;
    }
};
int main(){
    Vector<int, 3> hello{1,1,1}, world{2,3,4};
    auto hehe=hello+world;
    hehe.show_elements();
    cout<<"Norm is "<<hehe.norm()<<endl;
}
