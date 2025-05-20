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
    class Meta:
        model = Profile
        fields = ['user', 'phone_number']
        read_only_fields = ['user']

class ListingSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'price', 'status',
            'created_at', 'updated_at', 'expires_at',
            'author', 'category', 'tags', 'image'
        ]

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        category_data = validated_data.pop('category', None)
        listing = Listing.objects.create(**validated_data)

        if category_data:
            cat, _ = Category.objects.get_or_create(**category_data)
            listing.category = cat
        for t in tags_data:
            tag, _ = Tag.objects.get_or_create(**t)
            listing.tags.add(tag)
        listing.author = self.context['request'].user
        listing.save()
        return listing

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)