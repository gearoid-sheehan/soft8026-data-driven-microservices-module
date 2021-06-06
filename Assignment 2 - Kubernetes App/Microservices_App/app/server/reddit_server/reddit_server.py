from concurrent import futures
import logging

import grpc

import route_guide_pb2
import route_guide_pb2_grpc

import pandas as pd
import time

class Reddit(route_guide_pb2_grpc.RouteGuideServicer):

    def SendRedditPost(self, request, context):

        # Open file in read mode
        df = pd.read_csv('server/reddit_server/r_dataisbeautiful_posts.csv', sep=',',header=None)
        
        # Remove first row of column descriptions
        df = df.iloc[1:]
        
        # Iterate over each row in the csv using reader object
        for row in df.index:
            yield route_guide_pb2.GetRedditPost(id=str(df[0][row]), title=str(df[1][row]), score=str(df[2][row]), author=str(df[3][row]), author_flair_text=str(df[4][row]), 
                                    removed_by=str(df[5][row]), total_awards_received=str(df[6][row]), awarders=str(df[7][row]), created_utc=str(df[8][row]),
                                    full_link=str(df[9][row]), num_comments=str(df[10][row]), over_18=str(df[11][row]))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    route_guide_pb2_grpc.add_RouteGuideServicer_to_server(Reddit(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
