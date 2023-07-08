from http import HTTPStatus

import pytest


@pytest.mark.django_db(transaction=True)
class Test01UserAPI:
    def test_01_users_not_authenticated(self, client):
        response = client.get('/api/v1/users/')

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            'Эндпоинт `/api/v1/users/` не найден. Проверьте настройки в '
            '*urls.py*.'
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Проверьте, что GET-запрос к `/api/v1/users/` без токена '
            'авторизации возвращается ответ со статусом 401.'
        )

    def test_02_users_username_not_authenticated(self, client, admin):
        response = client.get(f'/api/v1/users/{admin.username}/')

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            'Эндпоинт `/api/v1/users/{username}/` не найден. Проверьте '
            'настройки в *urls.py*.'
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Проверьте, что GET-запрос `/api/v1/users/{username}/` без '
            'токена авторизации возвращает ответ со статусом 401.'
        )

    def test_03_users_me_not_authenticated(self, client):
        response = client.get('/api/v1/users/me/')

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            'Эндпоинт `/api/v1/users/me/` не найден. Проверьте настройки '
            'в *urls.py*.'
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Проверьте, что GET-запрос `/api/v1/users/me/` без токена '
            'авторизации возвращает ответ со статусом 401.'
        )


    def test_05_04_users_post_user_superuser(self, user_superuser_client,
                                             django_user_model):
        valid_data = {
            'username': 'TestUser_3',
            'email': 'testuser3@yamdb.fake'
        }
        response = user_superuser_client.post(
            '/api/v1/users/', data=valid_data
        )
        assert response.status_code == HTTPStatus.CREATED, (
            'Если POST-запрос суперпользователя к `/api/v1/users/` '
            'содержит корректные данные - должен вернуться ответ со статусом '
            '201.'
        )
        users_after = (
            django_user_model.objects.filter(email=valid_data['email'])
        )
        assert users_after.exists(), (
            'Если POST-запрос суперпользователя к `/api/v1/users/` '
            'содержит корректные данные - должен быть создан новый '
            'пользователь.'
        )

    def test_06_users_username_get_admin(self, admin_client, moderator):
        response = admin_client.get(f'/api/v1/users/{moderator.username}/')
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            'Эндпоинт `/api/v1/users/{username}/` не найден. Проверьте '
            'настройки в *urls.py*.'
        )
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос администратора к '
            '`/api/v1/users/{username}/` возвращает ответ со статусом 200.'
        )

        response_data = response.json()
        expected_keys = (
            'first_name', 'last_name', 'username', 'email'
        )
        for key in expected_keys:
            assert response_data.get(key) == getattr(moderator, key), (
                'Проверьте, что ответ на GET-запрос администратора к '
                '`/api/v1/users/{username}/` содержит данные пользователя.'
                f'Сейчас ключ {key} отсутствует в ответе либо содержит '
                'некорректные данные.'
            )

    
    def test_08_02_users_username_delete_moderator(self, moderator_client,
                                                   user, django_user_model):
        users_cnt = django_user_model.objects.count()
        response = moderator_client.delete(f'/api/v1/users/{user.username}/')
        assert response.status_code == HTTPStatus.FORBIDDEN, (
            'Проверьте, что DELETE-запрос модератора к '
            '`/api/v1/users/{username}/` возвращает ответ со статусом 403.'
        )
        assert django_user_model.objects.count() == users_cnt, (
            'Проверьте, что DELETE-запрос модератора к '
            '`/api/v1/users/{username}/` не удаляет пользователя.'
        )

    def test_08_03_users_username_delete_user(self, user_client, user,
                                              django_user_model):
        users_cnt = django_user_model.objects.count()
        response = user_client.delete(f'/api/v1/users/{user.username}/')
        assert response.status_code == HTTPStatus.FORBIDDEN, (
            'Проверьте, что DELETE-запрос пользователя с ролью `user` к '
            '`/api/v1/users/{username}/` возвращает ответ со статусом 403.'
        )
        assert django_user_model.objects.count() == users_cnt, (
            'Проверьте, что DELETE-запрос пользователя с ролью `user` к'
            '`/api/v1/users/{username}/` не удаляет пользователя.'
        )

    def test_08_04_users_username_delete_superuser(self, user_superuser_client,
                                                   user, django_user_model):
        users_cnt = django_user_model.objects.count()
        response = user_superuser_client.delete(
            f'/api/v1/users/{user.username}/'
        )
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            'Проверьте, что DELETE-запрос суперпользователя к '
            '`/api/v1/users/{username}/` возвращает ответ со статусом 204.'
        )
        assert django_user_model.objects.count() == (users_cnt - 1), (
            'Проверьте, что DELETE-запрос суперпользователя к '
            '`/api/v1/users/{username}/` удаляет пользователя.'
        )

    def test_09_users_me_get(self, user_client, user):
        response = user_client.get('/api/v1/users/me/')
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос обычного пользователя к '
            '`/api/v1/users/me/` возвращает ответ со статусом 200.'
        )

        response_data = response.json()
        expected_keys = ('username', 'role', 'email', 'bio')
        for key in expected_keys:
            assert response_data.get(key) == getattr(user, key), (
                'Проверьте, что GET-запрос к `/api/v1/users/me/` возвращает '
                'данные пользователя в неизмененном виде. Сейчас ключ '
                f'`{key}` отсутствует либо содержит некорректные данные.'
            )

    def test_09_02_users_me_delete_not_allowed(self, user_client, user,
                                               django_user_model):
        response = user_client.delete('/api/v1/users/me/')
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, (
            'Проверьте, что DELETE-запрос к `/api/v1/users/me/` возвращает '
            'ответ со статусом 405.'
        )
        user = (
            django_user_model.objects.filter(username=user.username).first()
        )
        assert user, (
            'Проверьте, что DELETE-запрос к `/api/v1/users/me/` не удаляет '
            'пользователя.'
        )

   
    @pytest.mark.parametrize(
        'data,messege', invalid_data_for_user_patch_and_creation
    )
    def test_10_02_users_me_has_field_validation(self, user_client, data,
                                                 messege):
        url = '/api/v1/users/me/'
        request_method = 'PATCH'
        response = user_client.patch(url, data=data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            messege[0].format(url=url, request_method=request_method)
        )

    def test_10_03_users_me_patch_change_role_not_allowed(self,
                                                          user_client,
                                                          user,
                                                          django_user_model):
        data = {
            'first_name': 'New user first name',
            'last_name': 'New user last name',
            'bio': 'new user bio',
        }
        response = user_client.patch('/api/v1/users/me/', data=data)
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что PATCH-запрос пользователя с ролью `user` к '
            '`/api/v1/users/me/` возвращает ответ со статусом 200.'
        )

        current_role = user.role
        data = {
            'role': 'admin'
        }
        response = user_client.patch('/api/v1/users/me/', data=data)
        user = django_user_model.objects.filter(username=user.username).first()
        assert user.role == current_role, (
            'Проверьте, что PATCH-запрос к `/api/v1/users/me/` с ключом '
            '`role` не изменяет роль пользователя.'
        )