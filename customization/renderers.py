from rest_framework.renderers import BaseRenderer
from django.utils.encoding import smart_text
from six import BytesIO, text_type
from django.conf import settings
import unicodecsv as csv


class CSVTextRenderer(BaseRenderer):
    """
    Renderer which serializes to CSV
    """

    media_type = 'text/csv'
    format = 'csv'
    level_sep = '.'
    header = None
    labels = None  # {'<field>':'<label>'}
    writer_opts = None

    def render(self, data, media_type=None, renderer_context={}, writer_opts=None):
        """
        Renders serialized *data* into CSV. For a dictionary:
        """
        if data is None:
            return ''

        if not isinstance(data, list):
            data = [data]

        writer_opts = renderer_context.get('writer_opts', writer_opts or self.writer_opts or {})
        header = renderer_context.get('header', self.header)
        labels = renderer_context.get('labels', self.labels)
        encoding = renderer_context.get('encoding', settings.DEFAULT_CHARSET)

        table = self.tablize(data, header=header, labels=labels)
        csv_buffer = BytesIO()
        csv_writer = csv.writer(csv_buffer, encoding=encoding, **writer_opts)
        for row in table:
            csv_writer.writerow(row)

        return csv_buffer.getvalue()

    def tablize(self, data, header=None, labels=None):

        if not header and hasattr(data, 'header'):
            header = data.header

        if data:

            data = self.flatten_data(data)

            if not header:
                data = tuple(data)
                header_fields = set()
                for item in data:
                    header_fields.update(list(item.keys()))
                header = sorted(header_fields)

            if labels:
                yield [labels.get(x, x) for x in header]
            else:
                yield header

            for item in data:
                row = [item.get(key, None) for key in header]
                yield row

        elif header:
            if labels:
                yield [labels.get(x, x) for x in header]
            else:
                yield header

        else:
            pass

    def flatten_data(self, data):
        for item in data:
            flat_item = self.flatten_item(item)
            yield flat_item

    def flatten_item(self, item):
        if isinstance(item, list):
            flat_item = self.flatten_list(item)
        elif isinstance(item, dict):
            flat_item = self.flatten_dict(item)
        else:
            flat_item = {'': item}

        return flat_item

    def nest_flat_item(self, flat_item, prefix):

        nested_item = {}
        for header, val in flat_item.items():
            nested_header = self.level_sep.join([prefix, header]) if header else prefix
            nested_item[nested_header] = val
        return nested_item

    def flatten_list(self, l):
        flat_list = {}
        for index, item in enumerate(l):
            index = text_type(index)
            flat_item = self.flatten_item(item)
            nested_item = self.nest_flat_item(flat_item, index)
            flat_list.update(nested_item)
        return flat_list

    def flatten_dict(self, d):
        flat_dict = {}
        for key, item in d.items():
            key = text_type(key)
            flat_item = self.flatten_item(item)
            nested_item = self.nest_flat_item(flat_item, key)
            flat_dict.update(nested_item)
        return flat_dict
