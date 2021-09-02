from django.http import HttpResponseRedirect
from django.urls import reverse


class ForceChangePasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (
            request.user.is_authenticated
            and not request.user.is_superuser
            and request.user.profile.alterar_senha
        ):
            while not (request.path == reverse("account:minha_conta")):
                return HttpResponseRedirect(reverse("account:minha_conta"))
        return response
