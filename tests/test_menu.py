import pytest

from menu import ENTER_TOWN, MAIN_MENU, handle, parse_amount

INVALID_AMOUNT = (
    "END Invalid amount. Enter a number from 1 to 500 with at most 2 decimal places."
)


# --- main menu --------------------------------------------------------------


def test_empty_history_shows_main_menu():
    assert handle("") == (
        "CON Welcome to Demo Wallet\n1. Buy airtime\n2. Register\n3. Check balance\n0. Exit"
    )


def test_default_argument_is_start_of_session():
    assert handle() == MAIN_MENU


@pytest.mark.parametrize("text", ["9", "4", "abc", "*", "00"])
def test_unknown_option(text):
    assert handle(text) == "END Invalid option."


# --- 1. Buy airtime ---------------------------------------------------------


def test_buy_airtime_asks_for_amount():
    assert handle("1") == "CON Enter amount in GHS (1-500):"


def test_buy_airtime_confirmation_formats_amount_to_2dp():
    assert handle("1*20") == "CON Buy GHS 20.00 airtime?\n1. Confirm\n2. Cancel"
    assert handle("1*7.5") == "CON Buy GHS 7.50 airtime?\n1. Confirm\n2. Cancel"


def test_buy_airtime_confirm():
    assert handle("1*20*1") == "END Airtime purchase of GHS 20.00 successful."


def test_buy_airtime_cancel():
    assert handle("1*20*2") == "END Purchase cancelled."


def test_buy_airtime_unknown_confirmation_choice():
    assert handle("1*20*3") == "END Invalid option."


def test_buy_airtime_input_after_confirmation():
    assert handle("1*20*1*1") == "END Invalid option."


@pytest.mark.parametrize("amount", ["1", "500", "1.5", "499.99", " 20 "])
def test_buy_airtime_accepts_amount(amount):
    assert handle(f"1*{amount}").startswith("CON Buy GHS ")


@pytest.mark.parametrize(
    "amount",
    ["", "abc", "0", "0.99", "500.01", "501", "-5", "10.123", "1e2", "10.", ".5", "١٠"],
)
def test_buy_airtime_rejects_amount(amount):
    assert handle(f"1*{amount}") == INVALID_AMOUNT


def test_parse_amount():
    assert parse_amount("1") == "1.00"
    assert parse_amount("12.3") == "12.30"
    assert parse_amount("500.00") == "500.00"
    assert parse_amount("500.001") is None
    assert parse_amount("GHS 5") is None


# --- 2. Register ------------------------------------------------------------


def test_register_asks_for_name():
    assert handle("2") == "CON Enter your full name:"


def test_register_asks_for_town():
    assert handle("2*Ama Mensah") == "CON Enter your town:"


def test_register_success():
    assert handle("2*Ama Mensah*Kumasi") == "END Registered Ama Mensah, Kumasi."


def test_register_trims_whitespace():
    assert handle("2*  Kofi Boateng *  Tamale ") == "END Registered Kofi Boateng, Tamale."


def test_register_name_length_boundaries():
    assert handle("2*Al") == ENTER_TOWN
    assert handle("2*" + "a" * 60) == ENTER_TOWN


@pytest.mark.parametrize("name", ["", " ", "A", "a" * 61])
def test_register_rejects_name(name):
    assert handle(f"2*{name}") == "END Invalid name. Use 2 to 60 characters."


@pytest.mark.parametrize("town", ["", "  ", "X", "x" * 41])
def test_register_rejects_town(town):
    assert handle(f"2*Ama Mensah*{town}") == "END Invalid town. Use 2 to 40 characters."


def test_register_input_after_town():
    assert handle("2*Ama Mensah*Kumasi*1") == "END Invalid option."


# --- 3. Check balance / 0. Exit ---------------------------------------------


def test_check_balance():
    assert handle("3") == "END Balance: GHS 42.50"


def test_check_balance_extra_input():
    assert handle("3*1") == "END Invalid option."


def test_exit():
    assert handle("0") == "END Goodbye."


def test_exit_extra_input():
    assert handle("0*1") == "END Invalid option."
