from django.conf.urls import url

from customauth.views import CustomLogoutView, CustomLoginView, CustomRegisterView, ForceLogoutView, TestView

urlpatterns = [
    url(r'^login/$', CustomLoginView.as_view(), name='rest_login'),
    # URLs that require a user to be logged in with a valid session / token.
    url(r'^logout/$', CustomLogoutView.as_view(), name='rest_logout'),
    url(r'^force_logout/$', ForceLogoutView.as_view(), name='rest_force_logout'),
    url(r'^signup/$', CustomRegisterView.as_view(), name='rest_register'),
    url(r'^test_api/$', TestView.as_view(), name='rest_test_api')
]
