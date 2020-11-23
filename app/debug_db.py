from flask_sqlalchemy import get_debug_queries


def print_query():
    info = get_debug_queries()[0]
    print(info.statement, info.parameters, info.duration, sep='\n')