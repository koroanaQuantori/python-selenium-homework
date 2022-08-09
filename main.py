import unittest

from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager

from Locators import Locator

VOWELS = ["у", "е", "а", "о", "э", "я", "и", "ю", "ы", "ё"]
SPACE = [" "]
SYMBOLS = ["!", ".", ",", ":", "-", "?"]

CUSTOM_TEXT = "Случайный текст с пробелами и символами!?"


class TestSuite(unittest.TestCase):
    """
        Test Suite to validate input parsing for VOWELS, SPACE and SYMBOLS
    """

    def tearDown(self):
        self.chrome_driver.quit()

    def setUp(self):
        self.chrome_driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )
        self.chrome_driver.get("https://rioran.github.io/ru_vowels_filter/main.html")
        self.chrome_driver.maximize_window()
        WebDriverWait(self.chrome_driver, 5) \
            .until(expected_conditions
                   .presence_of_element_located((By.XPATH, "//label[@for='text_input']")))

        self.button_clean_vowels = self.chrome_driver \
            .find_element(By.XPATH, Locator.button_vowels)
        self.button_clean_vowels_and_spaces = self.chrome_driver \
            .find_element(By.XPATH, Locator.button_vowels_and_space)
        self.button_clean_vowels_spaces_and_symbols = self.chrome_driver.find_element(
            By.XPATH, Locator.button_vowels_space_and_symbol)
        self.button_select_all = self.chrome_driver \
            .find_element(By.XPATH, Locator.button_select_all)
        self.output_text_element = self.chrome_driver.find_element(By.ID, Locator.text_output)
        self.input_text_element = self.chrome_driver.find_element(By.NAME, Locator.text_input)

    def test_validate_vowels_logic(self):
        """ GIVEN I click on 'Оставить только гласные' button
            THEN output text has vowels only
        """
        pattern = set(VOWELS)
        self.button_clean_vowels.click()
        output_text = self.output_text_element.text.replace('\n', "")
        assert set(output_text.lower()).issubset(pattern)

    def test_validate_vowels_and_spaces_logic(self):
        """ GIVEN I click on 'Hу и ещё пробелы' button
            THEN output text has vowels and spaces only
        """
        pattern = set(VOWELS + SPACE)
        self.button_clean_vowels_and_spaces.click()
        output_text = self.output_text_element.text.replace('\n', "")
        assert set(output_text.lower()).issubset(pattern)

    def test_validate_vowels_symbols_and_spaces_logic(self):
        """ GIVEN I click on 'Оставить ещё и .,-!?' button
            THEN output text has vowels, spaces and symbols only
        """
        pattern = set(VOWELS + SPACE + SYMBOLS)
        self.button_clean_vowels_spaces_and_symbols.click()
        output_text = self.output_text_element.text.replace('\n', "")
        assert set(output_text.lower()).issubset(pattern)

    def test_validate_custom_input(self):
        """ GIVEN I added custom text to input field
            AND I click on 'Оставить ещё и .,-!?' button
            THEN output text has vowels, spaces and symbols only
        """
        pattern = set(VOWELS + SPACE + SYMBOLS)
        self.input_text_element.send_keys(Keys.CONTROL + "a")
        self.input_text_element.send_keys(Keys.DELETE)
        self.input_text_element.send_keys(CUSTOM_TEXT)
        self.button_clean_vowels_spaces_and_symbols.click()
        output_text = self.output_text_element.text.replace('\n', "")
        assert set(output_text.lower()).issubset(pattern)

    def test_validate_empty_input(self):
        """ GIVEN I clean up input field
            AND I click on 'Оставить ещё и .,-!?' button
            THEN output text is empty
        """
        self.input_text_element.send_keys(Keys.CONTROL + "a")
        self.input_text_element.send_keys(Keys.DELETE)
        self.button_clean_vowels_spaces_and_symbols.click()
        output_text = self.output_text_element.text.replace('\n', "")
        assert len(output_text) == 0

    def test_validate_small_window_resolution(self):
        """ GIVEN I have min screen
            AND I click on 'Оставить ещё и .,-!?' button
            THEN output text has vowels, spaces and symbols only
        """
        self.chrome_driver.set_window_size(250, 800)
        assert self.button_clean_vowels_spaces_and_symbols.is_displayed()
        assert self.button_clean_vowels_and_spaces.is_displayed()
        assert self.button_clean_vowels.is_displayed()
        assert self.button_select_all.is_displayed()


if __name__ == '__main__':
    unittest.main()
