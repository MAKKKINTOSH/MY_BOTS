from datetime import datetime

current_year = datetime.now().year
current_month = datetime.now().month

class admins:
    """Класс, содержащий в себе id и группу пользователей, являющихся администраторами"""

    def __init__(self, user_id, group):

        self.user_id = user_id
        self.group = group

class user:
    """Класс, содержащий в себе атрибуты пользователя"""

    def __init__(self, user_id,
                 group,
                 select_year = current_year,
                 select_month = current_month,
                 edit_type = 3):

        """Содержит в себе следующие параметры:
        1. id пользователя
        2. группу пользователя
        3. год, выбранный пользователем в календаре
        4. Месяц, выбранный пользователем в календаре
        5. цель, с которой пользователь открыл календарь(просмотр/удаление/добавление)"""

        self.user_id = user_id
        self.group = group
        self.select_year = select_year
        self.select_month = select_month
        self.edit_type = edit_type