Feature: Simple order Without First Login

#  Scenario: set a city services
#    When Getting the list of cities
#    Then Status code must be 200
#
#  Scenario: choose a service
#    When Get the list of services
#    Then Status code must be 200
#
#  Scenario: Initiate order
#    When Order initiated for a services
#    Then Status code must be 201
#
#  Scenario: Get Times List of Services
#    When Getting the list of time in service in city
#    Then Status code must be 200
#    And set delivery at 2019-10-22T08:50:07.895880
#
#  Scenario: Get Zones List of city
#    When Get list of zones
#    Then Status code must be 200
#
#  Scenario: Set delivery location at for orders
#    When send delivery location with information
#      | address                | location | title     |
#      | آدرس برای دریافت سفارش | 56,21    | آدرس منزل |
#    Then Status code must be 204
#
#  Scenario: check questions for answer
#    When get the questions for service
#    Then Status code must be 204
#
#  Scenario: Set order detail
#    When set orders detail
#      | description                      |
#      | متن توضیحات اتوماتیک تست می باشد |
#    Then Status code must be 204
#
#
#  Scenario: User login for customer
#    When Customer Login with mobile 09127179264 and code 666666
#    Then Status code must be 201
#    And Some detailed must be show
#
#  Scenario: Customer Register and set profile
#    When Register as a customer
#      | first_name | last_name | picture                                                    | national_code |
#      | کوروش      | هخامنشی   | /buckets/images/files/1cc71c67-6c55-4d8a-a68e-7d3fe4411e91 | 0015440874    |
#    Then Status code must be 204
#
##  Scenario: Submit vouchers to this order
##    When choose and submit voucher code
##    Then Status code must be 204
#
#  Scenario: Submit order for update order status
#    When submit order
#    Then Status code must be 204
#
#
#
#  Scenario: provider login.
#    When provider logged in with 09125477537 and password 666666
#    Then Status code must be 201
#
#  Scenario: Provider Register
#    When provider register
#      | first_name | last_name | gender | description   |
#      | آقامحمدخان | قاجار     | Male   | این توضیح است |
#    Then Status code must be 201
#
#  Scenario: Send provider receipt
#    When create provider receipt
#    Then Status code must be 201
#
#  Scenario: Accept Provider receipt
#    When get receipt number
#    Then Status code must be 204
#
#  Scenario: check offers to providers
#    When get offers for an order to provider
#    Then Status code must be 200
#    And order status must be NeedQuote
#
#
#  Scenario: Create quote form providers
#    When create quote from providers to an order
#      | description             | final_cost | max_cost | min_cost | working_duration |
#      | رنگ ماشین نوک مدادی است | 10000      | 100000   | 1000     | ۱ تا ۲           |
#    Then Status code must be 201
#    And order status must be WithQuote
#
#  Scenario: Get list quotes for an order
#    When get quotes list for an order by customer
#    Then Status code must be 200
#
#
##   Scenario: Cancel quote by provider
##    When cancel quote by provider
##    Then Status code must be 204
#
#
#  Scenario: Accept a quote by customer
#    When accept quote for an order by customer
#    Then Status code must be 200
#
##  Scenario: Cancel Order by operator
##    When cancel order by operator
##    Then Status code must be 204
#
#
#  Scenario: check Accepted quote
#    When check quotes list for an order by customer
#    Then Status code must be 200
#    And order status must be QuoteAccepted
#
#  Scenario: check offers not find providers
#    When get offers for an order to provider
#    Then Status code must be 200
#    And order that started not be in list
#
#
##  Scenario: Cancel Order by customer
##    When cancel order by customer
##    Then Status code must be 204
#
#
#  Scenario: send final cost quote by provider
#    When send quote for an order by provider with final cost 1000
#    Then Status code must be 204
#    And order status must be WithInvoice
#
#  Scenario: accept invoice with customer
#    When send final patch by customer
#    Then Status code must be 204
#    And order status must be Started
#
#
#  Scenario: check for finish of order by providers
#    When final accept order by provider for finish
#    Then Status code must be 204
#    And order status must be Finished
#    And  order Payment status must be Pending
#
#  Scenario: payment order with customer
#    When patch on order by customer with Cash
#    Then Status code must be 204
#    And order Payment status must be Paid
#    And order status must be Done

#  Scenario: send Payment by Provider
#    When send patch by provider Paid
#    Then Status code must be 204
#    And  order Payment status must be Paid
#    And order status must be Done