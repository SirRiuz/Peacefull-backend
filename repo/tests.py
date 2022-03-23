

# Django
from django.test import TestCase


# Models
from .models import *




#program = Program.objects.create(name='Ing informatica',id=1)
#print(program)

program = Program.objects.get(name='Ing informatica')
semester = Semester.objects.get(program=program)

# semester = Semester.objects.create(
#     id=1,
#     program=program,
#     semester='1'
# )

print(semester)


#print(program.id)