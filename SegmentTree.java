import java.util.ArrayList;
import java.util.List;
import java.util.function.BinaryOperator;

public class SegmentTree<T> {
    List<List<T>> indexes = new ArrayList<>();
    BinaryOperator<T> acc;
    T defaultValue;
    public SegmentTree(List<T> elements, BinaryOperator<T> acc, T defaultValue) {
        int n = elements.size();
        int depth = 1 + (int) (Math.log(2*n-1)/Math.log(2));
        this.acc = acc;
        this.defaultValue = defaultValue;
        indexes.add(new ArrayList<>(elements));
        for (int i=1; i<depth; i++) {
            n = (n+1)/2;
            List<T> index = new ArrayList<>(n);
            for (int j=0; j<n; j++) {
                index.add(recompute(i, j));
            }
            this.indexes.add(index);
        }
    }

    private T recompute(int i, int k) {
        List<T> prev=indexes.get(i-1);
        return 2*k+1<prev.size()? acc.apply(prev.get(2*k), prev.get(2*k+1)) : prev.get(2*k);
    }
    
    public void set(int k, T v) {
        indexes.get(0).set(k, v);
        for (int i=1; i<indexes.size(); i++) {
            k/=2;
            indexes.get(i).set(k, recompute(i, k));
        }
    }
    public T get(int k) {
        return indexes.get(0).get(k);
    }
    
    public T prefix(int i) {
        T p = defaultValue;
        for (List<T> index: indexes) {
            if ((i&1)!=0)
                p = acc.apply(p, index.get(i-1));
            i >>= 1;
            if (i==0) break;
        }
        return p;
    }
    public static <T> SegmentTree<T> createEmpty(int n, BinaryOperator<T> acc, T defaultValue) {
        List<T> elements = new ArrayList<>(n);
        for (int i=0; i<n; i++) elements.add(defaultValue);
        return new SegmentTree<>(elements, acc, defaultValue);
    }
    public static void main(String[] args) {
        SegmentTree<Integer> pmax = SegmentTree.createEmpty(9, Integer::sum, 0);
        for (int i=0; i<9; i++) {
            pmax.set(i, 2*i+1);
        }
        for (int i=0; i<10; i++) {
            System.out.println(pmax.prefix(i));
        }
    }
}
