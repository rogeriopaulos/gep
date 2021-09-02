# -*- coding: utf-8 -*-

import notifications.urls
from ckeditor_uploader.views import browse as ckeditor_browse_view
from ckeditor_uploader.views import upload as ckeditor_upload_view
from core.views import busca_multi_orgaos, busca_multi_orgaos_api
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views import defaults as default_views
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('{}'.format(settings.ADMIN_URL), admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('conta/', include('account.urls', namespace='account')),
    path('processos/', include('adm.urls', namespace='adm')),
    path('ckeditor/upload/', login_required(ckeditor_upload_view), name="ckeditor_upload"),
    path('ckeditor/browse/', never_cache(ckeditor_browse_view), name="ckeditor_browse"),
    path('notificacao/', include('notifier.urls', namespace='notifier')),
    path('busca/', busca_multi_orgaos, name='busca_multi_orgaos'),
    path('busca/json/', busca_multi_orgaos_api, name='busca_multi_orgaos_api'),
    path('manutencao/', include('maintenance_mode.urls')),
    path('session_security/', include('session_security.urls')),
    path('inbox/notificacoes/', include(notifications.urls, namespace='notifications')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path('400/', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        path('403/', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        path('404/', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        path('500/', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
