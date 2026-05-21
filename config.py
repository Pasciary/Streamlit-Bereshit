import os

from dotenv import load_dotenv

load_dotenv()

USAR_MOCK = os.getenv("USAR_MOCK", "true").lower() == "true"

if USAR_MOCK:
    from gui import mock as api
else:
    from gui import client as api  # type: ignore[import]
