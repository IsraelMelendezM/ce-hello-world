import unittest
from unittest.mock import patch
from io import StringIO
from datetime import datetime

import sys
sys.path.append('../')

from cronJob_paymentReminder import as_spanish, twilio_reminder

class TestAsSpanish(unittest.TestCase):
    def test_as_spanish(self):
        test_date = datetime(2023, 10, 21)
        expected_result = "Sábado, 21 de Octubre de 2023"
        self.assertEqual(as_spanish(test_date), expected_result)

class TestTwilioReminder(unittest.TestCase):
    @patch('twilio.rest.Client.messages.create')
    def test_twilio_reminder_success(self, mock_twilio_messages_create):
        client_data = {
            "should_pay_by": "2023-10-21",
            "toPayAfterDiscount": 100,
            "name": "John Doe",
            "phone_number": "8180202938"
        }
        expected_msg = "¡Hola John! Como recordatorio debes una cantidad de: $100 MXN para el día Sábado, 21 de Octubre de 2023.\n    ¿Te redirijo a la app para pagar de una vez?"
        expected_to_number = "+528180202938"
        expected_from_number = "whatsapp:+1234567890"

        twilio_reminder(client_data)

        mock_twilio_messages_create.assert_called_once_with(to=expected_to_number, from_=expected_from_number, body=expected_msg)

    @patch('twilio.rest.Client.messages.create', side_effect=Exception("Twilio Error"))
    def test_twilio_reminder_failure(self, mock_twilio_messages_create):
        client_data = {
            "should_pay_by": "2023-10-21",
            "toPayAfterDiscount": 100,
            "name": "John Doe",
            "phone_number": "1234567890"
        }
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            twilio_reminder(client_data)
            self.assertEqual(mock_stdout.getvalue().strip(), 'Could not send whatsapp notification to 1234567890\nCould not send whatsapp TwilioException Twilio Error')

if __name__ == '__main__':
    unittest.main()
