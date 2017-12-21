import random
from decimal import *
class Customer(object):

    def __init__(self, customerArgs):
        """Create a customer: First Name, Last Name"""
        self.ID = customerArgs['Customer ID']
        self.firstName = customerArgs['First Name']
        self.lastName = customerArgs['Last Name']
        self.phone = customerArgs['Phone Number']
        self.email = customerArgs['Email']
        self.dateJoined = customerArgs['Date Joined']
        self.referralCode = customerArgs['Referral Code']
        self.connection = customerArgs['Connection']

        if self.referralCode == None:
            self.referralCode = self.createReferralID()

    def insert_customer(self):
        """Commit customer SQL to database"""
        customerArgs = [self.firstName, self.lastName, self.email, self.phone, self.referralCode, self.ID]
        cur = self.connection.cursor()
        response = cur.callproc('insert_customer', customerArgs)
        self.connection.commit()
        self.customerID = response[3]
        cur.close()
        print("Successfully added {} {} to the database and customer ID is: {}".format(self.firstName, self.lastName, self.customerID))

    def createReferralID(self):
        """Returns a 10 digit random referral code. 300 Quadrillion combinations"""
        symbols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u', 'v', 'w', 'x', 'y', 'z',
                   'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                   'U', 'V', 'W', 'x', 'y', 'Z',
                   '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        code = []
        count = 0
        while count < 10:
            code.append(random.choice(symbols))
            count += 1
        return ''.join(code)

    def add_phoneNumber(self, phoneNumber):
        """Add phone number to customer: phone number"""
        self.phone = phoneNumber
        cur = self.connection.cursor()
        cur.callproc('update_customer_phone',[self.ID, self.phone])
        self.connection.commit()
        cur.close()
        print("Successfully added {} to customer ID: {}".format(self.phone, self.ID))

    def add_email(self, email):
        """Add email to customer: email"""
        self.email = email
        cur = self.connection.cursor()
        cur.callproc('update_customer_email', [self.ID, self.email])
        self.connection.commit()
        cur.close()
        print("Successfully added {} to customer ID: {}".format(self.email, self.ID))

    def add_address(self):
        """Creates an Address instance, and adds it to the current customer:"""
        self.address.insert_address()
        self.update_address_ID()

    def update_address_ID(self):
        """Calls database to update the customer address ID"""
        updateAddressArgs = [self.ID, self.address.ID]
        cur = self.connection.cursor()
        cur.callproc('update_customer_address', updateAddressArgs)
        self.connection.commit()
        cur.close()
        print("Successfully updated customer address ID: {}".format(self.address.ID))

    def show_address(self, addressArgs):
        """Creates an Address instance for display"""
        self.address = Address(addressArgs)

class Amazon_Order(object):
    """Create an Amazon order"""

    def __init__(self, amazonArgs):
        self.connection = amazonArgs['Connection']
        self.ID = amazonArgs['Amazon ID']
        self.shipBy = amazonArgs['Ship By']
        self.deliverBy = amazonArgs['Deliver By']
        self.code = amazonArgs['Amazon Key']

    def insert_amazon_order(self):
        shipByDate = self.shipBy.split('/')
        shipByYear = shipByDate[2]
        shipByMonth = shipByDate[0]
        shipByDay = shipByDate[1]
        deliverByDate = self.deliverBy.split('/')
        deliverByYear = deliverByDate[2]
        deliverByMonth = deliverByDate[0]
        deliverByDay = deliverByDate[1]
        cur = self.connection.cursor()
        response = cur.callproc('insert_amazon_order', [self.code, shipByYear, shipByMonth, shipByDay, deliverByYear, deliverByMonth, deliverByDay, ''])
        self.connection.commit()
        self.ID = response[7]

class Order_Item(object):

    def __init__(self, orderItemArgs):
        self.itemNumber = orderItemArgs['Item Number']
        self.title = orderItemArgs['Title']
        self.authorFirst = orderItemArgs['Author First']
        self.authorLast = orderItemArgs['Author Last']
        self.edition = orderItemArgs['Edition']
        self.ISBN = orderItemArgs['ISBN']
        self.condition = orderItemArgs['Condition']
        self.price = orderItemArgs['Price']

class Shipping_Material(object):
    """Create a shipping material(box) for an order"""

    def __init__(self, shippingMaterialArgs):
        self.shipID = shippingMaterialArgs['Shipping ID']
        self.size = shippingMaterialArgs['Size']
        self.type = shippingMaterialArgs['Type']

class Order(object):
    """Create an order object"""

    def __init__(self, orderArgs):
        self.connection = orderArgs['Connection']
        self.ID = orderArgs['Order ID']
        self.customer = orderArgs['Customer']
        self.orderType = orderArgs['Order Type']
        self.transaction = orderArgs['Transaction']
        self.amazonOrder = orderArgs['Amazon Order']
        self.date = orderArgs['Order Date']
        self.status = orderArgs['Status']
        self.promotion = orderArgs['Promotion Code']
        self.shipping = orderArgs['Shipping']
        self.books = orderArgs['Books']

    def insert_order(self):
        cur = self.connection.cursor()
        response = cur.callproc('insert_order', [self.customer.firstName, self.customer.lastName, self.customer.phone,
                                                 self.customer.email, self.customer.referralCode,self.orderType.name,
                                                 self.transaction.name, self.status.name, self.promotion,
                                                self.ID, self.customer.ID])

        self.connection.commit()
        self.ID = response[9]

        if self.amazonOrder != None:
            self.amazonOrder.connection = self.connection
            self.amazonOrder.insert_amazon_order()
            cur.callproc('update_order_amazon_id', [self.ID, self.amazonOrder.ID])

        for book in self.books:
            if self.orderType.name == 'Sell Order':
                cur.callproc('insert_sell_order_item', [self.ID, book.title, book.authorFirst, book.authorLast, book.ISBN, book.edition])
                self.connection.commit()
            elif self.orderType.name == 'Buy Order':
                cur.callproc('insert_buy_order_item', [self.ID, book.title, book.authorFirst, book.authorLast, book.ISBN, book.edition, book.condition])
                self.connection.commit()
            else:
                print('Order Item Error')
                break

class Shipping_Order(object):
    """Create a shipping order for an order: shipping cost, tracking, expcted arrival, ship type, shipping materials used"""

    def __init__(self, shippingArgs):
        self.connection = shippingArgs['Connection']
        self.ID = shippingArgs['Shipping ID']
        self.orderID = shippingArgs['Order ID']
        self.shippingCost = shippingArgs['Shipping Cost']
        self.tracking = shippingArgs['Tracking']
        self.shipDate = shippingArgs['Shipping Date']
        self.expectedArrival = shippingArgs['Expected Arrival']
        self.shipType = shippingArgs['Shipping Type']
        self.shippingMaterials = shippingArgs['Shipping Materials']
        self.status = shippingArgs['Status']

    def split_date(self, date):
        dateList = date.split('/')
        return {'Day': dateList[1], 'Month': dateList[0], 'Year': dateList[2]}

    def insert_shipping(self):
        date = self.split_date(self.expectedArrival)
        cur = self.connection.cursor()
        results = cur.callproc('insert_shipping', [self.orderID, self.shippingCost, self.tracking, date['Year'], date['Month'], date['Day'], self.shipType.name, self.ID])
        self.connection.commit()
        self.ID = results[7]

        if self.shippingMaterials != None:

            for material in self.shippingMaterials:
                print(self.ID, material['Type']+' '+material['Size'])
                cur.callproc('insert_shipping_materials', [self.ID, (material['Size']+' '+material['Type'])])
                self.connection.commit()


    def insert_shipping_materials(self):
        cur = self.connection.cursor()

        for material in self.shippingMaterials:
            cur.callproc('insert_shipping_materials', [material.shippingOrderId, (material.size+' '+material.type)])
            self.connection.commit()

        cur.close()

class Buy_Order(Order):
    """Create a buy order"""

    def __init__(self, buyOrderArgs):
        super().__init__(buyOrderArgs)

        self.bookData = buyOrderArgs['Books']
        self.books = []
        self.createBooks()

    def createBooks(self):
        """Instantiates buy order items for each book"""
        for x in self.bookData:
            y = Buy_Order_Item(title=x['Title'],condition=x['Condition'], authorFirst=x['Author First'],
                               authorLast=x['Author Last'], edition=x['Edition'], ISBN=x['ISBN'], price=x['Price'])
            self.books.append(y)

    def insert_order(self):
        """Insert an order into the database"""
        orderArgs = [self.customer.firstName, self.customer.lastName, self.customer.referralCode, self.orderType,
                     self.transactionType, self.status, self.promotion_code, self.orderID, self.customer.customerID]
        cur = self.connection.cursor()
        response = cur.callproc('insert_order', orderArgs)
        self.connection.commit()
        self.orderID = response[7]
        self.customer.customerID = response[6]

        for book in self.books:
            cur.callproc('insert_buy_order_item', [self.orderID, book.title, book.condition])
            self.connection.commit()

        cur.close()

class Buy_Order_Item():
    """Create a sell order item"""

    def __init__(self, title, condition, authorFirst=None, authorLast=None, edition=None, ISBN=None, price=None):
        self.title = title
        self.condition = condition
        self.authorFirst = authorFirst
        self.authorLast = authorLast
        self.edition = edition
        self.ISBN = ISBN
        self.price = price

class Address(object):
    """Create an address: house number, street, city, state, zip, country"""

    def __init__(self, addressArgs):
        self.ID = addressArgs['Address ID']
        self.customerID = addressArgs['Customer ID']
        self.buildingNumber = addressArgs['Building Number']
        self.street = addressArgs['Street Number']
        self.city = addressArgs['City']
        self.state = addressArgs['State']
        self.zipCode = addressArgs['Zip Code']
        self.country = addressArgs['Country']
        self.connection = addressArgs['Connection']

    def insert_address(self):
        """Commit address to SQL database"""
        addressArgs = [self.customerID,  self.buildingNumber, self.street, self.city, self.state.name, self.zipCode, self.country.name, self.ID]
        cur = self.connection.cursor()
        response = cur.callproc('insert_address', addressArgs)
        self.connection.commit()
        cur.close()
        self.ID = response[6]
        print("Successfully added {} {} {} {} {} {} with an address ID: {}".format(self.buildingNumber, self.street,
                                                                                   self.city, self.state.name, self.zipCode,
                                                                                   self.country.name, self.ID))
    def get_address_ID(self):
        """Returns the address ID"""
        return self.ID

class State(object):
    """Create a state object"""

    def __init__(self, stateArgs):
        self.ID = stateArgs['State ID']
        self.name = stateArgs['State Name']
        self.tax = stateArgs['State Tax']

class Country(object):
    """Create a country object"""

    def __init__(self, countryArgs):
        self.ID = countryArgs['Country ID']
        self.name = countryArgs['Country Name']

class OrderType(object):
    """Create an OrderType object"""
    def __init__(self, orderTypeArgs):
        self.orderTypeID = orderTypeArgs['Order Type ID']
        self.name = orderTypeArgs['Order Type Name']

class TransactionType(object):
    """Create a Transaction Type object"""
    def __init__(self, transactionTypeArgs):
        self.ID = transactionTypeArgs['Transaction Type ID']
        self.name = transactionTypeArgs['Transaction Type Name']

class Status(object):
    """Create a Status object"""
    def __init__(self, statusArgs):
        self.ID = statusArgs['Status ID']
        self.name = statusArgs['Status Name']

class ShippingType(object):
    """Create a Shipping Type object"""
    def __init__(self, shippingTypeArgs):
        self.ID = shippingTypeArgs['Shipping Type ID']
        self.name = shippingTypeArgs['Shipping Type Name']

class OrderRow(object):
    """Create a datastructure that holds the keys to load individual orders"""
    def __init__(self, rowArgs):
        self.orderID = rowArgs['Order ID']
        self.firstName = rowArgs['First Name']
        self.lastName = rowArgs['Last Name']
        self.orderType = rowArgs['Order Type']
        self.payMethod = rowArgs['Pay Method']
        self.amazonID = rowArgs['Amazon ID']
        self.date = rowArgs['Date']
        self.status = rowArgs['Status']

class CustomerRow(object):
    """Create a datastructure that holds the keys to load individual customers"""
    def __init__(self, rowArgs):
        self.customerID = rowArgs['Customer ID']
        self.firstName = rowArgs['First Name']
        self.lastName = rowArgs['Last Name']
        self.email = rowArgs['Email']
        self.phone = rowArgs['Phone']
        self.date = rowArgs['Date']


