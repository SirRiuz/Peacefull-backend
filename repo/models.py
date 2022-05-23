
# Models
from this import d
from django.db import models


# Settins
from core.settings import CDN_URL




# program - semestre - asignatura - file


class Program(models.Model):
        
    name = models.CharField(
        max_length=20,
        unique=True,
        null=False,help_text='Program name'
    )
    
    dateCreated = models.DateField(auto_now_add=True)
    
    
    @property
    def countSemesters(self) -> (list):
        count = Semester.objects.filter(program=self)
        return len(count)
    
    
    def __str__(self) -> (str):
        return self.name



class Semester(models.Model):
    
    program = models.ForeignKey(
        to=Program,
        on_delete=models.CASCADE,
        null=False,
        help_text='Semester the program'
    )
    
    semester = models.CharField(
        max_length=100,
        null=False,
        help_text='Semester number'
    )
    
    
    def __str__(self) -> (str):
        return f'{self.program.name} - {self.semester}'

    

class Signature(models.Model):
    
    
    semester = models.ForeignKey(
        to=Semester,
        on_delete=models.CASCADE,
        null=False
    )
    
    name = models.CharField(
        null=False,
        max_length=500,
        help_text='Signature name'
    )
    
    dateCreated = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return f'{self.name}#{self.id}'
    


class Item(models.Model):
    
    signature = models.ForeignKey(to=Signature,on_delete=models.CASCADE)
    
    title = models.CharField(
        null=False,
        max_length=200,
        help_text='Title the item'
    )
    
    # by = ''
    # program = ''
    
    fileOrigin = models.CharField(
        null=False,
        max_length=1000,
        help_text='The adress of item'
    )
    
    date = models.DateField(auto_now_add=True)
    
    
    @property
    def item (self) -> (dict):
        print(self.fileOrigin)
        return ({
            'self':f'{CDN_URL}media/{self.fileOrigin}',
            'name':self.fileOrigin
        })
    
    
    
    def __str__(self) -> str:
        return self.fileOrigin
