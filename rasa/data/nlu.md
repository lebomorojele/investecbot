## intent:find_transactions
  - [show](show) transactions
  - transactions
  - [show](show) all transactions
  - [show](show) todays transactions
  - [show](show) transactions [today](time)
  - [show](show) transactions made [yesterday](time)
  - [show](show) transactions between [25 may 2020 and 27 may 2020](time)
  - [show](show) transactions made on [26 may](time)
  - [show](show) [todays](time) transactions
  - [show](show) transactions happened on the [26th of May 2020](time)
  - [show](show) transactions from [26 May](time)
  - [show](show) transactions from [account](account_number) [0987654321](number)
  - account from [account](account_number) [0987654321](number) [show](show) transactions
  - [show](show) transactions in [account](account_number) [0987654321](number)
  - [show](show) transactions with amount [bigger than](operator_greater_than) [200](number)
  - transactions [bigger than](operator_greater_than) [200](number)
  - [show](show) all transactions [bigger than](operator_greater_than) [200](number)
  - [show](show) transactions with amount [equal to](operator_equal) [200](number)
  - transactions [equal to](operator_equal) [200](number)
  - [show](show) all transactions [equal to](operator_equal) [200](number)
  - [show](show) transactions with amount [smaller than](operator_less_than) [200](number)
  - transactions [smaller than](operator_less_than) [200](number)
  - [show](show) all transactions [smaller than](operator_less_than) [200](number)
  - [show](show) transactions with amount [equal to](operator_equal) [200](number)
  - transactions with [card](card) ending [1234 4567 7890 1234](number)
  - [card](card) [1234 4567 7890 1234](number) transactions
  - transactions using [card](card) [1234 4567 7890 1234](number)
  - [1234 4567 7890 1234](number) [card](card) transactions
  - [show](show) transactions at [Woolies](merchant_name)
  - [show](show) [Woolies](merchant_name) transactions
  - spending at [Woolies](merchant_name)
  - [show](show) transactions in [Cape Town](city)
  - [show](show) transactions with amount [smaller than](operator_less_than) [1000](number) in [Cape Town](city)
  - transactions in [Cape Town](city) [smaller than](operator_less_than) [1000](number)
  - In [Cape Town](city), [smaller than](operator_less_than) [1000](number)
  - [show](show) transactions with amount [bigger than](operator_greater_than) [1000](number) in [Cape Town](city)
  - transactions in [Cape Town](city) [bigger than](operator_greater_than) [1000](number)
  - In [Cape Town](city), [bigger than](operator_greater_than) [1000](number)
  - [show](show) transactions with amount [equal to](operator_equal) [1000](number) in [Cape Town](city)
  - transactions in [Cape Town](city) [equal to](operator_equal) [1000](number)
  - In [Cape Town](city), [equal to](operator_equal) [1000](number)
  - [show](show) transactions with [card](card) [1234 4567 7890 1234](number) in [Cape Town](city)
  - [show](show) transactions from [account](account_number) made with [zar](currency)
  - [show](show) [zar](currency) transactions on [account](account_number)
  - [zar](currency) account transactions
  - [zar](currency) transactions
  - [show](show) transactions with [card](card) [1234](number) made at [woolies](merchant_name)
  - [show](show) the [woolies](merchant_name) transactions with [card](card) [1234 4567 7890 1234](number)
  - [show](show) transactions with [card](card) [1234](number) made at [woolies](merchant_name)

## intent:category_breakdown
- category breakdown
- what is my category breakdown
- what do I spend on
- breakdown my spending
- what is my favourite category
- what do i spend the most money on
- i like to spend money on

## intent:show_menu
## - I need help
## - help me
## - help
## - show help
## - in need of help

## intent:set_alert
- set up [alert](alert)
- setup an [alert](alert)
- set up an [alert](alert)
- i need an [alert](alert)
- make [alert](alert)

## intent:category_entry
- the category is [food](reminder_category)
- [food](reminder_category) is the category
- [food](reminder_category)
- it is [food](reminder_category)

## intent:amount_entry
- the amount is [100](reminder_amount)
- [100](reminder_amount) is the amount
- it is [100](reminder_amount)
- [100](reminder_amount)

## regex:amount_entry
- [0-9]

## synonym:food
- entertainment
- groceries
- bills
- payments

## synonym:alert
- alarm
- notification
- push
- bell
- reminder

## regex:account_number
- [0-9](11)

## synonym:show
- find
- my
- explore
- search for
- collect
- grab
- select
- any
- only
- all

## synonym:bigger than
- greater than
- larger than
- over

## synonym:equal to
- same as
- same
- equal
- matching

## synonym:smaller than
- less than
- lesser than
- under

## intent:greet
- hey
- hello
- hi
- good morning
- good evening
- hey there

## intent:goodbye
- bye
- goodbye
- see you around
- see you later

## intent:affirm
- yes
- indeed
- of course
- that sounds good
- correct

## intent:deny
- no
- never
- I don't think so
- don't like that
- no way
- not really

## intent:mood_great
- perfect
- very good
- great
- amazing
- wonderful
- I am feeling very good
- I am great
- I'm good

## intent:mood_unhappy
- sad
- very sad
- unhappy
- bad
- very bad
- awful
- terrible
- not very good
- extremely sad
- so sad

## intent:bot_challenge
- are you a bot?
- are you a human?
- am I talking to a bot?
- am I talking to a human?
