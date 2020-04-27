import json


#  подготавливаем данные для записи
def create_output_file(top10_users):
    output = []

    for user in top10_users:

        user_vk = {
            'vk_link': f"https://vk.com/id{user['id']}",
            'photos': []
        }

        for photo in user['top3_photos']:
            user_vk['photos'].append(photo['sizes'][-1]['url'])

        output.append(user_vk)

    return output


# записываем результат в файл JSON
def write_output_file(output):
    with open('top_users.json', 'w') as json_file:
        data = json.dumps(output, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))

        json_file.write(data)
