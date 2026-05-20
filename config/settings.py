import os

class Config:
    BASE_URLS = {
        'the_internet': 'https://the-internet.herokuapp.com/',
        'automation_exercise': 'https://automationexercise.com/',
        'samokat': 'https://qa-scooter.praktikum-services.ru/',
        'reqres': 'https://reqres.in/api/'

    }

    ENV = os.getenv("ENV", "stage")
    BASE_URL = os.getenv("BASE_URL", BASE_URLS['the_internet'])

