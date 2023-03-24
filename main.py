from bs4 import BeautifulSoup as bs
import requests
import values
import logging


homepage = requests.get(values.URL)
soup = bs(homepage.text, "html.parser")
csrf_name = soup.find(attrs={"name":values.KEY_CSRF_NAME}).get("value")
csrf_token = soup.find(attrs={"name":values.KEY_CSRF_TOKEN}).get("value")

#print(tag_inputs)
logging.info(f"{values.KEY_CSRF_NAME}: {csrf_name}")
logging.info(f"{values.KEY_CSRF_TOKEN}: {csrf_token}")

s = requests.session()
print(s.get(values.URL).cookies)
login_payload = {
    values.KEY_LOGIN: values.LOGIN,
    values.KEY_PASSWORD: values.PASSWORD,
    values.KEY_CSRF_NAME: csrf_name,
    values.KEY_CSRF_TOKEN: csrf_token
}
login_result = s.post(values.LOGIN_REQ_URL, headers=values.USER_AGENT_HEADERS, data=login_payload)

print(login_result.status_code)

# csrf_token = s.get(values.URL).cookies[values.KEY_CSRF_TOKEN]
# csrf_name = s.get(values.URL).cookies[values.KEY_CSRF_NAME]
#
# print(f"TOKEN {csrf_token}")
# print(f"NAME {csrf_name}")
