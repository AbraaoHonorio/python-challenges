import json
import logging

from core import loader
from payment_app.payment_app.core.factory import PaymentServiceFactory

PLUGIN_DIR = 'plugins'
logging.basicConfig(level=logging.INFO)


# main entry point for the application to start the payment process and load the plugins

def main():
    logging.info('Starting the payment app')

    with open("./payment_plugins.json") as file:
        data = json.load(file)
        # load the plugins
        loader.load_plugins(data[PLUGIN_DIR])

        plugins = [PaymentServiceFactory.create(item) for item in data["payments"]]

        for plugin in plugins:
            logging.info(plugin.process_payment())


if __name__ == '__main__':
    while True:  # loop forever for simulation purposes
        main()
