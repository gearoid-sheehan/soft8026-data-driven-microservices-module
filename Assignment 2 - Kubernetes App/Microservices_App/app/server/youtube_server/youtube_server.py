from concurrent import futures
import logging

import grpc

import route_guide_pb2
import route_guide_pb2_grpc

import pandas as pd
import time

class Youtube(route_guide_pb2_grpc.RouteGuideServicer):

    def SendYouTubePost(self, request, context):

        #Open file in read mode
        df = pd.read_csv('server/youtube_server/GBvideos.csv', sep=',',header=None)
        
        #Remove first row of column descriptions
        df = df.iloc[1:]
        
        # Iterate over each row in the csv using reader object
        for row in df.index:
            yield route_guide_pb2.GetYouTubePost(video_id=str(df[0][row]), trending_date=str(df[1][row]), title=str(df[2][row]), channel_title=str(df[3][row]), category_id=str(df[4][row]), 
                                    publish_time=str(df[5][row]), tags=str(df[6][row]), views=str(df[7][row]), likes=str(df[8][row]),
                                    dislikes=str(df[9][row]), comment_count=str(df[10][row]), thumbnail_link=str(df[11][row]),
                                    comments_disabled=str(df[12][row]), ratings_disabled=str(df[13][row]), video_error_or_removed=str(df[14][row]),
                                    description=str(df[15][row]))

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    route_guide_pb2_grpc.add_RouteGuideServicer_to_server(Youtube(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
