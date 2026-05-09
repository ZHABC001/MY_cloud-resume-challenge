"""Lambda 関数の単体テスト"""
import json
import pytest


class TestLambdaHandler:
    """訪問者カウンター Lambda のテスト"""

    def test_first_visit_returns_count_1(self, dynamodb_table):
        """初回アクセスで count が 1 になることを確認"""
        from lambda_function import lambda_handler

        response = lambda_handler({}, None)

        assert response['statusCode'] == 200

        body = json.loads(response['body'])
        assert body['count'] == 1

    def test_multiple_visits_increment_count(self, dynamodb_table):
        """複数回アクセスで count が正しくインクリメントされる"""
        from lambda_function import lambda_handler

        for expected_count in [1, 2, 3]:
            response = lambda_handler({}, None)
            body = json.loads(response['body'])
            assert body['count'] == expected_count, \
                f"Expected count={expected_count}, got {body['count']}"

    def test_response_has_cors_headers(self, dynamodb_table):
        """レスポンスに CORS ヘッダーが含まれる"""
        from lambda_function import lambda_handler

        response = lambda_handler({}, None)

        assert 'Access-Control-Allow-Origin' in response['headers']
        assert response['headers']['Access-Control-Allow-Origin'] == '*'

        assert 'Access-Control-Allow-Methods' in response['headers']
        assert 'GET' in response['headers']['Access-Control-Allow-Methods']

    def test_response_content_type_is_json(self, dynamodb_table):
        """レスポンスの Content-Type が JSON"""
        from lambda_function import lambda_handler

        response = lambda_handler({}, None)

        assert response['headers']['Content-Type'] == 'application/json'

    def test_count_is_integer_not_decimal(self, dynamodb_table):
        """count が int 型で返される (Decimal ではない)"""
        from lambda_function import lambda_handler

        response = lambda_handler({}, None)
        body = json.loads(response['body'])

        assert isinstance(body['count'], int)