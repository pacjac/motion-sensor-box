import unittest 

import os

from msb_serial.SerialReader import SerialReader

class TestSerialConfig(unittest.TestCase):
    def test_correct_env(self):
        env_varname = "MSB_CONFIG_DIR"
        self.assertIn(env_varname, os.environ)

class TestSerialReader(unittest.TestCase):
    def test_can_import(self):
        self.reader = SerialReader()
        self.assertEqual(self.reader.extractFloats(b""), [])

# class TestExtractFloats(unittest.TestCase):
#     def setUp(self):
#         self.reader = SerialReader()

#     def test_empty_string(self):
#         self.assertEqual(self.reader.extractFloats(b""), [])

#     def test_wrong_byte_flag(self):
#         with self.assertRaises(TypeError):
#             self.reader.extractFloats("someNonbinaryString", isBytes=True)

#     def test_detects_simple_float_from_bytestring(self):
#         message = b"somestuff19.3"
#         self.assertListEqual(self.reader.extractFloats(message), [19.3])

#     def test_detects_multiple_floats_from_bytestring(self):
#         testfloats = [3.4, 9.5]
#         message = (f"somestuff{testfloats[0]}lallaa{testfloats[1]}").encode("utf-8")
#         self.assertListEqual(self.reader.extractFloats(message), testfloats)

#     def test_detects_multiple_floats_from_string(self):
#         testfloats = [3.4, 9.5]
#         message = f"somestuff{testfloats[0]}lallaa{testfloats[1]}"
#         self.assertListEqual(
#             self.reader.extractFloats(message, isBytes=False), testfloats
#         )

#     def test_correct_sign(self):
#         testfloat = -1.9
#         message = (f"somestuff  {testfloat}").encode("utf-8")
#         self.assertEqual(self.reader.extractFloats(message)[0], testfloat) 

#     # def test_detects_integer(self):
#     #    testintegers = [4, 8]
#     #    message= f'somestuff{testintegers[0]}lallaa{testintegers[1]}'
#     #    self.assertListEqual(self.reader.extractFloats(message, isBytes=False), testintegers)


# class TestExtractRe(unittest.TestCase):
#     def no_test_returns_correct_string(self):
#         front = "somestring09%3Pitch"
#         target = "18.3kWh  9.2m/s"
#         back = "%kjlsiu9$Q"
#         message = front + target + back
#         self.assertEqual(self.reader.extract_re(message), target)


if __name__ == "__main__":
    unittest.main()
