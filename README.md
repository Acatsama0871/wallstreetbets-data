# wallstreetbets-data
## Overview
This repository contains the submissions(posts) and comments scraped from the
r/wallstreetbets subreddit. The time interval is from 2021-01-18 to 2021-02-02.

## Downloaded data
The downloaded data is saved at the *Data* folder. Because the pushshift exerts 
a limitation on data request, the data downloaded by the program is capped at 100.

The data is queryed with the "GME" and "gamestop" keywords(not case-sensitive). For
exmaple, the csv file: "2021-01-18_2021-01-24_gamestop_submission.csv" indicates
the file contains the submissions from 2021-01-18 to 2021-01-24 and is searched
with keyword "gamestop". 

For each submission, the corresponding comments were
also downloaded. The comments and submission are connected by the "id" and
"parent_id". For example, for a submission with id "kzotqk", the corresponding
comments are those with "kzotqk" as parent id.
