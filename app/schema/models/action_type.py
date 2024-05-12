from enum import Enum


class ActionType(str, Enum):
    REGISTER = "Зарегестрировать пользователя"
    CALC_CLICK = "Считать количество кликов"
    SUPPORT = "Отправить сообщение в поддержку"  # need user message text
    SAVE_RESPONSE = "Сохранить ответ пользователя"  # need name of response
    # LOAD_ORDERS = "Загрузить заказы"
