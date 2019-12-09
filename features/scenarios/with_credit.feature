Feature: Simple order with credit

  Scenario: set a city services
    When Getting the list of cities
    Then Status code must be 200

  Scenario: choose a service
    When Get the list of services
    Then Status code must be 200

  Scenario: Initiate order
    When Order initiated for a services
    Then Status code must be 201

  Scenario: Get Times List of Services
    When Getting the list of time in service in city
    Then Status code must be 200
    And set delivery at 2019-10-22T08:50:07.895880

  Scenario: Get Zones List of city
    When Get list of zones
    Then Status code must be 200

  Scenario: Set delivery location at for orders
    When send delivery location with information
      | address                | location | title     |
      | آدرس برای دریافت سفارش | 56,21    | آدرس منزل |
    Then Status code must be 204

  Scenario: check questions for answer
    When get the questions for service
    Then Status code must be 204

  Scenario: Set order detail
    When set orders detail
      | description                      |
      | متن توضیحات اتوماتیک تست می باشد |
    Then Status code must be 204


  Scenario: User login for customer
    When Customer Login with mobile 09124406923 and code 666666
    Then Status code must be 201
    And Some detailed must be show

  Scenario: Customer Register and set profile
    When Register as a customer
      | first_name | last_name | picture                                                    | national_code |
      | پیرمرد     | دیوانه    | /buckets/images/files/1cc71c67-6c55-4d8a-a68e-7d3fe4411e91 | 0015040874    |
    Then Status code must be 204


  Scenario: Submit vouchers to this order
    When choose and submit voucher code
    Then Status code must be 204

  Scenario: Submit order for update order status
    When submit order
    Then Status code must be 204

  Scenario: provider login.
    When provider logged in with 09125477537 and password 666666
    Then Status code must be 201

  Scenario: Provider Register
    When provider register
      | first_name | last_name | gender | description   |
      | تنها       | در خانه   | Male   | این توضیح است |
    Then Status code must be 201

  Scenario: Send provider receipt
    When create provider receipt
    Then Status code must be 201

  Scenario: Accept Provider receipt
    When get receipt number
    Then Status code must be 204


  Scenario: check offers to providers
    When get offers for an order to provider
    Then Status code must be 200
    And order status must be NeedQuote


  Scenario: Create quote form providers
    When create quote from providers to an order
      | description             | final_cost | max_cost | min_cost | working_duration |
      | رنگ ماشین نوک مدادی است | 10000      | 100000   | 1000     | ۱ تا ۲           |
    Then Status code must be 201
    And order status must be WithQuote


  Scenario: Get list quotes for an order
    When get quotes list for an order by customer
    Then Status code must be 200


  Scenario: Accept a quote by customer
    When accept quote for an order by customer
    Then Status code must be 200


  Scenario: check Accepted quote
    When check quotes list for an order by customer
    Then Status code must be 200
    And order status must be QuoteAccepted

  Scenario: send final cost quote by provider
    When send quote for an order by provider with final cost 100
    Then Status code must be 204
    And order status must be WithInvoice


  Scenario: accept invoice with customer
    When send final patch by customer
    Then Status code must be 204
    And order status must be Started


  Scenario: check for finish of order by providers
    When final accept order by provider for finish
    Then Status code must be 204
    And order status must be Finished
    And  order Payment status must be Pending

  Scenario: Send customer receipt
    When create customer receipt
    Then Status code must be 201

  Scenario: Accept customer receipt
    When get receipt number
    Then Status code must be 204

  Scenario: payment order by customer
    When patch on order by customer with Credit
    Then Status code must be 204
    And order Payment status must be Paid
    And order status must be Done

  Scenario: Send comment with customer
    When send comment with customer for order
        |behavior_appearance| fairness|is_name_shown|is_satisfied|punctuality|quality|responsiveness|description|
        |    10      |    5   |       False |      True  |     10    |    7   |       8     |  بسیار با ادب بود   |
    Then Status code must be 201
    And order status must be WithFeedback

  Scenario: Get all comments for this provider
    When check all comments for this provider
    And Status code must be 200

  Scenario: Get summary comments for this provider
    When check summery comments for this provider
    And Status code must be 200
#

