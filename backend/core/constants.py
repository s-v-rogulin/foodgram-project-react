from rest_framework.permissions import IsAuthenticated

# User
MAX_EMAEL_LENGHT = 254
MAX_USER_LENGHT = 100


# Recipe
MAX_TAG_COLOR_LENGHT = 7
MAX_NAME_SLUG_MEASUREMENT_UNIT_LENGHT = 200
MIN_TEXT_LENGHT = 2
MIN_HEX_LENGHT = 4
MIN_MEASUREMENT_UNIT_LENGHT = 1
MIN_COOKING_TIME = 1
MAX_COOKING_TIME = 500
MIN_AMOUNT = 1
MAX_AMOUNT = 999

# Decorators
ARGUMENTS_TO_ACTION_DECORATORS = {
    'post_del': {
        'methods': ('post', 'delete',),
        'detail': True,
        'permission_classes': (IsAuthenticated,),
    },
    'get': {
        'detail': False,
        'permission_classes': (IsAuthenticated,),
    },
}
