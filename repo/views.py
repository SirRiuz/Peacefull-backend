


# Rest_framework
from http.client import BAD_REQUEST
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination


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





class ItemView(ListAPIView):
    
    serializer_class = ItemSerializer
    pagination_class = LimitOffsetPagination
    
    
    def get_queryset(self):
        id = self.kwargs.get('signatureId',0)
        signature = Signature.objects.filter(id=id)
        
        if not signature:
            return []
        
        signature = signature[0]
        
        return Item.objects.filter(signature=signature).order_by('-id')


    def get(self,request,*args,**kwargs) -> (Response):
        itemId = kwargs.get('itemId')
        signatureId = kwargs.get('signatureId')
        
        if signatureId:
            data = super().list(self,request,*args,**kwargs).data
            print(data)
            return Response({ 'data':data },status=HTTP_200_OK)
        
        if itemId:
            data = self.get_serializer().get(id=itemId,model=Item)
            if data:
                return Response({ 'data':data },status=HTTP_200_OK)
            
        return Response({ 'data':{ 'status':'error','type-error':'item-not-exist' } },status=HTTP_400_BAD_REQUEST)
        
    
    
    def post(self,request,*args,**kwargs) -> (Response):
        file = request.FILES.get('file')
        title = request.POST.get('title')
        signatureId = request.POST.get('signatureId')
        
        
        data = self.get_serializer().create(
            file=file,
            title=title,
            signatureId=signatureId,
            model=Item
        )
        
        if data:
            return Response({ 'data':data },status=HTTP_200_OK)
                
        
        return Response({
            'data':{ 'status':'error','type-error':'create-error' }
        },status=HTTP_400_BAD_REQUEST)
    
    
    def delete(self,request,*args,**kwargs) -> (Response):
        itemId = kwargs.get('itemId',0)
        data = self.get_serializer().delete(id=itemId,model=Item)
        
        if data:
            return Response({ 'data':data },status=HTTP_200_OK)
        
        return Response({
            'data':{ 'status':'error','type-error':'delete-error' }
        },status=HTTP_400_BAD_REQUEST)
    



class SignatureView(ListAPIView):
    
    
    serializer_class = SignatureSerializer
    
    
    def get(self,request,signatureId=None,*args, **kwargs) -> (Response):
        
        if signatureId:
            data = self.get_serializer().get( id=signatureId, model=Signature )
            
            if data:
                return Response({ 'data':data },status=HTTP_200_OK)
            
            return Response({
                'data':{ 'status':'error','type-error':'signature-error' }
            },status=HTTP_200_OK)
        
        if self.get_queryset():        
            data = super().list(self, request, *args, **kwargs).data
            return Response({
                'data':{ 'status':'ok', 'signatures':data }
            },status=HTTP_200_OK)
            
        return Response({
            'data':{ 'status':'error','type-error':'signature-error' }
        },status=HTTP_400_BAD_REQUEST)
    
    
    
    def delete(self,request,signatureId=None,*args, **kwargs) -> (Response):
        data = self.get_serializer().delete( id=signatureId, model=Signature )
        
        if not data:
            return Response({
                'data':{ 'status':'error', 'type-error':'signature-error', }
            },status=HTTP_400_BAD_REQUEST)      
              
        return Response(data,status=HTTP_200_OK)

        
    
    def post(self,request,id,semester) -> (Response):
        serializer = self.get_serializer()
        data = serializer.create(data=request.data,programId=id,semester=semester)
        
        if data:
            return Response(data,status=HTTP_200_OK)
        
        return Response({
            'data':{ 'status':'error', 'type-error':'create-error' }
        },status=HTTP_200_OK)
    
    
    
    def get_queryset(self) -> (object):
        try:
            id = self.kwargs.get('id')
            semester = self.kwargs.get('semester')
            program = Program.objects.get(id=id)
            semester = Semester.objects.get(program=program,semester=semester)
            signature = Signature.objects.filter(semester=semester)
            return signature
        except Exception:
            return None



class ProgramsView(ListAPIView): 
    
    
    serializer_class = ProgramSerialzer
    queryset = Program.objects.all()
    
    
    
    def list(self, request, *args, **kwargs) -> (Response):
        data = super().list(request, *args, **kwargs)
        return Response({'data':{'status':'ok','programs':data.data}},status=HTTP_200_OK)
        
        
        
    def get(self, request,id=None, *args, **kwargs) -> (Response):
        serializer = self.get_serializer()
        
        if id:
            data = serializer.get(id=id,model=Program)
            if data:
                return Response(data, status=HTTP_200_OK)
            
            return Response({
                'data':{ 'status':'error', 'type-error':'program-not-exist' }
            },status=BAD_REQUEST)
            
        
        return self.list(self, request, *args, **kwargs)
    
    
    
    def post(self,request,id=None) -> (Response):
        
        serializer = self.get_serializer()
        data = serializer.create(data=request.data,model=Program)
        
        if data:
            return Response(data,status=HTTP_200_OK)
        
        return Response({
            'data':{ 'status':'error', 'type-error':'create-error' }
        },status=BAD_REQUEST)
    
    
    
    def delete(self,request,id=None) -> (Response):
        serializer = self.get_serializer()
        data = serializer.delete(id=id,model=Program)
        
        if data:
            return Response({
                'data':{ 'status':'ok', 'text':'The program is deleted' }
            },status=HTTP_200_OK)
            
        return Response({
            'data':{ 'status':'error', 'type-error':'delete-error' }
        },status=BAD_REQUEST)
        
        
        



