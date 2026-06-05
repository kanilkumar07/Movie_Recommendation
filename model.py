import pandas as pd
import difflib

# ================= LOAD DATASET =================

movies = pd.read_csv("dataset\movies_datasets.csv")

# ================= FILL NULL VALUES =================

movies = movies.fillna('')

# ================= DEFAULT POSTER =================

DEFAULT_POSTER = (
    "https://via.placeholder.com/300x450?text=No+Poster"
)

# ================= POSTER FUNCTION =================

def get_poster(poster_path):

    if (
        poster_path
        and str(poster_path).startswith('/')
    ):

        return (
            "https://image.tmdb.org/t/p/w500"
            + str(poster_path)
        )

    return DEFAULT_POSTER


# ================= MOVIE DATA FUNCTION =================

def create_movie_data(movie_data):

    title = movie_data.get('title', 'Unknown')

    poster = get_poster(
        movie_data.get(
            'poster_path',
            ''
        )
    )

    overview = movie_data.get(
        'overview',
        'No overview available.'
    )

    release_date = movie_data.get(
        'release_date',
        'Unknown'
    )

    vote_average = movie_data.get(
        'vote_average',
        'N/A'
    )

    popularity = movie_data.get(
        'popularity',
        'N/A'
    )

    original_language = movie_data.get(
        'original_language',
        'Unknown'
    )

    return {

        "title": title,

        "poster": poster,

        "overview": overview,

        "release_date": release_date,

        "rating": vote_average,

        "popularity": popularity,

        "language": original_language.upper(),

        "trailer":
        f"https://www.youtube.com/results?search_query={title}+official+trailer"

    }


# ================= RECOMMEND FUNCTION =================

def recommend(movie_name):

    movie_list = movies['title'].tolist()

    close_matches = difflib.get_close_matches(
        movie_name,
        movie_list,
        n=20,
        cutoff=0.3
    )

    recommendations = []

    # ================= IF MATCH FOUND =================

    if close_matches:

        for title in close_matches:

            movie_data = movies[
                movies['title'] == title
            ].iloc[0]

            recommendations.append(
                create_movie_data(movie_data)
            )

    # ================= DEFAULT MOVIES =================

    else:

        sample_movies = movies.head(20)

        for _, movie_data in sample_movies.iterrows():

            recommendations.append(
                create_movie_data(movie_data)
            )

    return recommendations


# ================= GET SINGLE MOVIE =================

def get_movie(movie_name):

    movie_row = movies[
        movies['title']
        .str.lower()
        == movie_name.lower()
    ]

    if not movie_row.empty:

        movie_data = movie_row.iloc[0]

        return create_movie_data(movie_data)

    return None