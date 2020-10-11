from api_smart_link.handlers import duty, v1

routes = [
    ('*', '/_health', duty.HealthHandler, 'health'),

    # v1
    ('*', r'/api/v1/pages/{endpoint:\w+}', v1.PagesByEndpointHandler, 'pages_by_endpoint'),
    ('*', r'/api/v1/users/{user_id:\d+}', v1.UsersHandler, 'users'),
    ('*', r'/api/v1/users/{user_id:\d+}/pages', v1.UsersPagesListHandler, 'users_pages_list'),
    ('*', r'/api/v1/users/{user_id:\d+}/pages/{page_id:\d+}', v1.UsersPagesHandler, 'users_pages'),
    ('*', r'/api/v1/users/{user_id:\d+}/pages/{page_id:\d+}', v1.UsersPagesHandler, 'users_pages'),
]
