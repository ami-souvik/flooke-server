from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from transaction.models import TransactionModel
from transaction.serializers import TransactionSerializer

# Create your views here.
class TransactionView(APIView):

    def get(self, request, *args, **kwargs):
        transactions = []
        for m in TransactionModel.query("souvik"):
            transactions.append(m.to_dict())
        return Response(
            {
                'transactions': transactions
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        try:
            serialized = TransactionSerializer(data=request.data)
            serialized.is_valid(raise_exception=True)
            serialized.save()
            return Response(
                {
                    'transaction': str(serialized.data)
                },
                status=status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {
                    'message': f"[ERROR] Request is invalid {e}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
