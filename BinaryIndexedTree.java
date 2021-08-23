class BinaryIndexedTree {
    int[] tree;

    static int lowbit(int x) {
        return x & -x;
    }
    public BinaryIndexedTree(int[] nums) {
        tree = new int[nums.length+1];
        for (int i = 0; i < nums.length; i++)
            add(i, nums[i]);
    }
    public int query(int x) { // sum(nums[:x])
        int ans = 0;
        for (int i = x; i > 0; i -= lowbit(i))
            ans += tree[i];
        return ans;
    }
    public void add(int x, int u) { // nums[x] += u
        for (int i = x+1; i < tree.length; i += lowbit(i))
            tree[i] += u;
    }
    public void set(int x, int y) { // nums[x] = y
        add(x, y - query(x+1) + query(x));
    }
    public int sumRange(int l, int r) {
        return query(r+1) - query(l);
    }
}
