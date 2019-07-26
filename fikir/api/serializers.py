from rest_framework import serializers
from fikir.models import Department, Idea, IdeaType, Photo

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            'id',
            'DepartmentName',
            'Description']

class IdeaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdeaType
        fields = ('IdeaName', 'Icon')

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('Image', 'ImageType')
  

class IdeaSerializer(serializers.ModelSerializer):
    Ideatype = IdeaTypeSerializer(many=False, read_only=True)
    Department = DepartmentSerializer(many=False, read_only=True)
    photo_set = PhotoSerializer(many=True,read_only=True)
    class Meta:
        model = Idea
        fields = [
            'id',
            "Title",      
            "Ideatype",
            "Description",
            "Department",
            "photo_set",
            "CreatedDate"]

