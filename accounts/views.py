# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User, Organisation
from .serializers import UserSerializer, OrganisationSerializer
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user_data = serializer.data
        refresh = RefreshToken.for_user(User.objects.get(email=user_data['email']))
        return Response({
            "status": "success",
            "message": "Registration successful",
            "data": {
                "accessToken": str(refresh.access_token),
                "user": user_data
            }
        }, status=status.HTTP_201_CREATED)
    return Response({"errors": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.get(email=email)
        if not user.check_password(password):
            raise ValueError("Invalid password")
        refresh = RefreshToken.for_user(user)
        return Response({
            "status": "success",
            "message": "Login successful",
            "data": {
                "accessToken": str(refresh.access_token),
                "user": {
                    "userId": user.userId,
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "phone": user.phone
                }
            }
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
        }, status=status.HTTP_401_UNAUTHORIZED)
    except ValueError:
        return Response({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, id):
    try:
        user = User.objects.get(userId=id)
        serializer = UserSerializer(user)
        return Response({
            "status": "success",
            "message": "User details fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({
            "status": "error",
            "message": "User not found",
            "statusCode": 404
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_organisations(request):
    user = request.user
    organisations = user.organisations.all()
    serializer = OrganisationSerializer(organisations, many=True)
    return Response({
        "status": "success",
        "message": "Organisations fetched successfully",
        "data": {"organisations": serializer.data}
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_organisation(request, orgId):
    try:
        organisation = Organisation.objects.get(orgId=orgId)
        if request.user not in organisation.users.all():
            return Response({
                "status": "error",
                "message": "You do not have access to this organisation",
                "statusCode": 403
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = OrganisationSerializer(organisation)
        return Response({
            "status": "success",
            "message": "Organisation details fetched successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    except Organisation.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Organisation not found",
            "statusCode": 404
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_organisation(request):
    serializer = OrganisationSerializer(data=request.data)
    if serializer.is_valid():
        organisation = serializer.save()
        organisation.users.add(request.user)
        return Response({
            "status": "success",
            "message": "Organisation created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_user_to_organisation(request, orgId):
    try:
        organisation = Organisation.objects.get(orgId=orgId)
        user = User.objects.get(userId=request.data['userId'])
        organisation.users.add(user)
        return Response({
            "status": "success",
            "message": "User added to organisation successfully"
        }, status=status.HTTP_200_OK)
    except Organisation.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Organisation not found",
            "statusCode": 404
        }, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({
            "status": "error",
            "message": "User not found",
            "statusCode": 404
        }, status=status.HTTP_404_NOT_FOUND)
