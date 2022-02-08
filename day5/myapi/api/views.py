from django.shortcuts import render
from .models import Student, Intake
from .serializers import StudentSerializer, IntakeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,  mixins
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets, authentication, permissions

# Create your views here.

# student and intake list and edit using Generic view


class Student_List(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class Intake_List(generics.ListCreateAPIView):
    queryset = Intake.objects.all()
    serializer_class = IntakeSerializer


class StudentDetailsAPI(generics.ListCreateAPIView, mixins.ListModelMixin, mixins.DestroyModelMixin,
                               mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = 'id'

    def list(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def update(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.delete(request, id)


# student and intake list and edit using APIView

class StudentList(APIView):
    def get(self, request):
        students = Student.objects.all()
        student_data = StudentSerializer(students, many=True).data
        return Response(student_data)

    def post(self,request):
        insertstudent = StudentSerializer(data=request.data)
        if insertstudent.is_valid():
            insertstudent.save()
            return Response(insertstudent.data, status=status.HTTP_200_OK)


class IntakeList(APIView):
    def get(self,request):
        intakes = Intake.objects.all()
        intakes_data = IntakeSerializer(intakes, many=True).data
        return Response(intakes_data)

    def post(self,request):
        insert_intake = IntakeSerializer(data=request.data)
        if insert_intake.is_valid():
            insert_intake.save()
            return Response(insert_intake.data,status=status.HTTP_200_OK)

        return Response(insert_intake.errors, status=status.HTTP_400_BAD_REQUEST)


class Student_DetailsAPI(APIView):
    def get_object(self, id):
        try:
            return Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        student = self.get_object(id)
        serializer = StudentSerializer(student).data
        return Response(serializer)

    def put(self, request, id):
        student = self.get_object(id)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        student = self.get_object(id)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






# student and intake list using viewsets
class StudentViewSet(viewsets.ViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class IntakeViewSet(viewsets.ModelViewSet):
    queryset = Intake.objects.all()
    serializer_class = IntakeSerializer


# use function based

@api_view(['GET', 'POST'])
def student_list(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def student_detail(request, pk):
    try:
        students = Student.objects.get(pk=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentSerializer(students)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StudentSerializer(students, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        students.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)