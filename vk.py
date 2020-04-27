import requests
import time
from datetime import date, datetime
import sorting as s

# пока использую токен с прошлого диплома
token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'

params = {
    'access_token': token,
    'v': 5.101
}


# функции реализующие get-запросы на получение списка id друзей пользователя и списка сообществ

def get_user_friends():
    response = requests.get('https://api.vk.com/method/friends.get', params)
    print('-')
    friends_list = response.json()['response']['items']
    return friends_list


def get_user_groups():
    response = requests.get('https://api.vk.com/method/groups.get', params)

    print('-')
    groups_list = response.json()['response']['items']
    return groups_list


# Узнаем город, пол, дату рождения, интересы, музыку и книги пользователя
def get_user_info():
    params['fields'] = ['sex, city, bdate, music, books, interests']
    response = requests.get('https://api.vk.com/method/users.get', params)
    print('-')
    info = response.json()
    # print(info)

    # search_users(info)
    return info


def calculate_age(bdate):
    today = date.today()
    age = today.year - bdate.year
    if today.month < bdate.month:
        age -= 1
    elif today.month == bdate.month and today.day < bdate.day:
        age -= 1

    return age


# Устанавливаем параметры (город, пол, возрастной диапозон) поиска и запускаем поиск (пока для теста ограничние 100)
def search_users(user_info):
    # print(user_info)
    city_id = user_info['response'][0]['city']['id']
    sex = 2 if user_info['response'][0]['sex'] == 1 else 1
    bdate_str = user_info['response'][0]['bdate']
    try:
        bdate = datetime.strptime(bdate_str, "%d.%m.%Y")
        age = calculate_age(bdate)
        age_from = age - 2
        age_to = age + 2
    except ValueError:
        print("У подьзователя не указан год рождения")
        age = int(input('Введите ваш возраст'))
        age_from = age - 2
        age_to = age + 2

    params['age_from'] = [age_from]
    params['age_to'] = [age_to]
    params['count'] = [100]
    params['city'] = [city_id]
    params['sex'] = [sex]
    params['status'] = [1, 6]

    response = requests.get('https://api.vk.com/method/users.search', params)
    print('-')
    info = response.json()['response']['items']
    # print(info)
    return info


# проходимся по пользователям, cобираем список сообществ, сравниваем с пользователем
# записываем совпадения в новый словарь с id и совпавшими группами

def compare_friends_groups(users_list):
    result = []
    user_groups = get_user_groups()
    errors = 0

    for user in users_list:
        try:
            params['user_id'] = user['id']
            groups_list = get_user_groups()

            user_coincidences = {
                'id': user['id'],
                'matching_groups': [],
                'number_matching_groups': 0
            }

            for group in groups_list:
                if group in user_groups:
                    user_coincidences['matching_groups'].append(group)
                user_coincidences['number_matching_groups'] = len(user_coincidences['matching_groups'])

            result.append(user_coincidences)

        except KeyError:
            errors += 1
            continue
        finally:
            print('-')
            time.sleep(0.3)

    # print(result)
    return result


# сортировка по кол-ву совпавших групп


# у топ-10 запрашиваем фото
def find_top3_photos(top10_users):
    for user in top10_users:
        params['user_id'] = user['id']
        params['album_id'] = ['profile']
        params['extended'] = [1]

        response = requests.get('https://api.vk.com/method/photos.get', params)
        profile_photos = response.json()['response']['items']

        # и ищем топ3 фото

        top3 = s.find_top3(profile_photos)
        user['top3_photos'] = top3

        time.sleep(0.3)

    return top10_users

