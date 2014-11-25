#import the necessary packages
import pandas as pd
import us
import numpy as np
from multiprocessing import Pool,cpu_count,Queue,Manager

# the data in one particular column was number in the form that horrible excel version 
# of a number where '12000' is '12,000' with that beautiful useless comma in there. 
# did I mention I excel bothers me?
# instead of converting the number right away, we only convert them when we need to
def median_maker(column):
    return np.median([int(x.replace(',','')) for x in column])

# dictionary_of_dataframes contains a dataframe with information for each title; e.g title is 'Data Scientist'
# related_title_score_df is the dataframe of information for the title; columns = ['title','score'] 
### where title is a similar_title and score is how closely the two are related, e.g. 'Data Analyst', 0.871
# code_title_df contains columns ['code','title']
# oes_data_df is a HUGE dataframe with all of the Bureau of Labor Statistics(BLS) data for a given time period (YAY FREE DATA, BOO BAD CENSUS DATA!)


def job_title_location_matcher(title,location):
    try:
        related_title_score_df = dictionary_of_dataframes[title]
        # we limit dataframe1 to only those related_titles that are above 
        # a previously established threshold
        related_title_score_df = related_title_score_df[title_score_df['score']>80]

        #we merge the related titles with another table and its codes
        codes_relTitles_scores = pd.merge(code_title_df,related_title_score_df)
        codes_relTitles_scores = codes_relTitles_scores.drop_duplicates()

        # merge the two dataframes by the codes
        merged_df = pd.merge(codes_relTitles_scores, oes_data_df)
        #limit the BLS data to the state we want
        all_merged = merged_df[merged_df['area_title']==str(us.states.lookup(location).name)]

        #calculate some summary statistics for the time we want
        group_med_emp,group_mean,group_pct10,group_pct25,group_median,group_pct75,group_pct90 = all_merged[['tot_emp','a_mean','a_pct10','a_pct25','a_median','a_pct75','a_pct90']].apply(median_maker)
        row = [title,location,group_med_emp,group_mean,group_pct10,group_pct25, group_median, group_pct75, group_pct90]
        #convert it all to strings so we can combine them all when writing to file
        row_string = [str(x) for x in row]
        return row_string
    except:
        # if it doesnt work for a particular title/state just throw it out, there are enough to make this insignificant
        'do nothing' 
#runs the function and puts the answers in the queue
def worker(row, q):
        ans = job_title_location_matcher(row[0],row[1])
        q.put(ans)

# this writes to the file while there are still things that could be in the queue
# this allows for multiple processes to write to the same file without blocking eachother
def listener(q):
    f = open(filename,'wb')
    while 1:
        m = q.get()
        if m =='kill':
                break
        f.write(','.join(m) + '\n')
        f.flush()
    f.close()

def main():
    #load all your data, then throw out all unnecessary tables/columns
    filename = 'skill_TEST_POOL.txt'

    #sets up the necessary multiprocessing tasks 
    manager = Manager()
    q = manager.Queue()
    pool = Pool(cpu_count() + 2)
    watcher = pool.map_async(listener,(q,))

    jobs = []
    #titles_states is a dataframe of millions of job titles and states they were found in
    for i in titles_states.iloc:
        job = pool.map_async(worker, (i, q))
        jobs.append(job)

    for job in jobs:
        job.get()
    q.put('kill')
    pool.close()
    pool.join()
        
if __name__ == "__main__":
    main()
