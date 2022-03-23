

# rest_framework
from itsdangerous import Serializer
from rest_framework import serializers


# Models
from .models import *


# Python 
import random
import json
import requests


# Settings
from core.settings import CDN_URL



class SearchSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Item
        fields = '__all__'




class ItemSerializer(serializers.ModelSerializer):
    
    
    def __saveToCdn(self,file) -> (dict):
        URL = f'{CDN_URL}api/v1/push-file/'
        data = { 'file':file }
        
        try:
            response = requests.post(URL,files=data)
            response = json.loads(response.text)
            
            if response['status'] == 'ok':
                return (response['name'])
        
        except Exception as e:
            print('[ERROR] > The cnd is not connected')
            return None
        
    
    def __deleteToCnd(self,fileName) -> (None):
        print(fileName)
        data = { 'file_name':fileName }
        URL = f'{CDN_URL}api/v1/delete-file/'
        response = requests.post(URL,json=data)
    
    
    
    def get(self,**kwargs) -> (dict):
        id = kwargs.get('id')
        model = kwargs.get('model')
        
        if id and model:
            item = model.objects.filter(id=id)
            item = item[0] if item else None
            
            if item:
                return({
                    'status':'ok',
                    'item':{
                        'program':item.signature.semester.program.name,
                        'signature':item.signature.name,
                        'by':'',
                        'title':item.title,
                        'description':'',
                        'link':{
                            'name':item.fileOrigin,
                            'self':f'{CDN_URL}media/{item.fileOrigin}/'
                        },
                        'date':item.date
                    }
                })

    def create(self,**kwargs) -> (dict):
        signatureId = kwargs.get('signatureId',0)
        title = kwargs.get('title')
        file = kwargs.get('file')
        
        signature = Signature.objects.filter(id=signatureId)
        signature = signature[0] if signature else None
        
        if signature and title and file:
            cndFile = self.__saveToCdn(file=file)
            
            if not cndFile:
                return ({
                    'status':'error',
                    'messege':'Error to send file',
                    'type-error':'cnd-conection-error'
                })
            
            if cndFile:
                item = Item.objects.create(
                    signature=signature,
                    title=title,
                    fileOrigin=cndFile
                )
                
                return({
                    'status':'ok',
                    'item':{
                        'id':item.id,
                        'name':item.fileOrigin,
                        'program':item.signature.semester.program.name,
                        'signature':item.signature.name
                    }
                })
        


    def delete(self,**kwargs) -> (dict):
        id = kwargs.get('id')
        model = kwargs.get('model')
        
        if id and model:
            item = model.objects.filter(id=id)
            item = item[0] if item else None
            
            if item:
                result = self.__deleteToCnd(fileName=item.fileOrigin)
                print(result)
                item.delete()
                return({ 'status':'ok' })
            
    
    class Meta(object):
        model = Item
        fields = [ 'id','title','item' ]



class SignatureSerializer(serializers.ModelSerializer):
    class Meta(object):
        fields = [ 'id','name' ]
        model = Signature


    def get(self,id,model) -> (dict):
        signature = model.objects.filter(id=id)
        
        if signature:
            signature = signature[0]
            return({
                'status':'ok',
                'signature':{
                    'name':signature.name,
                    'semester':signature.semester.semester,
                    'program':signature.semester.program.__str__(),
                    'articles_size':''
                }
            })
        

    def delete(self,id,model) -> (dict):
        signature = model.objects.filter(id=id)
        
        if signature:
            signature = signature[0]
            signature.delete()
            
            return({ 'status':'ok', 'text':'The signature is deleted' })
            
                    
    
    def create(self,data,programId,semester) -> (dict):
        
        try:
            program = Program.objects.get(id=programId)
            semester = Semester.objects.get(program=program,semester=semester)
            Signature.objects.create(name=data['name'],semester=semester)
            
            return({
                'status':'ok',
                'text':'Signature created'
            })
            
        except Exception as e:
            return None



class ProgramSerialzer(serializers.ModelSerializer):
    class Meta(object):
        model = Program
        fields = [ 'id','name','countSemesters' ]
        
    
    def __createSemesters(self,model,size) -> (None):
        for x in range(1,size + 1):
            Semester.objects.create(program=model,semester=str(x))
        
    
    def get(self,id,model) -> (dict):
        try:
            program = model.objects.get(id=id)
            return ({
                'program':{
                    'id':program.id,
                    'name':program.name,
                    'semesters':program.countSemesters,
                    'description':'',
                }
            })
        except Exception:
            return None
        
        
        
    def delete(self,id,model) -> (bool):
        program = model.objects.filter(id=id)
        
        if program:
            program = program[0].delete()
            return True
        
        return False
 
 
    def create(self,data,model) -> (object):
        try:
            id = random.randint(0,99999999)
            semesters = data.get('semesters',10)
            model = model.objects.create(name=data['name'], id=id)
            self.__createSemesters(model=model,size=semesters)
            return ({
                'status':'ok',
                'program':{
                    'id':model.id,
                    'name':model.name
                }
            })
        except Exception as e:
            return None
        
        
        
        