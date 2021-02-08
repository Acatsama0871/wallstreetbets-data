# download.py
# download data from subreddit


import os
import json
import requests
from datetime import datetime

import pandas as pd


def redditDownloader(subreddit, keyword, start_date, end_date, submission_size, comment_size, save_as_pd):
    """
    The data downloader for subreddit

    :param subreddit: the name of the subreddit
    :param keyword: the search keyword
    :param start_date: beginning date of the data
    :param end_date: end date of the data
    :param submission_size: the download length of the submission, limited by pushshift server to 100
    :param comment_size: the download length of the comment, limited by pushshift server to 100
    :param save_as_pd: save result as pandas dataframe
    :return: if save_as_pd is False, return submission_response and comment_response as lists. If save_as_pd is True,
            return submission_response and comment_response as pandas dataframe
    """


    # helper functions
    def make_request(url):
        response = requests.get(url)
        assert response.status_code == 200
        return json.loads(response.content)['data']

    def process_submission(raw_response):
        organized = []
        for resp in raw_response:
            if 'selftext' in resp.keys():
                text = resp['selftext']
            else:
                text = ''

            record = {'id': resp['id'], 'title': resp['title'],
                      'num_comments': resp['num_comments'],
                      'text': text, 'link': resp['full_link'],
                      'subreddit': resp['subreddit'], 'subreddit_id': resp['subreddit_id'], }
            organized.append(record)

        return organized

    def process_comment(raw_response):
        organized = []
        for resp in raw_response:
            if len(resp) != 0:
                text = resp['body']
            else:
                text = ''
            record = {'parent_id': resp['parent_id'].split('_')[1], 'id': resp['id'], 'text': resp['body']}
            organized.append(record)

        return organized

    def submission2dataFrame(submission_response):
        submission_df = pd.DataFrame(columns=submission_response[0].keys())
        for resp in submission_response:
            row = [resp[i] for i in resp]
            submission_df.loc[len(submission_df)] = row

        return submission_df

    def comments2dataFrame(comment_response):
        comment_df = pd.DataFrame(columns=['parent_id', 'id', 'text'])
        for resp in comment_response:
            if len(resp) != 0:
                for record in resp:
                    row = [record[z] for z in record]
                    comment_df.loc[len(comment_df)] = row

        return comment_df

    # calculate the days
    now_date = datetime.now()
    after_days = str((now_date - datetime.strptime(start_date, "%Y-%m-%d")).days) + "d"
    before_days = str((now_date - datetime.strptime(end_date, "%Y-%m-%d")).days) + "d"

    # define url template
    submission_url_temp = "https://api.pushshift.io/reddit/search/submission/?q={}&subreddit={}&after={}&before={}&size={}"
    comments_url_temp = "https://api.pushshift.io/reddit/comment/search/?link_id={}&limit={}"

    # request for submission
    print("Requesting for submissions:")
    submission_url = submission_url_temp.format(keyword, subreddit, after_days, before_days, submission_size)
    submission_response = make_request(submission_url)
    submission_response = process_submission(submission_response)
    print("Done")

    # request for comments
    print("Requesting for comments:")
    comment_response = []
    count = 0
    for resp in submission_response:
        cur_id = resp['id']
        cur_request_link = comments_url_temp.format(cur_id, comment_size)
        cur_response = make_request(cur_request_link)
        cur_response = process_comment(cur_response)
        comment_response.append(cur_response)
        count += 1
        if count % 10 == 0:
            print(f"Extracting comments: {count}/{len(submission_response)}")
    print("Done")

    # return
    if save_as_pd is True:
        submission_df = submission2dataFrame(submission_response)
        comment_df = comments2dataFrame(comment_response)

        return submission_df, comment_df
    else:
        return submission_response, comment_response
