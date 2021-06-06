
from __future__ import print_function
import logging

import grpc

import reddit_pb2
import reddit_pb2_grpc

import time
import datetime

import redis

def run():

    try:
        conn = redis.StrictRedis(host='redis', port=6379)
        conn.flushdb()
    except Exception as ex:
        print('Error:', ex) 
         
    while True:
        with grpc.insecure_channel('redditserver:50051') as channel:
            stub = reddit_pb2_grpc.RedditStub(channel)
            responses = stub.SendPost(reddit_pb2.PostRequest(response='Recieved'))

            #Average number of comments metric
            average_num_comments = 0
            response_count = 0
            comment_count = 0
            
            #Removed by moderator
            removed_by_mod = 0

            #Rolling metric
            t = 180
            responses_three_min = 0

            while t:
                time.sleep(1)
                t -= 1

                #Single post with most letters in title
                lg_post_title = ''

                for response in responses:

                    response_count = response_count + 1
                    comment_count = int(response.num_comments) + comment_count
                    average_num_comments  = avg(response_count, comment_count)

                    if (response.over_18 == "TRUE"):
                        responses_three_min = responses_three_min + 1

                    if (response.removed_by == "moderator"):
                        removed_by_mod = removed_by_mod + 1

                    if (len(response.title) > len(lg_post_title)):
                        lg_post_title = response.title

                    try:
                        conn = redis.StrictRedis(host='redis', port=6379)
                        conn.set(response_count, "//" + str(average_num_comments) + "// Over 18 in last 3 min: " 
                        + str(responses_three_min) + "// Post removed by Moderator: " + str(removed_by_mod) + 
                        "// Longest Post Title: " + lg_post_title)

                    except Exception as ex:
                        print('Error:', ex)
                    time.sleep(2)
            
            t = 180

def avg(response_count, comment_count):

    avg = comment_count/response_count

    return avg

if __name__ == '__main__':
    logging.basicConfig()
    run()