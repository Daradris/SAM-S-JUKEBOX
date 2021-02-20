class controller:
    def __init__(self):
        pass


class PythonSwitchStatement:

    ACTION_QR_CODES = {}

    def execute(self, qr_code):
        default = ""
        return getattr(self, 'case_' + str(month), lambda: default)()

    def case_1(self):
        return "January"

    def case_2(self):
        return "February"

    def case_3(self):
        return "March"

    def case_4(self):
        return "April"

    def case_5(self):
        return "May"

    def case_6(self):
        return "June"

s = PythonSwitchStatement()

print(s.switch(1))
print(s.switch(3))
print(s.switch(9))