from rest_framework import viewsets
from .serializers import OrderSerializer
from .models import Order
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt


# User Authentication view
def validate_user_session(id, token):
    """Allow ordering for only authenticated users"""
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        
        # Check if Session Token matches User Token
        if user.session_token == token:
            return True # User is authenticated
        else:
            return False # User is unauthenticated
    
    except UserModel.DoesNotExist:
        return False


# Add Order view
def add_order(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error':'Please login again', 'code':'1'})

    if request.method == "POST":
        user_id = id
        transaction_id = request.POST['transaction_id']
        amount = request.POST['amount']
        products = request.POST['products']
        total_no_products = len(products.split(',')[:-1])

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(pk=user_id)
        
        except UserModel.DoesNotExist:
            return JsonResponse({'error':'User does not exist'})

        order_detail = Order(user=user, product_names=products, total_products=total_no_products, total_amount=amount, transaction_id=transaction_id)

        order_detail.save()

        return JsonResponse({'success':True, 'error':False, 'msg':'Order placed successfully'})

# Order View
class OrderViewSet(viewsets.ModelViewSet):
    # Operations to be performed
    queryset = Order.objects.all().order_by('id')
    # Class responsible for serializing the data 
    serializer_class = OrderSerializer












