from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet

from polls.models import Country, Poll


class CountryField(serializers.IntegerField):
    def to_representation(self, value):
        # Country('AUS').label => 'Australia'
        return Country(value).label

    def to_internal_value(self, value):
        # Country['AUSTRALIA'] => <Country.AUSTRALIA: 'AUS'>
        return Country[value.upper()]


class EditPollSerializer(serializers.ModelSerializer):
    modified_by = serializers.CharField(source='modified_by.username')

    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_by', 'pub_date', 'modified_by']


class RetrievePollSerializer(serializers.ModelSerializer):
    lastest_vote = serializers.SerializerMethodField()
    country = CountryField()

    class Meta:
        model = Poll
        fields = fields = ['id', 'question', 'created_by', 'pub_date', 'country', 'lastest_vote']

    def get_lastest_vote(self, obj):
        return obj.vote_set.order_by('timestamp').last().choice.choice_text


class PollSerializer(serializers.ModelSerializer):
    country = CountryField()

    class Meta:
        model = Poll
        fields = ['id', 'question', 'created_by', 'pub_date', 'country']


class AdminPollViewSet(ModelViewSet):
    def get_queryset(self):
        admin = User.objects.get(username='admin')
        return Poll.objects.filter(created_by=admin).order_by('id')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrievePollSerializer

        if self.action == 'partial_update':
            return EditPollSerializer

        return PollSerializer
