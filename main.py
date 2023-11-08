from DataBase import DataBase
import openpyxl


# Функция для обработки файла Excel
def process_xlsx(file_name, db):
    wb = openpyxl.load_workbook(file_name)
    sheet = wb.active
    rows = sheet.iter_rows(values_only=True, max_col=6)
    next(rows)
    for row in rows:
        id_tovar, name_tovar, id_isg, isg, country, barcod = row
        db.insert_country(country)
        db.insert_isg(id_isg, isg)
        db.insert_good(name_tovar, barcod, country, id_isg)

# Функция для подсчета количества товаров по странам и записи в TSV файл
def count_goods_by_country(db, tsv_file):
    result = {}
    for row in db.cur.execute('SELECT NAME_COUNTRY, COUNT(*) '
                              'FROM GOODS '
                              'INNER JOIN COUNTRY ON GOODS.ID_COUNTRY = COUNTRY.ID_COUNTRY '
                              'GROUP BY NAME_COUNTRY'):
        country, count = row
        result.setdefault(country, count)


    with open(tsv_file, 'w') as f:
        for country, count in result.items():
            f.write(f"{country}\t{count}\n")

if __name__ == '__main__':
    db = DataBase('base.sqlite')
    # db.create_tables()
    # process_xlsx('data.xlsx', db)
    count_goods_by_country(db, 'data.tsv')
    db.close()

