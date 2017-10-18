from unittest import TestCase
try:
    from unittest.mock import MagicMock, patch
except ImportError as err:
    from mock import MagicMock, patch

import duco.ducobox as dut


class TestDucoValveCO2Sensor(TestCase):

    @patch('duco.ducobox.DucoInterface', autospec=True)
    def test_happy(self, itf_mock):
        sensor = dut.DucoValveCO2Sensor(1, 2)
        itf_mock_object = MagicMock(spec=dut.DucoInterface)
        sensor.bind(itf_mock_object)

        with open('tests/cmd_paraget_co2.txt') as cmdfile:
            itf_mock_object.execute_command.return_value = cmdfile.read()
        sensor.sample()
        itf_mock_object.execute_command.assert_called_once_with('nodeparaget 1 74')

        self.assertEqual(float(sensor.value), 512)

    @patch('duco.ducobox.DucoInterface', autospec=True)
    def test_no_values(self, itf_mock):
        sensor = dut.DucoValveCO2Sensor(1, 2)
        itf_mock_object = MagicMock(spec=dut.DucoInterface)
        sensor.bind(itf_mock_object)

        itf_mock_object.execute_command.return_value = 'invalid command'
        sensor.sample()
        itf_mock_object.execute_command.assert_called_once_with('nodeparaget 1 74')

        self.assertEqual(sensor.value, None)
