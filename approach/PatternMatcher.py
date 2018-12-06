import re
import sqlite3

class PatternMatcher():

    def __init__(self, query):
        self.query = str(query).lower()

    def movie_featuring_actor(self):
        match = re.search(r'.*(?:movi\w+|film\w*).*(?:featur\w+|actor\w*|actress\w*|with\b)(.+)\b', self.query)
        
        if match:
            actor = match.group(1).strip()
            
            return 'SELECT m.* FROM movies m, people p, cast_in_movie c WHERE m.poster_path != \'\' AND m.id = c.movie_id AND p.id = c.person_id AND p.name LIKE \'{}\' LIMIT 24 COLLATE NOCASE;'.format(actor)
            
        return None

    def movie_release_date(self):
        match = re.search(r'(?:(([12]\d{3})\D{1,2}(0[1-9]|1[0-2])\D{1,2}(0[1-9]|[12]\d|3[01]))|((0[1-9]|[12]\d|3[01])\D{1,2}(0[1-9]|1[0-2])\D{1,2}([12]\d{3})))|([12]\d{3})', self.query)
        
        if match:
            # YYYY-MM-DD
            if match.group(1):
                return 'SELECT * FROM movies m WHERE m.poster_path != \'\' AND m.release_date = \'{}-{}-{}\';'.format(match.group(2), match.group(3), match.group(4))

            # DD-MM-YYYY
            if match.group(5):
                return 'SELECT * FROM movies m WHERE m.poster_path != \'\' AND strftime(\'%d-%m-%Y\', m.release_date) =  \'{}-{}-{}\';'.format(match.group(6), match.group(7), match.group(8))

            # YYYY
            if match.group(9):
                return 'SELECT * FROM movies m WHERE m.poster_path != \'\' AND strftime(\'%Y\', m.release_date) =  \'{}\';'.format(match.group(9))

        return None


    def movie_of_genre(self):
        matches = re.findall(r'(action)|(adventure)|(animation)|(comedy)|(crime)|(documentary)|(drama)|(family)|(fantasy)|(history)|(horror)|(music)|(mystery)|(romance)|(science fiction)|(tv movie)|(thriller)|(war)|(western)', self.query)

        if matches:
            genres = list(filter(None, [genre for sublist in matches for genre in sublist]))


            return 'SELECT * FROM movies m WHERE m.poster_path != \'\' AND m.id IN (SELECT movie_id FROM genres WHERE (name = \'{}\' COLLATE NOCASE) GROUP BY movie_id HAVING COUNT(movie_id) = {});'.format('\' COLLATE NOCASE OR name = \''.join(genres), len(genres))
                
        return None

    def movie_of_length(self):
        match = re.search(r'.*(?:movi\w+|film\w*).*(?:(longer|greater)|(shorter|less))\D*(\d+).*(?:(hour\w*|hr\w*)|(minut\w+|min\w*)|(second\w*|sec\w*))', self.query)

        if match:
            if match.group(1):
                if(match.group(4)):
                    return 'SELECT * FROM movies m WHERE m.poster_path != \'\' AND m.runtime > \'{}\';'.format(str(int(match.group(3)) * 60))
                elif(match.group(5)):
                    return 'SELECT * FROM movies m WHERE m.poster_path != \'\' AND m.runtime > \'{}\';'.format(str(int(match.group(3))))
                elif(match.group(6)):
                    return 'SELECT * FROM movies m WHERE m.poster_path != \'\' AND m.runtime > \'{}\';'.format(str(int(match.group(3)) / 60))
            if match.group(2):
                if(match.group(4)):
                    return 'SELECT * FROM movies m WHERE m.poster_path != \'\' AND m.runtime < \'{}\';'.format(str(int(match.group(3)) * 60))
                elif(match.group(5)):
                    return 'SELECT * FROM movies m WHERE m.poster_path != \'\' AND m.runtime < \'{}\';'.format(str(int(match.group(3))))
                elif(match.group(6)):
                    return 'SELECT * FROM movies m WHERE m.poster_path != \'\' AND m.runtime < \'{}\';'.format(str(int(match.group(3)) / 60))
        return None

    def movie_by_popularity(self):
        match = re.search(r'.*(?:(popular\w*|trend\w*)|(unpopular\w*|not trend\w*)).*(?:movi\w+|film\w*).*', self.query)

        if match:
            if match.group(1):
                return 'SELECT * FROM movies m WHERE m.poster_path != \'\' ORDER BY m.popularity DESC LIMIT 24;'
            if match.group(2):
                return 'SELECT * FROM movies m WHERE m.poster_path != \'\' ORDER BY m.popularity ASC LIMIT 24;'

        return None

    def movies_by_director(self):
        match = re.search(r'.*(?:movi\w+|film\w*).*(?:direct\w+|by)(.+)\b', self.query)

        if match:
            director = match.group(1).strip()

            return 'SELECT m.* FROM movies m, people p, crew_in_movie c WHERE m.poster_path != \'\' AND m.id = c.movie_id AND p.id = c.person_id AND c.job = \'Director\' AND p.name LIKE \'{}\' COLLATE NOCASE;'.format(director)

        return None

    def movies_in_movie_series(self):
        match = re.search(r'.*(?:movi\w+|film\w*).*(?:in|part of)(.+)(?:series|saga)', self.query)

        if match:
            movie_series = match.group(1).strip()

            return 'SELECT m.* FROM movies m, part_of_series p, movie_series s WHERE m.poster_path != \'\' AND m.id = p.movie_id AND p.movie_series_id = s.id AND s.name LIKE \'{}%\' COLLATE NOCASE;'.format(movie_series)


    def run_pattern_matcher(self):
        query = self.movie_featuring_actor()

        if(query == None):
            query = self.movies_by_director()
            if(query == None):
                query = self.movies_in_movie_series()
                if(query == None):
                    query = self.movie_by_popularity()
                    if(query == None):
                        query = self.movie_of_length()
                        if(query == None):
                            query = self.movie_release_date()
                            if(query == None):
                                query = self.movie_of_genre()
                                if(query == None):
                                    query = ""
                                    print("returning empty string")
        return query

if __name__ == '__main__':
    print('Testing Pattern Matching Approach')

    conn = sqlite3.connect('NLIM.db')

    c = conn.cursor()


    # for one row only
    #c.execute().fetchone()
    # for multiple rows
    for row in c.execute(PatternMatcher('Movies part of star wars series.').movies_in_movie_series()):
        print(row)

    