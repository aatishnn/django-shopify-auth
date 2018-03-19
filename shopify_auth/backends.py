from django.contrib.auth.backends import RemoteUserBackend
from django.conf import settings
from django.contrib.auth.hashers import check_password

class ShopUserBackend(RemoteUserBackend):
    def authenticate(self, request=None, myshopify_domain=None, token=None, **kwargs):
        if not myshopify_domain or not token or not request:
            return

        try:
            user = super(ShopUserBackend, self).authenticate(request=request, remote_user=myshopify_domain)
        except TypeError:
            #  Django < 1.11 does not have request as a mandatory parameter for RemoteUserBackend
            user = super(ShopUserBackend, self).authenticate(remote_user=myshopify_domain)

        if not user:
            return

        user.token = token
        user.save()
        return user

class SuperShopBackend(RemoteUserBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not settings.SHOPIFY_APP_DEV_MODE:
            return

        if not username or not password:
            return

        user = super(SuperShopBackend, self).authenticate(request, remote_user=username)
        if user and user.check_password(password):
            return user
        return
