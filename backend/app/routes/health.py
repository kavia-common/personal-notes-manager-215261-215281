from flask_smorest import Blueprint
from flask.views import MethodView

# Health check endpoint under /api for consistency with API prefixing
blp = Blueprint("Health", "health", url_prefix="/api", description="Health check route")


@blp.route("/health")
class HealthCheck(MethodView):
    def get(self):
        """Returns a simple message to indicate the service is healthy."""
        return {"message": "Healthy"}
