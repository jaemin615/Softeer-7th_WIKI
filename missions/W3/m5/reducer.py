import sys

current_movie = None
current_sum = 0
current_count = 0

for line in sys.stdin:
    line = line.strip()
    try:
        movie_id, rating = line.split('\t')
        rating = float(rating)
    except ValueError:
        continue

    if current_movie == movie_id:
        current_sum += rating
        current_count += 1
    else:
        if current_movie:
            average = current_sum / current_count
            print(f"{current_movie}\t{average:.1f}")
        
        current_movie = movie_id
        current_sum = rating
        current_count = 1

if current_movie == movie_id:
    average = current_sum / current_count
    print(f"{current_movie}\t{average:.1f}")