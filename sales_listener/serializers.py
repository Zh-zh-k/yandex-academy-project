from rest_framework import serializers
from .models import Position

from datetime import datetime


def isotime_valid(dt_str):
    try:
        datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except:
        return False
    return True


class PositionSerializer(serializers.Serializer):
    id = serializers.CharField()
    parentId = serializers.CharField(required=False, allow_null=True)
    name = serializers.CharField()
    type = serializers.CharField()
    price = serializers.IntegerField(required=False, allow_null=True)
    date = serializers.CharField(required=False)

    def create(self, validated_data):
        validated_data |= self.context
        try:
            curObj = Position.objects.get(self.validated_data["id"])
            return self.update(curObj, validated_data)
        except:
            print("VC")
            return Position.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print("VU")
        instance.parentId = validated_data.get('parentId', instance.parentId)
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.price = validated_data.get('price', instance.price)
        instance.date = validated_data.get('date', instance.date)
        return instance


    def validate_parentId(self, value) :
        if value == None:
            return value
        try:
            print(value)
            print(Position.objects.all())
            obj = Position.objects.get(id=value)
            if obj.type != "CATEGORY" :
                raise serializers.ValidationError("Parent is not a category")
        except:
            pass
            #raise serializers.ValidationError("Error in getting parent")
    
        return value


    def validate(self, data) :
        if not isotime_valid(self.context['date']) :
            raise serializers.ValidationError("Invalid Date format")

        if not data['type'] in dict(Position.available_types) :
            raise serializers.ValidationError("Invalid Type")
        
        try:
            obj = Position.objects.get(data['id'])
            if obj.type != data["type"]:
                raise serializers.ValidationError("Cannot change offer to category and vice-versa")
        except:
            pass
        
        if data["type"] == "OFFER" :
            if data["price"] is None or data["price"] < 0 :
                raise serializers.ValidationError("Invalid price for item")
        elif data["type"] == "CATEGORY" :
            if "price" in data and not data["price"] is None :
                raise serializers.ValidationError("Invalid price for category")

        return data

