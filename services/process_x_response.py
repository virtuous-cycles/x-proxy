def process_x_response(response):
    if not response or not response.data:
        return None

    if not hasattr(response, 'includes'):
        return response.data

    includes = response.includes

    def process_single_tweet(tweet):
        if not tweet or not hasattr(tweet, 'data'):
            return None

        processed_tweet = tweet.data.copy()

        # Add author information
        if 'users' in includes:
            author = next((user for user in includes['users'] if user.id == tweet.author_id), None)
            if author:
                processed_tweet['author'] = author.data

        # Add referenced tweets
        if 'tweets' in includes and 'referenced_tweets' in tweet.data:
            for ref in tweet.data['referenced_tweets']:
                referenced_tweet = next((t for t in includes['tweets'] if t.id == ref['id']), None)
                if referenced_tweet:
                    if 'referenced_tweets' not in processed_tweet:
                        processed_tweet['referenced_tweets'] = []
                    processed_tweet['referenced_tweets'].append(referenced_tweet.data)

        # Add media attachments
        if 'media' in includes and 'attachments' in tweet.data and 'media_keys' in tweet.data['attachments']:
            media_items = [m.data for m in includes['media'] if m.media_key in tweet.data['attachments']['media_keys']]
            if media_items:
                processed_tweet['media'] = media_items

        return processed_tweet

    # Handle both single tweet and multiple tweet responses
    if isinstance(response.data, list):
        return [process_single_tweet(tweet) for tweet in response.data if tweet]
    else:
        return process_single_tweet(response.data)