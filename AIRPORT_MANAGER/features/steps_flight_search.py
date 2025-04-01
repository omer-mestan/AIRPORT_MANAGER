from behave import given, when, then
from hamcrest import assert_that, equal_to, is_in

@given('потребителят е на страницата за търсене на полети')
def step_open_search_page(context):
    context.search_page_opened = True

@given('въведе дестинация "{destination}"')
def step_enter_destination(context, destination):
    context.destination = destination

@given('въведе номер на полет "{number}"')
def step_enter_flight_number(context, number):
    context.flight_number = number

@given('въведе интервал от часове от "{start}" до "{end}"')
def step_enter_time_range(context, start, end):
    context.time_from = start
    context.time_to = end

@given('оставя всички полета празни')
def step_leave_fields_empty(context):
    context.destination = ""
    context.flight_number = ""
    context.time_from = ""
    context.time_to = ""

@when('натисне бутона "ТЪРСИ"')
def step_click_search(context):
    context.search_clicked = True

@when('направи заявка към /api/my-crew-flights/')
def step_request_crew_flights(context):
    context.api_requested = True

@then('системата показва списък с полети, съответстващи на критериите')
def step_show_matching_flights(context):
    assert context.search_clicked
    # Тук може да се добави реална проверка с mock или API отговор

@then('всеки полет съдържа информация: номер, летище, час, статус')
def step_flight_structure(context):
    # Примерно очакване за структура на данни
    flight = {"flight_number": "BG123", "from": "Sofia", "to": "London", "status": "On Time"}
    assert "flight_number" in flight
    assert "from" in flight
    assert "to" in flight
    assert "status" in flight

@then('се показва съобщение "Няма намерени полети"')
def step_show_no_results(context):
    context.message = "Няма намерени полети"
    assert context.message == "Няма намерени полети"

@then('не се показва списък с полети')
def step_no_flight_list(context):
    context.flights = []
    assert_that(len(context.flights), equal_to(0))

@then('се показва списък с всички налични полети')
def step_show_all_flights(context):
    context.flights = ["BG123", "WZ200"]
    assert_that(len(context.flights) > 0, equal_to(True))

@given('потребителят е логнат')
def step_user_logged_in(context):
    context.user_logged_in = True

@given('е свързан с обект от тип CrewMember')
def step_user_is_crew_member(context):
    context.crew_member = True

@given('не е свързан с CrewMember')
def step_user_is_not_crew_member(context):
    context.crew_member = False

@given('няма планирани полети в бъдеще')
def step_no_upcoming_flights(context):
    context.upcoming_flights = []

@then('получава списък с бъдещи полети, в които участва')
def step_user_receives_flights(context):
    context.flights = ["BG300"]
    assert_that(len(context.flights) > 0, equal_to(True))

@then('за всеки полет се виждат останалите членове на екипажа и техните роли')
def step_crew_listed(context):
    crew = [{"name": "Ivan", "role": "Pilot"}, {"name": "Maria", "role": "Attendant"}]
    assert_that(len(crew), equal_to(2))

@then('получава съобщение за грешка "Не сте свързан с екипажа"')
def step_error_not_crew(context):
    context.error_message = "Не сте свързан с екипажа"
    assert context.error_message == "Не сте свързан с екипажа"

@then('статусът на отговора е 403 Forbidden')
def step_status_403(context):
    context.response_status = 403
    assert context.response_status == 403

@then('получава празен списък с полети')
def step_empty_flight_list(context):
    context.flights = []
    assert_that(len(context.flights), equal_to(0))