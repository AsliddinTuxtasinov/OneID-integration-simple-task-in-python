from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import response, status, validators

from auusers.utils import OneId
oneId = OneId()


class GetCode(APIView):
    permission_classes = ()

    def get(self, *args, **kwargs):
        return redirect(to=oneId.initializer())


class GetOneIdAccessToken(APIView):
    permission_classes = ()

    def get_oneId_code(self):
        oneIdCode = self.request.GET.get('code', None)
        if oneIdCode is None:
            raise validators.ValidationError(
                detail={"message": "OneId code is none"}, code=status.HTTP_400_BAD_REQUEST)
        return oneIdCode

    def get(self, *args, **kwargs):
        oneIdCode = self.get_oneId_code()
        res, access_token = oneId.get_oneId_access_token(code=oneIdCode)
        self.request.session['oneIdCode'] = oneIdCode
        self.request.session['oneIdAccessToken'] = access_token

        return response.Response(data=res, status=status.HTTP_200_OK)


class GetUserInfoFromOneId(APIView):
    permission_classes = ()

    def get_oneId_access_token(self):
        access_token = self.request.session.get('oneIdAccessToken')
        if access_token is None:
            raise validators.ValidationError(
                detail={"message": "OneId access token none"}, code=status.HTTP_400_BAD_REQUEST)
        return access_token

    def get(self, *args, **kwargs):
        user_info = oneId.get_user_info_from_oneId(access_token=self.get_oneId_access_token())
        return response.Response(data=user_info, status=status.HTTP_200_OK)


class LogoutFromOneId(APIView):
    def get_oneId_code_access_token(self):
        oneIdCode = self.request.session.get('oneIdCode')
        access_token = self.request.session.get('oneIdAccessToken')

        if access_token and oneIdCode is None:
            raise validators.ValidationError(
                detail={"message": "OneId oneId code or access token none"}, code=status.HTTP_400_BAD_REQUEST)

        return oneIdCode, access_token

    def post(self, *args, **kwargs):
        oneIdCode, access_token = self.get_oneId_code_access_token()
        oneId.logout_from_oneId(access_token=access_token)

        del self.request.session['oneIdCode']
        del self.request.session['oneIdAccessToken']
        self.request.session.modified = True

        return response.Response({"message": "you are successfully logout out from oneId"}, status=status.HTTP_200_OK)
