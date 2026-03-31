from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    app_name: str = "MediScope Worker"
    debug: bool = False

    # Auth
    worker_api_key: str = ""

    # Supabase
    supabase_url: str = ""
    supabase_secret_key: str = ""

    # Crawler limits
    crawler_timeout: int = 30
    crawler_max_pages: int = 50
    crawler_max_depth: int = 3

    # Rate limiting
    rate_limit_rpm: int = 10

    # PageSpeed Insights API (optional)
    pagespeed_api_key: str = ""

    # Perplexity API (optional, for GEO/AEO AI search checks)
    perplexity_api_key: str = ""

    # Gemini API (optional, for GEO/AEO AI search checks)
    gemini_api_key: str = ""

    # International Search (optional)
    google_cse_id: str = ""  # Google Custom Search Engine ID
    naver_client_id: str = ""
    naver_client_secret: str = ""

    # Supabase Storage
    supabase_storage_bucket: str = "reports"
    supabase_image_bucket: str = "generated-images"

    # Resend API (optional, for alert emails)
    resend_api_key: str = ""

    # LINE Messaging API (optional)
    line_channel_secret: str = ""
    line_channel_access_token: str = ""

    # WeChat Official Account (optional)
    wechat_token: str = ""
    wechat_app_id: str = ""
    wechat_app_secret: str = ""


settings = Settings()
