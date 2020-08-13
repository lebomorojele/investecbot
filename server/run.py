from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
import datetime
import operator


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///debug.db'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    dateTime: datetime.datetime = db.Column(db.Date)

    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    card = db.relationship('Card', back_populates='transactions')

    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'))
    merchant = db.relationship('Merchant', back_populates='transactions')


card_merchant_assosiation = db.Table('card_merchant_assosiation',
                                     db.Column('card_id', db.Integer,
                                               db.ForeignKey('card.id')),
                                     db.Column('merchant_id', db.Integer,
                                               db.ForeignKey('merchant.id')))


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display = db.Column(db.String)
    transactions = db.relationship('Transaction', back_populates='card')
    merchants = db.relationship('Merchant',
                                secondary='card_merchant_assosiation',
                                back_populates='cards')


class Merchant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String)
    category = db.Column(db.String)
    transactions = db.relationship('Transaction', back_populates='merchant')
    cards = db.relationship('Card',
                            secondary='card_merchant_assosiation',
                            back_populates='merchants')


transaction_map = {
    'id': Transaction.id,
    'centsAmount': Transaction.amount,
    'dateTime': Transaction.dateTime
}

card_map = {
    'id': Card.id,
    'display': Card.display
}

merchant_map = {
    'id': Merchant.id,
    'name': Merchant.name,
    'city': Merchant.city,
    'category': Merchant.category
}


entity_map = {
    'transaction': transaction_map,
    'card': card_map,
    'merchant': merchant_map
}


db.drop_all()
db.create_all()


def addRow(object):
    db.session.add(object)
    try:
        db.session.commit()
    except IntegrityError:  # as err:
        db.session.rollback()
        print('Duplicate: '+type(object))
        # print('Duplicate Addition: '+str(err.args))


# Build Test Transactions

m1 = Merchant(name='Woolies', city='Cape Town', category='Groceries')
m2 = Merchant(name='Pnp', city='Cape Town', category='Groceries')
m3 = Merchant(name='Mavericks', city='Joburg', category='Entertainment')
merchant_list = [m1, m2, m3]
for m in merchant_list:
    addRow(m)


c1 = Card(display='1234 4567 7890 1234')
c2 = Card(display='4567 7890 1234 4567')
c3 = Card(display='7890 1234 4567 7890')
card_list = [c1, c2, c3]
for c in card_list:
    addRow(c)


t1 = Transaction(amount=100, dateTime=datetime.datetime(2020, 5, 26), card=c1, merchant=m1)
c1.merchants.append(m1)
t2 = Transaction(amount=200, dateTime=datetime.datetime(2020, 4, 30), card=c1, merchant=m2)
c1.merchants.append(m2)
t3 = Transaction(amount=4000, dateTime=datetime.datetime(2020, 6, 1), card=c2, merchant=m3)
c2.merchants.append(m3)
t4 = Transaction(amount=700, dateTime=datetime.datetime(2020, 5, 14), card=c1, merchant=m1)
c1.merchants.append(m1)
t5 = Transaction(amount=350, dateTime=datetime.datetime(2020, 5, 4), card=c2, merchant=m1)
c2.merchants.append(m1)
t6 = Transaction(amount=10000, dateTime=datetime.datetime(2020, 6, 15), card=c1, merchant=m1)
c1.merchants.append(m1)
t7 = Transaction(amount=1, dateTime=datetime.datetime(2020, 5, 26), card=c3, merchant=m2)
c3.merchants.append(m2)
transaction_list = [t1, t2, t3, t4, t5, t6, t7]
for t in transaction_list:
    addRow(t)


ops = {
    '<': operator.lt,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '>=': operator.ge,
    '>': operator.gt
}


def objectOperation(left, op, right):
    operation = ops.get(op)
    result = operation(left, right)
    return result


def buildJoin(object):
    if object == Transaction:
        joins = ["Card", "Merchant"]
    elif object == Merchant:
        joins = ["Transaction", "Card"]
    else:
        joins = ["Transaction", "Merchant"]

    query = object.query
    for j in joins:
        query = query.join(eval(j))
    return query


def queryObjects(object, filter_list):
    query = buildJoin(object)
    for single_filter in filter_list:
        query = query.filter(single_filter)

    results = query.all()
    return results


def buildFilter(objectOfParam, param, operator, operand):
    if objectOfParam:
        if objectOfParam.property.uselist:
            return objectOfParam.any(objectOperation(param, operator, operand))
        else:
            return objectOfParam.has(objectOperation(param, operator, operand))
    else:
        return objectOperation(param, operator, operand)


def transactionResponse(transactions):
    message = "🤖Wow, I'm struggling to do anything today."
    if len(transactions) == 0:
        message = "🤖I found zero transactions matching your request 😭"
    elif len(transactions) == 1:
        transaction = transactions[0]
        message = "🤖Is this what you wanted?\nTransaction made on the {} for {} at {}".format(transaction.dateTime, transaction.amount, transaction.merchant.name)
    elif len(transactions) == 2:
        transaction = transactions[0]
        transaction2 = transactions[1]
        m1 = "🤖I deserve a raise working this hard 😅. Here's what I found"
        m2 = "🤖First transaction was made on the {} for {} at {}".format(transaction.dateTime, transaction.amount, transaction.merchant.name)
        m3 = "🤖The second was made on the {} for {} at {}".format(transaction2.dateTime, transaction2.amount, transaction2.merchant.name)
        message = "\n".join([m1, m2, m3])
    else:
        total = 0
        ids = []
        count = len(transactions)
        m1 = "🤖This is quite a bit, I summarised it for you."
        for tx in transactions:
            total += tx.amount
            ids.append(tx.id)
        m2 = "🤖You have {} ".format(count)+"transaction"+("" if count == 1 else "s") +" totallying {} 💵💵💵".format(total)
        m3 = "🤖For reference here are the ids: {}".format(str(ids))
        message = "\n".join([m1, m2, m3])

    return message


def categoryResponse(categories):
    print(categories)
    if len(categories) == 0:
        message = "🤖You don't spend much huh. I found nothing."
    if len(categories) == 1:
        message = "🤖You have one true love 💖: {}".format(categories[0][0])
    if len(categories) > 1:
        m1 = "🤖Your favourite category is {} 💖".format(categories[0][0])
        m2 = "🤖Your least favourite category is {} 👎".format(categories[1][0])
        message = "\n".join([m1, m2])

    return message


@app.route('/')
def index():
    return '🥳', 200


@app.route('/category')
def category():

    results = db.session.query(Merchant.category, func.count(Merchant.transactions)).join(Transaction).group_by(Merchant.category).order_by(Merchant.category.desc()).all()
    summary = categoryResponse(results)
    return jsonify(summary), 200


@app.route('/transactions', methods=['POST'])
def fetchAll():

    print('recieved: transaction filter request with body:')
    print(request.json)
    filter_list = []
    for filter_set in request.json['results']:
        if filter_set['type'] == 'transaction':
            # Transaction Filter Set
            for filter in filter_set['values']:
                if filter['type'] == 'dateTime':
                    dateFormat = "%Y-%m-%d"
                    date = datetime.datetime.strptime(filter['value'], dateFormat)
                    filter_list.append(buildFilter(None, transaction_map.get(filter['type']), filter['operator'], date.date()))
                else:
                    filter_list.append(buildFilter(None, transaction_map.get(filter['type']), filter['operator'], filter['value']))
        if filter_set['type'] == 'card':
            # Card Filter Set
            for filter in filter_set['values']:
                filter_list.append(buildFilter(None, card_map.get(filter['type']), filter['operator'], filter['value']))
        if filter_set['type'] == 'merchant':
            # Merchant Filter Set
            for filter in filter_set['values']:
                filter_list.append(buildFilter(None, merchant_map.get(filter['type']), filter['operator'], filter['value']))

    results = queryObjects(Transaction, filter_list)
    print(results)
    summary = transactionResponse(results)
    print(summary)

    return jsonify(summary), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8080')
