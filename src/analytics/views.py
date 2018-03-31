import datetime
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, Avg
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.utils import  timezone

from orders.models import Order

class SalesAjaxView(View):
    def get(self, request, *args, **kwargs):
        data = {}
        if request.user.is_staff:
            qs = Order.objects.all().by_weeks_range(weeks_ago=5, number_of_weeks=5)
            if request.GET.get('type') == 'week':
                days = 7
                start_date = timezone.now().today() - datetime.timedelta(days=days-1)
                datetime_list = []
                labels = []
                salesItems = []
                for x in range(0, days):
                    new_time = start_date + datetime.timedelta(days=x)
                    datetime_list.append(
                            new_time
                        )
                    labels.append(
                        new_time.strftime("%a") # mon
                    )
                    new_qs = qs.filter(updated__day=new_time.day, updated__month=new_time.month)
                    day_total = new_qs.totals_data()['total__sum'] or 0
                    salesItems.append(
                        day_total
                    )
                #print(datetime_list)
                data['labels'] = labels
                data['data'] = salesItems
            if request.GET.get('type') == '4weeks':
                data['labels'] = ["Four Weeks Ago", "Three Weeks Ago", "Two Weeks Ago", "Last Week", "This Week"]
                current = 5
                data['data'] = []
                for i in range(0, 5):
                    new_qs = qs.by_weeks_range(weeks_ago=current, number_of_weeks=1)
                    sales_total = new_qs.totals_data()['total__sum'] or 0
                    data['data'].append(sales_total)
                    current -= 1
        return JsonResponse(data)



class SalesView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/sales.html'

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_staff:
            return render(self.request, "400.html", {})
        return super(SalesView, self).dispatch(*args, **kwargs)


    def get_context_data(self, *args, **kwargs):
        context = super(SalesView, self).get_context_data(*args, **kwargs)
        #two_weeks_ago = timezone.now() - datetime.timedelta(days=14)
        #one_week_ago = timezone.now() - datetime.timedelta(days=7)
        qs = Order.objects.all().by_weeks_range(weeks_ago=10, number_of_weeks=10)
        context['today'] = qs.by_range(start_date=timezone.now().date()).get_sales_breakdown()
        context['this_week'] = qs.by_weeks_range(weeks_ago=1, number_of_weeks=1).get_sales_breakdown()
        context['last_four_weeks'] = qs.by_weeks_range(weeks_ago=5, number_of_weeks=4).get_sales_breakdown()
        # qs = Order.objects.all().by_date()
        # context['orders'] = qs
        # context['recent_orders'] =  qs.recent().not_refunded()
        # context['recent_orders_data'] = context['recent_orders'].totals_data()
        # context['recent_orders_cart_data'] = context['recent_orders'].cart_data()
        # context['shipped_orders'] = qs.recent().not_refunded().by_status(status='shipped')
        # context['shipped_orders_data'] =  context['shipped_orders'].totals_data()
        # context['paid_orders'] = qs.recent().not_refunded().by_status(status='paid')
        # context['paid_orders_data'] = context['paid_orders'].totals_data()
        # context['recent_orders_total'] = context['recent_orders'].aggregate(
        #                                 Sum("total"), 
        #                                 Avg("total"), 
        #                                 # Avg("cart__products__price"), 
        #                                 # Count("cart__products")
        #                             )
        # test in shell
        # context['recent_cart_data'] = context['recent_orders'].aggregate(
        #                                 Avg("cart__products__price"), 
        #                                 Count("cart__products")
        #                             )
        # qs = Order.objects.all().aggregate(Sum("total"), Avg("total"), Avg("cart__products__price"), Count("cart__products"))
        # ann = qs.annotate(product_avg=Avg('cart__products__price'), product_total = Sum('cart__products__price'), product__count = Count('cart__products'))
        # context['shipped_orders'] = qs.recent().not_refunded().by_status(status='shipped')[:5]
        # context['paid_orders'] = qs.recent().not_refunded().by_status(status='paid')[:5]
        return context