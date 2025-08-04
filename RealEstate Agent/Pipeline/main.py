from CsvToMongodb import InsertData
from PipelineTogetDataCitySpecfic import RunPipeline
from cleaning import CleanCsv
def StartPipeline():

    try:
        page = 1
        city = str(input("Enter city or address")).lower()
        if not city:
            city = 'new york'
        RunPipeline(city,page)
        CleanCsv(f'data/{city}_PropertyDataComplete{page}.csv')
        # CleanCsv('charlotte NC_PropertyDataComplete.csv')
        InsertData(city,page)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    StartPipeline()