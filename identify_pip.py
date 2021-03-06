import numpy as np
import matplotlib.pyplot as plt

'''
Minimalistic implementation of the Identification of Perceptually Important Points
'''

class Pip(object):
    def __init__(self):
        '''Initializes a Identification Machine of Perceptually Important Points

        Data is a two-dimention array(n*m) which contains n time series whose dimention is m
        And imp_count is the number of important points which will be returned.
        imp_count should less than m

        Parameters
        ----------
        data:2-dimention array[[float]]
             Raw time series should be converted.
        imp_count:int
             Dimention of return time series
        '''
        #self.data=data
        #self._check_imp_count(imp_count)
        #self.imp_count=imp_count

    def _check_imp_count(self,imp_count):
        m=self.data.shape[1]
        imp_count=int(imp_count)
        if imp_count>=m:
            raise ValueError('imp_count(%d) should be less than dimention of time series(which is %d)' % (imp_count,m))
        if imp_count<3:
            raise ValueError('imp_count(%d) should be more than 2' % (imp_count))
        return None

    def get_single_pip(self,t):
        if t is None:
            return None
        m=len(t)
        for i in range(m):
            t[i]=float(t[i])
        start_index=[0]*m
        end_index=[m-1]*m
        imp_point_index=[]
        imp_point_dis=[]
        for _ in range(m-2):
            max_dist=0
            max_index=None
            #Seach max distance
            for i in range(m):
                x_s,x_e,x_c=start_index[i],end_index[i],i
                y_s,y_e,y_c=t[start_index[i]],t[end_index[i]],t[i]
                if x_s==x_e or x_s==x_c or x_e==x_c:
                    dist=0
                else:
                    dist=np.abs(y_s+(y_e-y_s)*(x_c-x_s)/(x_e-x_s)-y_c)
                    if dist>=max_dist:
                        max_dist=dist
                        max_index=i
            imp_point_index.append(max_index)
            imp_point_dis.append(max_dist)
            #Update start_index and end_index
            for i in range(m):
                change_area_start=start_index[max_index]
                change_area_end=end_index[max_index]
                #Update start_index
                if i > max_index and start_index[i]==change_area_start:
                    start_index[i]=max_index
                if i <= max_index and end_index[i]==change_area_end:
                    end_index[i]=max_index
        return imp_point_index

    def plot_single_imp(self,orgin_t,import_t_index,first_count):
        if first_count>=len(orgin_t):
            raise ValueError('first_count should less than length of orgin_t')
        import_t_index = import_t_index[:first_count]
        import_t_index.append(0)
        import_t_index.append(len(orgin_t)-1)
        import_t_index.sort()
        import_t_val = []
        for i in import_t_index:
            import_t_val.append(t[i])
        plt.plot(t)
        plt.plot(import_t_index, import_t_val, '--ro')

    def get_all_pip(self,data):
        result=[]
        for t in data:
            result.append(self.get_single_pip(t))
        return result








if __name__=='__main__':
    t=[1, 3, 7, -5, -8, 5, 3, 7, 10, 12, 4, 8, 10,15,1,13,-7,-5,-1,6,7,-8,12,10,8,5,7,4,12,15,18,9]
    data=[[1, 3, 7, -5, -8, 5, 3, 7, 10, 12, 4, 8, 10,15,1,13,-7,-5,-1,6,7,-8,12,10,8,5,7,4,12,15,18,9],
          [1, 3, 7, -5, 10, 5, 3, 7, 7, 12, 4, 8, 10, 12, 1, -4, -7, -5, -1, 6, 7, 9, 12, 10, 8, 2, 7, 4, 5, 4, 2,
           9],
          [1, 3, 7, -5, 9, 5, 12, 7, 10, 4, 4, 8, 9, 7, 1, -5, -7, -5, -1, 6, 10, 11, 12, 10, 8, 5, 7, 4, 12, 15, 18,
           9]]
    pi=Pip()
    import_t_index_data=pi.get_all_pip(data)
    for i in range(3):
        t=data[i]
        import_t_index=import_t_index_data[i]
        pi.plot_single_imp(t,import_t_index,5)
    plt.show()



