# --- General & Welcome ---
welcome_message =
    🙌 Привет, рады тебя видеть 🙌

    Этот бот поможет тебе получить доступ к меню нашей пиццерии 🍕
    Ты также можешь сделать заказ и получить информацию о нас 📋

    Всё это и многое другое будет доступно после регистрации 🔽✅

    Сначала напишите свое имя пользователя, а затем следуйте инструкциям.

# --- Language ---
select_language = 🌐 Пожалуйста, выберите ваш язык:
language_selected = 🇷🇺 Язык изменен на русский

# --- Navigation Buttons ---
back_button = ⬅️ Назад
next_button = Далее ▶
prev_button = ◀ Пред
main_menu_button = Главное меню 🏠

# --- Main Menu ---
main_menu_goods = Товары 🍕
main_menu_cart = Корзина 🛒
main_menu_orders = Заказы 📦
main_menu_about = О нас ℹ️
main_menu_payment = Оплата 💰
main_menu_delivery = Доставка 🚚
main_menu_profile = Профиль 👤
main_menu_language = Язык 🌐

# --- Subscription ---
subscription_required =
    🚫 Пожалуйста, подпишитесь на каналы, чтобы использовать бота:
    [Подписаться на канал]({$channel_link})
check_subscription_button = 🔄 Проверить подписку
subscription_successful = ✅ Вы успешно подписались на канал!
subscription_required_callback = ❌ Вы не подписаны на канал. Пожалуйста, сначала подпишитесь.

subscribe_to_channel_button = ✅ Подписаться на канал

# --- Captcha ---
captcha_text =
    Привет! Прежде чем мы начнем, пожалуйста, подтвердите, что вы не робот. Выберите указанное слово: <strong>{$word}</strong>
    <i>После прохождения капчи, вы сможете продолжить регистрацию</i>
captcha_success = Капча пройдена успешно!
captcha_expired = Сессия капчи истекла. Пожалуйста, начните снова.
captcha_wrong_selection = Неверный выбор. Попробуйте снова с новой капчей.
captcha_passed = ✅ Пройдена
captcha_not_passed = ❌ Не пройдена
complete_captcha_first = Пожалуйста, сначала пройдите капчу.

# --- Registration ---
first_name_request = Пожалуйста, введите ваше имя:
name_length_error = Имя должно быть от 2 до 50 символов. Пожалуйста, введите ваше имя снова:
name_too_long = ❌ Имя слишком длинное. Пожалуйста, введите имя короче 30 символов.
phone_request =
    Теперь, пожалуйста, введите ваш номер телефона
    📱 Формат номера телефона должен быть +7xxxxxxxxxx
    ⚠️ Внимание! Номер телефона должен быть уникальным
invalid_phone_format =
    ❌ Неверный формат номера телефона. Пожалуйста, введите номер в международном формате
    Примеры:
    +380 XX XXX XXXX
    +7 XXX XXX XXXX
invalid_phone_format_intl = ❌ Неверный формат номера телефона. Пожалуйста, введите номер в международном формате (например, +79123456789):
invalid_phone_retry = ❌ Неверный формат номера телефона. Пожалуйста, попробуйте снова.
phone_already_registered = ❌ Этот номер телефона уже зарегистрирован на другом аккаунте. Пожалуйста, используйте другой номер или обратитесь к администратору.
registration_complete_with_data =
    ✅ Регистрация завершена успешно!
    Имя: {$name}
    Телефон: {$phone}
user_creation_error = Ошибка создания пользователя. Пожалуйста, попробуйте снова.
registration_error = ❌ Произошла ошибка при регистрации. Пожалуйста, попробуйте позже.

# --- User Profile ---
profile_text =
    <b>⚡️ Профиль</b>
    👉🏼 ID: <code>{$user_id}</code>
    ➖➖➖➖➖➖➖➖➖➖➖➖
    ⚙️ Полное имя: <code>{$first_name} {$last_name}</code>
    🎮 Имя пользователя: <code>@{$username}</code>
    📱 Телефон: <code>{$phone}</code>
    🔐 Капча: <code>{$captcha_status}</code>
    🚩 Язык: <code>{$language}</code>
    ➖➖➖➖➖➖➖➖➖➖➖➖
    📊 Статистика:
    📅 Дней в боте: <code>{$days_in_bot}</code>
    📦 Всего заказов: <code>{$orders_count}</code>
    ➖➖➖➖➖➖➖➖➖➖➖➖
    📆 Дата регистрации: <code>{$registration_date}</code>
profile_load_error = Произошла ошибка при загрузке профиля

# --- Catalog & Products ---
select_category = Выберите категорию:
categories_not_found = Категории не найдены
product_details =
    <strong>{$name}</strong>
    {$description}
    Цена: {$price}
    <strong>Товар {$current_page} из {$total_pages}</strong>
product_no_image = У товара нет изображения
menu_banner_with_image =
    <b>{$description}</b>
    Выберите категорию:

# --- Cart ---
cart_button = Корзина 🛒
buy_button = Купить 💵
delete_button = Удалить
product_added_to_cart = Товар добавлен в корзину.
error_adding_to_cart = Ошибка добавления товара в корзину.
cart_item_details =
    <strong>{$name}</strong>
    {$price} x {$quantity} = {$cart_price}
    Товар {$current_page} из {$total_pages} в корзине.
    Общая цена в корзине {$total_price}

# --- Ordering Process ---
order_button = Оформить заказ 🛍️
name_request_again = Пожалуйста, введите ваше имя снова:
phone_request_order = Пожалуйста, введите ваш номер телефона:
phone_request_again = Пожалуйста, введите ваш номер телефона снова:
invalid_phone_format_order = Неверный номер телефона. Пожалуйста, введите действительный номер телефона (10-15 цифр):
phone_accepted_address_request = Номер телефона принят. Пожалуйста, введите ваш адрес:
address_request_again = Пожалуйста, введите ваш адрес снова:
address_length_error = ❌ Адрес должен быть от 5 до 100 символов. Пожалуйста, введите ваш адрес снова:
order_confirmation =
    <b>📋 Детали заказа</b>
    <i>👤 Информация о клиенте:</i>
        • Имя: <code>{$name}</code>
        • Телефон: <code>{$phone}</code>
        • Адрес: <code>{$address}</code>
    <i>💰 Информация об оплате:</i>
        • Общая сумма: <b>{$total_amount}</b>
    <i>⬇️ Пожалуйста, выберите способ оплаты ниже</i>
select_payment_btn = Выбрать способ оплаты 💳
cancel_order_btn = Отменить ❌
user_agreement_btn = Пользовательское соглашение 📜
order_canceled = Заказ отменен ❌

# --- Promo Code ---
promo_code_request =
    🎟️ У вас есть промокод?
    Введите его ниже или нажмите «Пропустить».
promo_skip_button = Пропустить ➡️
promo_applied = ✅ Промокод применён! Скидка: {$discount}%
promo_not_found = ❌ Промокод не найден. Проверьте код и попробуйте снова.
promo_inactive = ❌ Этот промокод больше не активен.
promo_not_started = ❌ Этот промокод ещё не начал действовать.
promo_expired = ❌ Срок действия промокода истёк.
promo_limit_reached = ❌ Промокод исчерпал лимит использований.
order_confirmation_with_promo =
    <b>📋 Детали заказа</b>
    <i>👤 Информация о клиенте:</i>
        • Имя: <code>{$name}</code>
        • Телефон: <code>{$phone}</code>
        • Адрес: <code>{$address}</code>
    <i>🎟️ Применён промокод:</i>
        • Код: <code>{$promo_code}</code>
        • Скидка: <b>-{$discount_percent}%</b>
        • Исходная цена: <s>{$original_amount}</s>
        • Скидка: -{$discount_amount}
        • Итого: <b>{$total_amount}</b>
    <i>⬇️ Пожалуйста, выберите способ оплаты ниже</i>

# --- Payment ---
select_payment_method = <b>💳 Выберите способ оплаты:</b>
pay_with_crypto_btn = Оплатить через {$crypto} 💳
pay_with_stars_btn = Оплатить {$stars_amount} звезд ⭐
star_payment_btn = Оплата Stars ⭐
order_payment_title = Оплата заказа
order_payment_description = Оплата заказа для пользователя ID: {$user_id}
star_payment_description = Оплата на сумму {$stars_amount} звезд
payment_details =
    <b>📋 Детали платежа</b>
    <i>💰 Информация об оплате:</i>
        • Сумма USD: <b>{$amount_usd}</b>
        • Сумма {$crypto}: <b>{$crypto_amount}</b>
        • Валюта: <b>{$crypto}</b>
        • Истекает: <code>{$expiration_time}</code>
    <i>⏰ Времени осталось: 3 минуты</i>
    <b>ℹ️ Пожалуйста, завершите платеж до истечения таймера</b>
payment_successful =
    <b>Оплата прошла успешно</b>
    <i>Информация о заказе:</i>
        • ID заказа: <code>{$order_id}</code>
        • Статус: <b>{$order_status}</b>
    <i>Детали платежа:</i>
        • Сумма: <b>{$amount}</b>
        • Валюта: <b>{$crypto}</b>
    <i>Информация о доставке:</i>
        • Имя: <code>{$name}</code>
        • Телефон: <code>{$phone}</code>
        • Адрес: <code>{$address}</code>
    <i>Вы можете посмотреть детали заказа в меню "Заказы"</i>
payment_time_expired =
    <b>⏰ Время платежа истекло!</b>
    ❌ Платеж не был завершен в отведенное время.
    Пожалуйста, попробуйте снова, если хотите завершить покупку.

# --- Order History ---
no_orders = У вас пока нет заказов.
order_item =
    🔸 Заказ {$order_id}
    👤 Имя: {$name}
    📦 Статус: {$status}
    📍 Адрес: {$address}
    📱 Телефон: <code>{$phone}</code>
    -------------------
order_detail_button = 📋 Детали заказа #{$order_id}
back_to_orders_btn = ◀️ Назад к заказам

order_detail_header =
    📋 <b>Детали заказа #{$order_id}</b>
    📅 Дата создания: {$created_at}
    👤 Имя: {$name}
    📦 Статус: {$status}
    📍 Адрес: {$address}
    📱 Телефон: <code>{$phone}</code>

    <b>Товары в заказе:</b>

order_detail_item =
    • <b>{$name}</b>
      <i>{$quantity} шт. x ${$price}</i>

order_detail_total =
    -----------------------------------
    💰 <b>Общая стоимость: ${$total_sum}</b>

# --- Admin: Promo Codes ---
admin_promo_codes = 🎟️ Промокоды
admin_promo_list_header = <b>🎟️ Промокоды</b>
admin_promo_legend =
    ─────────────
    🟢 Активен  ⏳ Ещё не начался  💀 Истёк  🔴 Отключён
    ✏️ Редакт.  🗑️ Удалить  ✅/❌ Вкл/Откл
admin_promo_empty = Промокодов пока нет. Нажмите ➕ чтобы добавить.
admin_promo_add_btn = ➕ Добавить промокод
admin_promo_deleted = ✅ Промокод удалён.
admin_promo_toggled = Статус изменён на {$status}
admin_promo_not_found = ❌ Промокод не найден.
admin_promo_created = ✅ Промокод успешно создан!
admin_promo_updated = ✅ Промокод успешно обновлён!
admin_promo_save_error = ❌ Не удалось сохранить. Возможно, такой код уже существует.
admin_promo_edit_hint =
    ✏️ Редактирование: <b>{$current}</b>
    Отправьте "." чтобы сохранить текущее значение.
    Введите новый код:
admin_promo_enter_code = Введите промокод (например SUMMER25):
admin_promo_code_length_error = ❌ Код должен быть от 2 до 50 символов. Попробуйте снова:
admin_promo_enter_discount = Введите процент скидки (0–100){$hint}:
admin_promo_discount_error = ❌ Введите число от 1 до 100. Попробуйте снова:
admin_promo_enter_valid_from = Введите дату начала ДД.ММ.ГГГГ{$hint}:
admin_promo_enter_valid_until = Введите дату окончания ДД.ММ.ГГГГ{$hint}:
admin_promo_date_error = ❌ Неверный формат даты. Используйте ДД.ММ.ГГГГ (например 31.12.2025):
admin_promo_date_range_error = ❌ Дата окончания должна быть позже даты начала. Введите дату начала снова:
admin_promo_enter_max_uses = Введите макс. число использований (0 = безлимит){$hint}:
admin_promo_max_uses_error = ❌ Введите целое неотрицательное число. Попробуйте снова:

# --- System Errors & Messages ---
unrecognized_action = Нераспознанное действие.
error_loading_menu = Ошибка загрузки меню
error_opening_menu = Ошибка открытия меню {$menu_name}
banner_not_found = Баннер не найден
banner_no_image = У баннера нет изображения
banner_image_not_found = Изображение баннера не найдено: {$path}
banner_not_found_or_no_image = Баннер не найден или не имеет изображения
product_image_not_found = Изображение товара не найдено: {$path}
order_details_error = Произошла ошибка при получении деталей заказа
order_not_found = Заказ не найден
order_no_products = В заказе нет товаров
order_already_processed = Этот заказ уже обработан!
captcha_save_error = Ошибка сохранения статуса капчи. Пожалуйста, попробуйте снова.
captcha_general_error = Произошла ошибка. Пожалуйста, попробуйте снова.
crypto_rate_error = ❌ Ошибка получения курса валют. Пожалуйста, попробуйте снова.
crypto_calculation_error = ❌ Ошибка расчета суммы в криптовалюте. Пожалуйста, попробуйте снова.
crypto_invoice_error = ❌ Ошибка создания криптоинвойса. Пожалуйста, попробуйте снова.
invalid_payment_response = ❌ Неверный ответ платежа. Пожалуйста, попробуйте снова.
payment_data_save_error = ❌ Ошибка сохранения данных платежа. Пожалуйста, попробуйте снова.
payment_details_display_error = ❌ Ошибка отображения деталей платежа. Пожалуйста, попробуйте снова.
payment_processing_error = ❌ Ошибка обработки платежа. Пожалуйста, попробуйте снова или обратитесь в поддержку.
star_payment_error = Ошибка обработки платежа звездами
payment_received_order_failed =
    ❌ <b>Платеж получен, но создание заказа не удалось.</b>
    Пожалуйста, обратитесь в поддержку.

# --- Admin Panel ---
admin_no_access = ❌ У вас недостаточно прав для доступа к этой функции.
admin_kb_placeholder = Что вы хотите сделать?
admin_add_good = ➕ Добавить товар
admin_assortment = 🛒 Ассортимент
admin_add_banner = 🖼️ Добавить/Изменить баннер
admin_statistics = 📊 Статистика
admin_newsletter = 📣 Рассылка
admin_statistics_text =
    📊 Статистика:
    👥 Всего пользователей: {$users}
    🛒 Всего заказов: {$orders}
    📦 Всего товаров: {$products}
    📂 Товары по категориям:
     {$category_stats_text}
admin_products_list = Хорошо, список товаров ⏫
admin_choose_category = Выберите категорию:
admin_product_card =
    <strong>{$name}</strong>
    {$description}
    Цена: {$price}💵
admin_delete_btn = Удалить
admin_edit_btn = Редактировать
admin_product_deleted = Товар успешно удален!
admin_banner_instructions =
    Отправьте фото баннера.
    Выберите страницу для баннера:
    {$pages}
admin_banner_wrong_page = Вы написали неправильное название страницы, пожалуйста, выберите страницу из списка
admin_banner_success = Баннер успешно добавлен/изменен!
admin_product_add_en_name = Введите название товара на англ, который хотите добавить:
admin_product_add_ru_name = Введите название товара на рус, который хотите добавить:
admin_product_edit_name = Введите название товара, который хотите изменить:
admin_product_add_en_description = Введите описание товара на англ:
admin_product_add_ru_description = Введите описание товара на рус:
admin_product_price = Введите цену товара:
admin_product_image = Загрузите изображение товара:
admin_image_keep_current = Отправьте фото или '.' чтобы оставить текущее изображение
admin_product_success = Товар успешно добавлен/обновлен!
admin_canceled = Отменено
admin_no_previous_step = Предыдущий шаг недоступен, или напишите "отмена"
admin_previous_step =
    Хорошо, вы на предыдущем шаге
    {$step_text}
admin_newsletter_content = Введите содержание рассылки
admin_newsletter_success =
    <b> 🎉 Рассылка отправлена успешно!
    ✅ Отправлено: {$success_count}
    ❌ Ошибки при отправке: {$error_count}
    ⏳ Затрачено времени: <code>{$time_taken} сек.</code></b>

# --- Admin Errors ---
admin_products_error = Произошла ошибка при обработке товаров
admin_banner_wrong_data = Вы ввели неправильные данные, пожалуйста, загрузите изображение баннера:
admin_product_name_error = Название товара слишком длинное или короткое, пожалуйста, напишите название товара:
admin_product_name_wrong_data = Вы ввели неправильные данные, пожалуйста, напишите название товара:
admin_product_description_error =
    Описание товара слишком длинное или короткое,
    пожалуйста, напишите описание товара:
admin_product_description_wrong_data = Вы ввели неправильные данные, пожалуйста, напишите описание товара:
admin_category_wrong_choice = Выберите категорию из списка
admin_category_wrong_data = Вы ввели неправильные данные, пожалуйста, выберите категорию из списка:
admin_price_error = Напишите правильные данные, только цифры
admin_product_price_wrong_data = Вы ввели неправильные данные, пожалуйста, напишите цену товара:
admin_product_image_wrong_data = Вы ввели неправильные данные, пожалуйста, загрузите изображение товара:
admin_product_error = Произошла ошибка. Попробуйте снова или напишите 'отмена'

# --- Group Management (Admin) ---
messages_deleted = Удалено {$count} сообщений!
invalid_clear_format = Неверный формат команды. Используйте: /clear или /clear <число>
clear_error = Не удалось удалить сообщения. Проверьте права бота.
clear_admin_only = Команда доступна только администраторам группы.
bot_admin_required = Бот должен быть администратором группы для удаления сообщений
clear_command_format = Неверный формат команды. Используйте: /clear <число>
restricted_words_warning = {$user_name}, соблюдай порядок в чате! 🤬