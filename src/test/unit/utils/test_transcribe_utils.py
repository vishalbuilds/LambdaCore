import unittest
from unittest.mock import patch, MagicMock
from strategies.utils.transcribe_utils import TranscribeUtils


class TestTranscribeUtils(unittest.TestCase):
    def setUp(self):
        patcher = patch('boto3.client')
        self.addCleanup(patcher.stop)
        self.mock_client = patcher.start()
        self.mock_transcribe = MagicMock()
        self.mock_client.return_value = self.mock_transcribe
        self.transcribe_utils = TranscribeUtils(region_name='us-east-1')

    def test_start_transcription_job(self):
        self.mock_transcribe.start_transcription_job.return_value = {'TranscriptionJob': {'TranscriptionJobStatus': 'IN_PROGRESS'}}
        result = self.transcribe_utils.start_transcription_job('job', 'uri', 'bucket')
        self.assertEqual(result, {'TranscriptionJob': {'TranscriptionJobStatus': 'IN_PROGRESS'}})
        self.mock_transcribe.start_transcription_job.assert_called_once()

    def test_get_transcription_job(self):
        self.mock_transcribe.get_transcription_job.return_value = {'TranscriptionJob': {'TranscriptionJobStatus': 'COMPLETED'}}
        result = self.transcribe_utils.get_transcription_job('job')
        self.assertEqual(result, {'TranscriptionJob': {'TranscriptionJobStatus': 'COMPLETED'}})
        self.mock_transcribe.get_transcription_job.assert_called_once_with(TranscriptionJobName='job')

    @patch('time.sleep', return_value=None)  # Patch sleep to speed up test
    def test_check_transcription_status(self, mock_sleep):
        self.mock_transcribe.get_transcription_job.side_effect = [
            {'TranscriptionJob': {'TranscriptionJobStatus': 'IN_PROGRESS'}},
            {'TranscriptionJob': {'TranscriptionJobStatus': 'COMPLETED'}}
        ]
        status = self.transcribe_utils.check_transcription_status('job')
        self.assertEqual(status, 'COMPLETED')
        self.assertEqual(self.mock_transcribe.get_transcription_job.call_count, 2)
        mock_sleep.assert_called_once_with(5)

    @patch('time.sleep', return_value=None)
    def test_check_transcription_status_failed(self, mock_sleep):
        self.mock_transcribe.get_transcription_job.side_effect = [
            {'TranscriptionJob': {'TranscriptionJobStatus': 'FAILED'}}
        ]
        status = self.transcribe_utils.check_transcription_status('job')
        self.assertEqual(status, 'FAILED')
        self.mock_transcribe.get_transcription_job.assert_called_once_with(TranscriptionJobName='job')
        mock_sleep.assert_not_called()

    @patch('time.sleep', return_value=None)
    def test_check_transcription_status_unknown(self, mock_sleep):
        self.mock_transcribe.get_transcription_job.side_effect = [
            {'TranscriptionJob': {'TranscriptionJobStatus': 'OTHER'}}
        ]
        status = self.transcribe_utils.check_transcription_status('job')
        self.assertEqual(status, 'UNKNOWN')
        self.mock_transcribe.get_transcription_job.assert_called_once_with(TranscriptionJobName='job')
        mock_sleep.assert_not_called()

    def test_check_transcription_status_exception(self):
        self.mock_transcribe.get_transcription_job.side_effect = Exception('fail')
        with self.assertRaises(Exception):
            self.transcribe_utils.check_transcription_status('job')
        self.mock_transcribe.get_transcription_job.assert_called_once_with(TranscriptionJobName='job')


if __name__ == '__main__':
    unittest.main()
