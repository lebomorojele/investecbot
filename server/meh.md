*Find all transactions
PrimaryTarget=Transaction, Filters=[]
Transaction


*Find transaction/s larger than 100
PrimaryTarget=Transaction, Filters=[PrimaryTarget.param]
Transaction, Transaction.amount > 100


*Find transaction/s made with card 1234
PrimaryTarget=Transaction, Filters=[PrimaryTarget.child]
Transaction, Transaction.Card.display=1234


*Find transaction/s with card 1234 card & in Cape Town
PrimaryTarget=Transaction, Filters=[PrimaryTarget.child1, PrimaryTarget.child2]
Transaction, Transaction.Card.display=1234, Transaction.Merchant.city=CPT


*Find transaction/s from Woolies and < 500
PrimaryTarget=Transaction, Filters=[PrimaryTarget.child, PrimaryTarget.param]
Transaction, Transaction.Merchant.name=Woolies, Transaction.amount<500


*Find cards used with transaction amount large than 3000
PrimaryTarget=Card, Filters=[PrimaryTarget.child]
Card, Card.Transaction.amount>3000


*Find merchants where transaction spend has been less than 200
PrimaryTarget=Merchant, Filters=[PrimaryTarget.child]
Merchant, Merchant.Transaction.amount<200


Find cards used at Woolies with a spend above 3000
PrimaryTarget=Card, Filters=[PrimaryTarget.child, PrimaryTarget.child.child]
Card, Card.Transactions.amount>3000, Card.Transaction.Merchant.name=Woolies
[If there's a transaction as a child, go that route and use AND_]

Find merchants where the card 5678 was used
PrimaryTarget=Card, Filters=[PrimaryTarget.child]
Card, Card.Merchant.display==5678



TYPES OF QUERIES:
Primary Target w/ no filters
Primary Target w/ param filter
Primary Target w/ child.param filter
Primary Target w/ param AND child.param filter
Primary Target w/ multiple params filter eg. Tx.amount > 300 & Tx.date == today
Primary Target w/ multiple child.params filter eg. Tx.merchant=Pnp & Tx.card=1234
Primary Target w/ child of child

















Targets:
  transaction
    - centsAmount
    - date
  card
    - display
  merchant
    - number
    - city



Show me all my Transactions
