
import glob
import matplotlib.pyplot as plt
import os
import numpy as np

class pycolor:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    END = '\033[0m'
    BOLD = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE = '\033[07m'

class attom:
    def __init__(self):
        self.filepath = os.getcwd()+'/RunNo.csv'

    def run_no(self):
        if os.path.exists(self.filepath) == True:
            run_no = open('RunNo.csv','r')
        else:
            run_no = open('RunNo.csv','w')
            print('Please input Run No.')
            data_list = [i for i in glob.glob('*') if not '.py' in i and not '.txt' in i and not '.csv' in i]
            if 'data' in data_list:del data_list[data_list.index('data')]
            if 'figure' in data_list:del data_list[data_list.index('figure')]
            data_list = sorted(data_list)
            for i in data_list:
                id = input(i+' : ')
                run_no.write(','.join([i,id+'\n']))
            run_no.close()
            print('RunNo.csv > .')
            run_no = open('RunNo.csv','r')

    def binary2txt(self):
        jobid = 1
        data_list = [i for i in glob.glob('*') if not '.py' in i and not '.txt' in i and not '.csv' in i]
        data_list = sorted(data_list)
        if 'data' in data_list:del data_list[data_list.index('data')]
        if 'figure' in data_list:del data_list[data_list.index('figure')]
        for fname in data_list:
            fi = open(fname,'r').readlines()
            fo = open(fname+'.txt','w')
            for line in fi:fo.write(line)
            print(pycolor.RED+'JOB_id = data '+str(jobid)+' '+pycolor.END+fname+'.txt > '+pycolor.BLUE+'data'+pycolor.END)
            jobid += 1
            fo.close()
        data_list = [i for i in glob.glob('*.txt')]
        data_list = sorted(data_list)
        filepath = os.getcwd()+'/data'
        if os.path.exists(filepath) == False:os.system('mkdir data')
        os.system('mv *.txt data')

    def txt2png(self):
        jobid = 1
        filepath = os.getcwd()+'/data/*.txt'
        data_list = [i for i in glob.glob(filepath)]
        data_list = sorted(data_list)
        for fname in data_list:
            fi,frag = open(fname,'r').readlines(),0
            for line in fi:
                if 'Timestamp' in line:array = np.array(line.rstrip().split(','))
                if frag >= 10:array = np.vstack((array,np.array(line.rstrip().split(','))))
                frag += 1
            x = [float(i) for i in array.T[0][1:]]
            for j in range(len(array.T)-2):
                name = fname.split('/')[-1].split('.')[0] + '_' + array[0][j+2]
                y = [float(i) for i in array.T[j+2][1:]]
                self.genpng(x,y,name)
                print(pycolor.RED+'JOB_id = plot '+str(jobid)+' '+pycolor.END+name+'.png > '+pycolor.BLUE+'figure'+pycolor.END)
                jobid += 1
        filepath = os.getcwd()+'/figure'
        if os.path.exists(filepath) == False:os.system('mkdir figure')
        os.system('mv *.png figure')

    def genpng(self,x,y,name):
        plt.figure()
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.size'] = 10
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams['xtick.major.width'] = 1.0
        plt.rcParams['ytick.major.width'] = 1.0
        plt.rcParams['lines.linewidth'] = 0.8
        plt.grid(which='major',color='lightgray',linestyle='-')
        plt.grid(which='minor',color='lightgray',linestyle='-')
        plt.plot(x,y,color='black')
        plt.title(name)
        plt.xlabel('Cycle')
        plt.ylabel('cps')
        plt.savefig(name+'.png')
        plt.close()

#attom = attom()
#attom.run_no()
#attom.binary2txt()
#attom.txt2png()
