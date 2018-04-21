from FinalProj import *
import unittest
import requests
import json

class TestBillboard(unittest.TestCase):
    def setup(self):
        self.test_chart = get_billboard()
        self.output_chart = print(str(counter) + '. ' + ''.join(billboard_dict[counter]))
    def test_chart_size(self):
        self.assertEqual(len(self.test_chart.keys()), 100)
        self.assertEqual(self.test_chart[1][0], 'Drake')
        self.assertEqual(self.test_chart[1][4], '--')
        self.assertEqual(self.test_chart[100][0], 'Alone')
        self.assertIsInstance(self.test_chart[1], list)

class TestClass(unittest.TestCase):
    def setup(self):
        obj_billboard = get_billboard()
        counter = 1
        self.obj_list = []
        for x in obj_billboard.keys():
            counter = BillboardArtistData(obj_billboard[x][0], obj_billboard[x][1], x, obj_billboard[x][2], obj_billboard[x][3], obj_billboard[x][4])
            self.obj_list.append(counter)
            counter += 1

    def test_objects(self):
        self.assertIsInstance(print(self.obj_list[0]), str)
        self.assertEqual(print(self.obj_list[0]), "Nice For What by Drake is currently charting at number 1. Throughout its 1 week(s) charting, its top position was 1, and its last position was --.")
        self.assertEqual(print(self.obj_list[65]), "Changes by XXXTENTACION is currently charting at number 66. Throughout its 6 week(s) charting, its top position was 37, and its last position was 58.")
        self.assertIsInstance(self.obj_list[0], BillboardArtistData)

class TestSpotifyFunctions(unittest.TestCase):

    def setup(self):
        self.test_list = get_top_tracks('Migos')
        self.another_list = get_top_tracks('The Beatles')
        self.compare_list = chart_compare('Migos')

    def test_top_tracks(self):
        self.assertEqual(self.test_list[0], 'Walk It Talk It')
        self.assertIsInstance(self.compare_list, str)
        self.assertEqual(self.another_list[9], 'In My Life - Remastered')


class TestSpotify(unittest.TestCase):
    def setup(self):
        f = open(MUSICJSON, 'r')
        fcontents = f.read()
        self.music_data = json.loads(fcontents)

    def test_extra_stats(self):
        self.assertEqual(self.music_data[0]['artists']['items'][0]['popularity'], '88')
        self.assertIsInstance(self.music_data, dict)
        self.assertEqual(self.music_data[x]['artists']['items'][0]['followers']['total'], '2559212')




if __name__ == '__main__':
    unittest.main()
