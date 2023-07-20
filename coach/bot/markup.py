from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

YearsCallback = CallbackData("btn", "space", "year")
MonthCallback = CallbackData("btn", "space", "year", "month")
ThemesCallback = CallbackData("btn", "space", "topic")


btnCancel = InlineKeyboardButton(text="Отмена", callback_data="cancel")

# ---UserMainMenu---
UserMainMenu = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text="Доступная информация", 
                              callback_data="btn:UserMainMenu:access")],
        [InlineKeyboardButton(text="Подписка", 
                              callback_data="btn:UserMainMenu:subscription")],
        [btnCancel]
    ]
)

SubscriptionMenu1 = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text="Да", 
                              callback_data="btn:SubscriptionMenu:yes"),
         InlineKeyboardButton(text="Нет", 
                              callback_data="cancel")]
    ]
)

SubscriptionMenu2 = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text="Продожить", 
                              callback_data="btn:SubscriptionMenu:have_name")],
        [InlineKeyboardButton(text="Отменить продление", 
                              callback_data="cancel")]
    ]
)


# ---UserPlusMainMenu---
UserPlusMainMenu = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text="Доступная информация",
                              callback_data="btn:UserPlusMainMenu:access")],
        [InlineKeyboardButton(text="Управление подпиской",
                              callback_data="btn:UserPlusMenu:subscription")],
        [btnCancel]
    ]
)

# ---AdminMenu---
AdminMenu = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text='Документы', 
                             callback_data="btn:AdminMenu:docs")],

        [InlineKeyboardButton(text='Отправить сообщение',
                              callback_data="btn:AdminMenu:message")],

        [InlineKeyboardButton(text='Удалить последнее сообщение',
                              callback_data="btn:AdminMenu:del_message")],
        [InlineKeyboardButton(text='Синхронизировать гугл диск и бд',
                              callback_data="btn:AdminMenu:sync_db")],

        [btnCancel]]
)


# ---SendMesMenu---
SendMesMenu = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [InlineKeyboardButton(text='Всем', 
                              callback_data="btn:SendMesMenu:all")],
        [InlineKeyboardButton(text='С активной подпиской',
                              callback_data="btn:SendMesMenu:act_sub")],
        [InlineKeyboardButton(text='Подписка была',
                              callback_data="btn:SendMesMenu:had_sub")],
        [InlineKeyboardButton(text='Без подписки',
                              callback_data="btn:SendMesMenu:minus")],
        [btnCancel]
    ]
)


# #---Admin:UsersMenu---
# AdminUsersMenu = InlineKeyboardMarkup(
#     row_width=1,
#     inline_keyboard=[
#         [InlineKeyboardButton(text='Инфо обо всех пользователях', callback_data="btn:Admin:UsersMenu:info_all")],
#         [InlineKeyboardButton(text='Инфо о пользователях с подпиской', callback_data="btn:Admin:UsersMenu:info_plus")],
#         [InlineKeyboardButton(text='Активировать подписку', callback_data="btn:Admin:UsersMenu:ActivePlus")],
#         [InlineKeyboardButton(text='Редактировать базу данных', callback_data="btn:Admin:UsersMenu:Edit")],
#         [btnCancel]
#     ]
# )


HaveFileMenu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [InlineKeyboardButton(text='ОК', 
                              callback_data="btn:HaveFileMenu:OK")],
        [InlineKeyboardButton(text='Изменить', 
                              callback_data="btn:HaveFileMenu:Change")],
        [btnCancel]
    ]
)


HaveTgFileMenu = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [InlineKeyboardButton(text='Заменить', 
                              callback_data="btn:HaveFileMenu:OK")],
        [InlineKeyboardButton(text='Изменить название', 
                              callback_data="btn:HaveFileMenu:Change")],
        [btnCancel]
    ]
)

# ---DocsYearsMenu---
def years_markup(years_list, admin=False):
    DocsYearMenu = InlineKeyboardMarkup(row_width=2)
    if admin:
        space = "ChoiceAdminYear"
        years_list.append('Другой')
    else:
        space = "ChoiceYear"
        years_list.append('Отправить всё')

    for year in years_list:
        DocsYearMenu.insert(InlineKeyboardButton(
            text=year,
            callback_data=YearsCallback.new(
                space=space,
                year=year)
        ))
    return DocsYearMenu

# print(years_markup(['2022', '2023'], True))

# ---DocsMonthMenu---


def month_markup(month_list, prefix=2000, admin=False):  # '2022/ДЕКАБРЬ', '2023/ЯНВАРЬ'
    if admin:
        space = "ChoiceAdminMonth"
        month_list.append(prefix+'/Другой')
    else:
        space = "ChoiceMonth"
        month.list.append(prefix+'/Отправить всё')

    DocsMonthMenu = InlineKeyboardMarkup(row_width=2)
    for yy_month in month_list:
        year, month = yy_month.split('/')
        print(yy_month)

        DocsMonthMenu.insert(InlineKeyboardButton(
            text=month,
            callback_data=MonthCallback.new(
                space=space,
                year=year,
                month=month)
        ))
    return DocsMonthMenu


# ---DocsTopicsMenu---
def themes_markup(themes_list):  # 'ДЕКАБРЬ/    "month", "topic", "title"
    themes_list.append('Другая')
    print(themes_list)
    DocsTopicsMenu = InlineKeyboardMarkup(row_width=1)
    for topic in themes_list:
        if len(topic) > 10:
            topic = topic[0:10]+'...'
        DocsTopicsMenu.insert(InlineKeyboardButton(
            text=topic,
            callback_data=ThemesCallback.new(
                space="ChoiceAdminThemes",
                topic=topic)
        ))
    return DocsTopicsMenu
