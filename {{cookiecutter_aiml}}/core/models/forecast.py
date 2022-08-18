from math import prod



# TODO: {{cookiecutter.author}} need to be configurable?
class ForecastRuleSystem:
    def __init__(self):
        pass

    def __check_for_data_availability(self, service_account_id: str):
        """
        Refer to account summary collection to find if latest data is availble for
        the provided service account and return the available data in terms of months
        """
        pass

    # TODO: {{cookiecutter.author}} interval?
    def get_period_frequency(self, service_account_id: str):
        """
        based on the availability of data collected the frequency of period
        that has to be considered for forecasting is suggested

        For example:
            if 1 < datapoints_available_in_months < 20:
                period_frequency = "daily"
            else:
                period_frequency = "monthly"
        """
        pass
