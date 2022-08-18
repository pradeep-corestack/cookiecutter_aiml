class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Environment(Enum):
    LOCAL = "LOCAL"
    DEV = "DEV"
    QA = "QA"
    SANDBOX = "SANDBOX"
    PRODUCTION = "PRODUCTION"

    def get(env: str):
        env = env.lower()
        return {
            "dev": Environment.DEV,
            "qa": Environment.QA,
            "sandbox": Environment.SANDBOX,
            "prod": Environment.PRODUCTION,
            "production": Environment.PRODUCTION,
        }


class ServiceName(Enum):
    AWS = "AWS"
    Azure = "Azure"
    GCP = "GCP"
    OCI = "OCI"
