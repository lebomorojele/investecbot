from run import Card, Transaction, Merchant
from run import and_
from run import c1, c2
from run import m1, m2, m3
from run import t1, t2, t3, t4, t5, t6, t7
from run import buildFilter
from run import queryObjects


"""""

Abstract Transaction Lookups

1) Creates filter from abstracted operator and operands
eg. Transaction.centsAmount, 3590, ==

2) Builds a query using a list of filters built in (1) as well as a base object
eg. [filter1, filter2], Transaction

"""""


def unitTest(str, expected, result):
    # print('Expected:')
    # print(expected)
    # print('Result:')
    # print(result)
    test_passed = set(expected) == set(result)
    print(str + ('pass ✅' if test_passed is True else 'fail'))


# Advanced testSix
def testNine():
    print('========Test Nine========')
    print('Find cards used at Woolies with a spend above 3000')

    results = Card.query\
        .filter(Card.transactions.any(
            and_(Transaction.amount > 3000,
                Transaction.merchant.has(Merchant.name == 'Woolies'))))\
        .all()

    results2 = Card.query\
        .join(Transaction, Merchant)\
        .filter(Transaction.amount > 3000)\
        .filter(Merchant.name == 'Woolies')\
        .all()

    results3 = Merchant.query\
        .join(Transaction)\
        .join(Card)\
        .filter(Transaction.amount > 300)\
        .filter(Card.display == '5678')\
        .all()

    unitTest('Test 9a ', [c1], results)
    unitTest('Test 9b ', [c1], results2)
    unitTest('Test 9c ', [m1, m3], results3)
    print('========================')


def testTen():
    print('========Test Ten========')
    print('Find merchants where the card 5678 was used')
    results = Merchant.query.filter(Merchant.cards
                                    .any(Card.display == '5678'))\
        .all()
    results2 = Merchant.query\
        .join(Transaction)\
        .join(Card)\
        .filter(Card.display == '5678')\
        .all()
    unitTest('Test 10a ', [m1, m3], results)
    unitTest('Test 10b ', [m1, m3], results2)
    print('========================')


# Basic Card/Merchant Tests
def testSeven():
    print('========Test Seven========')
    print('Find cards used with transaction amount large than 3000')
    f1 = buildFilter(Card.transactions, Transaction.amount, ">", 3000)
    results = queryObjects(Card, [f1])
    results2 = Card.query\
        .join(Transaction)\
        .join(Merchant)\
        .filter(Transaction.amount > 3000)\
        .all()
    unitTest('Test 7a', [c1, c2], results)
    unitTest('Test 7b', [c1, c2], results2)


def testEight():
    print('========Test Eight========')
    print('Find merchants where transaction spend has been less than 200')
    f1 = buildFilter(Merchant.transactions, Transaction.amount, "<", 200)
    results = queryObjects(Merchant, [f1])
    results2 = Merchant.query\
        .join(Transaction)\
        .join(Card)\
        .filter(Transaction.amount < 200)\
        .all()
    unitTest('Test 8a', [m1, m2], results)
    unitTest('Test 8b', [m1, m2], results2)
    print('========================')


# Basic Transaction Tests
def testZero():
    print('========Test Zero========')
    print('eg. Find all transaction/s')
    results = queryObjects(Transaction, [])
    results2 = Transaction.query\
        .all()
    unitTest('Test 0a ', [t1, t2, t3, t4, t5, t6, t7], results)
    unitTest('Test 0b ', [t1, t2, t3, t4, t5, t6, t7], results2)


def testone():
    print('========Test One========')
    print('eg. Find transaction/s made with card 1234')
    # f1 = filterBuilder(Transaction.card.display, "==", '1234')
    # print(type(Transaction.card.display))
    # results = queryObjects(Transaction, [f1])
    # results = Transaction.query.filter(Transaction.card.has(display="1234"))\
    #               .all()

    # If we're querying 1 level deep -> (object.param operator operand)
    # eg. Transaction.query,filter(XXX).all()
    # XXX = Transaction.amount == 100 =>

    # If we're querying another level deeper -> (object.object
    #    .has(param operator operand))
    # Transaction.query.filter(XXX).all()
    # XXX = Transaction.card.has(YYY)
    # YYY = name='woolies' => Transaction.merchant.has(name = 'Woolies')
    # YYY = Merchant.name == 'woolies' => Transaction.merchant
    #    .has(Merchant.name == 'Woolies')
    f1 = buildFilter(Transaction.card, Card.display, "==", '1234')
    results = queryObjects(Transaction, [f1])
    # Transaction.query.filter(Transaction.card.has(Card.display == '1234'))\
    #          .all()
    # results = Transaction.query.filter(Transaction.merchant
    #                           .has(Merchant.name == 'Woolies')).all()
    results2 = Transaction.query\
        .join(Card)\
        .filter(Card.display == '1234')\
        .all()
    unitTest('Test 1a ', [t1, t2, t4, t6], results)
    unitTest('Test 1b ', [t1, t2, t4, t6], results2)


def testtwo():
    print('========Test Two========')
    print('Find transaction/s from Woolies')
    f1 = buildFilter(Transaction.merchant, Merchant.name, "==", 'Woolies')
    results = queryObjects(Transaction, [f1])
    results2 = Transaction.query\
        .join(Merchant)\
        .filter(Merchant.name == 'Woolies')\
        .all()
    unitTest('Test 2a ', [t1, t4, t5, t6], results)
    unitTest('Test 2b ', [t1, t4, t5, t6], results2)


def testthree():
    print('========Test Three========')
    print('Find transaction/s in Joburg')
    f1 = buildFilter(Transaction.merchant, Merchant.city, "==", 'Joburg')
    results = queryObjects(Transaction, [f1])
    results2 = Transaction.query\
        .join(Merchant)\
        .filter(Merchant.city == 'Joburg')\
        .all()
    unitTest('Test 3a ', [t3], results)
    unitTest('Test 3b ', [t3], results2)


def testfour():
    print('========Test Four========')
    print('Find transaction/s larger than 500')
    f1 = buildFilter(None, Transaction.amount, ">", 500)
    results = queryObjects(Transaction, [f1])
    results2 = Transaction.query\
        .filter(Transaction.amount > 500)\
        .all()
    unitTest('Test 4a ', [t3, t4, t6], results)
    unitTest('Test 4b ', [t3, t4, t6], results2)


def testFive():
    print('========Test Five========')
    print('Find transaction/s with card 1234 card & in Cape Town')
    f1 = buildFilter(Transaction.card, Card.display, "==", '1234')
    f2 = buildFilter(Transaction.merchant, Merchant.city, "==", 'Cape Town')
    results = queryObjects(Transaction, [f1, f2])
    results2 = Transaction.query\
        .join(Card)\
        .join(Merchant)\
        .filter(Card.display == '1234')\
        .filter(Merchant.city == 'Cape Town')\
        .all()
    unitTest('Test 5a ', [t1, t2, t4, t6], results)
    unitTest('Test 5b ', [t1, t2, t4, t6], results2)


def testSix():
    print('========Test Six========')
    print('Find transaction/s from Woolies and < 500')
    f1 = buildFilter(Transaction.merchant, Merchant.name, "==", 'Woolies')
    f2 = buildFilter(None, Transaction.amount, "<", 500)
    results = queryObjects(Transaction, [f1, f2])
    results2 = Transaction.query\
        .join(Merchant)\
        .filter(Transaction.amount < 500)\
        .filter(Merchant.name == 'Woolies')\
        .all()
    unitTest('Test 6a ', [t1, t5], results)
    unitTest('Test 6b ', [t1, t5], results2)
