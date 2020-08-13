## Find Transactions
* find_transactions
  - action_find_transactions

## Category Breakdown
* category_breakdown
  - action_category_breakdown

## Show Menu
## * show_menu
##  - utter_menu_options

## Set Alert
* set_alert
  - utter_alert_clarification
  - reminder_form
  - form{"reminder_category" :"reminder_form"}
  - form{"reminder_category": null}
  - utter_reminder_confirmation

## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy
  - utter_menu_options

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot
