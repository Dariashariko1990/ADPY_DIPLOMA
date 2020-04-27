# сортировка по кол-ву совпавших групп

def find_top10(list):
    users_sorted = sorted(list, key=lambda x: x['number_matching_groups'])

    top10_users = users_sorted[len(users_sorted) - 10:len(users_sorted)]

    return top10_users


# cортировка топ3 фото

def find_top3(list):
    photos_sorted = sorted(list, key=lambda x: x['likes']['count'])

    top3_photos = photos_sorted[len(photos_sorted) - 3:len(photos_sorted)]

    return top3_photos
