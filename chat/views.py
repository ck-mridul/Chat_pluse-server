from .models import Document
from rest_framework import viewsets
from .serializers import DocumentSerializer

# Create your views here.

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer