import sys

current_product = None
rating_sum = 0
rating_count = 0

for line in sys.stdin:
    line = line.strip()
    try:
        product_id, rating = line.split('\t')
        rating = float(rating)
    except ValueError:
        continue

    if current_product == product_id:
        rating_sum += rating
        rating_count += 1
    else:
        if current_product:
            avg_rating = rating_sum / rating_count
            print(f"{current_product}\t{rating_count}\t{avg_rating:.1f}")
        
        current_product = product_id
        rating_sum = rating
        rating_count = 1

if current_product == product_id:
    avg_rating = rating_sum / rating_count
    print(f"{current_product}\t{rating_count}\t{avg_rating:.1f}")