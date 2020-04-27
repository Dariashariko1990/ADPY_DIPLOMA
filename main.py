import output as o
import sorting as s
import db
import vk


def start_program():
    account = input('Введите id аккаунта или ник')
    # спрашиваем у пользователя ник или id аккаунта, записываем в параметры запроса
    try:
        vk.params['user_id'] = int(account)
    except ValueError:
        print("введен ник")
        vk.params['screen_name'] = account

    user_info = vk.get_user_info()
    print(user_info['response'][0]['id'])
    user_id = user_info['response'][0]['id']
    users = vk.search_users(user_info)
    result = vk.compare_friends_groups(users)
    top10_users = s.find_top10(result)
    top10_users_with_photos = vk.find_top3_photos(top10_users)
    output = o.create_output_file(top10_users_with_photos)
    db.write_db_output(user_id, output)
    o.write_output_file(output)
    print("Программа завершена")


if __name__ == '__main__':
    start_program()

# мой id для проверки 250821644
