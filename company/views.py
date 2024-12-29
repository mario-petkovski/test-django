from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import Company
from .serializers import CompanySerializer, CompanyUpdateSerializer
from company.functions import send_company_creation_email


class CompanyCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CompanySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            company = serializer.save(owner=request.user)

            send_company_creation_email(company)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, company_id):
        company = get_object_or_404(Company, id=company_id)

        if company.owner != request.user:
            raise PermissionDenied("You do not have permission to view this company.")

        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        page_size = int(request.query_params.get('page_size', 1))
        page_number = int(request.query_params.get('page_number', 1))

        page_number = page_number - 1

        offset = page_number * page_size
        limit = offset + page_size

        order_by = request.query_params.get('ordering', 'id')

        valid_ordering_fields = ['id', 'company_name', 'number_of_employees']
        if order_by.lstrip('-') not in valid_ordering_fields:
            order_by = 'id'
        companies = Company.objects.filter(owner=request.user).order_by(order_by)[offset:limit]
        total_count = Company.objects.filter(owner=request.user).count()

        serializer = CompanySerializer(companies, many=True)

        return Response({
            "total_count": total_count,
            "page_size": page_size,
            "page_number": page_number + 1,
            "results": serializer.data
        })


class CompanyDeleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, company_id):
        try:
            company = Company.objects.get(id=company_id)

            if company.owner != request.user:
                return Response(
                    {"detail": "You do not own this company and cannot delete it."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            return Response(
                {"detail": "You are not allowed to delete this company."},
                status=status.HTTP_403_FORBIDDEN,
            )
        except Company.DoesNotExist:
            return Response(
                {"detail": "Company not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class CompanyUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, company_id):
        try:
            company = Company.objects.get(id=company_id)

            if company.owner != request.user:
                return Response(
                    {"detail": "You do not own this company and cannot update it."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = CompanyUpdateSerializer(company, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Company.DoesNotExist:
            return Response(
                {"detail": "Company not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


