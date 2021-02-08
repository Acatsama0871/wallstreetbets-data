# main.py
# download data

import os
import time
import pandas as pd
from download import redditDownloader

data_path = os.path.join(os.getcwd(), "Data")


def main():
    keywords = ["GME", "gamestop"]  # search keywords, not case sensitive
    time_interval = [('2021-01-18', '2021-01-24'),
                     ('2021-01-25', '2021-01-26'),
                     ('2021-01-27', '2021-01-28'),
                     ('2021-01-29', '2021-02-02')]

    print("Download start:")
    for i, (start, end) in enumerate(time_interval):
        for cur_keyword in keywords:
            print(f"Work: {i + 1}/{len(time_interval)} start:")
            cur_data_path = start + '_' + end + '_' + cur_keyword
            cur_data_path_submission = os.path.join(data_path, cur_data_path + "_submission.csv")
            cur_data_path_comment = os.path.join(data_path, cur_data_path + "_comment.csv")
            submission_df, comment_df = redditDownloader(subreddit='wallstreetbets',
                                                         keyword=cur_keyword,
                                                         start_date=start,
                                                         end_date=end,
                                                         submission_size=100,
                                                         comment_size=100,
                                                         save_as_pd=True)
            submission_df.to_csv(cur_data_path_submission)
            comment_df.to_csv(cur_data_path_comment)
            print("Done")
            time.sleep(60)
            # The Pushshift is currently limiting requests to 200 requests per minute.
            # See: https://www.reddit.com/r/pushshift/comments/8ewz4o/pushshift_rate_limit_info/

    return


if __name__ == '__main__':
    main()
