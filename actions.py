# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
import re
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

# class ActionHelloWorld(FormAction):
# 
#      def name(self) -> Text:
#          return "admission_form"
#      
# 
#      @staticmethod
#      def required_slots(tracker: Tracker) -> List[Text]:
#         """A list of required slots that the form has to fill"""
#         
#         print("required_slots(tracker: Tracker)")
#         return ["name",  "ssn", "subject"]
# 
#      def submit(self, dispatcher: CollectingDispatcher,
#              tracker: Tracker,
#              domain: Dict[Text, Any],
#      ) -> List[Dict]:
# 
#          dispatcher.utter_message(template="utter_submit")
# 
#          return []
def redirectToSlot(slot, value, dispatcher, tracker, remapping):
    response = {slot: value} # default response

    if (slot == "pinnumber"):
        if len(value) == 6:
            if(value.isdigit()):
                response = {slot: value}
            else:
                dispatcher.utter_message(template="utter_wrong_pinalpha")
                response = {slot: None}  
        else:
            dispatcher.utter_message(template="utter_wrong_pinnumber")
            response = {slot: None}
    elif (slot == "mailid"):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if(re.search(regex, value)):
            response = {slot: value}
        else:
            dispatcher.utter_message(template="utter_wrong_emailid")
            response = {slot: None}
    elif (slot == "aadhaar"):
        if len(value) == 12:
            if(value.isdigit()):
                response = {slot: value}
            else:
                dispatcher.utter_message(template="utter_wrong_aadhaaralpha")
                response = {slot: None}  
        else:
            dispatcher.utter_message(template="utter_wrong_aadhaar")
            response = {slot: None}
    elif (slot == "phone_number"):
        if len(value) == 10:
            if(value.isdigit()):
                response = {slot: value}
            else:
                dispatcher.utter_message(template="utter_wrong_phonenumberalpha")
                response = {slot: None}  
        else:
            dispatcher.utter_message(template="utter_wrong_phonenumber")
            response = {slot: None}
    if (type(remapping) == str):
        response[remapping] = None

    return response



class ActionHelloWorld(FormAction):

     def name(self) -> Text:
        return "admission_form"
     

     @staticmethod
     def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
    
        return ["name","mailid", "aadhaar", "statename","districtname",  "cityname", "postofficename","villagename",  "muncorppanchname", "pinnumber","phone_number","mailid"]


     def validate_phone_number(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
     ) -> Dict[Text, Any]:
        """Validate phone."""
        value=tracker.get_slot("phone_number")

        print("validate_phone_number() method  ", value)

        requestedSlot = tracker.get_last_event_for("slot", skip=1)
        if (requestedSlot['name'] == 'requested_slot'):
            if (requestedSlot['value'] == 'phone_number'): # If requested slot was phone_number and value also corresponds to the phone_number 
                return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, None)
            else: # If value corresponds to the wrong slot
                return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, 'phone_number')
        else:
            return redirectToSlot('phone_number', value, dispatcher, tracker, None)

     def validate_mailid(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
     ) -> Dict[Text, Any]:
        """Validate mailid."""
        value=tracker.get_slot("mailid")

        print("validate_mailid() method", value)

        requestedSlot = tracker.get_last_event_for("slot", skip=1)
        if (requestedSlot['name'] == 'requested_slot' and requestedSlot['value']):
            if (requestedSlot['value'] == 'mailid'): # If requested slot was mailid and value also corresponds to the mailid 
                return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, None)
            else: # If value corresponds to the wrong slot
                return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, 'mailid')
        else:
            return redirectToSlot('mailid', value, dispatcher, tracker, None)

     def submit(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any],
     ) -> List[Dict]:
          name=tracker.get_slot("name")
          Aadhaar=tracker.get_slot("aadhaar")
          statename=tracker.get_slot("statename")
          districtname=tracker.get_slot("districtname")
          cityname=tracker.get_slot("cityname")
          postofficename=tracker.get_slot("postofficename")
          villagename=tracker.get_slot("villagename")
          muncorppanchname=tracker.get_slot("muncorppanchname")
          pinnumber=tracker.get_slot("pinnumber")
          phone_number=tracker.get_slot("phone_number")
          mailid=tracker.get_slot("mailid")
          message="USER DETAILS:"+"\n\n"+"Name:"+name+"\n"+"Email:"+mailid+"\n"+"Phone_nuumber:"+phone_number+"\n"+"Aadhaar:"+Aadhaar+"\n"+"statename:"+statename+"\n"+"districtname:"+districtname+"\n"+"Thanks! for sharing the information."
          saveFile = open("some.txt", 'a')
          saveFile.write(message)
          saveFile.close()
          dispatcher.utter_message(message)
          return []