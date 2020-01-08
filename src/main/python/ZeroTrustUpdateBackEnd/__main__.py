from ZeroTrustUpdateBackEnd import Feed
import os

API_KEY = os.getenv("OTX_API_KEY")
OUTPUT_FILE = os.getenv("RULES_FILE")
REFRESH_RATE = os.getenv("REFRESH_RATE")


if API_KEY is not None and OUTPUT_FILE is not None and REFRESH_RATE is not None:
    refresh = int(REFRESH_RATE)
    feed = Feed()
    feed.open(api_key=API_KEY)
    feed.run(refresh, OUTPUT_FILE)
else:
    print("Environment variables aren't defined")