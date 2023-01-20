import os
import requests
from dotenv import load_dotenv
load_dotenv()


def get_access_token(code, client_id, client_secret):
    reqUrl = f"{os.getenv('BASE_URL')}?grant_type=one_authorization_code&client_id={client_id}&client_secret={client_secret}&code="+code+"&redirect_uri=%2Foauth%2Foauth-test.jsp"
    res = requests.request("POST", reqUrl).json()
    access_token = res.get("access_token")
    return res, access_token


def get_user_info(access_token, client_id, client_secret, scope):
    reqUrl = f"{os.getenv('BASE_URL')}?grant_type=one_access_token_identify&client_id={client_id}&client_secret={client_secret}&access_token="+access_token+f"&scope={scope}"
    response = requests.request("POST", reqUrl).json()
    return response


def logout_util(client_id, client_secret, access_token, scope):
    reqUrl = f"{os.getenv('BASE_URL')}?grant_type=one_log_out&client_id={client_id}&client_secret={client_secret}&access_token={access_token}&scope={scope}"
    requests.request("POST", reqUrl)
