from datetime import timedelta, date

class DateUtil(object):
    # dictionaries
    date_format_dict = {
            "custom": "%m%d%Y",
            "send_date": "%m, %d, %Y"
    }

    def get_current_date(self, format):
        return date.today().strftime(format)

    def get_ninety_days_before_current_date(self, format):
        return (date.today() - timedelta(90)).strftime(format)

    def get_ninety_days_after_current_date(self, format):
        return (date.today() + timedelta(90)).strftime(format)