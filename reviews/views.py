from django.shortcuts import render

import json

def index(request):
    # Load the review data from the reviews.json file
    with open('reviews/reviews.json', 'r') as file:
        reviews = json.load(file)

    # Apply the filtering and sorting options
    text_prioritize = request.GET.get('text_prioritize') == 'yes'
    minimum_rating = int(request.GET.get('minimum_rating', 1))
    order_by_rating = request.GET.get('order_by_rating', 'highest')
    order_by_date = request.GET.get('order_by_date', 'newest')

    filtered_reviews = []
    for review in reviews:
        if review['rating'] >= minimum_rating:
            filtered_reviews.append(review)

    if text_prioritize:
        filtered_reviews = sorted(
            filtered_reviews, key=lambda x: x.get('reviewText', ''))

    if order_by_rating == 'highest':
        filtered_reviews = sorted(
            filtered_reviews, key=lambda x: x['rating'], reverse=True)
    elif order_by_rating == 'lowest':
        filtered_reviews = sorted(filtered_reviews, key=lambda x: x['rating'])

    if order_by_date == 'newest':
        filtered_reviews = sorted(
            filtered_reviews, key=lambda x: x['reviewCreatedOnDate'], reverse=True)
    elif order_by_date == 'oldest':
        filtered_reviews = sorted(
            filtered_reviews, key=lambda x: x['reviewCreatedOnDate'])

    # Render a template or return the JSON response
    context = {'reviews': filtered_reviews}

    return render(request , "index.html" , context)

