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

    response_count = 1

    # Metrics count for GBVideos Data
    gb_response_count = 0
    gb_response_count = 0
    gb_comment_count = 0
    gb_lg_post_title = ''

    while True:

        with grpc.insecure_channel('youtube-server:50052') as channel:

            stub = route_guide_pb2_grpc.RouteGuideStub(channel)
            gb_responses = stub.SendYouTubePost(route_guide_pb2.PostRequestYoutube(response='Recieved'))

            # Loop over GBVideos GRPC Stream
            for gb_response in gb_responses:

                response_count += 2
                gb_response_count += 1

                gb_comment_count = int(gb_response.comment_count) + gb_comment_count
                gb_average_num_comments = avg(gb_response_count, gb_comment_count)

                if (len(gb_response.title) > len(gb_lg_post_title)):
                    gb_lg_post_title = gb_response.title

                gb_dict = {"id": response_count, "Largest Post Title": gb_lg_post_title, "Comment Count": gb_comment_count, "Average No Comments": gb_average_num_comments, 
                            "SourceKey": "GBPost"}

                db= ""

                db = get_db()

                db.analytics_tb.insert_one(gb_dict)

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