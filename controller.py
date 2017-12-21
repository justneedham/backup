from view import *
import mysql.connector
import sys, os
from collections import OrderedDict
from mysql.connector import Error

###################  Auxillary and helper functions  ###################

def connect():
    """Connect to the MySQL Database"""
    try:
        connection = mysql.connector.connect(
            host='35.197.44.156',
            database='alexandriabooks',
            user='Justin Needham',
            password='DeoJuvante',
        )
        if connection.is_connected():
            print("Successfully connected Alexandria Books")
            return connection
    except Error as e:
        print("Unable to connect to the database")
        print(e)

def clear():
    """Clear Screen"""
    os.system('Cls' if os.name == 'nt' else 'clear')

def unpack(results):
    """Unpacks the results of fetchall() into a local list"""
    temp = []
    list = []
    for result in results:
        temp.append(result.fetchall())
    for x in temp:
        for y in x:
            list.append(y)
    return list

##########################################################################

def updateOrder(order):
    cur = connection.cursor()
    cur.callproc('show_order_keys', [order.ID])
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:

        order.connection = connection
        order.ID = result[0]
        order.customer = loadCustomer(result[1])
        order.orderType = loadOrderType(result[2])
        order.transaction = loadTransactionType(result[3])
        order.amazonOrder = loadAmazonOrder(result[4])
        order.date = result[5]
        order.status = loadStatus(result[6])
        order.promotion = result[7]
        order.shipping = loadShipping(result[0])
        order.books = loadOrderItems(result[0], result[2])

def loadData():
    data = {}
    print('Loading database...')
    data['Orders'] = loadOrders()
    data['Customers'] = loadCustomers()

    return data

def loadOrders():
    """Calls the database for all orders and related tables and instantiates them into their respective classes"""
    orders = []
    cur = connection.cursor()
    cur.callproc('show_all_order_keys')
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:

        orderData = {}
        orderData['Connection'] = connection
        orderData['Order ID'] = result[0]
        orderData['Customer'] = loadCustomer(result[1])
        orderData['Order Type'] = loadOrderType(result[2])
        orderData['Transaction'] = loadTransactionType(result[3])
        orderData['Amazon Order'] = loadAmazonOrder(result[4])
        orderData['Order Date'] = result[5]
        orderData['Status'] = loadStatus(result[6])
        orderData['Promotion Code'] = result[7]
        orderData['Shipping'] = loadShipping(result[0])
        orderData['Books'] = loadOrderItems(result[0], result[2], result[6])
        print('Order ID {}, Amazon ID {}'.format(orderData['Order ID'], orderData['Amazon Order']))
        orders.append(Order(orderData))

    return orders

def loadStatus(statusID):
    cur = connection.cursor()
    cur.callproc('show_status', [statusID])
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:
        statusData = {}
        statusData['Status ID'] = result[0]
        statusData['Status Name'] = result[1]
        return Status(statusData)

def loadTransactionType(transactionID):
    cur = connection.cursor()
    cur.callproc('show_transaction_type', [transactionID])
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:
        transactionTypeData = {}
        transactionTypeData['Transaction Type ID'] = result[0]
        transactionTypeData['Transaction Type Name'] = result[1]
        return TransactionType(transactionTypeData)

def loadTransactionTypeByName(transactionTypeName):
    cur = connection.cursor()
    cur.callproc('show_transaction_type_keys_by_name', [transactionTypeName])
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:
        transactionTypeData = {}
        transactionTypeData['Transaction Type ID'] = result[0]
        transactionTypeData['Transaction Type Name'] = result[1]
        return TransactionType(transactionTypeData)

def loadOrderType(orderTypeID):
    cur = connection.cursor()
    cur.callproc('show_order_type', [orderTypeID])
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:
        orderTypeData = {}
        orderTypeData['Order Type ID'] = result[0]
        orderTypeData['Order Type Name'] = result[1]
        return OrderType(orderTypeData)

def loadOrderTypeByName(orderTypeName):
    cur = connection.cursor()
    cur.callproc('show_order_type_keys_by_name', [orderTypeName])
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:
        orderTypeData = {}
        orderTypeData['Order Type ID'] = result[0]
        orderTypeData['Order Type Name'] = result[1]
        return OrderType(orderTypeData)

def loadAmazonOrder(amazonID):
    cur = connection.cursor()
    cur.callproc('show_amazon_order', [amazonID])
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:
        amazonData = {}
        amazonData['Connection'] = connection
        amazonData['Amazon ID'] = result[0]
        amazonData['Amazon Key'] = result[1]
        amazonData['Ship By'] = result[2]
        amazonData['Deliver By'] = result[3]
        return Amazon_Order(amazonData)

def loadOrderItems(orderID, orderTypeID, statusID):
    cur = connection.cursor()
    if orderTypeID == 1:
        cur.callproc('show_sell_order_items', [orderID])

    elif orderTypeID == 2 and statusID == 2:
        cur.callproc('show_buy_order_items_shipping', [orderID])

    elif orderTypeID == 2:
        cur.callproc('show_buy_order_items', [orderID])

    else:
        print('Load Order Items Error: {}'.format(str(orderTypeID)))
        pass

    results = cur.stored_results()
    unpackedResults = unpack(results)
    orderItemsList = []

    for result in unpackedResults:
        orderItemData = {}
        orderItemData['Item Number'] = result[0]
        orderItemData['Title'] = result[1]
        orderItemData['Author First'] = result[2]
        orderItemData['Author Last'] = result[3]
        orderItemData['Edition'] = result[4]
        orderItemData['ISBN'] = result[5]
        orderItemData['Condition'] = result[6]
        orderItemData['Price'] = result[7]
        orderItemsList.append(Order_Item(orderItemData))

    return orderItemsList

def loadShipping(orderID):
    cur = connection.cursor()
    cur.callproc('show_shipping_keys', [orderID])
    results = cur.stored_results()
    unpackedResults = unpack(results)
    shippingDataList = []

    for result in unpackedResults:
        shippingData = {}
        shippingData['Connection'] = connection
        shippingData['Shipping ID'] = result[0]
        shippingData['Order ID'] = result[1]
        shippingData['Shipping Cost'] = result[2]
        shippingData['Tracking'] = result[3]
        shippingData['Shipping Date'] = result[4]
        shippingData['Expected Arrival'] = result[5]
        shippingData['Shipping Type'] = loadShippingType(result[6])
        shippingData['Status'] = loadStatus(result[7])
        shippingData['Shipping Materials'] = loadShippingMaterials(result[0])
        shippingDataList.append(Shipping_Order(shippingData))

    return shippingDataList

def loadShippingType(shippingTypeID):
    cur = connection.cursor()
    cur.callproc('show_shipping_type', [shippingTypeID])
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:
        shipTypeData = {}
        shipTypeData['Shipping Type ID'] = result[0]
        shipTypeData['Shipping Type Name'] = result[1]
        return ShippingType(shipTypeData)

def loadShippingMaterials(shippingID):
    cur = connection.cursor()
    cur.callproc('show_shipping_materials', [shippingID])
    results = cur.stored_results()
    unpackedResults = unpack(results)
    shippingMaterialList = []

    for result in unpackedResults:
        shippingMaterialData = {}
        shippingMaterialData['Shipping ID'] = result[0]
        shippingMaterialData['Size'] = result[1]
        shippingMaterialData['Type'] = result[2]
        shippingMaterialList.append(Shipping_Material(shippingMaterialData))

    return shippingMaterialList

def loadCustomer(customerID):
    cur = connection.cursor()
    cur.callproc('show_customer_keys', [customerID])
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:

        customerData = {}
        customerData['Connection'] = connection
        customerData['Customer ID'] = result[0]
        customerData['First Name'] = result[1]
        customerData['Last Name'] = result[2]
        customerData['Phone Number'] = result[3]
        customerData['Email'] = result[4]
        customerData['Date Joined'] = result[5]
        customerData['Referral Code'] = result[6]
        return Customer(customerData)

def loadCustomers():
    """Calls the database for all customers and instantiates them into classes and returns a list of objects"""
    customers = []
    cur = connection.cursor()
    cur.callproc('show_all_customer_keys')
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:

        customerArgs = {}
        customerArgs['Connection'] = connection
        customerArgs['Customer ID'] = result[0]
        customerArgs['First Name'] = result[1]
        customerArgs['Last Name'] = result[2]
        customerArgs['Phone Number'] = result[3]
        customerArgs['Email'] = result[4]
        customerArgs['Date Joined'] = result[5]
        customerArgs['Referral Code'] = result[6]
        customers.append(Customer(customerArgs))

    return customers

def loadAddress(addressID):
    cur = connection.cursor()
    cur.callproc('show_address_keys', [addressID])
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:

        addressData = {}
        addressData['Connection'] = connection
        addressData['Address ID'] = result[0]
        addressData['Customer ID'] = result[1]
        addressData['Building Number'] = result[2]
        addressData['Street Number'] = result[3]
        addressData['City'] = result[4]
        addressData['State'] = loadState(result[5])
        addressData['Zip Code'] = result[6]
        addressData['Country'] = loadCountry(result[7])
        return Address(addressData)

def loadState(stateID):
    cur = connection.cursor()
    cur.callproc('show_state_keys', [stateID])
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:
        stateData = {}
        stateData['State ID'] = result[0]
        stateData['State Name'] = result[1]
        stateData['State Tax'] = result[2]
        return State(stateData)

def loadStateByName(stateName):
    cur = connection.cursor()
    cur.callproc('show_state_keys_by_name', [stateName])
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:
        stateData = {}
        stateData['State ID'] = result[0]
        stateData['State Name'] = result[1]
        stateData['State Tax'] = result[2]
        return State(stateData)

def loadCountry(countryID):
    cur = connection.cursor()
    cur.callproc('show_country_keys', [countryID])
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:
        countryData = {}
        countryData['Country ID'] = result[0]
        countryData['Country Name'] = result[1]
        return Country(countryData)

def loadCountryByName(countryName):
    cur = connection.cursor()
    cur.callproc('show_country_keys_by_name', [countryName])
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:
        countryData = {}
        countryData['Country ID'] = result[0]
        countryData['Country Name'] = result[1]
        return Country(countryData)

def loadStatusByName(statusName):
    cur = connection.cursor()
    cur.callproc('show_status_keys_by_name', [statusName])
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:
        statusData = {}
        statusData['Status ID'] = result[0]
        statusData['Status Name'] = result[1]
        return Status(statusData)

def loadShipTypeByName(shipTypeName):
    cur = connection.cursor()
    cur.callproc('show_ship_type_keys_by_name', [shipTypeName])
    results = cur.stored_results()
    unpackedResults = unpack(results)

    for result in unpackedResults:
        shipTypeData = {}
        shipTypeData['Shipping Type ID'] = result[0]
        shipTypeData['Shipping Type Name'] = result[1]
        return ShippingType(shipTypeData)

def getCustomer(choice):
    data = {}
    customer = None
    for x in data['Customers']:
        if str(x.ID) == choice:
            customer = x
        else:
            continue
    return customer

def getOrder(choice):
    data = {}
    order = None
    for x in data['Orders']:
        if str(x.ID) == choice:
            order = x
        else:
            continue
    return order

def addAddress():
    """Add an address to an existing customer"""
    clear()

    print("\nEnter the id of the customer to add an address to\n")
    choice = input('> ')
    customer = getCustomer(choice)

    if customer != None:
        house = input('House: > ')
        street = input('Street: > ')
        city = input('City: > ')
        state = input('State: > ')
        zipCode = input('Zip: > ')
        country = input('Country: > ')
        addressID = ''

        addressArgs = {}
        addressArgs['Connection'] = connection
        addressArgs['Building Number'] = house
        addressArgs['Street Number'] = street
        addressArgs['City'] = city
        addressArgs['State'] = loadStateByName(state)
        addressArgs['Zip Code'] = zipCode
        addressArgs['Country'] = loadCountryByName(country)
        addressArgs['Address ID'] = addressID

        customer.address = Address(addressArgs)
        customer.add_address()

def addShipping():
    """Add shipping to an existing order"""

    print('\n Enter the number of the order you want to add shipping to')
    choice = input('> ')

    order = getOrder(choice)

    shippingCost = 13.50
    tracking = 'abcdefg'
    expectedArrival = ('2017', '1', '28')
    shipType = 'Sell Books'
    status = 'Processing'
    shippingMaterialsData = [{'Type': 'Box', 'Size': 'Large'}, {'Type': 'Box', 'Size': 'Medium'}]

    shippingArgs = {}
    shippingArgs['Connection'] = connection
    shippingArgs['Order ID'] = order.ID
    shippingArgs['Shipping Cost'] = shippingCost
    shippingArgs['Tracking'] = tracking
    shippingArgs['Expected Arrival'] = expectedArrival
    shippingArgs['Shipping Type'] = loadShipTypeByName(shipType)
    shippingArgs['Status'] = loadStatusByName(status)
    shippingArgs['Shipping Materials'] = shippingMaterialsData
    order.shipping.append(Shipping_Order(shippingArgs).insert_shipping())

    updateOrder(order)

def addPhone():
    """Add a phone number to an existing customer"""
    clear()


    print("\nEnter the id of the customer to add a phone number to\n")
    choice = input('> ')
    customer = getCustomer(choice)

    if customer != None:
        phoneNumber = input('Phone Number: > ')
        customer.add_phoneNumber(phoneNumber)

def addEmail():
    """Add an email to an existing customer"""
    clear()


    print("\nEnter the id of the customer to add an email to\n")
    choice = input('> ')
    customer = getCustomer(choice)

    if customer != None:
        email = input('Email: > ')
        customer.add_email(email)

def addBuyOrder():
    """Add a buy order to the database"""
    data = []
    firstName = input('First Name: >')
    lastName = input('Last Name: >')
    promotionCode = input('Referral Code: >')

    orderType = 'Buy Books'
    transactionType = 'Paypal'
    status = 'Processing'
    books = [{'Item Number': '1', 'Title': 'The Prince', 'Author First': None, 'Author Last': None, 'Edition': None, 'ISBN': None, 'Condition': 'New', 'Price': None},
             {'Item Number': '2', 'Title': 'Atlas Shrugged','Author First': None, 'Author Last': None, 'Edition': None, 'ISBN': None, 'Condition': 'New', 'Price': None},
             {'Item Number': '3', 'Title': 'Zero To One', 'Author First': None, 'Author Last': None, 'Edition': None, 'ISBN': None, 'Condition': 'New', 'Price': None}]

    customerData = {}
    customerData['Connection'] = connection
    customerData['Customer ID'] = None
    customerData['First Name'] = firstName
    customerData['Last Name'] = lastName
    customerData['Phone Number'] = None
    customerData['Email'] = None
    customerData['Address'] = None
    customerData['Date Joined'] = None
    customerData['Referral Code'] = None

    amazonInput = input('Amazon order? >').lower().strip()

    if amazonInput == 'yes':
        amazonOrderData = {}
        amazonOrderData['Connection'] = connection
        amazonOrderData['Amazon ID'] = None
        amazonOrderData['Ship By'] = ('2017', '09', '01')
        amazonOrderData['Deliver By'] = ('2017', '12', '01')
        amazonOrderData['Amazon Key'] = 'AmazonKey123'
    else:
        amazonOrderData = None

    buyOrderArgs = {}
    buyOrderArgs['Connection'] = connection
    buyOrderArgs['Order ID'] = None
    buyOrderArgs['Customer'] = Customer(customerData)
    buyOrderArgs['Order Type'] = loadOrderTypeByName(orderType)
    buyOrderArgs['Transaction'] = loadTransactionTypeByName(transactionType)
    if amazonOrderData == None:
        buyOrderArgs['Amazon Order'] = None
    else:
        buyOrderArgs['Amazon Order'] = Amazon_Order(amazonOrderData)
    buyOrderArgs['Order Date'] = None
    buyOrderArgs['Status'] = loadStatusByName(status)
    buyOrderArgs['Shipping'] = None
    buyOrderArgs['Promotion Code'] = promotionCode
    buyOrderArgs['Books'] = []

    for book in books:
        bookItem = Order_Item(book)
        buyOrderArgs['Books'].append(bookItem)

    newOrder = Order(buyOrderArgs)
    newOrder.insert_order()
    updateOrder(newOrder)
    data['Orders'].append(newOrder)
    data['Customers'] = loadCustomers()

def addSellOrder():
    """Add a sell order to the database"""
    data = []
    orderType = 'Sell Books'
    transactionType = 'Paypal'
    status = 'Processing'
    books = [{'Item Number': '1',
              'Title': 'Naked Economics',
              'Author First': 'Charles',
              'Author Last': 'Wheelan',
              'Edition': None,
              'ISBN': '9780753555198',
              'Condition': None,
              'Price': None}]

    customerData = {}
    customerData['Connection'] = connection
    customerData['Customer ID'] = None
    customerData['First Name'] = 'Amber'
    customerData['Last Name'] = 'Heard'
    customerData['Phone Number'] = None
    customerData['Email'] = None
    customerData['Address'] = None
    customerData['Date Joined'] = None
    customerData['Referral Code'] = None

    sellOrderArgs = {}
    sellOrderArgs['Connection'] = connection
    sellOrderArgs['Order ID'] = None
    sellOrderArgs['Customer'] = Customer(customerData)
    sellOrderArgs['Order Type'] = loadOrderTypeByName(orderType)
    sellOrderArgs['Transaction'] = loadTransactionTypeByName(transactionType)
    sellOrderArgs['Amazon Order'] = None
    sellOrderArgs['Order Date'] = None
    sellOrderArgs['Status'] = loadStatusByName(status)
    sellOrderArgs['Shipping'] = None
    sellOrderArgs['Promotion Code'] = None
    sellOrderArgs['Books'] = []

    for book in books:
        bookItem = Order_Item(book)
        sellOrderArgs['Books'].append(bookItem)

    newOrder = Order(sellOrderArgs)
    newOrder.insert_order()
    updateOrder(newOrder)
    data['Orders'].append(newOrder)
    data['Customers'] = loadCustomers()

def moveOrderToHistory():
    """Move order to archives"""
    orderID = input('Enter order ID: > ')
    cur = connection.cursor()
    cur.callproc('move_to_orders_history', [orderID])
    connection.commit()

def addQuote():

    orderID = input('Enter the order ID: > ')

    itemNumber = input('Enter the item number: > ')
    condition = input('Enter the condition: > ')
    price = input('Enter the price: > ')
    order = getOrder(orderID)
    orderItem = getOrderItem(order, itemNumber)

    quoteArgs = {}
    quoteArgs['Order ID'] = order.ID
    quoteArgs['Connection'] = connection
    quoteArgs['Condition'] = condition
    quoteArgs['Price'] = price

    orderItem.addQuote(quoteArgs)

def getOrderItem(order, itemNumber):

    orderItem = None
    for item in order.books:
        if str(item.itemNumber) == itemNumber:
            orderItem = item
    if orderItem != None:
        return orderItem
    else:
        print("Unable to find item number {} in order {}".format(itemNumber, order.ID))

class Controller(object):
    def __init__(self):
        self.loadData()
        self.mainWindow = MainWindow(self.data, self)

    def loadData(self):
        self.data = {
            'Views': {'Orders': self.loadOrderView(), 'Customers': self.loadCustomersView()},
            'Data': {'Orders': [], 'Customers': []}
        }

    def loadOrderView(self):
        rows = []
        cur = connection.cursor()
        cur.callproc('show_orders_list')
        results = cur.stored_results()
        unpackedResults = unpack(results)

        for result in unpackedResults:
            rowArgs = {}
            print(result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7])
            rowArgs['Order ID'] = result[0]
            rowArgs['First Name'] = result[1]
            rowArgs['Last Name'] = result[2]
            rowArgs['Order Type'] = result[3]
            rowArgs['Pay Method'] = result[4]
            rowArgs['Amazon ID'] = result[5]
            rowArgs['Date'] = result[6]
            rowArgs['Status'] = result[7]
            rows.append(OrderRow(rowArgs))

        return rows

    def loadCustomersView(self):
        rows = []
        cur = connection.cursor()
        cur.callproc('show_customers_list')
        results = cur.stored_results()
        unpackedResults = unpack(results)

        for result in unpackedResults:
            rowArgs = {}
            print(result[0], result[1], result[2], result[3], result[4], result[5])
            rowArgs['Customer ID'] = result[0]
            rowArgs['First Name'] = result[1]
            rowArgs['Last Name'] = result[2]
            rowArgs['Email'] = result[3]
            rowArgs['Phone'] = result[4]
            rowArgs['Date'] = result[5]
            rows.append(CustomerRow(rowArgs))

        return rows

    def load_order(self, orderID):
        """Calls the database to load a specific order with orderID"""
        cur = connection.cursor()
        cur.callproc('show_order_keys', [orderID])
        results = cur.stored_results()
        unpackedResults = unpack(results)

        for result in unpackedResults:
            orderData = {}
            orderData['Connection'] = connection
            orderData['Order ID'] = result[0]
            orderData['Customer'] = loadCustomer(result[1])
            orderData['Order Type'] = loadOrderType(result[2])
            orderData['Transaction'] = loadTransactionType(result[3])
            orderData['Amazon Order'] = loadAmazonOrder(result[4])
            orderData['Order Date'] = result[5]
            orderData['Status'] = loadStatus(result[6])
            orderData['Promotion Code'] = result[7]
            orderData['Shipping'] = loadShipping(result[0])
            orderData['Books'] = loadOrderItems(result[0], result[2], result[6])
            return Order(orderData)

    def add_order(self, order):
        order.connection = connection
        order.customer.connection = connection
        order.insert_order()

    def add_quote(self, orderItemObject):
        """Takes an orderItemObject from the MainWindow and updates the database"""
        cur = connection.cursor()
        cur.callproc('add_quote', [orderItemObject.itemNumber, orderItemObject.condition, Decimal(orderItemObject.price)])
        connection.commit()
        cur.close()

    def add_amazon_order(self, amazonOrderArgs):
        """Takes the amazon order args and updates the database"""
        shipByDateList = amazonOrderArgs['Ship By'].split('/')
        deliverByDateList = amazonOrderArgs['Deliver By'].split('/')
        shipByDay = shipByDateList[1]
        shipByMonth = shipByDateList[0]
        shipByYear = shipByDateList[2]
        deliverByDay = deliverByDateList[1]
        deliverByMonth = deliverByDateList[0]
        deliverByYear = deliverByDateList[2]
        cur = connection.cursor()
        cur.callproc('insert_amazon_order', [amazonOrderArgs['Amazon Key'], shipByYear, shipByMonth, shipByDay, deliverByYear, deliverByMonth, deliverByDay, ''])
        connection.commit()
        results = cur.stored_results()
        unpackedResults = unpack(results)

        for result in unpackedResults:
            amazonID = result[7]
        self.update_order_amazon_ID()
        cur.close()

    def update_order_amazon_ID(self, orderID, amazonID):
        """Called when inserting an amazon order, updates the orders table with the amazon id"""
        cur = connection.cursor()
        cur.callproc('update_order_amazon_id', [orderID, amazonID])
        connection.commit()
        cur.close()

    def update_order_status(self, orderID, status):
        """Takes an order ID and status string and updates the database"""
        cur = connection.cursor()
        cur.callproc('update_order_status', [orderID, status])
        connection.commit()
        cur.close()

    def add_shipping(self, shippingObject):
        """Take the shipping object and updates the database"""
        shippingObject.connection = connection
        shippingObject.insert_shipping()

    def add_address(self, addressObject):
        """Takes the address object and updates the database"""
        addressObject.connection = connection
        addressObject.insert_address()

    def add_book_to_inventory(self, orderItem):
        """Takes an order item and inserts it into the database"""
        cur = connection.cursor()
        cur.callproc('insert_inventory', [orderItem.title, orderItem.authorFirst, orderItem.authorLast, orderItem.edition, orderItem.ISBN, orderItem.price, 'Provo', orderItem.condition])
        connection.commit()
        cur.close()

    def remove_book_from_inventory(self, orderItem):
        """Takes an order item and removes it from the inventory table"""
        cur = connection.cursor()
        cur.callproc('remove_book_from_inventory', [orderItem.ISBN, orderItem.condition, 'Salt Lake'])
        connection.commit()
        cur.close()

    def get_current_price(self, orderItem):
        """Call the database for the current price of an orderItem"""
        cur = connection.cursor()
        cur.callproc('get_current_price_by_ISBN', [orderItem.ISBN, ''])
        connection.commit()
        results = cur.stored_results()
        unpackedResults = unpack(results)

        for result in unpackedResults:
            return result[1]

    def refresh_data(self):
        """Reloads all the data and sends it back to the view"""
        self.data = {}
        self.data['Orders'] = loadOrders()
        self.data['Customers'] = loadCustomers()
        return self.data

    def move_to_history(self, order):
        """Calls the database to move the order and all supporting columns into the archives"""
        cur = connection.cursor()
        cur.callproc('move_to_orders_history', [order.ID])
        connection.commit()
        cur.close()



if __name__ == '__main__':
    connection = connect()
    app = QApplication(sys.argv)
    Alexandria = Controller()
    Alexandria.mainWindow.show()
    sys.exit(app.exec_())



