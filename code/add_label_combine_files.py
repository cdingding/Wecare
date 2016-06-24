# from pandas import Series
# import string

import pandas as pd
import glob

def get_file_name(file_names):
    namelist=[]
    for filename in file_names:
        namelist.append(filename.split('.')[0].split('/')[1])
    return namelist

# add subreddit names to each file as label
def add_subreddit_and_combine(file_names, names):
    frame = pd.DataFrame()
    list_ = []
    for i in xrange(len(file_names)):
        df = pd.read_csv(file_names[i], index_col=False, header=0)
        df['comments_replies'] = df['comments_replies'].dropna()
        df['target'] = names[i]
        print df.columns
        #print df['target'].head(2)
        list_.append(df)
    frame = pd.concat(list_)
    frame.to_csv('dataall/allfiles1.csv', index=False) #index=False will not give you Unnamed:0 column.
    print frame.columns
    pass

def __name__=='__main__':
    file_names = glob.glob('datacopy/*')
    names = get_file_name(file_names)
    add_subreddit_and_combine(file_names,names)



