#include <iostream>
#include <set>
#define NDEBUG
#include <cassert>
using namespace std;
class Range {
public:
    int left, right;
    Range(){}
    Range(int i){
        left = i;
        right = i+1;
    }
    Range(int l, int r){
        left = l;
        right = r;
        assert(l<r && "Empty set encountered");
    }
    Range(const Range &rhs){
        left = rhs.left;
        right = rhs.right;
    }
    ~Range(){}
    bool operator<(const Range &rhs)const{
        return right < rhs.left;
    }
    //connect: intersect or touch
    bool operator==(const Range &rhs)const{
        return (rhs.right >= left) && (right >= rhs.left);
    }
    //Intersection is not empty
    bool intersect(const Range &rhs)const{
        return (rhs.right > left) && (right > rhs.left);
    }
    bool operator>(const Range &rhs)const{
        return left > rhs.right;
    }
    //Merge rhs
    const Range operator+=(const Range &rhs){
        assert(*this == rhs);
        if (left>rhs.left) left = rhs.left;
        if (right<rhs.right) right = rhs.right;
        return *this;
    }
    //Merge two conecting ranges
    const Range operator+(const Range &rhs)const{
        Range lhs(*this);
        lhs += rhs;
        return lhs;
    }
    //Test equivalence
    bool equiv(const Range &rhs) const{
        return left==rhs.left && right == rhs.right;
    }
    //Test subset
    bool in(const Range &rhs) const{
        return left>=rhs.left && right <= rhs.right;
    }
    bool in_proper(const Range &rhs) const{
        return left>rhs.left && right < rhs.right;
    }
    int length()const{
        return right-left;
    }
    friend ostream &operator <<(ostream& os, const Range &r){
        os << "["<<r.left<<", "<<r.right<<")";
        return os;
    }
};


class RangeModule {
    set<Range> R;
public:
    void addRange(const Range &rhs) {
        auto loc = R.find(rhs);
        if (loc != R.end() && !rhs.in(*loc)){
            int left = loc->left, right;
            do {
                right = loc->right;
                loc = R.erase(loc);
            } while(loc != R.end() && (rhs == *loc));
            if (left > rhs.left) left = rhs.left;
            if (right < rhs.right) right = rhs.right;
            R.insert(Range(left, right));
        }
        else R.insert(rhs);
    }
    bool queryRange(const Range q) const{
        auto loc = R.find(q);
        return (loc != R.end()) && q.in(*loc);
    }
    void removeRange(const Range q) {
        auto loc = R.find(q);
        if (loc == R.end()) return;
        if (!q.intersect(*loc)) loc++;
        if (loc == R.end() || !q.intersect(*loc)) return;
        int left = loc->left, right;

        do {right = loc->right;
            loc = R.erase(loc);
        }while (loc != R.end() && q.intersect(*loc));

        if (left < q.left) R.insert(Range(left, q.left));
        if (right > q.right) R.insert(Range(q.right, right));
    }

    void addRange(int left, int right) {
        this->addRange(Range(left, right));
    }
    bool queryRange(int left, int right) const{
        return this->queryRange(Range(left, right));
    }
    void removeRange(int left, int right) {
        this->removeRange(Range(left, right));
    }
    friend ostream &operator<<(ostream &os, const RangeModule &r){
        for (auto i:r.R){
            os<<i<<" U ";
        }
        os<<"\b\b "<<endl;
        return os;
    }
};



int main(){
    Range r(3,4), s(4, 7);
    RangeModule R;
    R.addRange(2,5);
    cout<<R;
    R.addRange(6,7);
    cout<<R;
    R.addRange(8,10);
    cout<<R;
    R.addRange(4,9);
    cout<<R;
    R.removeRange(4,7);
    cout<<R;
    R.addRange(5,6);
    cout<<R;
    R.removeRange(4,5);
    cout<<R;
}
