# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

# from rasa_sdk import Action
# from rasa_sdk.executor import CollectingDispatcher

# class ActionLeaveBalance(Action):
#     def name(self) -> str:
#         return "action_leave_balance"

#     def run(self, dispatcher: CollectingDispatcher, tracker, domain):
#         # Example logic to fetch leave balance
#         leave_balance = "You have 5 annual leaves remaining."
#         dispatcher.utter_message(text=leave_balance)
#         return []

# class ActionExpenseReportStatus(Action):
#     def name(self) -> str:
#         return "action_expense_report_status"

#     def run(self, dispatcher: CollectingDispatcher, tracker, domain):
#         # Example logic to fetch expense report status
#         expense_status = "Your last expense report was approved on August 25."
#         dispatcher.utter_message(text=expense_status)
#         return []