import reflex as rx

config = rx.Config(
    app_name="gce",
    db_url="sqlite:///gce.db",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)
