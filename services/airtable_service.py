from pyairtable import Api
from datetime import datetime

class AirtableService:
    def __init__(self, config):
        self.api = Api(config['AIRTABLE_API_KEY'])
        self.base_id = config['AIRTABLE_BASE_ID']
        self.candidate_tweets_table_id = config['AIRTABLE_CANDIDATE_TWEETS_TABLE_ID']
        self.draft_tweets_view_id = config['AIRTABLE_EXOS_DRAFT_TWEETS_VIEW_ID']
        self.tables = {}

    def get_table(self, table_id):
        if table_id not in self.tables:
            self.tables[table_id] = self.api.table(self.base_id, table_id)
        return self.tables[table_id]

    def get_records(self, table_id, view_id=None, filter_by_formula=None, sort=None, max_records=None):
        table = self.get_table(table_id)
        try:
            params = {}
            if view_id:
                params['view'] = view_id
            if filter_by_formula:
                params['filter_by_formula'] = filter_by_formula
            if sort:
                params['sort'] = sort
            if max_records:
                params['max_records'] = max_records
            records = table.all(**params)
            return self._process_records(records)
        except Exception as e:
            print(f"Error fetching records from Airtable: {e}")
            return []

    def _process_records(self, records):
        return [{'id': record['id'], 'fields': record['fields']} for record in records]

    def get_record(self, table_id, record_id):
        table = self.get_table(table_id)
        try:
            record = table.get(record_id)
            return self._process_records([record])[0] if record else None
        except Exception as e:
            print(f"Error fetching record from Airtable: {e}")
            return None

    def update_record(self, table_id, record_id, fields):
        table = self.get_table(table_id)
        try:
            updated_record = table.update(record_id, fields)
            return self._process_records([updated_record])[0]
        except Exception as e:
            print(f"Error updating record in Airtable: {e}")
            return None
            
    def get_candidate_tweets(self):
        candidate_tweets = self.get_records(
            table_id=self.candidate_tweets_table_id,
            view_id=self.draft_tweets_view_id,
            sort=['id'],
            max_records=50
        )
        return candidate_tweets