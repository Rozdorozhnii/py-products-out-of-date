import datetime
import pytest
from unittest.mock import patch


from app.main import outdated_products

products_to_check = [
    {
        "name": "salmon",
        "expiration_date": datetime.date(2022, 2, 10),
        "price": 600
    },
    {
        "name": "chicken",
        "expiration_date": datetime.date(2022, 2, 5),
        "price": 120
    },
    {
        "name": "duck",
        "expiration_date": datetime.date(2022, 2, 1),
        "price": 160
    }
]


class TestOutdatedProducts:
    @pytest.mark.parametrize(
        "products, year_to_mock, month_to_mock, date_to_mock, expected_result",
        [
            pytest.param(
                products_to_check,
                2022,
                1,
                5,
                [],
                id="should return empty list as outdated if today is 5/1/2022"
            ),
            pytest.param(
                products_to_check,
                2022,
                2,
                5,
                ["duck"],
                id="should return 'duck' as outdated if today is 5/2/2022"
            ),
            pytest.param(
                products_to_check,
                2022,
                2,
                6,
                ["chicken", "duck"],
                id="should return 'duck' as outdated if today is 6/2/2022"
            ),
            pytest.param(
                products_to_check,
                2022,
                2,
                11,
                ["salmon", "chicken", "duck"],
                id="should return 'duck' as outdated if today is 11/2/2022"
            ),
        ]
    )
    def test_outdated_products(
            self,
            products: list,
            year_to_mock: int,
            month_to_mock: int,
            date_to_mock: int,
            expected_result: list,
    ) -> None:
        with (patch("app.main.datetime") as mock_datetime):
            mock_datetime.date.today.return_value = datetime.date(
                year_to_mock,
                month_to_mock,
                date_to_mock)
            assert outdated_products(products) == expected_result
