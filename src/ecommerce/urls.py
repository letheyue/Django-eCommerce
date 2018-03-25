"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.views import LogoutView

from accounts.views import LoginView, RegisterView, GuestRegisterView
from .views import home_page, about_page, contact_page
from addresses.views import checkout_address_create_view, checkout_address_reuse_view, AddressListView, AddressCreateView, AddressUpdateView 
from carts.views import cart_detail_api_view
from billing.views import payment_method_view, payment_method_createview
from marketing.views import MarketingPreferenceUpdateView, MailchimpWebhookView
from orders.views import LibraryView

# from products.views import (
# 		ProductListView, 
# 		product_list_view, 
# 		ProductDetailView, 
# 		product_detail_view,
# 		ProductFeaturedListView,
# 		ProductFeaturedDetailView,
# 		ProductDetailSlugView
# 		)


urlpatterns = [
	url(r'^$', home_page, name='home'),
	url(r'^about/$', about_page, name='about'),
	url(r'^contact/$', contact_page, name='contact'),
	url(r'^login/$', LoginView.as_view(), name='login'),
	url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^bootstrap/$', TemplateView.as_view(template_name='bootstrap/example.html')),
	url(r'^products/', include(("products.urls",'products'), namespace='products')),
    url(r'^search/', include(("search.urls",'search'), namespace='search')),
    url(r'^cart/', include(("carts.urls", 'cart'), namespace='cart')),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/guest/$', GuestRegisterView.as_view(), name='guest_register'),
    url(r'^checkout/address/create/$', checkout_address_create_view, name='checkout_address_create'),
    url(r'^checkout/address/reuse/$', checkout_address_reuse_view, name='checkout_address_reuse'),
    url(r'^api/cart/$', cart_detail_api_view, name='api-cart'),
    url(r'^billing/payment-method/$', payment_method_view, name='billing-payment-method'),
    url(r'^billing/payment-method/create/$', payment_method_createview, name='billing-payment-method-endpoint'),
    url(r'^settings/email/$', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    url(r'^webhooks/mailchimp/$', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),
    #url(r'^accounts/login/$', RedirectView.as_view(url='/login')),
    url(r'^account/', include(("accounts.urls", 'accounts'), namespace='account')),
    url(r'^accounts/$', RedirectView.as_view(url='/account')),
    url(r'^settings/$', RedirectView.as_view(url='/account')),
    url(r'^accounts/', include("accounts.passwords.urls")),
    url(r'^orders/', include("orders.urls", namespace='orders')),  
    url(r'^address/$', RedirectView.as_view(url='/addresses')),
    url(r'^addresses/$', AddressListView.as_view(), name='addresses'), 
    url(r'^addresses/create/$', AddressCreateView.as_view(), name='address-create'),
    url(r'^addresses/(?P<pk>\d+)/$', AddressUpdateView.as_view(), name='address-update'), 
    url(r'^library/$', LibraryView.as_view(), name='library'),
    # url(r'^products/$', ProductListView.as_view()),
    # url(r'^products-fbv/$', product_list_view),
    # # url(r'^products/(?P<pk>\d+)/$', ProductDetailView.as_view()),
    # url(r'^products-fbv/(?P<pk>\d+)/$', product_detail_view),
    # url(r'^featured/$', ProductFeaturedListView.as_view()),
    # url(r'^featured/(?P<pk>\d+)/$', ProductFeaturedDetailView.as_view()),
    # url(r'^products/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()), 
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
	urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)