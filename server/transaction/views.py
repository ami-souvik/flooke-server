from rest_framework.views import APIView
from transaction.models import TransactionModel
from transaction.serializers import Transaction

# Create your views here.
class TransactionView(APIView):

    def get(self, request, *args, **kwargs):
        TransactionModel.query()

    def post(self, request, *args, **kwargs):
        Transaction(request.data)
