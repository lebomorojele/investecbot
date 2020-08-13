# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction

import requests
import dateutil.parser

flaskServer = "https://5490d8517ebc.ngrok.io/"


class ActionCategoryBreakdown(Action):

    def name(self) -> Text:
        return "action_category_breakdown"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        response = requests.get(flaskServer+'category')\
            .json()
        print("response: "+response)
        dispatcher.utter_message(text=str(response))

        return []


class ActionFindTransactionSummary(Action):

    def name(self) -> Text:
        return "action_find_transactions"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message['entities']

        transaction = []
        card = []
        merchant = []

        number_list = list(filter(lambda e: e['entity'] == 'number', entities))
        number = number_list[0]['value'] if len(number_list) > 0 else None
        print('Transaction Actions 🔨')
        for e in entities:
            if e['entity'] == 'account_number' and number is not None:
                print('Filtering by account')
                transaction.append({'type': 'accountNumber', 'operator': '==', 'value': number})
            if e['entity'] == 'currency':
                print('Filtering by currency')
                transaction.append({'type': 'currency', 'operator': '==', 'value': e['value']})
            if e['entity'] == 'time' and e['extractor'] == 'DucklingHTTPExtractor':
                print('Filtering by time')
                if e['additional_info']['type'] == 'interval':
                    if e['value']['from'] is not None:
                        date = dateutil.parser.parse(e['value']['from']).strftime('%Y-%m-%d')
                        transaction.append({'type': 'dateTime', 'operator': '>=', 'value': date})
                    if e['value']['to'] is not None:
                        date = dateutil.parser.parse(e['value']['to']).strftime('%Y-%m-%d')
                        transaction.append({'type': 'dateTime', 'operator': '<=', 'value': date})
                elif e['additional_info']['type'] == 'value':
                    date = dateutil.parser.parse(e['value']).strftime('%Y-%m-%d')
                    transaction.append({'type': 'dateTime', 'operator': '==', 'value': date})
                else:
                    print("Could not determine date range")
            if e['entity'] == 'reference':
                print('Filtering by tx reference')
                transaction.append({'type': 'reference', 'operator': '==', 'value': e['value']})
            if e['entity'] == 'card' and number is not None:
                print('Filtering by card')
                card.append({'type': 'display', 'operator': '==', 'value': number})
            if e['entity'] == 'city':
                print('Filtering by city')
                merchant.append({'type': 'city', 'operator': '==', 'value': e['value']})
            if e['entity'] == 'merchant_name':
                print('Filtering by merchant')
                merchant.append({'type': 'name', 'operator': '==', 'value': e['value']})
            if e['entity'] == 'operator_equal' and number is not None:
                print('Filtering by = {}'.format(number))
                transaction.append({'type': 'centsAmount', 'operator': '==', 'value': number})
            if e['entity'] == 'operator_greater_than' and number is not None:
                print('Filtering by > {}'.format(number))
                transaction.append({'type': 'centsAmount', 'operator': '>', 'value': number})
            if e['entity'] == 'operator_less_than' and number is not None:
                print('Filtering by < {}'.format(number))
                transaction.append({'type': 'centsAmount', 'operator': '<', 'value': number})

        payload = {'results': [{'type': 'transaction', 'values': transaction},
                               {'type': 'merchant', 'values': merchant},
                               {'type': 'card', 'values': card}]}
        print('Request Payload: {}'.format(payload))

        response = requests.post(flaskServer+'transactions',
                                 json=payload).json()
        dispatcher.utter_message(text=str(response))

        return []


class ActionReminderForm(FormAction):

    def name(self) -> Text:
        return "reminder_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        # A list of required slots that the form has to fill

        print("required_slots(tracker: Tracker)")
        return ["reminder_category", "reminder_amount"]

    def submit(self, dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]) -> List[Dict]:

        dispatcher.utter_message(template="utter_submit")

        return []
