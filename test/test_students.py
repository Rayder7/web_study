import pytest
from http import HTTPStatus
from web_study.api.models import Student
from fixtures import student


def test_filter_student(student):
    assert Student.objects.filter(first_name="Пупкин").exists()

def test_update_student(student):
    student.first_name = "Непупкин"
    student.save()
    student_from_db = Student.objects.get(name="Непупкин")
    assert student_from_db.first_name == "Пупкин"

@pytest.mark.django_db(transaction=True)
class Test01StudentAPI:

    def test_01_student_not_auth(self, client):
        response = client.get('/api/students/')
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            'Эндпоинт `/api/students/` не найден. Проверьте настройки в '
            '*urls.py*.'
        )
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что GET-запрос неавторизованного пользователя к '
            '`/api/students/` возвращает ответ со статусом 200.'
        )

    def test_02_student_with_admin_user(self, admin_client):
        student_count = 0

        url = '/api/students/'
        data = {}
        response = admin_client.post(url, data=data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если POST-запрос администратора, отправленный к `{url}`, '
            'содержит некорректные данные - должен вернуться ответ со '
            'статусом 400.'
        )

        data = {
            'first_name': 'Пупа',
            'last_name': 'Пупкин',
            'sur_name': 'Пупкович',
            'sex': 'MAN',
            'course': 1
            
        }
        response = admin_client.post(url, data=data)
        assert response.status_code == HTTPStatus.CREATED, (
            f'Если POST-запрос администратора, отправленный к `{url}`, '
            'содержит корректные данные - должен вернуться ответ со статусом '
            '201.'
        )
        student_count += 1

        post_data = {
            'first_name': 'Пупиния',
            'last_name': 'Пупкина',
            'sur_name': 'Пупковна',
            'sex': 'WOMAN',
            'course': 1
        }
        response = admin_client.post(url, data=post_data)
        assert response.status_code == HTTPStatus.CREATED, (
            f'Если POST-запрос администратора к `{url}` '
            'содержит корректные данные - должен вернуться ответ со статусом '
            '201.'
        )
        student_count += 1

        response = admin_client.get(url)
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что при GET-запросе к `{url}` возвращается статус '
            '200.'
        )
        data = response.json()
        check_pagination(url, data, student_count, post_data)


    def test_03_student_delete_admin(self, admin_client):
        student_1, student_2 = create_student(admin_client)
        response = admin_client.delete(
            f'/api/v1/categories/{student_1["slug"]}/'
        )
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            'Проверьте, что DELETE-запрос администратора к '
            '`/api/v1/categories/{slug}/` возвращает ответ со статусом 204.'
        )
        response = admin_client.get('/api/v1/categories/')
        test_data = response.json()['results']
        assert len(test_data) == 1, (
            'Проверьте, что DELETE-запрос администратора к '
            '`/api/v1/categories/{slug}/` удаляет категорию.'
        )

        response = admin_client.get(
            f'/api/v1/categories/{category_2["slug"]}/'
        )
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, (
            'Проверьте, что GET-запросы к `/api/v1/categories/{slug}/` '
            'запрещены и возвращают ответ со статусом 405.'
        )
        response = admin_client.patch(
            f'/api/v1/categories/{category_2["slug"]}/'
        )
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, (
            'Проверьте, что PATCH-запросы к `/api/v1/categories/{slug}/` '
            'запрещены и возвращают ответ со статусом 405.'
        )

    def test_05_category_check_permission_admin(self, client,
                                                user_client,
                                                moderator_client,
                                                admin_client):
        categories = create_categories(admin_client)
        data = {
            'name': 'Музыка',
            'slug': 'music'
        }
        url = '/api/v1/categories/'
        check_permissions(client, url, data, 'неавторизованного пользователя',
                          categories, HTTPStatus.UNAUTHORIZED)
        check_permissions(user_client, url, data,
                          'пользователя с ролью `user`', categories,
                          HTTPStatus.FORBIDDEN)
        check_permissions(moderator_client, url, data, 'модератора',
                          categories, HTTPStatus.FORBIDDEN)