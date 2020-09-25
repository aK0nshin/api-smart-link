from api_smart_link.handlers import duty, v1

routes = [
    ('*', '/_health', duty.HealthHandler, 'health'),

    # v1
    ('*', '/api/v1/pages', v1.PagesHandler, 'pages')
]
