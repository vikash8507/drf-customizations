from django.conf import settings
from rest_framework.parsers import BaseParser

class CSVTextParser(BaseParser):

    media_type = "text/csv"

    def parse(self, stream, media_type=None, parser_context=None):

        parser_context = parser_context or {}
        delimiter = parser_context.get('delimiter', ',')
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        
        requested_data = stream.read()
        streamed_data = requested_data.splitlines()
        rows = self.csv_rows(data=streamed_data, delimiter=delimiter, encoding=encoding)

        return self.convert_to_dictionary(rows)

    def csv_rows(self, data, delimiter=',', encoding='utf-8'):
        rows = []
        for row in data:
            row_data = row.decode(encoding).split(delimiter)
            if row_data:
                rows.append(row_data)
        return rows
    
    def convert_to_dictionary(self, rows):
        keys, keys_len = rows[0], len(rows[0])
        response = []
        for row in rows[1:]:
            res = {}
            for i in range(keys_len):
                try:
                    res[keys[i]] = {'value': row[i]}
                    response.append(res)
                except Exception as e:
                    print(e)
        return response
