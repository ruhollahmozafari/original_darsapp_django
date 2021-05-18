
from rest_framework import generics
from rest_framework.response import Response

class DestroyAPIView(generics.DestroyAPIView):

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer_data = self.get_serializer(instance).data
        self.perform_destroy(instance)
        return Response(serializer_data)