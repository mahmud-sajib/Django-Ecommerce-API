from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

import braintree

# Create your views here.

# BrainTree Credentials
gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="4ymx8dm8hyz2x6rt",
        public_key="6wt4d62db8rfsy7b",
        private_key="4741def360e584d5141d06e9b0f64dfc"
    )
)

# User Authentication view
def validate_user_session(id, token):
    """Allow payment completion for only authenticated users"""
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

# Generate Payment Token view
@csrf_exempt
def generate_token(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error':'Inavlid Session. Please login again'})
    
    # Generate token if user is authenticated
    return JsonResponse({'clientToken':gateway.client_token.generate(), 'success':True})

# Process Payment view
@csrf_exempt
def process_payment(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error':'Inavlid Session. Please login again'})

    # Get the payment nonce from client  
    nonce_from_the_client = request.POST["paymentMethodNonce"]
    # Get the amount from client
    amount_from_the_client = request.POST["amount"]

    # Process the payment
    result = gateway.transaction.sale({
        "amount": amount_from_the_client,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })

    # Post payment results
    if result.is_success:
        return JsonResponse({
            'success':result.is_success,
            'transaction':{
                'id':result.transaction.id,
                'amount':result.transaction.amount
            }
        })
    else:
        return JsonResponse({'error':True, 'success':False})
    

