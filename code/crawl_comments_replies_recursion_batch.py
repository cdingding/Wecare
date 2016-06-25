import praw
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import glob

def get_file_name(file_names):
    namelist=[]
    for filename in file_names:
        namelist.append(filename.split('.')[0].split('/')[1])
    return namelist

def get_all_comments(list_of_comments):
    comment_reply_list = []
    for comment in list_of_comments:
        comment_reply_list.append(comment)
        if hasattr(comment, 'replies'):
            current_reply = get_all_comments(comment.replies)
            comment_reply_list.append(current_reply)
    comments_replies = [str(x) for x in comment_reply_list]
    comments_replies_str=', '.join(comments_replies)
    return comments_replies_str

def save_to_csv(file_names, names):
    for i in xrange(len(file_names)):
        df = pd.read_csv(file_names[i], index_col=False, header=0)
        df['comments_replies']= None
        r = praw.Reddit(user_agent='my_cool_application')
        for j in xrange(df['permalink'].shape[0]):
            this_url = df.ix[j,'permalink']
            this_url.replace('http','https')
            submission = r.get_submission(url=this_url)
            result = ''
            comments= submission.comments
            result += get_all_comments(comments)
            df.ix[j,'comments_replies'] = result
        print '%d %s.csv' % (i, names[i])
        df.to_csv('datanew/%s.csv'% names[i],index=False)

if __name__=='__main__':
    file_names = glob.glob('data/*')
    names = get_file_name(file_names)
    save_to_csv(file_names, names)