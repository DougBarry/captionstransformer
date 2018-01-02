

try:
    import unittest2 as unittest
except ImportError:
    import unittest
from StringIO import StringIO
from captionstransformer.tt import Reader, Writer
from captionstransformer import core
from datetime import timedelta

class TestTTReader(unittest.TestCase):
    def setUp(self):
        test_content = StringIO(u"""00:00:24:457 >> SILVER TV HISTORY, I GUESS,
00:00:27:560 IS GOING TO CONTINUE WITH OUR
00:00:30:597 SILVER OFFER THAT WE HAVE.
00:00:31:898 HERE AT CSN, WE STARTED
00:00:33:133 SOMETHING HERE ABOUT, YOU KNOW,
00:00:34:768 ACTUALLY, NOT THAT LONG AGO, TO
00:00:36:269 MAKE SILVER AVAILABLE TO
00:00:38:204 EVERYBODY AT THE BEST POSSIBLE
00:00:40:774 PRICE, WHETHER YOU BUY 1 OUNCE,
00:00:42:142 5 OUNCES, 10 OUNCES, 100 OUNCES,
00:00:43:777 1,000 OUNCES -- IT DOESN'T
00:00:45:078 MATTER.
00:00:45:578 SILVER IS KIND OF NEAR 5-YEAR,
00:00:48:081 ALMOST 10-YEAR LOWS, AND PEOPLE
00:00:50:517 HAVE BEEN TAKING ADVANTAGE OF IT
00:00:52:385 IN AN ABSOLUTELY MONSTROUS WAY.
00:00:54:854 LITERALLY THOUSANDS AND
""")
        self.reader = Reader(test_content)
        
    def test_read(self):
        captions = self.reader.read()
        self.assertTrue(captions is not None)
        self.assertEqual(len(captions), 17)
        first = captions[0]
        last = captions[-1]
        self.assertEqual(type(first.text), unicode)
        self.assertEqual(first.text, u">> SILVER TV HISTORY, I GUESS,")
        self.assertEqual(first.start, core.get_date(second=24, millisecond=457))
        self.assertEqual(first.end, core.get_date(second=27, millisecond=560))
        self.assertEqual(first.duration, timedelta(seconds=3, milliseconds=103))
        self.assertEqual(type(last.text), unicode)
        self.assertEqual(last.text, u"LITERALLY THOUSANDS AND")
        self.assertEqual(last.start, core.get_date(second=54, millisecond=854))
        self.assertEqual(last.end, core.get_date(second=54, millisecond=854))
        self.assertEqual(last.duration, timedelta(seconds=0, milliseconds=0))
        
class TestTTWriter(unittest.TestCase):
    def setUp(self):
        test_content = StringIO(u"""00:00:24:457 >> SILVER TV HISTORY, I GUESS,
00:00:27:560 IS GOING TO CONTINUE WITH OUR
00:00:30:597 SILVER OFFER THAT WE HAVE.
00:00:31:898 HERE AT CSN, WE STARTED
00:00:33:133 SOMETHING HERE ABOUT, YOU KNOW,
00:00:34:768 ACTUALLY, NOT THAT LONG AGO, TO
00:00:36:269 MAKE SILVER AVAILABLE TO
00:00:38:204 EVERYBODY AT THE BEST POSSIBLE
00:00:40:774 PRICE, WHETHER YOU BUY 1 OUNCE,
00:00:42:142 5 OUNCES, 10 OUNCES, 100 OUNCES,
00:00:43:777 1,000 OUNCES -- IT DOESN'T
00:00:45:078 MATTER.
00:00:45:578 SILVER IS KIND OF NEAR 5-YEAR,
00:00:48:081 ALMOST 10-YEAR LOWS, AND PEOPLE
00:00:50:517 HAVE BEEN TAKING ADVANTAGE OF IT
00:00:52:385 IN AN ABSOLUTELY MONSTROUS WAY.
00:00:54:854 LITERALLY THOUSANDS AND
""")
        self.reader = Reader(test_content)
        self.writer = Writer(StringIO())
         
    def test_transformtext(self):
        captions = self.reader.read()
        self.writer.captions = captions
        text = self.writer.captions_to_text()
        
        should_be = u"""00:00:24:457 >> SILVER TV HISTORY, I GUESS,"""
        self.assertTrue(text.startswith(should_be),
                        "%s !startswith %s" % (text, should_be))
        

if __name__ == '__main__':
    unittest.main()