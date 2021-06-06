from __future__ import print_function
import logging

import grpc

import route_guide_pb2
import route_guide_pb2_grpc

import time
from time import sleep
import datetime

import pymongo
from pymongo import MongoClient

def run():

    response_count = 0

    # Metrics count for Reddit Data
    r_average_num_comments = 0
    r_response_count = 0
    r_comment_count = 0
    r_lg_post_title = ''
         
    while True:

        with grpc.insecure_channel('reddit-server:50051') as channel:

            stub = route_guide_pb2_grpc.RouteGuideStub(channel)
            r_responses = stub.SendRedditPost(route_guide_pb2.PostRequestReddit(response='Recieved'))

            # Loop over Reddit GRPC Stream
            for r_response in r_responses:

                response_count += 2
                r_response_count += 1

                r_comment_count = int(r_response.num_comments) + r_comment_count
                r_average_num_comments = avg(r_response_count, r_comment_count)

                if (len(r_response.title) > len(r_lg_post_title)):
                    r_lg_post_title = r_response.title

                r_dict = {"id": response_count, "Largest Post Title": r_lg_post_title, "Comment Count": r_comment_count, "Average No Comments": r_average_num_comments, 
                            "SourceKey": "RedditPost"}
                
                db= ""

                db = get_db()

                db.analytics_tb.insert_one(r_dict)

                time.sleep(2)

# Function to make MongoDB Connection
def get_db():
    client = MongoClient(host='test-mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")

    db = client["analytics_db"]
    return db

# Function which returns average comment count
def avg(response_count, comment_count):

    avg = comment_count/response_count
    
    return avg

# Main
if __name__ == '__main__':
    logging.basicConfig()
    run()