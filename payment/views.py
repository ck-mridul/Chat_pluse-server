import json
import razorpay
from .models import Order
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from .serializers import OrderSerializer
from rest_framework.response import Response
from authentication.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated



# Create your views here.

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        amount = request.data['amount']
        user = request.user
        
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
        
        payment = client.order.create({"amount": int(amount) * 100, 
                                   "currency": "INR", 
                                   "payment_capture": "1"})
        
        order = Order.objects.create(
            user = user,
            order_product='VClass Premium', 
            order_amount=amount, 
            order_payment_id=payment['id']
        )
        
        serializer = OrderSerializer(order)
        
        data = {
            "payment": payment,
            "order": serializer.data,
            "KEY" : settings.KEY,
            "SECRET" : settings.SECRET
        }
        
        return Response(data)
    
    
class PaymentSuccessView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        res = json.loads(request.data["response"])
        user = request.user
        ord_id = res['razorpay_order_id']
        raz_pay_id = res['razorpay_payment_id']
        raz_signature = res['razorpay_signature']
        
        order = Order.objects.get(order_payment_id=ord_id)

        data = {
            'razorpay_order_id': ord_id,
            'razorpay_payment_id': raz_pay_id,
            'razorpay_signature': raz_signature
        }
        
        print(data)
        client = razorpay.Client(auth=(settings.KEY, settings.SECRET))

        
        try:
            check = client.utility.verify_payment_signature(data)
            print(check)

            if check:
                
                order.isPaid = True
                order.save()
                
                user.premium = True
                user.save()
                
                serializer = UserSerializer(user)

                res_data = {
                    'message': 'payment successfully received!',
                    'user' : serializer.data
                }

                return Response(res_data,status=status.HTTP_200_OK)
        except:
            print("Redirect to error url or error page")
            return Response({'error': 'Something went wrong'},status=status.HTTP_400_BAD_REQUEST)