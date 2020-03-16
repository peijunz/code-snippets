#ifndef FRACTION_H
#define FRACTION_H
#include<cstdint>

template<class T>
class FractionBase{
public:
    T num, den;
    FractionBase():num(0), den(1){}
    FractionBase(const T n):num(n), den(1){}
    FractionBase(const T n, const T d):num(n), den(d){
        normalize();
    }
    FractionBase(const FractionBase &rhs):num(rhs.num), den(rhs.den){}
    FractionBase& operator=(const FractionBase &rhs){
        num=rhs.num;
        den=rhs.den;
        return *this;
    }
    bool operator==(const FractionBase &rhs) const{
        return (num==rhs.num)&&(den==rhs.den);
    }
    bool operator==(const T &rhs) const{
        return (num==rhs)&&(den==1);
    }
    bool operator<(const FractionBase &rhs) const{
        return num*rhs.den<den*rhs.num;
    }
    bool operator>(const FractionBase &rhs) const{
        return num*rhs.den>den*rhs.num;
    }
    bool operator<(const T &rhs) const{
        return num<den*rhs;
    }
    FractionBase& operator+=(const FractionBase &rhs){
        num = num*rhs.den+den*rhs.num;
        den *= rhs.den;
        normalize();
        return *this;
    }
    FractionBase operator+(const FractionBase &rhs) const{
        return FractionBase{*this}+=rhs;
    }
    FractionBase& operator-=(const FractionBase &rhs){
        num = num*rhs.den-den*rhs.num;
        den *= rhs.den;
        normalize();
        return *this;
    }
    FractionBase operator-(const FractionBase &rhs) const{
        return FractionBase{*this}-=rhs;
    }
    FractionBase& operator*=(const FractionBase &rhs){
        num *= rhs.num;
        den *= rhs.den;
        normalize();
        return *this;
    }
    FractionBase operator*(const FractionBase &rhs) const{
        return FractionBase{*this}*=rhs;
    }
    FractionBase& operator/=(const FractionBase &rhs){
        if(rhs.num<0){
            num *= -rhs.den;
            den *= -rhs.num;
        }
        else{
            num *= rhs.den;
            den *= rhs.num;
        }
        if(den){
            normalize();
        }
        return *this;
    }
    FractionBase operator/(const FractionBase &rhs) const{
        return FractionBase{*this}/=rhs;
    }
    inline void normalize(){
        T small, large, remainder=abs(num);
        if(remainder>den){
            small=den;
            large=remainder;
        }
        else{
            small=remainder;
            large=den;
        }
        while (small != 0){
            remainder = large % small;
            large = small;
            small = remainder;
        }
        num/=large;
        den/=large;
    }
//     void show() const{
//         cout << num << "/" << den<<" ";
//     }
};

template<class T>
FractionBase<T> abs(const FractionBase<T> &org){
    auto tmp=org;
    tmp.num=abs(tmp.num);
    return tmp;
}
using Fraction=FractionBase<int32_t>;
using LFraction=FractionBase<int64_t>;
#endif
