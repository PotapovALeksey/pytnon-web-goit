from generate_data import generate_data
import queries


def call_queries():
    queries.query_1()
    queries.query_2(2)
    queries.query_3(2)
    queries.query_4()
    queries.query_5(5)
    queries.query_6(1)
    queries.query_7(1, 2)
    queries.query_8(5)
    queries.query_9(1)
    queries.query_10(1, 1)
    queries.query_11(1, 1)
    queries.query_12(1, 3)


if __name__ == "__main__":
    # generate_data()
    call_queries()
