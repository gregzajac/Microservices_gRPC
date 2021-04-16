import random
from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from recommendations_pb2 import BookCategory, BookRecommendation, RecommendationResponse
from recommendations_pb2_grpc import (
    RecommendationsServicer,
    add_RecommendationsServicer_to_server,
)

all_books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title="The Maltese Falcon"),
        BookRecommendation(id=2, title="Murder on the Orient Express"),
        BookRecommendation(id=3, title="The Hound of the Baskervilles"),
    ],
    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(id=4, title="Away from the Galaxy"),
        BookRecommendation(id=5, title="Ender's Game"),
        BookRecommendation(id=6, title="The Dune Chronicles"),
    ],
    BookCategory.SELF_HELP: [
        BookRecommendation(id=7, title="Habbits of Effective People"),
        BookRecommendation(id=8, title="How to Win"),
        BookRecommendation(id=9, title="Become a Good Chef"),
    ],
}


class RecommendationService(RecommendationsServicer):
    def Recommend(self, request, context):
        if request.category not in all_books_by_category:
            # context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")
            raise NotFound("Category not found")

        books_for_category = all_books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(books_for_category, num_results)

        return RecommendationResponse(recommendations=books_to_recommend)


def serve():
    interceptors = [ExceptionToStatusInterceptor]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_RecommendationsServicer_to_server(RecommendationService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
