import boto3
from boto3.dynamodb.conditions import Key, Attr
from multiprocessing import Pool

dynamodb = boto3.resource('dynamodb',region_name="Your Region",aws_access_key_id="Change Here",aws_secret_access_key= "Change Here")
table = dynamodb.Table('Your Table Name')

pe = "Make Your ProjectionExpression"
fe = "Make Your FilterExpression"

def read_data(segment):
    response = table.scan(
        ProjectionExpression=pe,
        FilterExpression=fe,
        Segment=segment,
        TotalSegments=10,
        )
    
    print(response["Items"])s

    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ProjectionExpression=pe,
            FilterExpression=fe,
            ExclusiveStartKey=response['LastEvaluatedKey'],
            Segment=segment,
            TotalSegments=10,
            )
        print(response["Items"])
        


p = Pool(processes=10)
segments = range(1,10)
result = p.map(read_data, segments)
