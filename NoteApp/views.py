from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from NoteApp.serializers import RegisterSerializer,NotesSerializer,TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from NoteApp.models import NotesDb,TaskDb
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class RegistrationView(APIView):
    def post(self,request):
        serializer_instance = RegisterSerializer(data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={
                "Message" : "Registration Successful"
            })
        else:
            return Response(data=serializer_instance.errors)
        
class NoteListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        notes = NotesDb.objects.filter(user=request.user)
        serializer_instance = NotesSerializer(notes,many=True)
        return Response(serializer_instance.data)
    def post(self,request):
        serializer_instance = NotesSerializer(data=request.data)

        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(serializer_instance.data, status=201)

        return Response(serializer_instance.errors, status=400)

class RetreiveUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            note = NotesDb.objects.get(id=pk, user=request.user)
            serializer_instance = NotesSerializer(note)
            return Response(serializer_instance.data)

        except NotesDb.DoesNotExist:
            return Response({
                "Message": "Note not found"
            }, status=404)

    def put(self, request, pk):
        try:
            note = NotesDb.objects.get(id=pk, user=request.user)
            serializer_instance = NotesSerializer(note,data=request.data)
            if serializer_instance.is_valid():
                serializer_instance.save()
                return Response({
                    "Message": "Note updated successfully",
                    "Data": serializer_instance.data})
            return Response(serializer_instance.errors,status=400)
        except NotesDb.DoesNotExist:
            return Response({"Message": "Note not found"}, status=404)
    
    def delete(self, request, pk):
        try:
            note = NotesDb.objects.get(id=pk,user=request.user )
            note.delete()
            return Response({"Message": "Note deleted successfully"}, status=200)
        except NotesDb.DoesNotExist:
            return Response({ "Message": "Note not found"}, status=404)
# class NotesRetrieveUpdateDeleteView(APIView):
#     permission_classes=[IsAuthenticated]
#     def get_object(self,request,id):
#         return get_object_or_404(NotesDb,id=id,user=request.user)
#     def put(self,request,id):
#         note = self.get 
#     def delete(self,request,id):
#         note=self.get_object(request,id)
#         note.delete()
#         return Response(
#             ("message":"Note deleted successfully")
#         )
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        request.user.auth_token.delete()
        return Response({
            "Message":"Logout Success"
        })
        

class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notes = TaskDb.objects.filter(user=request.user)
        serializer_instance = TaskSerializer(notes, many=True)
        return Response(serializer_instance.data, status=200)

    def post(self, request):
        serializer_instance = TaskSerializer(data=request.data)

        if serializer_instance.is_valid():
            serializer_instance.save(user=request.user)
            return Response(serializer_instance.data, status=201)

        return Response(serializer_instance.errors, status=400)

class TaskReteriveUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def get_task(self,request,id):
        return get_object_or_404(TaskDb,id=id,user=request.user)

    def get(self, request, id):
        task = self.get_task(request, id)
        serializer_instance = TaskSerializer(task)
        return Response(serializer_instance.data, status=404)
    def put(self, request, id):
        task = self.get_task(request, id)
        serializer_instance = TaskSerializer(task,data=request.data)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response({
                "Message": "Task updated successfully",
                "Data": serializer_instance.data}, status=200)
        return Response(serializer_instance.errors,status=400)
    def delete(self, request, id):
        task = self.get_task(request, id)
        task.delete()
        return Response({
            "Message": "Task deleted successfully" }, status=200)
        
class JWT_Logout(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken (refresh_token)
            token.blacklist()
            return Response({
                "Message": "Logout Successful"
            })
        except Exception:
            return Response({
                "Error": "Invalid Refresh token "
            })