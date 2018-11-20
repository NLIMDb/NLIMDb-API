import re
import sqlite3

class PatternMatcher():

    def __init__(self, query):
        self.query = str(query).lower()


    # Movie Table Queries
    def movie_featuring_actor(self):
        match = re.search(r'.*(?:movi\w+|film\w*).*(?:featur\w+|actor\w*|actress\w*|with\b)(.+)\b', self.query)
        
        if match:
            actor = match.group(1).strip()
            
            return 'SELECT * FROM movies m, people p, cast_in_movie c WHERE m.id = c.movie_id AND p.id = c.person_id AND p.name LIKE \'{}\' COLLATE NOCASE;'.format(actor)

        return None

    def movie_release_year(self):
        match = re.search(r'(?:(([12]\d{3})\D{1,2}(0[1-9]|1[0-2])\D{1,2}(0[1-9]|[12]\d|3[01]))|((0[1-9]|[12]\d|3[01])\D{1,2}(0[1-9]|1[0-2])\D{1,2}([12]\d{3})))|([12]\d{3})', self.query)
        
        if match:
            # YYYY-MM-DD
            if match.group(1):
                return 'SELECT * FROM movies m WHERE m.release_date = \'{}-{}-{}\';'.format(match.group(2), match.group(3), match.group(4))

            # DD-MM-YYYY
            if match.group(5):
                return 'SELECT * FROM movies m WHERE strftime(\'%d-%m-%Y\', m.release_date) =  \'{}-{}-{}\';'.format(match.group(6), match.group(7), match.group(8))

            # YYYY
            if match.group(9):
                return 'SELECT * FROM movies m WHERE strftime(\'%Y\', m.release_date) =  \'{}\';'.format(match.group(9))

        return None


    def movie_of_genre(self):
        matches = re.findall('(action)|(adventure)|(animation)|(comedy)|(crime)|(documentary)|(drama)|(family)|(fantasy)|(history)|(horror)|(music)|(mystery)|(romance)|(science fiction)|(tv movie)|(thriller)|(war)|(western)', self.query)

        if matches:
            genres = list(filter(None, [genre for sublist in matches for genre in sublist]))

            return 'SELECT * FROM movies m WHERE m.id IN (SELECT movie_id FROM genres WHERE name = \'{}\' GROUP BY movie_id HAVING COUNT(movie_id) = {});'.format('\' COLLATE NOCASE OR name = \''.join(genres), len(genres))
                
        return None

    #def movie_of_length():

    #def movie_by_popularity():

    #def movies_by_director():

    #def videos_for_movie():

    #def movies_in_movie_series():

    #def person_by_popularity():

if __name__ == '__main__':
    print('Testing Pattern Matching Approach')

    conn = sqlite3.connect('NLIM.db')

    c = conn.cursor()

    # for one row only
    #c.execute().fetchone()
    
    # for multiple rows
    for row in c.execute(PatternMatcher('horror comedy action movies').movie_of_genre()):
        print(row)

    