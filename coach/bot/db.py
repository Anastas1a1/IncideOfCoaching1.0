from adminpanel.models import AdminProfile, File, UserProfile, Subscription, FileGoogle, FileTg
from datetime import datetime


def format_month(month):
    months_map = {
        '1': 'ЯНВАРЬ',
        '2': 'ФЕВРАЛЬ',
        '3': 'МАРТ',
        '4': 'АПРЕЛЬ',
        '5': 'МАЙ',
        '6': 'ИЮНЬ',
        '7': 'ИЮЛЬ',
        '8': 'АВГУСТ',
        '9': 'СЕНТЯБРЬ',
        '10': 'ОКТЯБРЬ',
        '11': 'НОЯБРЬ',
        '12': 'ДЕКАБРЬ',
    }
    return months_map[month]


def new_user_plus(us_name, tg_id, plus, date=None):
    user_exists = UserProfile.objects.filter(tg_id=tg_id).exists()
    if not user_exists:
        user = UserProfile(name=us_name, tg_id=tg_id)
        user.save()

    if not plus:
        return

    if not date:
        date = datetime.now()
    else:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    current_year = date.strftime('%Y')
    current_month = date.strftime("%-m")

    current_month = format_month(current_month)
    subscription = Subscription(
        tg_id=tg_id, subscription_date=date, year=current_year, month=current_month)
    subscription.save()


def is_plus(tg_id):
    try:
        subscription = Subscription.objects.select_related(
            'user').get(user__tg_id=tg_id)
        return subscription.user.name
    except Subscription.DoesNotExist:
        return None


def get_tg_id(category):
    date = datetime.now()
    current_year = date.strftime('%Y')
    current_month = date.strftime("%-m")
    current_month = format_month(current_month)

    if category == "minus":
        tg_ids = UserProfile.objects.exclude(
            subscription__isnull=True).values_list('tg_id', flat=True)
    elif category == "all":
        tg_ids = UserProfile.objects.all().values_list('tg_id', flat=True)
    else:
        tg_ids = Subscription.objects.filter(
            year=current_year, month=current_month).values_list('tg_id', flat=True).distinct()

        if category == "act_sub":
            return list(tg_ids)

        tg_ids_had_sub = Subscription.objects.exclude(
            tg_id__in=tg_ids).values_list('tg_id', flat=True).distinct()
        tg_ids = tg_ids_had_sub

    return list(tg_ids)


def add_google_file(year, category, topic, title, google_id, link):
    try:
        file_obj = File.objects.get(
            year=year, category=category, topic=topic, title=title)
    except File.DoesNotExist:
        file_obj = File.objects.create(
            year=year,
            category=category,
            topic=topic,
            title=title
        )

    if google_id != 0 and link:
        file_google, _ = FileGoogle.objects.get_or_create(
            file=file_obj,
            defaults={'google_id': google_id, 'link': link}
        )

    return file_obj


def get_files_by_name(file_name):
    if file_name == '-':
        return [], [] 
    file_objects = File.objects.filter(title=file_name)
    file_tg_objects = []
    for file_obj in file_objects:
        try:
            file_tg_obj = FileTg.objects.get(file=file_obj)
            file_tg_objects.append(file_tg_obj)
        except FileTg.DoesNotExist:
            file_tg_objects.append(None)
    return file_objects, file_tg_objects




def get_unique_years():
    unique_years = File.objects.values_list('year', flat=True).distinct()
    return list(unique_years)


def get_unique_category(year):
    unique_categories = File.objects.filter(year=year).values_list('category', flat=True).distinct()
    formatted_results = [f"{year}/{category}" for category in unique_categories]
    return formatted_results

def get_unique_topic(year, category):
    unique_topic = File.objects.filter(year=year, category=category).values_list('topic', flat=True).distinct()
    return list(unique_topic)


def add_file_tg(year, category, topic, title, tg_id, ext):
    file_obj, created = File.objects.get_or_create(year=year, category=category, topic=topic, title=title)

    if created:
        file_tg_obj = FileTg.objects.create(file=file_obj, tg_id=tg_id, ext=ext)
        file_tg_obj.save()
        
    if FileTg.objects.filter(file=file_obj).exists():
        FileTg.objects.filter(file=file_obj).delete()
    file_tg_obj = FileTg.objects.create(file=file_obj, tg_id=tg_id, ext=ext)
    file_tg_obj.save()

    return file_obj.title, file_tg_obj.tg_id, file_tg_obj.ext        

        
def my_info(user_id):

    try:
        user_profile = UserProfile.objects.get(tg_id=user_id)

        subscriptions = Subscription.objects.filter(user=user_profile)
    except Subscription.DoesNotExist:
        return []
    
    try:
        available_files = File.objects.filter(
            year__in=[subscription.year for subscription in subscriptions],
            category__in=[subscription.month for subscription in subscriptions]
        ).prefetch_related('files_tg')
        
    except File.DoesNotExist:
        return []

    result = []
    for file in available_files:
        file_tg = file.files_tg.first()
        if file_tg:
            result.append([file_tg.ext, user_id, file_tg.tg_id, file.title])
    print(result)
    return result

def degust(user_id):
    try:
        available_files = File.objects.filter(
            category='Дегустационное меню'
        ).prefetch_related('files_tg')
    except:
        return []
    result = []
    for file in available_files:
        file_tg = file.files_tg.first()
        if file_tg:
            result.append([file_tg.ext, user_id, file_tg.tg_id, file.title])
    print(result)
    return result    


def contract(user_id):
    try:
        available_files = File.objects.filter(
            category='Договор'
        ).prefetch_related('files_tg')
    except File.DoesNotExist:
        return []

    result = []
    for file in available_files:
        file_tg = file.files_tg.first()
        if file_tg:
            result.append([file_tg.ext, user_id, file_tg.tg_id, file.title])
    print(result)
    return result  
