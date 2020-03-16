from matplotlib.colors import Normalize

class CenterNorm(Normalize):
    '''Demos see peijun.me'''
    def __init__(self, vc=0, cc=0.5, vmin=None, vmax=None, clip=False):
        '''
        Args:
            vc      value of center
            cc      color of center
        '''
        Normalize.__init__(self, vmin, vmax, clip)
        assert 0< cc < 1, "Central color should be in (0, 1)"
        self.vc = vc
        self.cc = cc
    def __call__(self, value, clip=None):
        dv = np.array([self.vc - self.vmin, self.vmax - self.vc])
        dc = np.array([self.cc, 1 - self.cc])
        k = 1/max(dv/dc)
        return np.ma.masked_array((value-self.vc)*k+self.cc)