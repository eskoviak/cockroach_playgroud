"""test.py

"""
import sys
sys.path.append('../s3utils')
from budget import Budget
from s3_object import S3_object
from dotenv import dotenv_values

s3_object = S3_object()
config = dotenv_values(".env")
bytes_written = s3_object.upload_s3('./data/Budget Input.csv', config['S3_BUCKET'], key_prefix=config['DATA_SETS'])
print(f"{bytes_written} bytes uploaded to S3")

budget = Budget()

print(budget.add_expense((budget.bulk_load_s3('Data Sets/Budget Input.csv'))))


print(budget._archive_s3('Budget Input.csv'))

##s3://elasticbeanstalk-us-west-2-502865036487/Data Sets/Budget Input.csv
#https://elasticbeanstalk-us-west-2-502865036487.s3.us-west-2.amazonaws.com/Data+Sets/Budget+Input.csv