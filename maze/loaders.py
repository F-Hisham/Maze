import pandas as pd


class ExcelToIterablesMixin:
    
    @classmethod
    def load_from_excel(cls, file_path, sheet_name=None):
        
        if sheet_name:
            df = pd.read_excel(file_path, header=None, sheet_name=sheet_name)
        else:
            df = pd.read_excel(file_path, header=None)
        
        col_lists = [list(x.values()) for x in df.to_dict().values()]
        row_lists = list(zip(*col_lists))
        return row_lists
        
def main():
    
    excel_loader = ExcelToIterablesMixin()
    df = excel_loader.load_from_excel('mazes.xlsx')
    
if __name__ == '__main__':
    main()
