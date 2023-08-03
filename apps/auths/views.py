# Python
from typing import Any, Dict

#Django
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import (
    render, 
    redirect,
    resolve_url
)
from django.views import View
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView, 
    View, 
    DetailView
)
from django.views.generic.edit import UpdateView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, UpdateView
from django.utils.decorators import method_decorator
from django.core.validators import EmailValidator
# from rest_framework import mixins, viewsets, response, status, generics

#Local
from auths import (
    forms,
    models,
)


class UserRegisrtrationView(CreateView):
    """
    RegistrationView for custom user.
    """

    form_class = forms.CustomUserForm
    success_url = reverse_lazy('registraion')
    template_name = 'auths/registration.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context
    
    def form_valid(self, form):
        custom_user = form.save(commit=False)
        custom_user.password = make_password(form.cleaned_data['password'])
        custom_user.save()
        # return reverse_lazy('index')
        return render(self.request, 'auths/registration_success.html')


class CustomLoginView(LoginView):
    """
    CustomLoginView.
    """

    template_name = 'auths/login.html'
    # form_class = forms.CustomLoginForm
    def form_invalid(self, form: AuthenticationForm) -> HttpResponse:
        return super().form_invalid(form)
    
    def get_success_url(self):
        return resolve_url('base')


class CustomLogoutView(View):
    """
    CustomLogoutView.
    """

    def get(self, request) -> HttpResponse:
        if request.user:
            logout(request)
        
        return redirect('index')
    
    
@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView):
    """
    ProfileDetailView.
    """

    model = models.CustomUser
    template_name = 'auths/profile.html'
    context_object_name = 'user'
    pk_url_kwarg = 'pk'

    def get_object(self, queryset=None):
        user = get_object_or_404(models.CustomUser, pk=self.kwargs['pk'])
        return user

        
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    ProfileUpdateView.
    """

    model = models.CustomUser
    template_name = 'auths/update_profile.html'
    fields = ['email', 'nickname']

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        nickname = form.cleaned_data.get('nickname')

        if not EmailValidator()(email):
            form.add_error('email', 'Недопустимый формат почты')
        
        if len(nickname) < 1:
            form.add_error('first_name', 'Недопустимой длины данные')

        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)


class CustomUserPasswordChange(View):
    """
    CustomUserPasswordChange."""
    
    template_name = "auths/change_password.html"
    def get(self, request, *args, **kwargs):
        context = {"user": request.user}
        
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        current_password = request.POST.get("old_pass")
        if current_password:
            if request.user.check_password(current_password):
                new_password = request.POST.get('new_pass', '').strip()
                confirm_password = request.POST.get('confirm_new_pass', '').strip()
                if new_password and confirm_password and new_password == confirm_password:
                    request.user.set_password(new_password)
                    request.user.save()
                    return redirect('logout')
                else:
                    messag = 'Поля «Новый пароль» и «Подтверждение пароля» должны совпадать!'
                    messages = ""
                    context = {
                        
                        'messag': messag,
                        'messages':messages,
                    }
                    return render(request, 'main/profile.html', context)
            else:
                messag = 'Текущий пароль неверный!'
                messages = ""
                context = {
                    
                    'messag': messag,
                    'messages':messages,
                }
                return render(request, 'auths/change_profile', context)

        
# class OrderCreateViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
#     """
#     OrderCreateViewSet.
#     """

#     def create(self, request, *args, **kwargs):
#         is_many = isinstance(request.data, list)
#         if not is_many:
#             return super(OrderCreateViewSet, self).create(request, *args, **kwargs)
#         else:
#             user_id = request.data[0].get('user_id')
#             existing_orders = models.Order.objects.filter(user_id=user_id, is_done=False)
#             existing_orders_map = {order.food_id: order for order in existing_orders}
#             updated_orders = []

#             for order_data in request.data:
#                 food_id = order_data.get('food_id')
#                 existing_order = existing_orders_map.get(food_id)

#                 if existing_order:
#                     # Check if quantity, price, or total_price has changed
#                     if (existing_order.quantity != order_data['quantity'] or
#                             existing_order.price != order_data['price'] or
#                             existing_order.total_price != order_data['total_price']):
#                         existing_order.quantity = order_data['quantity']
#                         existing_order.price = order_data['price']
#                         existing_order.total_price = order_data['total_price']
#                         existing_order.save()
#                         updated_orders.append(existing_order)
#                 else:
#                     order_data['food'] = food_id
#                     order_data['user'] = user_id
#                     serializer = OrderSerializer(data=order_data)
#                     serializer.is_valid(raise_exception=True)
#                     updated_order = serializer.save()
#                     updated_orders.append(updated_order)

#             # Delete remaining orders in existing_orders_map (deleted items from cart)
#             for order in existing_orders_map.values():
#                 order.delete()

#             response_serializer = OrderSerializer(updated_orders, many=True)
#             headers = self.get_success_headers(response_serializer.data)
#             return response.Response(response_serializer.data, status.HTTP_201_CREATED, headers=headers)


# class PurchaseCreateApiView(generics.CreateAPIView):
#     """
#     ViewSet class to create purchase and update is_done status of related orders.
#     """

#     queryset = models.Purchase.objects.all()
#     serializer_class = PurchaseSerializer
#     def perform_create(self, serializer):
#         user = self.request.user
#         order_data = models.Order.objects.filter(user=user, is_done=False).values()
#         payment = self.request.data.get('payment', models.PaymentTypes.CASH)
#         address = self.request.data.get('address', '')
#         franchise_id = self.request.data.get("franchise")

#         # Retrieve the Franchise instance
#         franchise = models.Franchise.objects.get(id=franchise_id)

#         purchase_data = {
#             'order': list(order_data),
#             'payment': payment,
#             'address': address,
#             'franchise': franchise,
#         }

#         # Convert datetime objects to ISO 8601 string format
#         for order in purchase_data['order']:
#             order['datetime_created'] = order['datetime_created'].isoformat()

#         serializer.save(**purchase_data)

#         models.Order.objects.filter(user=user).update(is_done=True)


#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)

#         headers = self.get_success_headers(serializer.data)
#         return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



