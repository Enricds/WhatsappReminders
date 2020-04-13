FROM ibmfunctions/action-python-v3.7

RUN pip install \
  --upgrade pip \
  datetime \
  twilio \
  pytz
