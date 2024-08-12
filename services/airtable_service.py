from pyairtable import Api

class AirtableService:
    def __init__(self, config):
        self.api = Api(config['AIRTABLE_API_KEY'])
        self.base_id = config['AIRTABLE_BASE_ID']
        self.candidate_tweets_table_id = config['AIRTABLE_CANDIDATE_TWEETS_TABLE_ID']
        self.tweet_buffer_view_id = config['AIRTABLE_TWEET_BUFFER_VIEW_ID']
        self.tables = {}

    def get_table(self, table_id):
        if table_id not in self.tables:
            self.tables[table_id] = self.api.table(self.base_id, table_id)
        return self.tables[table_id]

    def get_records(self, table_id, view_id=None, filter_by_formula=None):
        table = self.get_table(table_id)
        try:
            params = {}
            if view_id:
                params['view'] = view_id
            if filter_by_formula:
                params['filter_by_formula'] = filter_by_formula
            records = table.all(**params)
            return self._process_records(records)
        except Exception as e:
            print(f"Error fetching records from Airtable: {e}")
            return []

    def _process_records(self, records):
        return [{'id': record['id'], 'fields': record['fields']} for record in records]

    def get_approved_candidate_tweets(self):
        approved_candidate_tweets = self.get_records(
            table_id=self.candidate_tweets_table_id,
            view_id=self.tweet_buffer_view_id
        )
        return approved_candidate_tweets