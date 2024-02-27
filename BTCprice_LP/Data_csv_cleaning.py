import pandas as pd
import os

file_name=os.listdir('/Users/andyma/Desktop/Projects/Roger/LP_data')

print(file_name)
# initiate the loop by setting up an empty dataframe with column names
data_first=pd.read_csv('/Users/andyma/Desktop/Projects/Roger/LP_data/'+file_name[0])
column_name=list(data_first.columns.values)
NFT_data_aggregated= pd.DataFrame(columns=column_name)
# loop through the csv list
file_name.remove('.DS_Store')
i=1
for f in file_name:
    print('processing no.'+str(i)+' out of '+str(len(file_name)))
    data_f=pd.read_csv('/Users/andyma/Desktop/Projects/Roger/LP_data/'+f)
    NFT_data_aggregated = pd.concat([NFT_data_aggregated, data_f])
    i+=1
    pass

NFT_data_aggregated.to_csv('LP_transactions.csv')