class Solution {
    int m, n;
    vector<int> parent, size;
    int offset(int i, int j){return i<0 ? m*n: i*n+j ;}
    int find(int i){
        if (parent[i] < 0) return i;
        parent[i] = find(parent[i]);
        return parent[i];
    }
    void Union(int i, int j){
        int p1=find(i), p2=find(j);
        if (p1 == p2) return;
        if (size[p1] < size[p2]) swap(p1, p2);
        parent[p2] = p1;
        size[p1] += size[p2];
    }
public:
    vector<int> hitBricks(vector<vector<int>>& grid, vector<vector<int>>& hits) {
        m = grid.size();
        n = grid[0].size();
        int top = m*n;
        parent = vector<int>(m*n+1, 0);
        size = vector<int>(m*n+1, 0);
        for (int i=0; i<=top; i++) parent[i] = -1;
        vector<bool> real_hits;
        for (auto&hit : hits){
            real_hits.push_back(grid[hit[0]][hit[1]]);
            grid[hit[0]][hit[1]] = 0;
        }
        for (int i=0; i<m; i++){
            for (int j=0; j<n; j++){
                if (!grid[i][j]) continue;
                size[offset(i, j)] = 1;
                for (int di=0; di<2; di++){
                    if (i-di<m && 0<=j+di-1 && j+di-1<n && (i-di<0 || grid[i-di][j+di-1])){
                        Union(offset(i, j), offset(i-di, j+di-1));
                    }
                }
            }
        }
        vector<int> answer;
        vector<pair<int, int>> delta={{0,1},{0,-1},{-1,0},{1,0}};
        for (int h=hits.size()-1; h>=0; h--){
            if (!real_hits[h]) {
                answer.push_back(0);
                continue;
            }
            int i=hits[h][0], j=hits[h][1], di, dj;
            size[offset(i, j)] = 1;
            grid[i][j] = 1;
            int topside=0, dropcount=0;
            for (auto &d: delta){
                di = d.first;
                dj = d.second;
                if (i+di<m && 0<=j+dj && j+dj<n && (i+di<0 || grid[i+di][j+dj])){
                    if (find(offset(i+di, j+dj)) == find(top))
                        topside = 1;
                    else
                        dropcount += size[find(offset(i+di, j+dj))];
                    Union(offset(i+di, j+dj), offset(i, j));
                }
            }
            answer.push_back(dropcount*topside);
        }
        return vector<int>(answer.rbegin(), answer.rend());
    }
};