from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QMainWindow, QVBoxLayout, QGridLayout, QGroupBox, \
    QStackedWidget, QLabel, QLineEdit, QComboBox, QScrollArea, QDialog, QSizePolicy, QCheckBox
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QColor
from model import *

class MainWindow(QMainWindow):
    def __init__(self, data, controller, parent=None):
        """Create a new instance of the main window"""
        super(MainWindow, self).__init__(parent)
        self.data = data
        self.controller = controller
        self.centralWidget = QGroupBox()

        self.mainWindowPalatte = self.palette()
        self.mainWindowPalatte.setColor(self.mainWindowPalatte.Window, Qt.white)
        self.setPalette(self.mainWindowPalatte)
        self.setAutoFillBackground(True)

        self.setCentralWidget(self.centralWidget)
        self.showFullScreen()
        self.build_main_window()

    def build_main_window(self):
        """Puts the menu and viewWindow widgets together"""
        self.build_viewWindow()
        self.build_menu()

        self.layout = QGridLayout()
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,4)
        self.layout.addWidget(self.menu.widget, 0, 0)
        self.layout.addWidget(self.viewWindow.centralWidget, 0, 1)
        self.centralWidget.setLayout(self.layout)

    def build_viewWindow(self):
        """Create a new instance of the viewWindow widget"""
        self.viewWindow = ViewWindow(self.data, self)

    def build_menu(self):
        """Create a new instance of the menu widget"""
        self.menu = Menu(self)

    def rebuild_menu(self):
        """Delete the layout of the central widgets and rebuilds"""
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

        self.build_viewWindow()
        self.build_menu()
        self.layout.addWidget(self.menu.widget, 0, 0)
        self.layout.addWidget(self.viewWindow.centralWidget, 0, 1)
        self.layout.update()

    def load_order(self, orderID):
        """Calls the controller to load an order with the orderID"""
        return self.controller.load_order(orderID)

    def refresh_data(self):
        """Button method that calls controller to refresh data and update the application"""
        self.data = self.controller.refresh_data()
        self.rebuild_menu()

    def add_order_to_database(self, order):
        """Button method that accepts raw data and pushes it to the controller"""
        self.controller.add_order(order)

    def add_quote(self, orderItemObject):
        """Takes an orderItemObject and calls the controller to update it with quote"""
        self.controller.add_quote(orderItemObject)

    def update_order_status(self, orderID, status):
        """Takes the order ID and a status string and calls the controller to update the database"""
        self.controller.update_order_status(orderID, status)

    def add_shipping(self, shippingObject):
        """Takes the shipping object and calls the controller to update the database"""
        self.controller.add_shipping(shippingObject)

    def add_address(self, addressObject):
        """Takes the address object and calls the controller to update the database"""
        self.controller.add_address(addressObject)

    def add_book_to_inventory(self, orderItem):
        """Takes an order Item and inserts into the inventory table"""
        self.controller.add_book_to_inventory(orderItem)

    def remove_book_from_inventory(self, orderItem):
        """Takes and order Item and removes it from the inventory table"""
        self.controller.remove_book_from_inventory(orderItem)

    def move_to_history(self, order):
        """Calls the controller to move order and all supporting rows into the archive"""
        self.controller.move_to_history(order)

    def show_orders(self):
        """Button method that calls ViewWindow to display orders"""
        self.viewWindow.show_orders()

    def show_order_detail(self):
        self.viewWindow.show_order_detail()

    def show_customers(self):
        """Button method that calls ViewWindow to display customers"""
        self.viewWindow.show_customers()

    def show_customer_detail(self):
        """Button method that calls ViewWindow to display customer detail"""
        self.viewWindow.show_customer_detail()

    def show_buy_order_form(self):
        """Button method that calls ViewWindow to display the buy order form"""
        self.viewWindow.show_buy_order_form()

    def show_sell_order_form(self):
        """Button method that calls ViewWindow to display the sell order form"""
        self.viewWindow.show_sell_order_form()

class ViewWindow(QMainWindow):
    def __init__(self, data, mainWindow):
        """Create an instance of ViewWindow which holds all the windows"""
        super().__init__()
        self.data = data
        self.mainWindow = mainWindow
        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)
        self.orders = OrdersListWindow(self.data, self.mainWindow)
        self.customers = CustomersWindow(self.data)
        self.customerDetail = CustomerDetailWindow()
        self.addBuyOrder = AddBuyOrderWindow(self.mainWindow)
        self.addSellOrder = AddSellOrderWindow(self.mainWindow)
        self.currentOrderDetailWidget = None

        self.centralWidget.addWidget(self.orders)
        self.centralWidget.addWidget(self.customers)
        self.centralWidget.addWidget(self.customerDetail)
        self.centralWidget.addWidget(self.addBuyOrder)
        self.centralWidget.addWidget(self.addSellOrder)

        self.centralWidget.setCurrentWidget(self.orders)

    def show_orders(self):
        self.centralWidget.setCurrentWidget(self.orders)

    def show_customers(self):
        self.centralWidget.setCurrentWidget(self.customers)

    def show_customer_detail(self):
        self.centralWidget.setCurrentWidget(self.customerDetail)

    def show_order_detail(self):
        self.centralWidget.addWidget(self.orders.orderDetailWindow)
        self.centralWidget.setCurrentWidget(self.orders.orderDetailWindow)

    def show_buy_order_form(self):
        self.centralWidget.setCurrentWidget(self.addBuyOrder)

    def show_sell_order_form(self):
        self.centralWidget.setCurrentWidget(self.addSellOrder)

class Menu(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.widget = QGroupBox()
        self.mainWindow = mainWindow
        self.orderBtn = Button('Orders', self.mainWindow.show_orders)
        self.customersBtn = Button('Customers', self.mainWindow.show_customers)
        self.customerDetailBtn = Button('Customer Detail', self.mainWindow.show_orders)
        self.addBuyOrderBtn = Button('Add Buy Order', self.mainWindow.show_buy_order_form)
        self.addSellOrderBtn = Button('Add Sell Order', self.mainWindow.show_sell_order_form)
        self.refreshBtn = Button('Refresh', self.mainWindow.refresh_data)

        self.menuPalatte = self.widget.palette()
        self.menuPalatte.setColor(self.menuPalatte.Window, Qt.gray)
        self.widget.setPalette(self.menuPalatte)
        self.widget.setAutoFillBackground(True)

        layout = QVBoxLayout()
        layout.addWidget(self.orderBtn.widget)
        layout.addWidget(self.customersBtn.widget)
        layout.addWidget(self.customerDetailBtn.widget)
        layout.addWidget(self.addBuyOrderBtn.widget)
        layout.addWidget(self.addSellOrderBtn.widget)
        layout.addWidget(self.refreshBtn.widget)
        self.widget.setLayout(layout)

class CustomersWindow(QWidget):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.window = QVBoxLayout()
        self.parent = parent
        self.rows = 1

        layout = QGridLayout()
        titleBox = QGroupBox()
        titleBox.setFixedHeight(60)
        titleLayout = QGridLayout()
        titleLayout.addWidget(QLabel('Customer ID'), 0, 0)
        titleLayout.addWidget(QLabel('First Name'), 0, 1)
        titleLayout.addWidget(QLabel('Last Name'), 0, 2)
        titleLayout.addWidget(QLabel('Phone'), 0, 3)
        titleLayout.addWidget(QLabel('Email'), 0, 4)
        titleLayout.addWidget(QLabel('Account Created'), 0, 5)
        self.rows = 1
        titleBox.setLayout(titleLayout)
        layout.addWidget(titleBox)

        if self.data != None:

            for row in self.data['Views']['Customers']:
                button = LinkCustomerButton(str(row.customerID), self)
                subBox = QGroupBox()
                subBox.setFixedHeight(60)
                subLayout = QGridLayout()
                subLayout.addWidget(button, 0, 0)
                subLayout.addWidget(QLabel(row.firstName), 0, 1)
                subLayout.addWidget(QLabel(row.lastName), 0, 2)
                if row.phone != None:
                    subLayout.addWidget(QLabel(row.phone), 0, 3)
                else:
                    subLayout.addWidget(QLabel('None'), 0, 3)
                if row.email != None:
                    subLayout.addWidget(QLabel(row.email), 0, 4)
                else:
                    subLayout.addWidget(QLabel('None'), 0, 4)
                subLayout.addWidget(QLabel(str(row.date)), 0, 5)
                self.rows += 1
                subBox.setLayout(subLayout)
                layout.addWidget(subBox, self.rows, 0, 1, 0)

        layout.setAlignment(Qt.AlignTop)

        self.setLayout(layout)

    def updateData(self, data):
        self.data = data

class OrderFormWindow(QWidget):
    def __init__(self, mainWindow):
        """Initializes an AddOrderWindow"""
        super().__init__()
        self.mainWindow = mainWindow
        self.count = 8
        self.bookEntries = []
        self.build_add_order_window()

    def build_add_order_window(self):
        """Builds the add order window"""
        self.layout = QGridLayout()
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)

        self.build_widgets()

        self.layout.addWidget(QLabel('First Name:'), 0, 0)
        self.layout.addWidget(self.firstNameEdit.widget, 0, 1)
        self.layout.addWidget(QLabel('Last Name:'), 1, 0)
        self.layout.addWidget(self.lastNameEdit.widget, 1, 1)
        self.layout.addWidget(QLabel('Email:'), 2, 0)
        self.layout.addWidget(self.emailEdit.widget, 2, 1)
        self.layout.addWidget(QLabel('Phone:'), 3, 0)
        self.layout.addWidget(self.phoneEdit.widget, 3, 1)
        self.layout.addWidget(QLabel('Pay Method'), 4, 0)
        self.layout.addWidget(self.payCombo.widget, 4, 1)
        self.layout.addWidget(QLabel('Order Type:'), 5, 0)
        self.layout.addWidget(QLabel('Referral Code:'), 6, 0)
        self.layout.addWidget(self.referralEdit.widget, 6, 1)
        self.layout.addWidget(QLabel('Amazon Order:'), 7, 0)
        self.layout.addWidget(self.amazonCheckBox.widget, 7, 1)
        self.layout.addWidget(self.addBookBtn.widget, 9, 0)
        self.layout.addWidget(self.removeBookBtn.widget, 10, 0)
        self.layout.addWidget(self.submitBtn.widget, 11, 0)

        self.layout.setAlignment(Qt.AlignTop)

        self.setLayout(self.layout)

    def build_widgets(self):
        """Builds the widgets for the main window"""
        self.build_buttons()
        self.build_combo_boxes()
        self.build_line_edits()
        self.build_check_boxes()

    def build_combo_boxes(self):
        """Builds the combo box widgets"""
        self.payCombo = ComboBox(['Paypal', 'Square Cash', 'Venmo', 'Cash'])

    def build_line_edits(self):
        """Builds the line edit widgets"""
        self.firstNameEdit = LineEdit()
        self.lastNameEdit = LineEdit()
        self.referralEdit = LineEdit()
        self.emailEdit = LineEdit()
        self.phoneEdit = LineEdit()

    def build_buttons(self):
        """Builds the buttons widgets"""
        self.addBookBtn = Button('Add Book', self.add_book)
        self.removeBookBtn = Button('Remove Book', self.remove_book)
        self.submitBtn = Button('Submit', self.confirm)

    def build_check_boxes(self):
        """Builds the check box widgets"""
        self.amazonCheckBox = CheckBox(self)

    def capture(self):
        """Captures all the input in the confirmation window"""
        self.firstName = self.firstNameEdit.capture()
        self.lastName = self.lastNameEdit.capture()
        self.referral = self.referralEdit.capture()
        self.transactionTypeName = self.payCombo.capture()
        self.email = self.emailEdit.capture()
        self.phone = self.phoneEdit.capture()

        if self.email == '':
            self.email = None

        if self.phone == '':
            self.phone = None

        if self.amazonWidget != None:
            self.amazonWidget.capture()
        else:
            self.amazonArgs = {
                'Ship By': None,
                'Deliver By': None,
                'Amazon Key': None
            }

        for book in self.bookEntries:
            book.capture()

    def convert_bookEntry_to_orderItem(self):
        """Returns a list of orderItems"""
        self.orderItems = []

        for bookEntry in self.bookEntries:
            self.orderItems.append(bookEntry.orderItem)

    def confirm(self):
        """Captures input, builds classes and displays the confirmation window"""
        self.capture()
        self.convert_bookEntry_to_orderItem()

        self.build_customer_object()
        self.build_amazon_order_object()
        self.build_order_type_object()
        self.build_status_type_object()
        self.build_transaction_object()
        self.build_order_object()

        self.confirmationWindow = ConfirmationWindow(self.order, self)
        self.confirmationWindow.show()

    def build_customer_object(self):
        """Builds a customer object"""
        customerArgs = {
            'Customer ID': None,
            'First Name': self.firstName,
            'Last Name': self.lastName,
            'Phone Number': self.phone,
            'Email': self.email,
            'Address': None,
            'Date Joined': None,
            'Referral Code': None,
            'Connection': None
        }
        self.customer = Customer(customerArgs)

    def build_amazon_order_object(self):
        """Builds an amazon order object"""
        if self.amazonWidget != None:

            amazonArgs = {
                'Connection': None,
                'Amazon ID': None,
                'Ship By': self.amazonWidget.shipByDate,
                'Deliver By': self.amazonWidget.deliverByDate,
                'Amazon Key': self.amazonWidget.amazonKey

            }
            self.amazonOrder = Amazon_Order(amazonArgs)
        else:
            self.amazonOrder = None

    def build_order_type_object(self):
        """Builds an order type object"""
        orderTypeArgs = {
            'Order Type ID': None,
            'Order Type Name': self.orderTypeName
        }
        self.orderType = OrderType(orderTypeArgs)

    def build_status_type_object(self):
        """Builds a status type object"""
        statusTypeArgs = {
            'Status ID': None,
            'Status Name': 'Processing'
        }
        self.status = Status(statusTypeArgs)

    def build_transaction_object(self):
        """Builds a transaction type object"""
        transactionTypeArgs ={
            'Transaction Type ID': None,
            'Transaction Type Name': self.transactionTypeName
        }
        self.transactionType = TransactionType(transactionTypeArgs)

    def build_order_object(self):
        """Build an order object"""
        orderArgs = {
            'Connection': None,
            'Order ID': None,
            'Customer': self.customer,
            'Order Type': self.orderType,
            'Transaction': self.transactionType,
            'Amazon Order': self.amazonOrder,
            'Order Date': None,
            'Status': self.status,
            'Promotion Code': self.referral,
            'Shipping': None,
            'Books': self.orderItems
        }
        self.order = Order(orderArgs)

    def submit(self):
        """Passes the outArgs to the controller to be submitted to the database"""
        self.mainWindow.add_order_to_database(self.order)
        self.confirmationWindow.close_window()

    def add_book(self):
        """Creates a BookEntry instance and adds it to the layout"""
        bookForm = BookEntry(self)
        self.bookEntries.append(bookForm)
        self.layout.addWidget(bookForm.widget, self.count, 1)
        self.count += 1
        self.layout.update()

    def remove_book(self):
        """Removes a BookEntry instance and updates the layout"""
        book = self.bookEntries.pop()
        self.layout.removeWidget(book.widget)
        book.widget.deleteLater()
        self.count -= 1
        self.layout.update()

    def display_amazon_order_box(self):
        """Displays a widget with addition information for an amazon order"""
        self.amazonWidget = AmazonWidget()
        self.layout.addWidget(self.amazonWidget.widget, 8, 0)
        self.layout.update()

    def remove_amazon_order_box(self):
        """Removes the amazon order box"""
        self.layout.removeWidget(self.amazonWidget.widget)
        self.amazonWidget.widget.deleteLater()
        self.amazonWidget = None
        self.layout.update()

class AddBuyOrderWindow(OrderFormWindow):
    def __init__(self, mainWindow):
        """Initializes an instance of OrderWindow with the buy widget variations"""
        super().__init__(mainWindow)
        self.orderTypeName = 'Buy Order'
        self.layout.addWidget(QLabel(self.orderTypeName), 5, 1)

    def add_book(self):
        """Creates a BookEntry instance and adds it to the layout"""
        bookForm = BookEntry(self)
        self.bookEntries.append(bookForm)
        self.layout.addWidget(bookForm.widget, self.count, 1)
        self.count += 1
        self.layout.update()


class AddSellOrderWindow(OrderFormWindow):
    def __init__(self, mainWindow):
        """Initializes an instance of OrderWindow with the sell widget variations"""
        super().__init__(mainWindow)
        self.orderTypeName = 'Sell Order'
        self.layout.addWidget(QLabel(self.orderTypeName), 5, 1)

    def add_book(self):
        """Creates a BookEntry instance and adds it to the layout"""
        bookForm = BookEntry(self)
        self.bookEntries.append(bookForm)
        self.layout.addWidget(bookForm.widget, self.count, 1)
        self.count += 1
        self.layout.update()

class AmazonWidget(QWidget):
    def __init__(self, parent=None):
        """Initializes an instance of AmazonWidget"""
        super().__init__()
        self.parent = parent
        self.widget = QGroupBox('')
        self.layout = QGridLayout()
        self.build_amazon_widget()

    def build_widget(self):
        """Builds all the widgets to be added to the layout"""
        self.amazonKeyLbl = Label('Amazon Key')
        self.amazonKeyEdit = LineEdit()
        self.shipByDateLbl = Label('Ship By')
        self.shipByDateEdit = LineEdit()
        self.deliverByDateLbl = Label('Deliver By')
        self.deliverByDateEdit = LineEdit()

    def build_amazon_widget(self):
        """Builds the Amazon Widget"""
        self.build_widget()
        self.layout.addWidget(self.amazonKeyLbl.widget, 0, 0)
        self.layout.addWidget(self.amazonKeyEdit.widget, 0, 1)
        self.layout.addWidget(self.shipByDateLbl.widget, 1, 0)
        self.layout.addWidget(self.shipByDateEdit.widget, 1, 1)
        self.layout.addWidget(self.deliverByDateLbl.widget, 2, 0)
        self.layout.addWidget(self.deliverByDateEdit.widget, 2, 1)
        self.widget.setLayout(self.layout)

    def capture(self):
        """Stores all the input provided into attributes"""
        self.amazonKey = self.amazonKeyEdit.capture()
        self.shipByDate = self.shipByDateEdit.capture()
        self.deliverByDate = self.deliverByDateEdit.capture()

class OrdersListWindow(QGroupBox):
    def __init__(self, data, mainWindow):
        super().__init__()
        self.data = data
        self.mainWindow = mainWindow

        GroupBoxPalette = self.palette()
        GroupBoxPalette.setColor(GroupBoxPalette.Window, Qt.gray)
        self.setPalette(GroupBoxPalette)
        self.setAutoFillBackground(True)

        layout = QGridLayout()
        titleBox = QGroupBox()

        titleBoxPalette = titleBox.palette()
        titleBoxPalette.setColor(titleBoxPalette.Window, Qt.white)
        titleBox.setPalette(titleBoxPalette)
        titleBox.setAutoFillBackground(True)

        titleBox.setFixedHeight(60)
        titleLayout = QGridLayout()
        titleLayout.addWidget(QLabel('ID'), 0, 0)
        titleLayout.addWidget(QLabel('First Name'), 0, 1)
        titleLayout.addWidget(QLabel('Last Name'), 0, 2)
        titleLayout.addWidget(QLabel('Order Type'), 0, 3)
        titleLayout.addWidget(QLabel('Pay Method'), 0, 4)
        titleLayout.addWidget(QLabel('Amazon ID'), 0, 5)
        titleLayout.addWidget(QLabel('Date'), 0, 6)
        titleLayout.addWidget(QLabel('Status'), 0, 7)
        self.rows = 1

        titleBox.setLayout(titleLayout)
        layout.addWidget(titleBox)

        if self.data != None:

            for row in self.data['Views']['Orders']:
                button = LinkOrderButton(str(row.orderID), self)
                subBox = QGroupBox()
                subBoxPalette = subBox.palette()
                subBoxPalette.setColor(subBoxPalette.Window, Qt.white)
                subBox.setPalette(subBoxPalette)
                subBox.setAutoFillBackground(True)

                subBox.setFixedHeight(60)
                sublayout = QGridLayout()
                sublayout.addWidget(button, 0, 0)
                sublayout.addWidget(QLabel(row.firstName), 0, 1)
                sublayout.addWidget(QLabel(row.lastName), 0, 2)
                sublayout.addWidget(QLabel(row.orderType), 0, 3)
                sublayout.addWidget(QLabel(row.payMethod), 0, 4)
                if row.amazonID != None:

                    sublayout.addWidget(QLabel(str(row.amazonID)), 0, 5)
                else:
                    sublayout.addWidget(QLabel('None'), 0, 5)
                sublayout.addWidget(QLabel(str(row.date)), 0, 6)
                sublayout.addWidget(QLabel(row.status), 0, 7)
                subBox.setLayout(sublayout)
                self.rows += 1
                layout.addWidget(subBox, self.rows, 0, 1, 0)

        layout.setAlignment(Qt.AlignTop)

        self.setLayout(layout)

    def show_order_detail_window(self, orderNumber):
        """Shows the specific order detail view dependent on the order status"""
        order = self.load_order(orderNumber)
        if order.orderType.name == 'Sell Order':
            if order.status.name == 'Processing':
                self.orderDetailWindow = SellOrderDetailWindowProcess(order, self.mainWindow)
                self.mainWindow.show_order_detail()
            elif order.status.name == 'Quoted':
                self.orderDetailWindow = SellOrderDetailWindowQuoted(order, self.mainWindow)
                self.mainWindow.show_order_detail()
            elif order.status.name == 'Accepted':
                self.orderDetailWindow = SellOrderDetailWindowAccepted(order, self.mainWindow)
                self.mainWindow.show_order_detail()
            elif order.status.name == 'In-Transit':
                self.orderDetailWindow = SellOrderDetailWindowInTransit(order, self.mainWindow)
                self.mainWindow.show_order_detail()
            elif order.status.name == 'Picked Up':
                self.orderDetailWindow = SellOrderDetailWindowInTransit(order, self.mainWindow)
                self.mainWindow.show_order_detail()
            else:
                print('Sell Order Detail Status Error')

        elif order.orderType.name == 'Buy Order':
            if order.status.name == 'Processing':
                self.orderDetailWindow = BuyOrderDetailWindowProcess(order, self.mainWindow)
                self.mainWindow.show_order_detail()
            elif order.status.name == 'In-Transit':
                self.orderDetailWindow = BuyOrderDetailWindowInTransit(order, self.mainWindow)
                self.mainWindow.show_order_detail()
            else:
                print('Buy Order Detail Status Error')
        else:
            print('Order Detail Window Error')

    def load_order(self, orderID):
        """Checks to see if order has been previously loaded and if not calls the controller to load"""
        order = None
        for x in self.data['Data']['Orders']:
            if str(x.ID) == orderID:
                order = x
            else:
                continue

        if order == None:
            order = self.mainWindow.load_order(orderID)
            self.mainWindow.data['Data']['Orders'].append(order)

        return order

class OrdersListWindowScroll(QWidget):
    def __init__(self, data, parent):
        super().__init__()
        self.controller = parent.controller
        self.data = data
        self.parent = parent
        self.layout = QGridLayout()
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaContents = QWidget()
        self.scrollAreaContentsLayout = QGridLayout()

        titleBox = QGroupBox()
        titleBox.setFixedHeight(60)
        titleLayout = QGridLayout()
        titleLayout.addWidget(QLabel('ID'), 0, 0)
        titleLayout.addWidget(QLabel('First Name'), 0, 1)
        titleLayout.addWidget(QLabel('Last Name'), 0, 2)
        titleLayout.addWidget(QLabel('Order Type'), 0, 3)
        titleLayout.addWidget(QLabel('Pay Method'), 0, 4)
        titleLayout.addWidget(QLabel('Amazon ID'), 0, 5)
        titleLayout.addWidget(QLabel('Date'), 0, 6)
        titleLayout.addWidget(QLabel('Status'), 0, 7)
        self.rows = 1
        titleBox.setLayout(titleLayout)
        self.scrollAreaContentsLayout.addWidget(titleBox)

        if self.data != None:

            for order in self.data['Orders']:
                button = LinkOrderButton(str(order.ID), self)
                subBox = QGroupBox()
                subBox.setFixedHeight(60)
                sublayout = QGridLayout()
                sublayout.addWidget(button, 0, 0)
                sublayout.addWidget(QLabel(order.customer.firstName), 0, 1, Qt.AlignVCenter)
                sublayout.addWidget(QLabel(order.customer.lastName), 0, 2, Qt.AlignVCenter)
                sublayout.addWidget(QLabel(order.orderType.name), 0, 3, Qt.AlignVCenter)
                sublayout.addWidget(QLabel(order.transaction.name), 0, 4, Qt.AlignVCenter)
                if order.amazonOrder != None:
                    sublayout.addWidget(QLabel(str(order.amazonOrder.ID)), 0, 5, Qt.AlignVCenter)
                else:
                    sublayout.addWidget(QLabel('None'), 0, 5, Qt.AlignVCenter)
                sublayout.addWidget(QLabel(str(order.date)), 0, 6, Qt.AlignVCenter)
                sublayout.addWidget(QLabel(order.status.name), 0, 7, Qt.AlignVCenter)
                subBox.setLayout(sublayout)
                self.rows += 1
                self.scrollAreaContentsLayout.addWidget(subBox, self.rows, 0, 1, 0)

        self.scrollAreaContentsLayout.setAlignment(Qt.AlignTop)
        self.scrollAreaContents.setLayout(self.scrollAreaContentsLayout)
        self.scrollArea.setWidget(self.scrollAreaContents)
        self.scrollArea.setMinimumWidth(self.scrollAreaContents.sizeHint().width())
        self.layout.addWidget(self.scrollArea)

        self.setLayout(self.layout)

    def show_order_detail_window(self, orderNumber):
        order = self.get_order(orderNumber)
        self.orderDetailWindow = OrderDetailWindow(order)
        self.parent.showOrderDetail()

    def get_order(self, orderNumber):
        order = None
        for x in self.data['Orders']:
            if str(x.ID) == orderNumber:
                order = x
            else:
                continue
        return order

class Button(QWidget):
    def __init__(self, name, method, parent=None):
        super().__init__()
        self.widget = QPushButton(name, self)
        self.name = name
        self.parent = parent
        self.method = method
        self.widget.clicked.connect(self.method)

class LinkOrderButton(QWidget):
    def __init__(self, name, parent=None):
        super().__init__()
        self.widget = QPushButton(name, self)
        self.name = name
        self.parent = parent
        self.widget.clicked.connect(self.link_order)

    def link_order(self):
        self.parent.show_order_detail_window(self.name)

class LinkCustomerButton(QWidget):
    def __init__(self, name, parent=None):
        super().__init__()
        self.widget = QPushButton(name, self)
        self.name = name
        self.parent = parent

    def link_customer(self):
        self.parent.show_customer_detail_window(self.name)

class LinkQuoteButton(QWidget):
    def __init__(self, name, parent=None):
        super().__init__()
        self.widget = QPushButton(name, self)
        self.name = name
        self.parent = parent


class Label(QWidget):
    def __init__(self, name, parent=None):
        super().__init__()
        self.widget = QLabel(name)
        self.parent = parent

    def update_text(self, text):
        self.widget.setText(text)

class Picture(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.widget = QLabel()
        self.parent = parent
        self.pixMap = QPixmap('logo.png')
        self.widget.setPixmap(self.pixMap)
        self.widget.setFixedWidth(518)
        self.widget.setFixedHeight(175)

class LineEdit(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.widget = QLineEdit()
        self.parent = parent

    def capture(self):
        self.text = self.widget.text()
        return self.text

class ComboBox(QWidget):
    def __init__(self, options, parent=None):
        super().__init__()
        self.widget = QComboBox()
        self.parent = parent
        self.options = options
        self.build_combo_box()

    def build_combo_box(self):
        for option in self.options:
            self.widget.addItem(option)

    def capture(self):
        self.text = str(self.widget.currentText())
        return self.text

class CheckBox(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.widget = QCheckBox()
        self.parent = parent
        self.widget.stateChanged.connect(self.display_amazon_order)
        self.widget.toggle()

    def display_amazon_order(self, state):
        if state == Qt.Checked:
            self.parent.display_amazon_order_box()
        else:
            self.parent.remove_amazon_order_box()

class BookEntry(QWidget):
    def __init__(self, parent=None):
        """Initializes an instance of BookEntry"""
        super().__init__()
        self.parent = parent
        self.widget = QGroupBox('Book '+str(self.parent.count-7))
        self.widget.setFixedHeight(240)
        self.layout = QGridLayout()
        self.build_widgets()
        self.build_book_entry()

    def build_widgets(self):
        """Builds all the widgets to be added to the layout"""
        self.titleLbl = Label('Title:')
        self.titleEdit = LineEdit()
        self.authorFirstLbl = Label('Author First:')
        self.authorFirstEdit = LineEdit()
        self.authorLastLbl = Label('Author Last')
        self.authorLastEdit = LineEdit()
        self.editionLbl = Label('Edition')
        self.editionEdit = LineEdit()
        self.ISBNLbl = Label('ISBN')
        self.ISBNEdit = LineEdit()
        self.conditionLbl = Label('Condition')
        self.conditionCombo = ComboBox(['New', 'Like New', 'Very Good', 'Good', 'Acceptable'])
        self.priceLbl = Label('Price')
        self.priceEdit = LineEdit()

    def build_book_entry(self):
        """Builds the BookEntry layout"""
        self.layout.addWidget(self.titleLbl.widget, 0, 0)
        self.layout.addWidget(self.titleEdit.widget, 0, 1)
        self.layout.addWidget(self.authorFirstLbl.widget, 1, 0)
        self.layout.addWidget(self.authorFirstEdit.widget, 1, 1)
        self.layout.addWidget(self.authorLastLbl.widget, 2, 0)
        self.layout.addWidget(self.authorLastEdit.widget, 2, 1)
        self.layout.addWidget(self.editionLbl.widget, 3, 0)
        self.layout.addWidget(self.editionEdit.widget, 3, 1)
        self.layout.addWidget(self.ISBNLbl.widget, 4, 0)
        self.layout.addWidget(self.ISBNEdit.widget, 4, 1)
        self.widget.setLayout(self.layout)

    def capture(self):
        """Stores all the input provided into attributes"""
        orderItemArgs = {
            'Item Number': None,
            'Title': self.titleEdit.capture(),
            'Author First': self.authorFirstEdit.capture(),
            'Author Last': self.authorLastEdit.capture(),
            'Edition': self.editionEdit.capture(),
            'ISBN': self.ISBNEdit.capture(),
            'Condition': self.conditionCombo.capture(),
            'Price': self.priceEdit.capture()
        }
        self.orderItem = Order_Item(orderItemArgs)

class BuyBookEntry(BookEntry):
    def __init__(self, parent=None):
        """Creates an instance of BookEntry with widgets specific to buy orders"""
        super().__init__(parent)
        self.build_extra_widgets()

    def build_extra_widgets(self):
        """Creates the specialized widgets for a buy order"""
        self.layout.addWidget(self.conditionLbl.widget, 5, 0)
        self.layout.addWidget(self.conditionCombo.widget, 5, 1)
        self.layout.update()

    def capture(self):
        """Stores all the input provided into attributes"""
        self.title = self.titleEdit.capture()
        self.authorFirst = self.authorFirstEdit.capture()
        self.authorLast = self.authorLastEdit.capture()
        self.edition = self.editionEdit.capture()
        self.ISBN = self.ISBNEdit.capture()
        self.condition = self.conditionCombo.capture()
        self.price = self.priceEdit.capture()

class SellBookEntry(BookEntry):
    def __init__(self, parent=None):
        """Creats an instance of BookEntry with widgets specific to sell orders"""
        super().__init__(parent)

    def capture(self):
        """Stores all the input provided into attributes"""
        self.title = self.titleEdit.capture()
        self.authorFirst = self.authorFirstEdit.capture()
        self.authorLast = self.authorLastEdit.capture()
        self.edition = self.editionEdit.capture()
        self.ISBN = self.ISBNEdit.capture()
        self.condition = None
        self.price = None

class QuoteWindow(QDialog):
    def __init__(self, args, orderDetailWindow):
        super().__init__()
        self.args = args
        self.orderDetailWindow = orderDetailWindow
        self.title = 'Add Quote'
        self.build_quote_window()

    def build_quote_window(self):
        self.setWindowTitle(self.title)
        self.setFixedHeight(800)
        self.setFixedWidth(1200)
        self.build_widgets()
        self.layout = QGridLayout()
        self.layout.setRowStretch(0,10)
        self.layout.setRowStretch(1,1)
        self.layout.addWidget(self.booksWidget, 0, 0)
        self.layout.addWidget(self.submitBtn.widget, 1, 0)

        self.setLayout(self.layout)

    def build_widgets(self):
        self.submitBtn = Button('Submit', self.submit)
        self.build_book_widgets()

    def build_book_widgets(self):
        self.booksWidget = QGroupBox()
        booksWidgetLayout = QGridLayout()
        booksWidgetLayout.setAlignment(Qt.AlignTop)
        books = self.args
        self.quoteWidgets = []
        row = 1

        titleBox = QGroupBox()
        titleBox.setFixedHeight(45)
        titleBoxLayout = QGridLayout()

        titleBoxLayout.setColumnStretch(0,3)
        titleBoxLayout.setColumnStretch(1,2)
        titleBoxLayout.setColumnStretch(2,2)
        titleBoxLayout.setColumnStretch(3,1)
        titleBoxLayout.setColumnStretch(4,2)
        titleBoxLayout.setColumnStretch(5,2)
        titleBoxLayout.setColumnStretch(6,1)
        titleBoxLayout.setColumnStretch(7,1)

        titleBoxLayout.addWidget(QLabel('Title'), 0, 0)
        titleBoxLayout.addWidget(QLabel('Author First'), 0, 1)
        titleBoxLayout.addWidget(QLabel('Author Last'), 0, 2)
        titleBoxLayout.addWidget(QLabel('Edition'), 0, 3)
        titleBoxLayout.addWidget(QLabel('ISBN'), 0, 4)
        titleBoxLayout.addWidget(QLabel('Condition'), 0, 5)
        titleBoxLayout.addWidget(QLabel('Price'), 0, 6)
        titleBoxLayout.addWidget(QLabel('Quote'), 0, 7)
        titleBox.setLayout(titleBoxLayout)
        booksWidgetLayout.addWidget(titleBox)

        for book in books:
            subBox = QuoteEntry(book)
            self.quoteWidgets.append(subBox)
            booksWidgetLayout.addWidget(subBox.widget, row, 0)
            row += 1

        self.booksWidget.setLayout(booksWidgetLayout)

    def submit(self):
        for quoteBox in self.quoteWidgets:
            quoteBox.capture()
            self.orderDetailWindow.add_quote(quoteBox.order)

        self.close()

class QuoteEntry(QWidget):
    def __init__(self, orderItemObject, parent=None):
        """Initializes an instance of QuoteEntry which holds an orderItemObject"""
        super().__init__()
        self.order = orderItemObject
        self.parent = parent
        self.widget = QGroupBox()
        self.layout = QGridLayout()
        self.build_quote_entry_widget()

    def build_quote_entry_widget(self):
        """Builds the quote entry widget"""
        self.build_widgets()

        self.layout.setColumnStretch(0, 3)
        self.layout.setColumnStretch(1, 2)
        self.layout.setColumnStretch(2, 2)
        self.layout.setColumnStretch(3, 1)
        self.layout.setColumnStretch(4, 2)
        self.layout.setColumnStretch(5, 2)
        self.layout.setColumnStretch(6, 1)
        self.layout.setColumnStretch(7, 1)

        self.layout.addWidget(self.titleLbl.widget, 0, 0)
        self.layout.addWidget(self.authorFirstLbl.widget, 0, 1)
        self.layout.addWidget(self.authorLastLbl.widget, 0, 2)
        self.layout.addWidget(self.editionLbl.widget, 0, 3)
        self.layout.addWidget(self.ISBNLbl.widget, 0, 4)
        self.layout.addWidget(self.conditionCombo.widget, 0, 5)
        self.layout.addWidget(self.priceLbl.widget, 0, 6)
        self.layout.addWidget(self.quoteEdit.widget, 0, 7)
        self.widget.setLayout(self.layout)

    def build_widgets(self):
        """Build the widgets"""
        self.quoteEdit = LineEdit()
        self.conditionCombo = ComboBox(['New', 'Like New', 'Very Good', 'Good', 'Acceptable'])
        self.titleLbl = Label(self.order.title)
        self.authorFirstLbl = Label(self.order.authorFirst)
        self.authorLastLbl = Label(self.order.authorLast)
        self.ISBNLbl = Label(self.order.ISBN)
        self.priceLbl = Label('None')

        if self.order.edition != None:
            self.editionLbl = Label(str(self.order.edition))
        else:
            self.editionLbl = Label('None')


    def capture(self):
        """Captures the input and assigns it to the orderItemObject"""
        self.quote = self.quoteEdit.capture()
        self.condition = self.conditionCombo.capture()
        self.order.price = self.quote
        self.order.condition = self.condition

class ShippingWindow(QDialog):
    def __init__(self, orderDetailWindow):
        super().__init__()
        self.orderDetailWindow = orderDetailWindow
        self.title = 'Add Shipping'
        self.build_shipping_window()

    def build_shipping_window(self):
        self.setWindowTitle(self.title)
        self.setFixedHeight(800)
        self.setFixedWidth(1200)
        self.build_widgets()
        self.layout = QGridLayout()
        self.layout.setRowStretch(0,10)
        self.layout.setRowStretch(1,1)
        self.layout.addWidget(self.addressWidget, 0, 0)
        self.layout.addWidget(self.shippingOptionsWidget, 0, 1)
        self.layout.addWidget(self.submitBtn.widget, 1, 0, 1, 0)

        self.setLayout(self.layout)

    def build_widgets(self):
        self.submitBtn = Button('Submit', self.submit)
        self.build_address_widget()
        self.build_shipping_options_widget()

    def build_address_widget(self):

        self.stateCombo = ComboBox([
            'Alabama',
            'Alaska',
            'Arizona',
            'Arkansas',
            'California',
            'Colorado',
            'Connecticut',
            'Delaware',
            'Florida',
            'Georgia',
            'Hawaii',
            'Idaho',
            'Illinois',
            'Indiana',
            'Iowa',
            'Kansas',
            'Kentucky',
            'Louisiana',
            'Maine',
            'Maryland',
            'Massasschusetts',
            'Michigan',
            'Minnesota',
            'Mississippi',
            'Missouri',
            'Montana',
            'Nebraska',
            'Nevada',
            'New Hampshire',
            'New Jersey',
            'New Mexico',
            'New York',
            'North Carolina',
            'North Dakota',
            'Ohio',
            'Oklahoma',
            'Oregon',
            'Pennsylvania',
            'Rhode Island',
            'South Carolina',
            'South Dakota',
            'Tennessee',
            'Texas',
            'Utah',
            'Vermont',
            'Virginia',
            'Washington',
            'West Virginia',
            'Wisconsin',
            'Wyoming'
        ])

        self.countryCombo = ComboBox([
            'Australia',
            'Canada',
            'United Kingdom',
            'United States',
        ])

        self.buildingNumberEdit = LineEdit()
        self.streetNumberEdit = LineEdit()
        self.cityEdit = LineEdit()
        self.zipEdit = LineEdit()

        self.addressWidget = QGroupBox()
        addressWidgetLayout = QGridLayout()
        addressWidgetLayout.addWidget(QLabel('Building Number'), 0, 0)
        addressWidgetLayout.addWidget(self.buildingNumberEdit.widget, 0, 1)
        addressWidgetLayout.addWidget(QLabel('Street Number'), 1, 0)
        addressWidgetLayout.addWidget(self.streetNumberEdit.widget, 1, 1)
        addressWidgetLayout.addWidget(QLabel('City'), 2, 0)
        addressWidgetLayout.addWidget(self.cityEdit.widget, 2, 1 )
        addressWidgetLayout.addWidget(QLabel('State'), 3, 0)
        addressWidgetLayout.addWidget(self.stateCombo.widget, 3, 1)
        addressWidgetLayout.addWidget(QLabel('Zip Code'), 4, 0)
        addressWidgetLayout.addWidget(self.zipEdit.widget, 4, 1)
        addressWidgetLayout.addWidget(QLabel('Country'), 5, 0)
        addressWidgetLayout.addWidget(self.countryCombo.widget, 5, 1)
        self.addressWidget.setLayout(addressWidgetLayout)

    def build_shipping_options_widget(self):
        self.shippingOptionsWidget = QGroupBox()
        shippingOptionsWidgetLayout = QGridLayout()

        self.shippingCostEdit = LineEdit()
        self.trackingNumberEdit = LineEdit()
        self.expectedArrivalEdit = LineEdit()

        self.shippingTypeCombo = ComboBox([
            'Sell Books',
            'Buy Books',
            'Sell Package',
            'Return'
        ])

        shippingOptionsWidgetLayout.addWidget(QLabel('Shipping Cost'), 0, 0)
        shippingOptionsWidgetLayout.addWidget(self.shippingCostEdit.widget, 0, 1)
        shippingOptionsWidgetLayout.addWidget(QLabel('Tracking Number'), 1, 0)
        shippingOptionsWidgetLayout.addWidget(self.trackingNumberEdit.widget, 1, 1)
        shippingOptionsWidgetLayout.addWidget(QLabel('Expected Arrival Date'), 2, 0)
        shippingOptionsWidgetLayout.addWidget(self.expectedArrivalEdit.widget, 2, 1)
        shippingOptionsWidgetLayout.addWidget(QLabel('Shipping Type'), 3, 0)
        shippingOptionsWidgetLayout.addWidget(self.shippingTypeCombo.widget, 3, 1)
        self.shippingOptionsWidget.setLayout(shippingOptionsWidgetLayout)

    def submit(self):
        """Captures the input builds a dictionary of shipping args and passes to the mainWindow"""
        self.shippingCost = self.shippingCostEdit.capture()
        self.tracking = self.trackingNumberEdit.capture()
        self.expectedArrival = self.expectedArrivalEdit.capture()
        self.shippingType = self.shippingTypeCombo.capture()

        self.buildingNumber = self.buildingNumberEdit.capture()
        self.street = self.streetNumberEdit.capture()
        self.city = self.cityEdit.capture()
        self.state = self.stateCombo.capture()
        self.zipCode = self.zipEdit.capture()
        self.country = self.countryCombo.capture()

        addressArgs = {
            'Address ID': None,
            'Customer ID': self.orderDetailWindow.order.customer.ID,
            'Building Number': self.buildingNumber,
            'Street Number': self.street,
            'City': self.city,
            'State': State({'State ID': None, 'State Name': self.state, 'State Tax': None}),
            'Zip Code': self.zipCode,
            'Country': Country({'Country ID': None, 'Country Name': self.country}),
            'Connection': None

        }

        addressObject = Address(addressArgs)

        shippingArgs = {
            'Shipping ID': None,
            'Order ID': self.orderDetailWindow.order.ID,
            'Shipping Cost': self.shippingCost,
            'Tracking': self.tracking,
            'Shipping Date': None,
            'Expected Arrival': self.expectedArrival,
            'Shipping Type': ShippingType({'Shipping Type ID': None, 'Shipping Type Name': self.shippingType}),
            'Shipping Materials': None,
            'Status': Status({'Status ID': None, 'Status Name': 'In-Transit'}),
            'Connection': None
        }

        shippingObject = Shipping_Order(shippingArgs)

        self.orderDetailWindow.mainWindow.add_shipping(shippingObject)
        self.orderDetailWindow.mainWindow.add_address(addressObject)
        self.orderDetailWindow.remove_from_inventory()
        self.orderDetailWindow.mainWindow.update_order_status(self.orderDetailWindow.order.ID, 'In-Transit')
        self.close()

class ConfirmationWindow(QDialog):
    def __init__(self, order, parent=None):
        super().__init__()
        self.order = order
        self.parent = parent
        self.title = 'Commit to Database?'
        self.build_confirmation_window()

    def build_confirmation_window(self):
        self.setWindowTitle(self.title)
        self.setFixedWidth(800)
        self.setFixedHeight(800)
        self.build_widgets()
        self.layout = QGridLayout()
        self.layout.addWidget(self.customerWidget, 0, 0)
        self.layout.addWidget(self.transactionWidget, 0, 1)
        self.layout.addWidget(self.booksWidget, 2, 0, 1, 0)
        self.layout.addWidget(self.yesBtn.widget, 3, 0)
        self.layout.addWidget(self.noBtn.widget, 3, 1)

        self.setLayout(self.layout)

        self.check_amazon_order()

    def build_widgets(self):
        self.yesBtn = Button('Yes', self.parent.submit)
        self.noBtn = Button('No', self.close_window)
        self.build_customer_widget()
        self.build_transaction_widget()
        self.build_books_widget()

    def build_customer_widget(self):
        self.customerWidget = QGroupBox()
        customerWidgetLayout = QGridLayout()
        customerWidgetLayout.addWidget(QLabel('First Name'), 0, 0)
        customerWidgetLayout.addWidget(QLabel(self.order.customer.firstName), 0, 1)
        customerWidgetLayout.addWidget(QLabel('Last Name'), 1, 0)
        customerWidgetLayout.addWidget(QLabel(self.order.customer.lastName), 1, 1)
        customerWidgetLayout.addWidget(QLabel('Phone'), 2, 0)
        customerWidgetLayout.addWidget(QLabel(self.order.customer.phone), 2, 1)
        customerWidgetLayout.addWidget(QLabel('Email'), 3, 0)
        customerWidgetLayout.addWidget(QLabel(self.order.customer.email), 3, 1)
        self.customerWidget.setLayout(customerWidgetLayout)

    def build_transaction_widget(self):
        self.transactionWidget = QGroupBox()
        transactionWidgetLayout = QGridLayout()
        transactionWidgetLayout.addWidget(QLabel('Order Type'), 0, 0)
        transactionWidgetLayout.addWidget(QLabel(self.order.orderType.name), 0, 1)
        transactionWidgetLayout.addWidget(QLabel('Transaction Method'), 1, 0)
        transactionWidgetLayout.addWidget(QLabel(self.order.transaction.name), 1, 1)
        transactionWidgetLayout.addWidget(QLabel('Promotion Code'), 2, 0)
        transactionWidgetLayout.addWidget(QLabel(self.order.promotion), 2, 1)
        self.transactionWidget.setLayout(transactionWidgetLayout)

    def check_amazon_order(self):
        if self.order.amazonOrder != None:
            self.build_amazon_widget()
            self.layout.addWidget(self.amazonWidget, 1, 0)
            self.layout.update()

    def build_amazon_widget(self):
        self.amazonWidget = QGroupBox()
        amazonWidgetLayout = QGridLayout()
        amazonWidgetLayout.addWidget(QLabel('Amazon Key'), 0, 0)
        amazonWidgetLayout.addWidget(QLabel(self.order.amazonOrder.code), 0, 1)
        amazonWidgetLayout.addWidget(QLabel('Ship By'), 1, 0)
        amazonWidgetLayout.addWidget(QLabel(self.order.amazonOrder.shipBy), 1, 1)
        amazonWidgetLayout.addWidget(QLabel('Deliver By'), 2, 0)
        amazonWidgetLayout.addWidget(QLabel(self.order.amazonOrder.deliverBy), 2, 1)
        self.amazonWidget.setLayout(amazonWidgetLayout)

    def build_books_widget(self):
        self.booksWidget = QGroupBox()
        booksWidgetLayout = QGridLayout()
        booksWidgetLayout.setAlignment(Qt.AlignTop)
        books = self.order.books
        row = 1

        titleBox = QGroupBox()
        titleBox.setFixedHeight(45)
        titleBoxLayout = QGridLayout()
        titleBoxLayout.addWidget(QLabel('Author First'), 0, 0)
        titleBoxLayout.addWidget(QLabel('Author Last'), 0, 1)
        titleBoxLayout.addWidget(QLabel('Edition'), 0, 2)
        titleBoxLayout.addWidget(QLabel('ISBN'), 0, 3)
        titleBoxLayout.addWidget(QLabel('Condition'), 0, 4)
        titleBoxLayout.addWidget(QLabel('Price'), 0, 5)
        titleBox.setLayout(titleBoxLayout)
        booksWidgetLayout.addWidget(titleBox)

        for book in books:
            subBox = QGroupBox()
            subBox.setFixedHeight(45)
            subLayout = QGridLayout()
            subLayout.addWidget(QLabel(book.authorFirst), 0, 0)
            subLayout.addWidget(QLabel(book.authorFirst), 0, 1)
            subLayout.addWidget(QLabel(str(book.edition)), 0, 2)
            subLayout.addWidget(QLabel(book.ISBN), 0, 3)
            subLayout.addWidget(QLabel(book.condition), 0, 4)
            subLayout.addWidget(QLabel(book.price), 0, 5)
            subBox.setLayout(subLayout)
            booksWidgetLayout.addWidget(subBox, row, 0)
            row += 1
        self.booksWidget.setLayout(booksWidgetLayout)

    def close_window(self):
        self.close()

class OrderDetailWindow(QWidget):
    def __init__(self, order, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.order = order
        self.build_order_detail_window()
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.orderOverview, 0, 0, 1, 0)
        self.mainLayout.addWidget(self.shippingDetail, 1, 0, 1, 2)
        self.mainLayout.addWidget(self.orderBasket, 2, 0, 1, 3)
        self.mainLayout.addWidget(self.paymentDetail, 1, 2, 1, 2)
        self.mainLayout.addWidget(self.orderActions, 2, 3, 1, 1)

        self.setLayout(self.mainLayout)

    def build_order_detail_window(self):
        self.build_order_overview()
        self.build_order_basket()
        self.create_payment_detail()
        self.build_shipping_detail()
        self.create_order_actions()

    def add_shipping_screen(self):
        self.screen = ShippingWindow()
        self.screen.show()

    def create_order_actions(self):
        self.orderActions = QGroupBox('Actions')
        self.addShippingBtn = Button('Add Shipping', self.show_shipping_window)
        self.addQuoteBtn = Button('Add Quote', self.show_quote_window)
        self.acceptBtn = Button('Accept', self.accept_order)
        self.addToInventoryBtn = Button('Add To Inventory', self.add_to_inventory)
        self.removeFromInventoryBtn = Button('Remove From Inventory', self.remove_from_inventory)
        self.getCurrentPricesBtn = Button('Get Current Prices', self.get_current_prices)
        self.cancelBtn = QPushButton('Cancel')

        layout = QGridLayout()
        layout.addWidget(self.addQuoteBtn.widget, 1, 0)
        layout.addWidget(self.addShippingBtn.widget, 2, 0)
        layout.addWidget(self.acceptBtn.widget, 3, 0)
        layout.addWidget(self.addToInventoryBtn.widget, 4, 0)
        layout.addWidget(self.removeFromInventoryBtn.widget, 5, 0)
        layout.addWidget(self.getCurrentPricesBtn.widget, 6, 0)
        layout.addWidget(self.cancelBtn, 7, 0)

        self.orderActions.setLayout(layout)

    def build_order_overview(self):
        self.orderOverview = QGroupBox()
        self.orderNumberTitleLbl = Label('Order Number')
        self.firstNameTitleLbl = Label('First Name')
        self.lastNameTitleLbl = Label('Last Name')
        self.typeTitleLbl = Label('Type')
        self.transactionTitleLbl = Label('Transaction')
        self.amazonTitleLbl = Label('Amazon')
        self.dateTitleLbl = Label('Date')
        self.statusTitleLbl = Label('Status')

        self.orderNumberLbl = Label(str(self.order.ID))
        self.firstNameLbl = Label(self.order.customer.firstName)
        self.lastNameLbl = Label(self.order.customer.lastName)
        self.orderTypeLbl = Label(self.order.orderType.name)
        self.transactionLbl = Label(self.order.transaction.name)

        if self.order.amazonOrder != None:
            self.amazonOrderLbl = Label(str(self.order.amazonOrder.ID))
        else:
            self.amazonOrderLbl = Label('None')
        self.dateLbl = Label(str(self.order.date))
        self.statusLbl = Label(self.order.status.name)

        orderOverviewPalette = self.orderOverview.palette()
        orderOverviewPalette.setColor(orderOverviewPalette.Window, Qt.gray)
        self.orderOverview.setPalette(orderOverviewPalette)
        self.orderOverview.setAutoFillBackground(True)

        layout = QGridLayout()

        layout.addWidget(self.orderNumberTitleLbl.widget, 1, 0)
        layout.addWidget(self.orderNumberLbl.widget, 1, 1)
        layout.addWidget(self.firstNameTitleLbl.widget, 2, 0)
        layout.addWidget(self.firstNameLbl.widget, 2, 1)
        layout.addWidget(self.lastNameTitleLbl.widget, 3, 0)
        layout.addWidget(self.lastNameLbl.widget, 3, 1)
        layout.addWidget(self.typeTitleLbl.widget, 4, 0)
        layout.addWidget(self.orderTypeLbl.widget, 4, 1)
        layout.addWidget(self.transactionTitleLbl.widget, 1, 2)
        layout.addWidget(self.transactionLbl.widget, 1, 3)
        layout.addWidget(self.amazonTitleLbl.widget, 2, 2)
        layout.addWidget(self.amazonOrderLbl.widget, 2, 3)
        layout.addWidget(self.dateTitleLbl.widget, 3, 2)
        layout.addWidget(self.dateLbl.widget, 3, 3)
        layout.addWidget(self.statusTitleLbl.widget, 4, 2)
        layout.addWidget(self.statusLbl.widget, 4, 3)
        layout.setAlignment(Qt.AlignTop)

        self.orderOverview.setLayout(layout)

    def build_order_basket(self):
        self.itemNumberTitleLbl = Label('Item Number')
        self.titleTitleLbl = Label('Title')
        self.authorFirstTitleLbl = Label('Author First')
        self.authorLastTitleLbl = Label('Author Last')
        self.editionTitleLbl = Label('Edition')
        self.ISBNTitleLbl = Label('ISBN')
        self.conditionTitleLbl = Label('Condition')
        self.priceTitleLbl = Label('Price')

        titleBox = QGroupBox()
        titleBox.setFixedHeight(60)
        titleBoxLayout = QGridLayout()
        titleBoxLayout.addWidget(self.itemNumberTitleLbl.widget, 0, 0)
        titleBoxLayout.addWidget(self.titleTitleLbl.widget, 0, 1)
        titleBoxLayout.addWidget(self.authorFirstTitleLbl.widget, 0, 2)
        titleBoxLayout.addWidget(self.authorLastTitleLbl.widget, 0, 3)
        titleBoxLayout.addWidget(self.editionTitleLbl.widget, 0, 4)
        titleBoxLayout.addWidget(self.ISBNTitleLbl.widget, 0, 5)
        titleBoxLayout.addWidget(self.conditionTitleLbl.widget, 0, 6)
        titleBoxLayout.addWidget(self.priceTitleLbl.widget, 0, 7)
        titleBox.setLayout(titleBoxLayout)

        self.orderBasket = QGroupBox('Order Basket')
        self.orderBasketLayout = QGridLayout()
        self.orderBasketLayout.addWidget(titleBox)


        for book in self.order.books:
            itemBox = QGroupBox()
            itemBox.setFixedHeight(60)
            itemBoxLayout = QGridLayout()
            itemBoxLayout.addWidget(QLabel(str(book.itemNumber)), 0, 0)
            itemBoxLayout.addWidget(QLabel(book.title), 0, 1)
            itemBoxLayout.addWidget(QLabel(book.authorFirst), 0, 2)
            itemBoxLayout.addWidget(QLabel(book.authorLast), 0, 3)
            itemBoxLayout.addWidget(QLabel(str(book.edition)), 0, 4)
            itemBoxLayout.addWidget(QLabel(book.ISBN), 0, 5)
            itemBoxLayout.addWidget(QLabel(book.condition), 0, 6)
            itemBoxLayout.addWidget(QLabel(str(book.price)), 0, 7)
            itemBox.setLayout(itemBoxLayout)
            self.orderBasketLayout.addWidget(itemBox)

        self.orderBasketLayout.setAlignment(Qt.AlignTop)
        self.orderBasket.setLayout(self.orderBasketLayout)

    def create_payment_detail(self):
        self.paymentDetail = QGroupBox('Payment Detail')
        layout = QGridLayout()
        layout.addWidget(QLabel('Payment Type'), 0, 0)
        layout.addWidget(QLabel(self.order.transaction.name), 0, 1)

        self.paymentDetail.setLayout(layout)

    def build_shipping_detail(self):
        self.shippingIDTitleLbl = Label('ID')
        self.shippingCostTitleLbl = Label('Cost')
        self.shippingTrackingTitleLbl = Label('Tracking')
        self.shippingDateTitleLbl = Label('Shipped')
        self.shippingExpectedArrivalTitleLbl = Label('Expected')
        self.shippingTypeTitleLbl = Label('Shipping Type')
        self.shippingStatusTitleLbl = Label('Status')

        titleBox = QGroupBox()
        titleBox.setFixedHeight(60)
        titleBoxLayout = QGridLayout()
        titleBoxLayout.addWidget(self.shippingIDTitleLbl.widget, 0, 0)
        titleBoxLayout.addWidget(self.shippingCostTitleLbl.widget, 0, 1)
        titleBoxLayout.addWidget(self.shippingTrackingTitleLbl.widget, 0, 2)
        titleBoxLayout.addWidget(self.shippingDateTitleLbl.widget, 0, 3)
        titleBoxLayout.addWidget(self.shippingExpectedArrivalTitleLbl.widget, 0, 4)
        titleBoxLayout.addWidget(self.shippingTypeTitleLbl.widget, 0, 5)
        titleBoxLayout.addWidget(self.shippingStatusTitleLbl.widget, 0, 6)
        titleBox.setLayout(titleBoxLayout)

        self.shippingDetail = QGroupBox('Shipping Detail')
        self.shippingDetailLayout = QGridLayout()
        self.shippingDetailLayout.addWidget(titleBox)
        self.shippingDetailLayout.setAlignment(Qt.AlignTop)

        for shipping in self.order.shipping:
            itemBox = QGroupBox()
            itemBox.setFixedHeight(60)
            itemBoxLayout = QGridLayout()
            itemBoxLayout.addWidget(QLabel(str(shipping.ID)), 0, 0)
            itemBoxLayout.addWidget(QLabel(str(shipping.shippingCost)), 0, 1)
            itemBoxLayout.addWidget(QLabel(shipping.tracking), 0, 2)
            itemBoxLayout.addWidget(QLabel(str(shipping.shipDate)), 0, 3)
            itemBoxLayout.addWidget(QLabel(str(shipping.expectedArrival)), 0, 4)
            itemBoxLayout.addWidget(QLabel(shipping.shipType.name), 0, 5)
            itemBoxLayout.addWidget(QLabel(shipping.status.name), 0, 6)
            itemBox.setLayout(itemBoxLayout)
            self.shippingDetailLayout.addWidget(itemBox)

        self.shippingDetail.setLayout(self.shippingDetailLayout)

    def accept_order(self):
        """Calls the main window to accept the order"""
        self.mainWindow.update_order_status(self.order.ID, 'Accepted')

    def show_quote_window(self):
        """Builds a QuoteWindow and displays"""
        self.quoteWindow = QuoteWindow(self.order.books, self)
        self.quoteWindow.show()

    def add_quote(self, orderItem):
        """Calls the main window to add quotes to the items in the order"""
        self.mainWindow.add_quote(orderItem)
        self.mainWindow.update_order_status(self.order.ID, 'Quoted')

    def show_shipping_window(self):
        """Builds a ShippingWindow and displays"""
        self.shippingWindow = ShippingWindow(self)
        self.shippingWindow.show()

    def add_to_inventory(self):
        """Completes order and moves book into inventory"""
        self.mainWindow.update_order_status(self.order.ID, 'Complete')
        for orderItem in self.order.books:
            self.mainWindow.add_book_to_inventory(orderItem)

    def remove_from_inventory(self):
        """Completes a selling order and removes book from inventory"""
        for orderItem in self.order.books:
            self.mainWindow.remove_book_from_inventory(orderItem)

    def get_current_prices(self):
        """Calls the main window for all buy order items"""
        for orderItem in self.order.books:
            orderItem.price = self.mainWindow.get_current_price(orderItem)

    def complete_order(self):
        """Calls the main window to update the status to complete"""
        self.mainWindow.update_order_status(self.order.ID, 'Complete')
        self.move_to_history()

    def move_to_history(self):
        """Calls the main window to archive the order"""
        self.mainWindow.move_to_history(self.order)

    def order_picked_up(self):
        """Calls the main window to update the status to picked up"""
        self.mainWindow.update_order_status(self.order.ID, 'Picked Up')

class BuyOrderDetailWindowProcess(OrderDetailWindow):
    def __init__(self, order, mainWindow):
        """Shows the buttons for the first step of a buy order"""
        super().__init__(order, mainWindow)

    def create_order_actions(self):
        self.orderActions = QGroupBox('Actions')
        self.addShippingBtn = Button('Add Shipping', self.show_shipping_window)
        self.cancelBtn = QPushButton('Cancel')

        layout = QGridLayout()
        layout.addWidget(self.addShippingBtn.widget, 1, 0)
        layout.addWidget(self.cancelBtn, 5, 0)

        self.orderActions.setLayout(layout)

class BuyOrderDetailWindowInTransit(OrderDetailWindow):
    def __init__(self, order, mainWindow):
        """Shows the buttons for the second step of a buy order"""
        super().__init__(order, mainWindow)

    def create_order_actions(self):
        self.orderActions = QGroupBox('Actions')
        self.completeBtn = Button('Order Complete', self.complete_order)
        self.cancelBtn = QPushButton('Cancel')

        layout = QGridLayout()
        layout.addWidget(self.completeBtn.widget, 0, 0)
        layout.addWidget(self.cancelBtn, 1, 0)

        self.orderActions.setLayout(layout)

class SellOrderDetailWindowProcess(OrderDetailWindow):
    def __init__(self, order, mainWindow):
        """Shows the button for the first step of a sell order"""
        super().__init__(order, mainWindow)

    def create_order_actions(self):
        self.orderActions = QGroupBox('Actions')
        self.addQuoteBtn = Button('Add Quote', self.show_quote_window)
        self.cancelBtn = QPushButton('Cancel')

        layout = QGridLayout()
        layout.addWidget(self.addQuoteBtn.widget, 0, 0)
        layout.addWidget(self.cancelBtn, 1, 0)

        self.orderActions.setLayout(layout)


class SellOrderDetailWindowQuoted(OrderDetailWindow):
    def __init__(self, order, mainWindow):
        """Shows the button for the second step of a sell order"""
        super().__init__(order, mainWindow)

    def create_order_actions(self):
        self.orderActions = QGroupBox('Actions')
        self.acceptedBtn = Button('Customer Accepted', self.accept_order)
        self.cancelBtn = QPushButton('Cancel')

        layout = QGridLayout()
        layout.addWidget(self.acceptedBtn.widget, 0, 0)
        layout.addWidget(self.cancelBtn, 1, 0)

        self.orderActions.setLayout(layout)

class SellOrderDetailWindowAccepted(OrderDetailWindow):
    def __init__(self, order, mainWindow):
        """Shows the button for the third step of a sell order"""
        super().__init__(order, mainWindow)

    def create_order_actions(self):
        self.orderActions = QGroupBox('Actions')
        self.addShippingBtn = Button('Add Shipping', self.show_shipping_window)
        self.addLocalBtn = Button('Local Pick Up', self.order_picked_up)
        self.cancelBtn = QPushButton('Cancel')

        layout = QGridLayout()
        layout.addWidget(self.addShippingBtn.widget, 0, 0)
        layout.addWidget(self.addLocalBtn.widget, 1, 0)
        layout.addWidget(self.cancelBtn, 2, 0)

        self.orderActions.setLayout(layout)

class SellOrderDetailWindowInTransit(OrderDetailWindow):
    def __init__(self, order, mainWindow):
        """Shows the button for the fourth step of a sell order"""
        super().__init__(order, mainWindow)

    def create_order_actions(self):
        self.orderActions = QGroupBox('Actions')
        self.completeBtn = Button('Order Complete', self.complete_order)
        self.cancelBtn = QPushButton('Cancel')

        layout = QGridLayout()
        layout.addWidget(self.completeBtn.widget, 0, 0)
        layout.addWidget(self.cancelBtn, 1, 0)

        self.orderActions.setLayout(layout)

class CustomerDetailWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window = QVBoxLayout()
        self.create_customer_overview()
        self.create_address_overview()
        self.create_referral_overview()
        self.create_order_history()

        layout = QGridLayout()
        layout.addWidget(self.customerOverview, 0, 0, 1, 0)
        layout.addWidget(self.referralOverview, 1, 0)
        layout.addWidget(self.addressOverview, 1, 1)
        layout.addWidget(self.orderOverview, 2, 0, 1, 0)

        self.setLayout(layout)

    def create_customer_overview(self):
        self.customerOverview = QGroupBox('Customer Overview')
        layout = QGridLayout()
        layout.addWidget(QLabel('First Name:'), 0, 0)
        layout.addWidget(QLabel('Last Name:'), 1, 0)
        layout.addWidget(QLabel('Phone:'), 0, 1)
        layout.addWidget(QLabel('Email:'), 1, 1)
        layout.addWidget(QLabel('Referral Code:'), 2, 0)
        layout.addWidget(QLabel('Account Created:'), 2, 1)

        self.customerOverview.setLayout(layout)

    def create_address_overview(self):
        self.addressOverview = QGroupBox('Address')
        layout = QGridLayout()
        layout.addWidget(QLabel('House/Apt:'), 0, 0)
        layout.addWidget(QLabel('Street:'), 1, 0)
        layout.addWidget(QLabel('City:'), 2, 0)
        layout.addWidget(QLabel('State:'), 3, 0)
        layout.addWidget(QLabel('Zip Code:'), 4, 0)
        layout.addWidget(QLabel('Country:'), 5, 0)

        self.addressOverview.setLayout(layout)

    def create_referral_overview(self):
        self.referralOverview = QGroupBox('Referrals')
        layout = QGridLayout()

        self.referralOverview.setLayout(layout)

    def create_order_history(self):
        self.orderOverview = QGroupBox('Orders')
        layout = QGridLayout()

        self.orderOverview.setLayout(layout)








