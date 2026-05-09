import json
import boto3
from botocore.exceptions import ClientError

# DynamoDB クライアント初期化
dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
table = dynamodb.Table('cloud-resume-counter')


def lambda_handler(event, context):
    """訪問者カウンターを更新し、最新のカウントを返す"""
    try:
        response = table.update_item(
            Key={'id': 'visitor_count'},
            UpdateExpression='ADD #count :inc',
            ExpressionAttributeNames={'#count': 'count'},
            ExpressionAttributeValues={':inc': 1},
            ReturnValues='UPDATED_NEW'
        )

        new_count = int(response['Attributes']['count'])

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'count': new_count
            })
        }

    except ClientError as e:
        print(f"DynamoDB error: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': 'Database operation failed'
            })
        }

    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': 'Internal server error'
            })
        }