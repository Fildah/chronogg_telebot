#!/usr/bin/env python3
import logging

import requests


class Chrono:
    def __init__(self, token):
        self.token = token
    
    def set_token(self, token):
        logging.info('Setting new token')
        self.token = token

    def coin_spin(self):
        logging.info('Fetching https://api.chrono.gg/quest/spin')
        response = requests.get('https://api.chrono.gg/quest/spin',
                                headers={'Accept': 'application/json', 'Authorization': self.token})
        if response.status_code == 420:
            logging.info('An error occurred while fetching results: Coin already clicked.')
            return 'An error occurred while fetching results: Coin already clicked.'
        if response.status_code == 401:
            logging.info('An error occurred while fetching results: Expired/invalid authorization token.')
            return 'An error occurred while fetching results: Expired/invalid authorization token.'
        if response:
            logging.info('Done.')
            return 'Coin spin successful.'
        else:
            logging.info('An error has occurred.')
            return 'An error has occurred.'
    
    def get_coin_balance(self):
        logging.info('Fetching https://api.chrono.gg/account')
        response = requests.get('https://api.chrono.gg/account',
                                headers={'Accept': 'application/json', 'Authorization': self.token})
        if response.status_code == 401:
            logging.info('An error occurred while fetching results: Expired/invalid authorization token.')
            return 'An error occurred while fetching results: Expired/invalid authorization token.'
        return str(response.json()['coins']['balance'])
    
    def get_sale(self):
        logging.info('Fetching https://api.chrono.gg/sale')
        response = requests.get('https://api.chrono.gg/sale',
                                headers={'Accept': 'application/json', 'Authorization': self.token})
        response = response.json()
        return (response['name'] + '\n' + response['normal_price'] + '$ -' + response['discount'] + ' ' +
                response['sale_price'] + '$\n' + response['unique_url'])
