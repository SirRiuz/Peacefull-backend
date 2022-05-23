

# rest_framework
from pyexpat import model
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


class ItemSerializer(serializers.Serializer):
    
    file = serializers.FileField(required=True)
    title = serializers.CharField(required=True)
    signatureId = serializers.IntegerField(required=True)
    
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
        requests.post(URL,json=data)


    def create(self,**kwargs) -> (dict):
        signatureId = kwargs['signatureId']
        title = kwargs['title']
        file = kwargs['_file']
        
        signature = Signature.objects.filter(id=signatureId)
        signature = signature[0] if signature else None
        
        if signature:
            cndFile = self.__saveToCdn(file=file)
            if not cndFile:
                return ({
                    'status':'error',
                    'error':{
                        'messege':'Error to send file',
                        'type-error':'cnd-conection-error'
                    }
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
        
        else:
            return ({
                'status':'error',
                'error':{
                    'messege':'The signature not exists',
                    'type-error':'signature-error'
                }
            })


    def delete(self,**kwargs) -> (dict):
        id = kwargs.get('id')
        
        if id:
            item = Item.objects.filter(id=id)
            item = item[0] if item else None
            
            if item:
                self.__deleteToCnd(fileName=item.fileOrigin)
                item.delete()
                return
        

class ProgramSerialzer(serializers.ModelSerializer):
    class Meta(object):
        model = Program
        fields = [ 'id','name','countSemesters' ]
        
    
    def getItem(self,**kwargs) -> (object):
        try:
            item = Item.objects.get(id=kwargs['itemId'])
            return ({
                'author':{},
                'item':{
                    'title':item.title,
                    'self':item.fileOrigin
                }
            })
        except:
            return None

    
    def getAllItems(sefl,**kwargs) -> (list):
        signature = Signature.objects.filter(id=kwargs['signatureId'])
        
        if signature:
            itemList = Item.objects.filter(signature=signature[0]).values()
            return itemList

    
    def getAllPrograms(self) -> (list):
        return Program.objects.all().values()
    
    
    def getAllSignatures(self,**kwargs) -> (object):
        try:
            semester = Semester.objects.get(id=kwargs['semester'])
            signatures = Signature.objects.filter(semester=semester).values()
            return signatures
        except:
            return None
    
    
    def getAllSemesters(self,**kwargs) -> (list):
        try:
            program = Program.objects.get(id=kwargs['programId'])
            return Semester.objects.filter(program=program).values()
        except:
            return None