import os
import django
from django.conf import settings
from django.urls import path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# ==== Configuración mínima de Django ====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DEBUG=True,
    SECRET_KEY='waaaaaaa',
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],
    MIDDLEWARE=[],
    INSTALLED_APPS=[],
)

django.setup()

VALID_MAP = {
    "abc123": "bronze",
    "def456": "silver",
    "xyz789": "diamond",
    "fsaoikOIJFOIJfiJDSOepSOLDFJOI": "demo"
}

# ==== Vista del endpoint /api/ ====
@csrf_exempt
def validate_code(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            vcode = body.get("vcode")
            if vcode in VALID_MAP:
                if vcode == "MmNKeoKOKOSKOfqiqoOEPLPopdm":
                    return JsonResponse({"valid": "true", "plan": VALID_MAP[vcode], "ltcbal": 0.14364})
                return JsonResponse({"valid": "true", "plan": VALID_MAP[vcode]})
            else:
                return JsonResponse({"valid": "error"})
        except json.JSONDecodeError:
            return JsonResponse({"valid": "error", "error": "Invalid JSON"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

@csrf_exempt
def send_req(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            wallet = body.get("wallet")
            amount = body.get("amount")
            if vcode in VALID_MAP:
                return JsonResponse({"valid": "true", "plan": VALID_MAP[vcode]})
            else:
                return JsonResponse({"valid": "error"})
        except json.JSONDecodeError:
            return JsonResponse({"valid": "error", "error": "Invalid JSON"})
    return JsonResponse({"error": "Method not allowed"}, status=405)

# ==== URL routing ====
urlpatterns = [
    path("api/", validate_code),
]

# ==== Servidor Railway ====
if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    import sys

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "__main__")

    # Usa el puerto de Railway si está definido
    port = os.environ.get("PORT", "8000")
    sys.argv = ["server.py", "runserver", f"0.0.0.0:{port}"]
    execute_from_command_line(sys.argv)
