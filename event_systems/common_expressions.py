from typing import Any, Dict


NEEDS_INITIALIZATION = "'{class_name}' must be initialized before posting events."
NO_SUBSCRIPTION_FOUND = "No subscription found with '{event}'."


def subscription_success(event_name: str) -> Dict[str, Any]:
    return {
        "success": True,
        "message": f"Successfully subscribed to event: {event_name}",
    }


def subscription_failure(event_name: str, e: Exception) -> Dict[str, Any]:
    return {
        "success": False,
        "message": f"Failed to subscribe to event: {event_name}. Error: {str(e)}",
    }
