from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^registration', views.registration, name='registration'),
    url(r'^error$', views.error, name='error'),
    url(r'^$', views.log_in, name='login'),
    url(r'^home$', views.home, name='home'),
    url(r'^inputs$', views.inputs, name='inputs'),
    url(r'^fsapl$', views.fsapl, name='fsapl'),
    url(r'^fsapl_excel$', views.fsapl_excel, name='fsapl_excel'),
    url(r'^fsabs$', views.fsabs, name='fsabs'),
    url(r'^fsabs_excel$', views.fsabs_excel, name='fsabs_excel'),
    url(r'^dcf$', views.dcf, name='dcf'),
    url(r'^wacc$', views.wacc, name='wacc'),
    url(r'^wacc_excel$', views.wacc_excel, name='wacc_excel'),
    url(r'^user_details$', views.user_details, name='user_details'),
    url(r'^logout$', views.log_out, name='logout'),
    url(r'^vdcf$', views.vdcf, name='vdcf'),
    url(r'^delete_input$', views.delete_input, name='delete_input'),
    url(r'^exportDcf$', views.dcf_export),
    url(r'^wacc_delete$', views.wacc_delete, name='wacc_delete$'),
    url(r'^fsapl_delete$', views.fsapl_delete, name='fsapl_delete'),
    url(r'^fsabs_delete$', views.fsabs_delete, name='fsabs_delete'),
    url(r'^dcf_delete$', views.dcf_delete, name='dcf_delete$'),
]
