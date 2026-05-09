"""pytest 共通設定 + フィクスチャー"""
import os
import sys
import pytest
import boto3
from moto import mock_aws

# Lambda 関数を import できるようにパス追加
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambda'))


@pytest.fixture
def aws_credentials():
    """テスト用の偽の AWS 認証情報を設定"""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'ap-northeast-1'


@pytest.fixture
def dynamodb_table(aws_credentials):
    """モックされた DynamoDB テーブルを準備"""
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')

        table = dynamodb.create_table(
            TableName='cloud-resume-counter',
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )

        table.put_item(Item={
            'id': 'visitor_count',
            'count': 0
        })

        yield table