import os
import requests
from dotenv import load_dotenv
from rest_framework import status, validators

load_dotenv()


class OneId:
    _base_url = os.getenv('BASE_URL')
    _client_id = os.getenv('CLIENT_ID')
    _client_secret = os.getenv('CLIENT_SECRET')
    _scope = os.getenv('Scope')
    _redirect_uri = os.getenv('REDIRECT_URI')
    _state = os.getenv('STATE')

    def initializer(self):
        return f"{self._base_url}?response_type=one_code&client_id={self._client_id}&redirect_uri={self._redirect_uri}&Scope={self._scope}&state={self._state}"

    def get_oneId_access_token(self, code):
        reqUrl = f"{self._base_url}?grant_type=one_authorization_code&client_id={self._client_id}&client_secret={self._client_secret}&code={code}&redirect_uri=%2Foauth%2Foauth-test.jsp"
        res = requests.request("POST", reqUrl)

        if res.status_code is not status.HTTP_200_OK:
            raise validators.ValidationError(
                detail={"message": "something is error because OneId code is none"}, code=status.HTTP_400_BAD_REQUEST)

        res = res.json()
        return res, res.get("access_token")

    def get_user_info_from_oneId(self, access_token):
        reqUrl = f"{self._base_url}?grant_type=one_access_token_identify&client_id={self._client_id}&client_secret={self._client_secret}&access_token={access_token}&scope={self._scope}"
        response = requests.request("POST", reqUrl)

        if response.status_code is not status.HTTP_200_OK:
            raise validators.ValidationError(
                detail={"message": "something is error because OneId access token is none"}, code=status.HTTP_400_BAD_REQUEST)

        return response.json()

    def logout_from_oneId(self, access_token):
        reqUrl = f"{self._base_url}?grant_type=one_log_out&client_id={self._client_id}&client_secret={self._client_secret}&access_token={access_token}&scope={self._scope}"
        if requests.request("POST", reqUrl).status_code is not status.HTTP_200_OK:
            raise validators.ValidationError(
                detail={"message": "something is error because OneId access token is none"}, code=status.HTTP_400_BAD_REQUEST)
