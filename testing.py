from db_functions import run_search_query_tuples


def get_day(db_path):
    sql = "select strftime('%w',date('now', 'localtime')) as date"
    result= run_search_query_tuples(sql,(),db_path,True)
    print(result[0]['date'])


if __name__ == "__main__":
    db_path = 'data/dance_db.sqlite'
    #get_news(db_path)
    get_day(db_path)