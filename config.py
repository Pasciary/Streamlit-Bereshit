USAR_MOCK = True

if USAR_MOCK:
    from gui import mock as api
else:
    from gui import client as api