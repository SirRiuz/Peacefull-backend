


# Rest_framework
from http.client import BAD_REQUEST
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView



# Serializers
from .serialisers import *



# Models
from .models import *




class SearchView(ListAPIView):
    
    serializer_class = SearchSerializer
    pagination_class = LimitOffsetPagination

    
    def get(self,request,*args,**kwargs) -> (Response):
        responseData = super().list(self,request,*args,**kwargs).data
        return Response({ 'data':responseData },status=HTTP_200_OK)


    def get_queryset(self) -> (list):
        param = self.request.GET.get('q',None)
        query = None
        
        if not param:
            return []
        
        query = Item.objects.filter(title__startswith=param)
        return query




class ItemView(APIView):


    def post(self,request,**kwargs) -> (Response):       
        data = ItemSerializer(data=request.data)
        data.is_valid()
        
        if not data.is_valid():
            return Response({
                'status':'error',
                'error':data.error_messages
            },status=BAD_REQUEST)
            

        result = data.create(**data.data,_file=request.FILES['file'])
        if result.get('status') == 'error':
            return Response({
                'status':'error',
                'error':result['error']
            },status=BAD_REQUEST)
            
        
        return Response({ 'status':'ok', 'data':result['item'] })
    
    
    def delete(self,request,**kwargs) -> (Response):
        id = kwargs.get('itemId')
        ItemSerializer().delete(id=id)
        return Response({ 'status':'ok' })





class ProgramsView(ListAPIView): 
    
    serializer_class = ProgramSerialzer
    
    def __formatResponse(self,data,context=None) -> (Response):
        return Response({
            'status':'ok' if data else 'error',
            'data':data ,
            'context':context
        })
    
           
    def get(self,request,*args, **kwargs) -> (Response):
                        
        programId = kwargs.get('programId')
        semester = kwargs.get('semester')
        itemId = kwargs.get('itemId')
        signatureId = kwargs.get('signatureId')

        if programId and semester and signatureId and itemId:
            data = self.get_serializer().getItem(itemId=itemId)
            return self.__formatResponse(data,'view_item')
        
        if programId and semester and signatureId:
            items = self.get_serializer().getAllItems(signatureId=signatureId)
            return self.__formatResponse(items,'item')
     
     
        if programId and semester:
            data = self.get_serializer().getAllSignatures(
                programId=programId,
                semester=semester
            )
            return self.__formatResponse(data,'signature')
       
        if programId:
            data = self.get_serializer().getAllSemesters(programId=programId)
            return self.__formatResponse(data,'semester')
        
        return self.__formatResponse(
            self.get_serializer().getAllPrograms(),'program')
    

