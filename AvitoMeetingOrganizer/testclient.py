import unittest
from client import AvitoMeetingsClient

class Tester(unittest.TestCase):
    def setUp(self):
        self.client = AvitoMeetingsClient()
        self.maxDiff = None

    #Testing one scenario
    def test_scenario(self):
        self.client.start()
        self.assertEqual(self.client.create_meeting('4000', '4000-01-01', '00:00'), '\nSuccessfully created!')
        self.assertEqual(self.client.add_participant('aaa', 'aaaovich', 'aa@aa.ru', '4000'), '\nSuccessfully created!')
        self.assertEqual(self.client.add_participant('bbb', 'bbbovich', 'bb@bb.ru', '4000'), '\nSuccessfully created!')
        self.assertEqual(self.client.add_participant('ccc', 'cccovich', 'asfasfasfv', '4000'), '\nSuccessfully created!')
        self.assertEqual(self.client.show_all_meetings(),"""Meeting bbb on 1900-01-01 at 00:00:00 is going to be attended by:
Name: Dima Dimovich email: d@d.ru
Name: Viktor Viktorovich email: v@v.ru
Meeting ccc on 1950-06-15 at 12:00:00 is going to be attended by:
Actually, no one is going to attend meeting ccc
Meeting aaa on 1999-02-10 at 10:00:00 is going to be attended by:
Name: Fedor Fedorovich email: f@f.ru
Name: Boris Borisovich email: b@b.ru
Name: Michail Michailovich email: m@m.ru
Name: Ivan Ivanovich email: i@i.ru
Meeting 4000 on 4000-01-01 at 00:00:00 is going to be attended by:
Name: aaa aaaovich email: aa@aa.ru
Name: bbb bbbovich email: bb@bb.ru
Name: ccc cccovich email: none
""")
        self.assertEqual(self.client.delete_participant('bbb', 'bbbovich', '4000'),
                         "\nSuccessfully deleted or that person wasn't attending this meeting in the first place")
        self.assertEqual(self.client.show_all_meetings(), """Meeting bbb on 1900-01-01 at 00:00:00 is going to be attended by:
Name: Dima Dimovich email: d@d.ru
Name: Viktor Viktorovich email: v@v.ru
Meeting ccc on 1950-06-15 at 12:00:00 is going to be attended by:
Actually, no one is going to attend meeting ccc
Meeting aaa on 1999-02-10 at 10:00:00 is going to be attended by:
Name: Fedor Fedorovich email: f@f.ru
Name: Boris Borisovich email: b@b.ru
Name: Michail Michailovich email: m@m.ru
Name: Ivan Ivanovich email: i@i.ru
Meeting 4000 on 4000-01-01 at 00:00:00 is going to be attended by:
Name: aaa aaaovich email: aa@aa.ru
Name: ccc cccovich email: none
""")
        self.assertEqual(self.client.delete_meeting('4000'), "\nSuccessfully deleted"
                                                             " or there wasn't 4000 in the first place")
        self.assertEqual(self.client.show_all_meetings(), """Meeting bbb on 1900-01-01 at 00:00:00 is going to be attended by:
Name: Dima Dimovich email: d@d.ru
Name: Viktor Viktorovich email: v@v.ru
Meeting ccc on 1950-06-15 at 12:00:00 is going to be attended by:
Actually, no one is going to attend meeting ccc
Meeting aaa on 1999-02-10 at 10:00:00 is going to be attended by:
Name: Fedor Fedorovich email: f@f.ru
Name: Boris Borisovich email: b@b.ru
Name: Michail Michailovich email: m@m.ru
Name: Ivan Ivanovich email: i@i.ru
""")

    #Testing normal work
    #def test_run(self):
    #    self.client.run()

if __name__ == "__main__":
    unittest.main()