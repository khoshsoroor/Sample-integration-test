import json
import random
import time
from timeit import default_timer as timer
import uuid

import geojson
from aloe import step, world, tools
from catalyst.service_invoker.service_interface import invoke_inter_service_operation_sync
from shapely.geometry import Point

import constants
from constants import OperationKeys
from features import logger

session_id = uuid.uuid4()
world.session_id = session_id
logger.info(world.session_id)


@step(r'Getting the list of cities')
def cities(_):
    start = timer()
    result = invoke_inter_service_operation_sync(OperationKeys.GetCity)
    end = timer()
    check_timer = end - start
    if check_timer > 1:
        logger.info("endpoint city get time")

    city_list = result.Body['value']
    logger.info(city_list)
    city = random.choice(city_list)
    world.city_slug = city['slug']
    # world.city_slug = "tehran"
    logger.info(world.city_slug)
    world.status_code = result.Status


@step(r'Get the list of services')
def services(_):
    start = timer()
    service = invoke_inter_service_operation_sync(OperationKeys.GetCityService, city_slug=world.city_slug,
                                                  filter='is_enabled eq true', top=254)
    end = timer()
    logger.info(end - start)
    logger.info(service.Body)
    get_service = random.choice(service.Body['value'])
    world.services_list = get_service
    world.service = get_service['slug']
    logger.info(world.service)
    world.status_code = service.Status


@step(r'Order initiated for a service')
def init_order(_):
    start = timer()
    result = invoke_inter_service_operation_sync(OperationKeys.InitiateOrder,
                                                 service_slug=world.service,
                                                 session_id=world.session_id)
    end = timer()
    logger.info(end - start)
    logger.info(result.Body)
    world.order_number = result.Body.get('number')
    world.status_code = result.Status
    if result.Status == 226:
        cancle = invoke_inter_service_operation_sync(OperationKeys.CancelOrderCustomer,
                                                     session_id=world.session_id,
                                                     order_number=world.order_number)
        logger.info(cancle)
        init_order(_)

    logger.info(world.status_code)
    logger.info(world.order_number)


@step(r'Getting the list of time in service in city')
def get_time_service(_):
    result = invoke_inter_service_operation_sync(OperationKeys.GetTime, service_slug=world.service,
                                                 city_slug=world.city_slug)
    world.status_code = result.Status


@step(r'Get list of zones')
def get_list_zone(_):
    result = invoke_inter_service_operation_sync(OperationKeys.GetZones, city_slug=world.city_slug, top=200)
    logger.info(result.Body)
    world.status_code = result.Status
    zones_list = result.Body['value']
    random_zone = random.choice(zones_list)
    world.zone_slug = random_zone['slug']
    logger.info(world.zone_slug)


@step(r'send delivery location with information')
def set_delivery_location(self):
    row = tools.guess_types(self.hashes)[0]
    location = json.loads(geojson.dumps(Point(*map(float, row["location"].split(",")))))
    row['location'] = location
    logger.info(row['location'])
    payload = {'location': row['location'], 'address': row['address'], 'city_slug': world.city_slug,
               'title': row['title'],
               'zone_slug': world.zone_slug}
    logger.info(json.dumps(payload, ensure_ascii=False))
    result = invoke_inter_service_operation_sync(OperationKeys.PutOrderDeliveries, order_number=world.order_number,
                                                 session_id=world.session_id,
                                                 payload=payload)
    logger.info(result)
    world.status_code = result.Status
    logger.info(world.status_code)


@step(r'set delivery at (\S+)')
def delivery(_, delivery_at: str):
    world.delivery_at = str(delivery_at)


@step('get the questions for service')
def questions(_):
    result = invoke_inter_service_operation_sync(OperationKeys.GetFirstQuestion, order_number=world.order_number
                                                 )
    world.questions = result.Body
    logger.info(world.questions)
    world.status_code = result.Status
    choices(world.questions)


def choices(body):
    world.choices = body.get('choices')
    logger.info(world.choices)
    answer = random.choice(world.choices)
    world.answer = answer['index']
    world.question_slug = body['slug']
    payload = {"values": [f"{world.answer}"]}
    send_answer = invoke_inter_service_operation_sync(OperationKeys.AnswerQuestion,
                                                      order_number=world.order_number,
                                                      session_id=world.session_id,
                                                      question_slug=world.question_slug
                                                      , payload=payload
                                                      )
    logger.info(payload)
    world.questions = send_answer.Body
    logger.info(world.questions)
    world.status_code = send_answer.Status
    if world.questions:
        choices(world.questions)


@step(r'set orders detail')
def set_orders_detail(self):
    row = tools.guess_types(self.hashes)[0]
    world.description = row['description']
    logger.info(world.description)
    result = invoke_inter_service_operation_sync(OperationKeys.PutOrder, order_number=world.order_number,
                                                 session_id=world.session_id,
                                                 payload={
                                                     'description': world.description,
                                                     'delivery_at': world.delivery_at
                                                 }
                                                 )
    logger.info(result)
    world.status_code = result.Status
    logger.info(world.status_code)


@step(r'Customer Login with mobile (\d+) and code (\d+)')
def authentication(_, mobile: str, code: str):
    world.customer_mobile = mobile
    logger.info(world.customer_mobile)
    payload = {"mobile": world.customer_mobile, "code": code}
    duration = invoke_inter_service_operation_sync(OperationKeys.Login, payload=payload)

    result_final = invoke_inter_service_operation_sync(OperationKeys.Login, payload=payload)
    world.status_code = result_final.Status
    logger.info(result_final)
    world.customer_token = result_final.Body['code']
    logger.info(world.customer_token)
    world.customer_user_name = result_final.Body['user_name']
    logger.info(world.customer_user_name)


@step('Some detailed must be show')
def get_order_detailed(_):
    result = invoke_inter_service_operation_sync(OperationKeys.GetOrderBySlug,
                                                 session_id=world.session_id,
                                                 order_number=world.order_number
                                                 )
    world.status_code = result.Status
    world.get_order = result.Body
    logger.info(world.get_order['answers'])
    logger.info(type(world.get_order))
    logger.info(world.status_code)
    if world.status_code == 200:
        for row in world.get_order['answers']:
            assert row['values']


@step('Register as a customer')
def register_customer(self):
    get_username = invoke_inter_service_operation_sync(OperationKeys.GetCustomerUsername, token=world.customer_token
                                                       , user_name=world.customer_user_name)
    if get_username.Status == 404:
        row = tools.guess_types(self.hashes)[0]
        payload = {"first_name": row['first_name'],
                   "last_name": row['last_name'],
                   "national_code": row['national_code'],
                   "picture": row['picture']
                   }
        logger.info(json.dumps(payload, ensure_ascii=False))
        result = invoke_inter_service_operation_sync(OperationKeys.PutCustomers, payload=payload,
                                                     token=world.customer_token)
        logger.info(result)
        world.status_code = result.Status
    world.status_code = 204


@step(r'create customer receipt')
def create_customer_receipt(_):
    result = invoke_inter_service_operation_sync(OperationKeys.PostCustomerReceipt,
                                                 token=world.customer_token,
                                                 payload={"amount": 900000, "bank_slug": "pasargad"})
    world.receipt = result.Body['number']
    logger.info(world.receipt)
    world.status_code = result.Status
    logger.info(world.status_code)


@step('choose and submit voucher code')
def get_voucher(_):
    check = invoke_inter_service_operation_sync(OperationKeys.GetVouchers, token=world.customer_token)
    logger.info(check.Body)
    vouchers = check.Body['value']
    logger.info(vouchers)
    random_voucher = random.choice(vouchers)
    logger.info(random_voucher['code'])
    world.random_voucher_code = random_voucher['code']
    logger.info(type(world.random_voucher_code))
    result = invoke_inter_service_operation_sync(OperationKeys.PutVoucher,
                                                 order_number=world.order_number,
                                                 session_id=world.session_id,
                                                 payload={"code": str(world.random_voucher_code)})
    logger.info(result)
    world.status_code = result.Status
    logger.info(world.status_code)


@step('submit order')
def submit_order(_):
    result = invoke_inter_service_operation_sync(OperationKeys.PostOrder,
                                                 order_number=world.order_number,
                                                 session_id=world.session_id,
                                                 token=world.customer_token)
    logger.info(result)
    world.status_code = result.Status
    logger.info(world.status_code)


@step(r'provider logged in with (\S+) and password (\d+)')
def provider_token(_, username: str, password: str):
    payload = {"mobile": username, "code": password}
    result = invoke_inter_service_operation_sync(constants.OperationKeys.Login, payload=payload)
    result_final = invoke_inter_service_operation_sync(constants.OperationKeys.Login, payload=payload)
    world.provider_mobile = username
    world.status_code = result_final.Status
    logger.info(result_final)
    world.provider_token = result_final.Body['code']
    logger.info(world.provider_token)
    world.provider_user_name = result_final.Body['user_name']
    logger.info(world.provider_user_name)


@step(r'provider register')
def register_provider(self):
    services = invoke_inter_service_operation_sync(OperationKeys.GetCityService,
                                                   **{'$top': 254, 'city_slug': world.city_slug, 'is_enabled': True})
    logger.info(services.Body)
    service_slug_list = list()
    for rows in services.Body['value']:
        service_slug_list.append(rows['slug'])
    logger.info(service_slug_list)
    get_provider_user_name = invoke_inter_service_operation_sync(OperationKeys.GetProviderUsername
                                                                 , user_name=world.provider_user_name,
                                                                 token=world.provider_token)
    logger.info(get_provider_user_name.Body)
    if get_provider_user_name.Status == 404:
        row = tools.guess_types(self.hashes)[0]
        payload = {"first_name": row['first_name'],
                   "last_name": row['last_name'],
                   "gender": row['gender'],
                   "mobile": world.provider_mobile,
                   "national_code": str(random.randint(1000000000, 9999999999)),
                   "service_slug_list": service_slug_list,
                   "city_slug": world.city_slug,
                   "description": row['description'],
                   "success_rate": int(20)
                   }
        logger.info(json.dumps(payload, ensure_ascii=False))
        result = invoke_inter_service_operation_sync(OperationKeys.PostProvider, payload=payload,
                                                     token=world.provider_token)
        logger.info(result.Status)
        world.status_code = result.Status
    world.status_code = 201
    logger.info(world.status_code)


@step(r'create provider receipt')
def create_provider_receipt(_):
    result = invoke_inter_service_operation_sync(OperationKeys.PostProviderReceipt,
                                                 token=world.provider_token,
                                                 payload={"amount": 200000, "bank_slug": "pasargad"})
    world.receipt = result.Body['number']
    logger.info(world.receipt)
    world.status_code = result.Status
    logger.info(world.status_code)


@step(r'get receipt number')
def accept_receipt(_):
    result = invoke_inter_service_operation_sync(OperationKeys.PatchReceipt,
                                                 receipt_number=world.receipt,
                                                 payload={"transition": "create"})
    logger.info(result)
    accept = invoke_inter_service_operation_sync(OperationKeys.PatchReceipt,
                                                 receipt_number=world.receipt,
                                                 payload={"transition": "confirm"})
    logger.info(accept)
    world.status_code = accept.Status
    logger.info(world.status_code)


@step(r'get offers for an order to provider')
def provider_offers(_):
    result = invoke_inter_service_operation_sync(OperationKeys.GetProvidersOffer, token=world.provider_token)
    world.provider_offers = result.Body['value']
    logger.info(world.provider_offers)
    world.status_code = result.Status
    logger.info(result)


@step(r'order that started not be in list')
def not_find_order(_):
    for row in world.provider_offers:
        logger.info(row['order_number'])
        assert row['order_number'] != world.order_number


@step(r'order status must be (\S+)')
def check_status(_, order_status):
    time.sleep(9)
    result = invoke_inter_service_operation_sync(OperationKeys.GetOrderBySlug,
                                                 order_number=world.order_number,
                                                 session_id=world.session_id,
                                                 token=world.customer_token)
    world.order_status = result.Body
    logger.info(world.order_status)
    logger.info(world.order_status['status'])
    assert order_status == world.order_status['status']


@step('get quotes list for an order')
def get_list_quote(_):
    result = invoke_inter_service_operation_sync(OperationKeys.GetQuoteList, token=world.customer_token,
                                                 order_number=world.order_number
                                                 )
    providers = result.Body['value']
    logger.info(providers)
    world.status_code = result.Status
    provider_num = dict
    for row in providers:
        logger.info(row)
        provider_num = row['provider_user_name']
    world.provider_num = provider_num
    logger.info(world.provider_num)


@step(r'create quote from providers to an order')
def provider_quote(self):
    row = tools.guess_types(self.hashes)[0]
    payload = {
        "description": row['description'],
        "final_cost": row['final_cost'],
        "max_cost": row['max_cost'],
        "min_cost": row['min_cost'],
        "working_duration": row['working_duration']
    }
    result = invoke_inter_service_operation_sync(OperationKeys.PostQuoteProvider, token=world.provider_token,
                                                 order_number=world.order_number,
                                                 payload=payload)
    logger.info(result.Body)
    world.status_code = result.Status
    logger.info(result)


@step('check quotes list for an order by customer')
def get_list_quote(_):
    result = invoke_inter_service_operation_sync(OperationKeys.GetQuoteList, token=world.customer_token,
                                                 order_number=world.order_number
                                                 )
    providers = result.Body['value']
    logger.info(providers)
    world.status_code = result.Status
    provider_random = random.choice(providers)

    world.provider_num = provider_random['provider_user_name']
    logger.info(world.provider_num)


@step(r'accept quote for an order by customer')
def customer_quote(_):
    result = invoke_inter_service_operation_sync(OperationKeys.PatchAcceptQuote, token=world.customer_token,
                                                 order_number=world.order_number,
                                                 provider_user_name=world.provider_num)
    world.status_code = result.Status
    logger.info(result)


@step('check quotes list for an order by customer')
def get_list_quote(_):
    result = invoke_inter_service_operation_sync(OperationKeys.GetQuoteList, token=world.customer_token,
                                                 order_number=world.order_number
                                                 )
    providers = result.Body['value']
    logger.info(providers)
    world.status_code = result.Status
    provider_num = dict
    for row in providers:
        logger.info(row)
        provider_num = row['provider_user_name']
    world.provider_num = provider_num
    logger.info(world.provider_num)


@step(r'send quote for an order by provider with final cost (\d+)')
def provider_quote(_, final_cost):
    payload = {
        "final_cost": int(final_cost)
    }
    result = invoke_inter_service_operation_sync(OperationKeys.PatchFinalProvider, token=world.provider_token,
                                                 order_number=world.order_number,
                                                 payload=payload)
    world.status_code = result.Status
    logger.info(result)


@step(r'send final patch by customer')
def accept_invoice(_):
    result = invoke_inter_service_operation_sync(OperationKeys.AcceptInvoiceCustomer, token=world.customer_token,
                                                 order_number=world.order_number
                                                 )
    world.status_code = result.Status
    logger.info(result)


@step('final accept order by provider for finish')
def provider_finish(_):
    result = invoke_inter_service_operation_sync(OperationKeys.PatchFinalProvider, token=world.provider_token,
                                                 order_number=world.order_number
                                                 )

    world.status_code = result.Status
    logger.info(result)


@step(r'order Payment status must be (\S+)')
def check_payment_status(_, order_payment_status):
    result = invoke_inter_service_operation_sync(OperationKeys.GetOrderBySlug,
                                                 order_number=world.order_number,
                                                 session_id=world.session_id,
                                                 token=world.customer_token)
    logger.info(result)
    world.order_payment_status = result.Body
    logger.info(world.order_payment_status)
    logger.info(world.order_payment_status['payment_status'])
    assert order_payment_status == world.order_payment_status['payment_status']


@step(r'patch on order by customer with (\S+)')
def payment_cash_customer(_, payment):
    payload = {
        "payment_status": payment
    }
    result = invoke_inter_service_operation_sync(OperationKeys.PatchPaymentCustomer, token=world.customer_token,
                                                 order_number=world.order_number, payload=payload
                                                 )
    world.status_code = result.Status
    logger.info(result)


@step(r'send patch by provider (\S+)')
def payment_cash_provider(_, pay):
    payload = {
        "payment_status": pay
    }
    result = invoke_inter_service_operation_sync(OperationKeys.PatchPaymentProvider, token=world.provider_token,
                                                 order_number=world.order_number, payload=payload
                                                 )
    world.status_code = result.Status
    logger.info(result)


@step('cancel order by customer')
def cancel_order(_):
    cancel = invoke_inter_service_operation_sync(OperationKeys.CancelOrderCustomer,
                                                 session_id=world.session_id,
                                                 order_number=world.order_number)
    logger.info(cancel)
    world.status_code = cancel.Status


@step('cancel order by operator')
def cancel_order_operator(_):
    cancel = invoke_inter_service_operation_sync(OperationKeys.CancelOrderOperator,
                                                 session_id=world.session_id,
                                                 order_number=world.order_number)
    logger.info(cancel)
    world.status_code = cancel.Status


@step('cancel quote by provider')
def cancel_order_provider(_):
    payload = {
        "reason_slug": "face"
    }
    cancel = invoke_inter_service_operation_sync(OperationKeys.CancelQuoteProvider,
                                                 token=world.provider_token, payload=payload,
                                                 order_number=world.order_number)
    logger.info(cancel)
    world.status_code = cancel.Status


@step('send comment with customer for order')
def comment_order_customer(self):
    row = tools.guess_types(self.hashes)[0]
    payload = {
                  "behavior_appearance": row['behavior_appearance'],
                  "description": row['description'],
                  "fairness": row['fairness'],
                  "is_name_shown": bool(['is_name_shown']),
                  "is_satisfied": bool(row['is_satisfied']),
                  "punctuality": row['punctuality'],
                  "quality": row['quality'],
                  "responsiveness": row['responsiveness']
        }
    result = invoke_inter_service_operation_sync(OperationKeys.CommentOrder,
                                                     token=world.customer_token, payload=payload,
                                                     order_number=world.order_number)
    logger.info(result)
    world.status_code = result.Status


@step('check all comments for this provider')
def get_comments_provider(_):
    result = invoke_inter_service_operation_sync(OperationKeys.GetAllComment,
                                                 token=world.provider_token,
                                                 user_name=world.provider_user_name)
    logger.info(result)
    world.status_code = result.Status


@step('check summery comments for this provider')
def get_summery_comments_provider(_):
    result = invoke_inter_service_operation_sync(OperationKeys.GetCommentSummery,
                                                 token=world.provider_token,
                                                 user_name=world.provider_user_name)
    logger.info(result)
    world.status_code = result.Status
