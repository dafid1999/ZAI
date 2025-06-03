from rest_framework import serializers
from ..models import Listing, Category, Tag, Profile

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class ProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user', 'phone_number']
        read_only_fields = ['user']

    def get_phone_number(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.phone_number
        return None


class ListingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')
    tags = serializers.SlugRelatedField(queryset=Tag.objects.all(), slug_field='name', many=True, required=False)

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'price', 'status',
            'created_at', 'updated_at', 'expires_at',
            'author', 'category', 'tags', 'image'
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        listing = Listing.objects.create(**validated_data)
        listing.tags.set(tags)
        return listing

    def update(self, instance, validated_data):
        if 'category' in validated_data:
            instance.category = validated_data.pop('category')
        if 'tags' in validated_data:
            instance.tags.set(validated_data.pop('tags'))
        return super().update(instance, validated_data)