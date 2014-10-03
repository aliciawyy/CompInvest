'''
This is the code test when learning the course
Computational investing with the book Python for
Data Science.

Ref. Ch2 MovieLens 1M Data Set

@author: Alicia Wang
@date: 3 Oct 2014
'''

import pandas as pd

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users  = pd.read_table('../pydata-book/ch02/movielens/users.dat',
                       sep='::', header = None, names = unames)

rnames  = ['user_id', 'movie_id', 'ratings', 'timestamp']
ratings = pd.read_table('../pydata-book/ch02/movielens/ratings.dat',
                       sep='::', header = None, names = rnames)

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('../pydata-book/ch02/movielens/movies.dat',
                       sep='::', header = None, names = mnames)

data = pd.merge(pd.merge(ratings, users), movies)

mean_ratings = data.pivot_table('ratings', 
                                rows = 'title', cols = 'gender', 
                                aggfunc = 'mean' )
