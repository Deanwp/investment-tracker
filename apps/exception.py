from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        customized_response = {}

        if isinstance(response.data, dict):
            errors = []
            for key, value in response.data.items():
                if isinstance(value, list):
                    errors.extend(value)
                else:
                    errors.append(str(value))

            customized_response['errors'] = errors
        else:
            customized_response['errors'] = [str(response.data)]

        customized_response['status_code'] = response.status_code
        customized_response['detail'] = response.status_text if hasattr(response, 'status_text') else ''

        response.data = customized_response

    else:
        return Response({
            'errors': ['An unexpected error occurred. Please try again later.'],
            'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
