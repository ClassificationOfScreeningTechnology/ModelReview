from imdb import Cinemagoer
import json
import locale
import sys
sys.stdout.reconfigure(encoding='utf-8')

def get_imdb_id(movie_list):

    ia = Cinemagoer()
    movie_title = movie_list['title']
    movie_date = movie_list['date']
    search_results = ia.search_movie(movie_title)
    
    for movie in search_results:
        if 'year' in movie.keys() and movie['year'] == movie_date:
            return movie
        elif movie_date == '':
            return movie
    return None


def get_movie_ids(movies_json, output_json):

    with open(movies_json, 'r', encoding='utf-8') as file:
        movies = json.load(file)


    movies_with_ids = []
    for movie in movies:
        title = movie['title']
        date = movie['date']
        imdb_id = get_imdb_id(movie)
        if imdb_id:
            movies_with_ids.append({'title': title, 'imdb_id': imdb_id.movieID})
            print(f"Processed: {title} -> {imdb_id.movieID}")
        else:
            print(f"No match for movie: {title} year: {date}")

    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(movies_with_ids, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    movies_json = 'live_action/la_title_date.json'
    output_json = 'live_action/la_title_imdb_id.json'
    get_movie_ids(movies_json, output_json)
