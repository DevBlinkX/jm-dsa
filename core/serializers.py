from .models import *
from rest_framework import serializers

#Write here logics
class LeadSerializers(serializers.ModelSerializer):
    pass


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category Model
    """
    class Meta:
       model = Category
       fields =  ('id', 'name', 'slug', 'is_active')


class TagsSerializer(serializers.ModelSerializer):
    """
    Serializer for Tags Model
    """
    class Meta:
       model = Tags
       fields =  ('id', 'name', 'slug')

class KnowlageCenterSerializer(serializers.ModelSerializer):
    """
    Serializer for KnowlageCenter Model
    """
    category = CategorySerializer(many=False, read_only=True,)
    tags = TagsSerializer(many=True, read_only=True,)

    class Meta:
       model = KnowlageCenter
       fields =  ('id', 'title', 'category', 'tags', 'slug', 'content','image','created_at','new_date_format')


class KnowlageAssetsSerializer(serializers.ModelSerializer):
    """
    Serializer for KnowlageAssets Model
    """
    knowlage = KnowlageCenterSerializer(many=False, read_only=True,)

    class Meta:
       model = KnowlageAssets
       fields =  ('id', 'file', 'knowlage', 'type','created_at')

# class FaqSerializer(serializers.ModelSerializer):

#     class Meta:
#        model = Faq
#        fields =  ('id', 'question', 'answer' ,'created_at')