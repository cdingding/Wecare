import pandas as pd
import glob
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def get_file_name(file_names):
    namelist=[]
    for filename in file_names:
        namelist.append(filename.split('.')[0].split('/')[1])
    return namelist

def add_subreddit_and_combine(file_names, names):
    # frame = pd.DataFrame()
    list_ = []
    for i in xrange(len(file_names)):
        df = pd.read_csv(file_names[i], index_col=False, encoding='utf8', header=0, engine='python')
        df['comments_replies'] = df['comments_replies'].fillna('')
        df['target'] = names[i]
        list_.append(df)
    frame = pd.concat(list_)
    frame.to_csv('data/allfilesfinal55.csv', index=False)

def __name__=='__main__':
    file_names = glob.glob('datanew/*.csv')
    names = get_file_name(file_names)
    add_subreddit_and_combine(file_names,names)