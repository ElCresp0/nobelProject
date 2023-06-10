from io import StringIO
import contextlib
import unittest
import unittest.mock
import datetime
import requests
from App import App
from constants import *


class AppTest(unittest.TestCase):
    def setUp(self):
        """sets up all the variables needed to run tests"""

        self.now = datetime.datetime.now()
        # response404 is a simple examplary negative response
        self.response404 = requests.Response()
        self.response404.status_code = 404
        # init_response200 - the same response as in the App().__init__()
        self.init_response200 = requests.get(
            f"http://api.nobelprize.org/2.1/nobelPrizes?sort=asc&nobelPrizeYear={START_YEAR}&yearTo={self.now.strftime('%Y')}&nobelPrizeCategory={CATEGORY}&format={FORMAT}")
        # laureate_response200 - get a response for the first laureate from the init_response200
        self.laureate_response200 = requests.get(
            f"http://api.nobelprize.org/2.1/laureate/{list(self.init_response200.json().values())[DATA_INDEX][DATA_INDEX]['laureates'][DATA_INDEX]['id']}")
        self.tmp_out = StringIO()

    @unittest.mock.patch("App.requests.get", create=True)
    def test_app_get_response(self, mocked_requests_get):
        """The application calls exit(1) if it fails to fetch the data in the __init__()"""

        mocked_requests_get.side_effect = [Exception, self.response404]
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(self.tmp_out):
                app = App()

        with self.assertRaises(SystemExit):
            with contextlib.redirect_stdout(self.tmp_out):
                app = App()

    @unittest.mock.patch("App.requests.get", create=True)
    @unittest.mock.patch("App.input", create=True)
    def test_print_year(self, mocked_input, mocked_requests_get):
        """Print that fetching organizations from API failed, then succeed"""

        prizes = list(self.init_response200.json().values())[DATA_INDEX]
        prize = list(
            filter(lambda prize_element: prize_element["awardYear"] == f"{START_YEAR}", prizes))[DATA_INDEX]
        nb_of_laureatues = len(prize["laureates"])
        mocked_input.side_effect = [str(START_YEAR), "exit",
                                    str(START_YEAR), "exit"]
        mocked_requests_get.side_effect = [self.init_response200] \
                                          + [self.response404 for _ in range(nb_of_laureatues)] \
                                          + [self.init_response200] \
                                          + [self.laureate_response200 for _ in range(nb_of_laureatues)]

        self.tmp_out = StringIO()
        with contextlib.redirect_stdout(self.tmp_out):
            app = App()
        self.assertIn("[Couldn't fetch organization]", self.tmp_out.getvalue())

        self.tmp_out = StringIO()
        with contextlib.redirect_stdout(self.tmp_out):
            app = App()
        self.assertNotIn("[Couldn't fetch organization]", self.tmp_out.getvalue())


if __name__ == '__main__':
    unittest.main()
