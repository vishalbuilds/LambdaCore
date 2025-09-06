import unittest
from unittest.mock import patch, MagicMock
from strategies.utils.s3_utils import S3Utils


class TestS3Utils(unittest.TestCase):
    def setUp(self):
        patcher = patch('boto3.client')
        self.addCleanup(patcher.stop)
        self.mock_client = patcher.start()
        self.mock_s3 = MagicMock()
        self.mock_client.return_value = self.mock_s3
        self.s3_utils = S3Utils(region_name='us-east-1')

    def test_get_object(self):
        self.mock_s3.get_object.return_value = {'Body': b'data'}
        result = self.s3_utils.get_object('bucket', 'key')
        self.assertEqual(result, {'Body': b'data'})
        self.mock_s3.get_object.assert_called_once_with(Bucket='bucket', Key='key')

    def test_put_object(self):
        self.mock_s3.put_object.return_value = {'ResponseMetadata': {'HTTPStatusCode': 200}}
        result = self.s3_utils.put_object('bucket', 'key', b'data')
        self.assertEqual(result, {'ResponseMetadata': {'HTTPStatusCode': 200}})
        self.mock_s3.put_object.assert_called_once_with(Bucket='bucket', Key='key', Body=b'data')

    def test_delete_object(self):
        self.mock_s3.delete_object.return_value = {'ResponseMetadata': {'HTTPStatusCode': 204}}
        result = self.s3_utils.delete_object('bucket', 'key')
        self.assertEqual(result, {'ResponseMetadata': {'HTTPStatusCode': 204}})
        self.mock_s3.delete_object.assert_called_once_with(Bucket='bucket', Key='key')

    def test_list_objects(self):
        self.mock_s3.list_objects_v2.return_value = {'Contents': []}
        result = self.s3_utils.list_objects('bucket')
        self.assertEqual(result, {'Contents': []})
        self.mock_s3.list_objects_v2.assert_called_once_with(Bucket='bucket')

    def test_list_objects_with_prefix(self):
        self.mock_s3.list_objects_v2.return_value = {'Contents': []}
        prefix = 'folder/subfolder/'
        result = self.s3_utils.list_objects('bucket', prefix)
        self.assertEqual(result, {'Contents': []})
        self.mock_s3.list_objects_v2.assert_called_once_with(Bucket='bucket', Prefix=prefix)

    def test_get_object_exception(self):
        self.mock_s3.get_object.side_effect = Exception('fail')
        with self.assertRaises(Exception):
            self.s3_utils.get_object('bucket', 'key')
        self.mock_s3.get_object.assert_called_once_with(Bucket='bucket', Key='key')


if __name__ == '__main__':
    unittest.main()
