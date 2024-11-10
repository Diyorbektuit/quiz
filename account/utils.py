import re

email_regex = re.compile(
    r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.["
    r"-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])"
)


def is_valid_email(email):
    if re.match(email_regex, email):
        return True
    else:
        return False