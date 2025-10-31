# Todo App - Android версия

Мобильное приложение для управления задачами (TODO) на Android, разработанное с использованием Kivy и KivyMD.

## 🚀 Функциональность

- ✅ Создание, чтение, обновление и удаление задач (CRUD)
- ✅ Красивый мобильный интерфейс на базе Material Design (KivyMD)
- ✅ SQLite база данных
- ✅ Аутентификация пользователей
- ✅ Регистрация новых пользователей
- ✅ Отметка задач как выполненных с автоматической установкой даты
- ✅ Нативное Android приложение

## 📋 Требования

- Python 3.8+
- pip
- Android SDK (для сборки APK)
- Buildozer (для сборки Android приложений)

## 🛠 Установка и запуск

### Локальная разработка

1. **Клонируйте репозиторий:**
   ```bash
   git clone <repository-url>
   cd kivy-todo
   ```

2. **Установите зависимости:**
   ```bash
   pip install kivy kivymd peewee bcrypt
   ```

3. **Запустите приложение:**
   ```bash
   python main.py
   ```

### Сборка APK для Android

1. **Установите Buildozer:**
   ```bash
   pip install buildozer
   ```

2. **Инициализируйте проект:**
   ```bash
   buildozer init
   ```

3. **Соберите APK (debug версия):**
   ```bash
   buildozer android debug
   ```

4. **Соберите APK (release версия):**
   ```bash
   buildozer android release
   ```

APK файл будет создан в папке `bin/`.

### Тестирование на устройстве

1. **Подключите Android устройство** с включенной отладкой USB
2. **Установите APK:**
   ```bash
   adb install bin/TodoApp-0.1-debug.apk
   ```

Или перенесите APK файл на устройство и установите вручную.

## 📖 Использование

### Запуск на ПК

Запустите приложение командой:
```bash
python main.py
```

### Использование на Android

1. **Установите APK** на ваше Android устройство
2. **Запустите приложение**
3. **Зарегистрируйтесь** или войдите под существующей учетной записью
4. **Добавляйте задачи** с помощью кнопки "+" в верхней панели
5. **Отмечайте задачи** как выполненные с помощью чекбоксов
6. **Редактируйте** или **удаляйте** задачи с помощью соответствующих кнопок

### Функции приложения

- **Регистрация/Вход**: Создание учетной записи или вход в систему
- **Список задач**: Просмотр всех ваших задач
- **Создание задач**: Добавление новых задач с заголовком и описанием
- **Редактирование**: Изменение существующих задач
- **Удаление**: Удаление ненужных задач
- **Отметка выполнения**: Автоматическая установка даты завершения при выполнении задачи

## 🗄 Модель данных

### User (Пользователь)
- `id` (Integer): Уникальный идентификатор
- `username` (String): Имя пользователя
- `email` (String): Email адрес
- `password_hash` (String): Хэшированный пароль
- `role` (ForeignKey): Роль пользователя
- `created_at` (DateTime): Дата регистрации

### Role (Роль)
- `id` (Integer): Уникальный идентификатор
- `name` (String): Название роли (admin/user)
- `description` (String): Описание роли

### Todo (Задача)
- `id` (Integer): Уникальный идентификатор
- `title` (String, required): Заголовок задачи
- `description` (String, optional): Описание задачи
- `completed` (Boolean): Статус выполнения
- `created_at` (DateTime): Дата создания
- `updated_at` (DateTime): Дата последнего обновления
- `due_date` (DateTime, optional): Дата выполнения задачи

### Options (Настройки)
- `id` (Integer): Уникальный идентификатор
- `name` (String): Название настройки
- `value` (String): Значение настройки
- `category` (String): Категория настройки
- `user_id` (Integer, optional): ID пользователя (null для глобальных настроек)

## 🏗 Архитектура проекта

```
kivy-todo/
├── main.py              # Основное приложение Kivy
├── models.py            # Модели данных (Peewee ORM)
├── buildozer.spec       # Конфигурация для сборки APK
├── requirements.txt     # Зависимости Python
├── README.md            # Эта документация
└── todo.db              # SQLite база данных (создается автоматически)
```

### Основные компоненты

- **main.py**: Содержит все экраны приложения (LoginScreen, RegisterScreen, DashboardScreen, TodoFormScreen)
- **models.py**: Определение моделей данных и функции инициализации БД
- **buildozer.spec**: Конфигурация для сборки Android приложения

## 🛡 Безопасность

- Хэширование паролей с bcrypt
- Валидация входных данных
- Защита от SQL-инъекций через Peewee ORM
- Локальная база данных (данные хранятся только на устройстве)

## 🔧 Настройка buildozer.spec

Файл `buildozer.spec` содержит настройки для сборки Android приложения. Основные параметры:

```ini
[app]
title = Todo App                    # Название приложения
package.name = todoapp              # Имя пакета
package.domain = org.test           # Домен пакета
source.dir = .                      # Директория с исходным кодом
requirements = python3,kivy,kivymd,peewee,bcrypt  # Зависимости
orientation = portrait              # Ориентация экрана
fullscreen = 0                      # Полноэкранный режим (0 - нет, 1 - да)

[buildozer]
log_level = 2                       # Уровень логирования
```

### Изменение настроек

1. **Название приложения:**
   ```ini
   title = My Todo App
   ```

2. **Иконка приложения:**
   ```ini
   icon.filename = %(source.dir)s/icon.png
   ```

3. **Версия приложения:**
   ```ini
   version = 1.0.0
   ```

4. **Разрешения Android:**
   ```ini
   android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
   ```

## 🐛 Решение проблем

### Приложение не запускается

**Проблема:** ImportError или ModuleNotFoundError
**Решение:**
```bash
pip install kivy kivymd peewee bcrypt
```

### Ошибки при сборке APK

**Проблема:** Buildozer не может найти Android SDK
**Решение:**
```bash
# Установите Android SDK через Android Studio
# Или используйте:
buildozer android clean
buildozer android debug
```

**Проблема:** Недостаточно памяти при сборке
**Решение:** Увеличьте объем оперативной памяти или закройте другие приложения

### База данных не создается

**Проблема:** Ошибки при инициализации БД
**Решение:**
```bash
# Удалите старую базу данных
rm todo.db
# Перезапустите приложение
python main.py
```

### Приложение закрывается на Android

**Проблема:** Приложение вылетает сразу после запуска
**Решение:**
- Проверьте логи: `adb logcat | grep python`
- Убедитесь, что все зависимости указаны в buildozer.spec
- Проверьте наличие необходимых разрешений

## 🤝 Вклад в проект

1. Форкните проект
2. Создайте ветку для вашей фичи: `git checkout -b feature/amazing-feature`
3. Зафиксируйте изменения: `git commit -m 'Add amazing feature'`
4. Отправьте изменения: `git push origin feature/amazing-feature`
5. Создайте Pull Request

### Структура проекта kivy-todo

При работе над проектом следуйте этой структуре:
- `main.py` - основной код приложения
- `models.py` - модели данных
- `buildozer.spec` - настройки сборки
- `requirements.txt` - зависимости
- `README.md` - документация

## 📄 Лицензия

Этот проект распространяется под лицензией MIT.

## 🙏 Благодарности

- [Kivy](https://kivy.org/) - Фреймворк для создания мобильных приложений на Python
- [KivyMD](https://kivymd.readthedocs.io/) - Material Design компоненты для Kivy
- [Peewee](https://peewee.readthedocs.io/) - Простая и легкая ORM для Python
- [Buildozer](https://buildozer.readthedocs.io/) - Инструмент для сборки APK из Python приложений