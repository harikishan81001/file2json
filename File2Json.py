"""
Base class for conversion, which takes as input a csv file
and gives as output a list of dictionaries.
The dictionary will contain header, value pairs.
The output will be a list of one such dictionary per row.
"""
import csv
import json
import xlrd
from datasync.exceptions import InvalidFileFormat


class File2Json(object):
    """
    Take as input a csv/xls/xlsx file and output json data
    """
    def __init__(self, file_name, *args, **kwargs):
        super(File2Json,self).__init__(*args,**kwargs)
        self.file_name = file_name
        self.file_extn = file_name.split('.')[-1]
        if self.file_extn == 'csv':
            self.converter = self.csv_converter
        elif self.file_extn == 'xls':
            self.converter = self.xls_converter
        elif self.file_extn == 'xlsx':
            self.converter = self.xlsx_converter
        else:
            raise InvalidFileFormat("Invalid file format.")

    def csv_converter(self):
        """
        csv to json converter
        """
        try:
            f = open(self.file_name,'rb')
        except IOError:
            raise IOError("invalid file path, please check")
        reader = csv.reader(f)
        keys = reader.next()
        out_dict = [dict(zip(keys, line)) for line in reader]
#        json_data = json.dumps(out_dict)
        return out_dict

    def xls_converter(self):
        """
        xls to json converter
        """
        try:
            xls = xlrd.open_workbook(self.file_name)
        except IOError:
            raise IOError("invalid file path, please check")

        #Assuming that data is only in sheet 0,
        work_sheet = xls.sheet_by_index(0)
        num_rows = work_sheet.nrows - 1
        curr_row = 0
        header_cells = work_sheet.row(0)
        #header values of the sheet
        header = [each.value for each in header_cells]
        out_list = []
        while curr_row < num_rows:
             curr_row += 1
             row = [int(each.value)
                    if isinstance(each.value, float) 
                    else each.value 
                    for each in work_sheet.row(curr_row)]
             out_list.append(dict(zip(header,row)))
#        json_data = json.dumps(out_list)
        return out_list

    def xlsx_converter(self):
        """
        xlsx to json converter, currently no difference from xls converter
        """
        self.xls_converter()

    def convert(self):
        """
        Call the converter as per the file format
        """
        return self.converter()

