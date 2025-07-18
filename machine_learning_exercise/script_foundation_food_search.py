


import foodDataParser as fdPar
import pprint

# Create the parser object.
parser = fdPar.foodDataParser()


keyword = 'grape'

# Find foundation foods containing the target keyword.
foundFood_df = parser.findFoundFood(keyword)
sub_foundFood_df = foundFood_df[['fdc_id','description']]


fdc_id_list = foundFood_df['fdc_id'].tolist()
desc_list = foundFood_df['description'].tolist()
tmp = dict(zip(fdc_id_list, zip(desc_list)))
pprint.pprint(tmp)




