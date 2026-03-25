from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_prefix": "MEDISCOPE_"}

    app_name: str = "MediScope Worker"
    debug: bool = False

    # Auth
    bearer_token: str = ""

    # Supabase
    supabase_url: str = ""
    supabase_service_key: str = ""

    # Crawler limits
    crawler_timeout: int = 30
    crawler_max_pages: int = 50
    crawler_max_depth: int = 3

    # Rate limiting
    rate_limit_rpm: int = 10

    # PageSpeed Insights API (optional)
    pagespeed_api_key: str = ""


settings = Settings()
