from rest_framework import serializers

from company.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'company_name', 'description', 'number_of_employees']

    def validate(self, data):
        user = self.context['request'].user
        if user.companies.count() >= 5:
            raise serializers.ValidationError("You can only create up to 5 companies.")
        return data


class CompanyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['number_of_employees']

    def validate_number_of_employees(self, value):
        if value < 1:
            raise serializers.ValidationError("The number of employees must be greater than 0.")
        return value
