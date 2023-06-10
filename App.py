# https://app.swaggerhub.com/apis/NobelMedia/NobelMasterData/2.1
import datetime
import requests
import re
from constants import *


class App:
    def __init__(self):
        """the costructor - downloads the data into self.prizes (or exits) and enters the application loop"""
        response = self.get_response(
            f"http://api.nobelprize.org/2.1/nobelPrizes?sort=asc&nobelPrizeYear={START_YEAR}&yearTo={datetime.datetime.now().strftime('%Y')}&nobelPrizeCategory={CATEGORY}&format={FORMAT}")
        if response.status_code != STATUS_CODE_CORRECT:
            exit(1)

        self.prizes = list(response.json().values())[DATA_INDEX]
        self.run()

    def get_response(self, href):
        """gets a response using requests.get() and checks the status code"""
        response = requests.Response()
        # try-except construction in case there is no internet connection
        try:
            response = requests.get(href)
        except:
            print(PRINT_RED.format("[Error] Please, check your internet connection"))
            return requests.Response()
        
        status_code = response.status_code
        if status_code != STATUS_CODE_CORRECT:
            codes = {400: "BadRequest",
                     422: "UnprocessableEntity", 404: "NotFound"}
            print(PRINT_RED.format(
                f"[API error {status_code}: {codes.get(status_code) if codes.get(status_code) else 'UnknownStatusCode'}], data cannot be fetched."))
            # exit(1)
        return response

    def controlled_input(self, regex, error_message):
        """enters a loop untill the user provides an input matching the regular expression (regex)"""
        n = input()
        while not re.match(regex, n):
            if n.lower() == "exit":
                return n
            print(PRINT_RED.format(error_message))
            n = input()
        return n

    def print_year(self, year):
        """Prints names of laureates, year of the prize and organizations they belonged to when they won the prize"""
        prize = list(
            filter(lambda prize_element: prize_element["awardYear"] == year, self.prizes))
        if not prize:
            print(PRINT_RED.format(
                f"There are no laureates for given year ({year})."))
            return
        else:
            prize = prize[DATA_INDEX]

        for laureate in prize["laureates"]:
            id = laureate["id"]
            # the organizations are fetched from the API for each candidate on the go
            laurate_response = self.get_response(
                f"http://api.nobelprize.org/2.1/laureate/{id}")
            organization = "[Couldn't fetch organization]"
            if laurate_response.status_code == STATUS_CODE_CORRECT:
                filtered_prize = list(filter(
                    lambda element: element["awardYear"] == year and element["category"]["en"] == CATEGORY_IN_JSON, laurate_response.json()[DATA_INDEX]["nobelPrizes"]))
                if filtered_prize:
                    affiliations = filtered_prize[DATA_INDEX]["affiliations"]
                    organization = "\nOrganizations:\n"
                    for affiliation in affiliations:
                        organization += f"\t- {affiliation['name']['en']}\n"

            print("***\n"
                  + laureate["fullName"]["en"] + " | "
                  + year + " | "
                  + organization)

    def run(self):
        """the main loop of the application - asks user for a year or to exit"""
        while True:
            print("Please enter a year above 2000 (or exit)")
            user_input = self.controlled_input(
                "^2[0-9]{3}$", "The input is incorrect: please follow the YYYY year format.")
            if user_input == "exit":
                print("Closing the app.")
                return
            self.print_year(user_input)


if __name__ == "__main__":
    app = App()
