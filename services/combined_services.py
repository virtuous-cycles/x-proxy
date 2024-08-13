from datetime import datetime

class CombinedServices:
    def __init__(self, airtable_service, x_service):
        self.airtable_service = airtable_service
        self.x_service = x_service

    def post_draft_tweet(self, draft_tweet_record_id):
        # Get the draft tweet record from Airtable
        draft_tweet = self.airtable_service.get_record(
            table_id=self.airtable_service.candidate_tweets_table_id,
            record_id=draft_tweet_record_id
        )

        if not draft_tweet:
            return {'error': 'Draft tweet not found'}, 404

        # Get the tweet content
        tweet_content = draft_tweet['fields'].get('content_cleaned') or draft_tweet['fields'].get('content')

        if not tweet_content:
            return {'error': 'No content found in draft tweet'}, 400

        # Post the tweet
        tweet_id = self.x_service.post_tweet(tweet_content)

        # Update the Airtable record
        tweet_url = f"https://x.com/truth_terminal/status/{tweet_id}"
        updated_fields = {
            'tweet_url': tweet_url,
            'tweet_date': datetime.now().isoformat()
        }
        self.airtable_service.update_record(
            table_id=self.airtable_service.candidate_tweets_table_id,
            record_id=draft_tweet_record_id,
            fields=updated_fields
        )

        return {
            'success': True,
            'tweet_id': tweet_id,
            'tweet_url': tweet_url
        }