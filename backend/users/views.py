from api.serializers import CustomUserSerializer
from .models import User
from api.pagination import CustomPagination
from core.constants import ARGUMENTS_TO_ACTION_DECORATORS
from core.servises import (create_subscription,
                           delete_subscription,
                           get_author_in_subscription,
                           get_subscriptions_serializer_with_pages)
from rest_framework.decorators import action
from djoser.views import UserViewSet

class CustomUserViewSet(UserViewSet):
    """Custom Djoser viewset for User model."""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = CustomPagination

    @action(**ARGUMENTS_TO_ACTION_DECORATORS.get('post_del'))
    def subscribe(self, request, id):
        if request.method == 'POST':
            return create_subscription(
                request=request, user=request.user, author_id=id,
            )
        return delete_subscription(
            user=request.user, author_id=id
        )

    @action(**ARGUMENTS_TO_ACTION_DECORATORS.get('get'))
    def subscriptions(self, request):
        return (
            self.get_paginated_response(
                get_subscriptions_serializer_with_pages(
                    request=request,
                    pages=self.paginate_queryset(
                        get_author_in_subscription(user=request.user)
                    )
                ).data
            )
        )
