import sys
import json

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    
    try:
        data = json.loads(line)
        product_id = data.get('asin')
        rating = data.get('rating')

        if product_id is not None and rating is not None:
            print(f"{product_id}\t{rating}")
    except json.JSONDecodeError:
        continue