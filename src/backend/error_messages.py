from enum import Enum


class ErrorMessages(Enum):
    NO_API_KEY = "API key not given"
    INVALID_API_KEY = "API key given is not valid"
    RATE_LIMIT = "You have reached your rate limit. See here for more " \
                 "information: " \
                 "https://platform.openai.com/docs/guides/rate-limits/overview"
