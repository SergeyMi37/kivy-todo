from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
# from kivymd.uix.snackbar import MDSnackbar
from kivymd.theming import ThemeManager
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from datetime import datetime
import os

from models import db, User, Role, Todo, Options, create_tables

# Инициализация базы данных
create_tables()

# Создание начальных данных
def init_data():
    # Создание ролей
    admin_role, created = Role.get_or_create(name='admin', defaults={'description': 'Администратор'})
    user_role, created = Role.get_or_create(name='user', defaults={'description': 'Пользователь'})

    # Создание администратора
    try:
        admin = User.get(User.username == 'admin')
    except User.DoesNotExist:
        admin = User(
            username='admin',
            email='admin@example.com',
            role=admin_role
        )
        admin.set_password('admin')
        admin.save()

# Инициализация данных
try:
    init_data()
except Exception as e:
    print(f"Init data error: {e}")

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        self.username_input = MDTextField(
            hint_text='Имя пользователя',
            size_hint_y=None,
            height=dp(48)
        )
        self.password_input = MDTextField(
            hint_text='Пароль',
            password=True,
            size_hint_y=None,
            height=dp(48)
        )

        login_btn = MDRaisedButton(
            text='Войти',
            size_hint_y=None,
            height=dp(48)
        )
        login_btn.bind(on_press=self.login)

        register_btn = MDFlatButton(
            text='Регистрация',
            size_hint_y=None,
            height=dp(48)
        )
        register_btn.bind(on_press=self.go_to_register)

        self.layout.add_widget(MDLabel(text='Вход в систему', halign='center', font_style='H5'))
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(login_btn)
        self.layout.add_widget(register_btn)

        self.add_widget(self.layout)

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        try:
            user = User.get(User.username == username)
            if user.check_password(password):
                app = MDApp.get_running_app()
                app.current_user = user
                self.manager.current = 'dashboard'
                print('Вход выполнен успешно')
            else:
                Snackbar(text='Неверный пароль').show()
        except User.DoesNotExist:
            print('Пользователь не найден')

    def go_to_register(self, instance):
        self.manager.current = 'register'

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        self.username_input = MDTextField(
            hint_text='Имя пользователя',
            size_hint_y=None,
            height=dp(48)
        )
        self.email_input = MDTextField(
            hint_text='Email',
            size_hint_y=None,
            height=dp(48)
        )
        self.password_input = MDTextField(
            hint_text='Пароль',
            password=True,
            size_hint_y=None,
            height=dp(48)
        )

        register_btn = MDRaisedButton(
            text='Зарегистрироваться',
            size_hint_y=None,
            height=dp(48)
        )
        register_btn.bind(on_press=self.register)

        back_btn = MDFlatButton(
            text='Назад',
            size_hint_y=None,
            height=dp(48)
        )
        back_btn.bind(on_press=self.go_back)

        self.layout.add_widget(MDLabel(text='Регистрация', halign='center', font_style='H5'))
        self.layout.add_widget(self.username_input)
        self.layout.add_widget(self.email_input)
        self.layout.add_widget(self.password_input)
        self.layout.add_widget(register_btn)
        self.layout.add_widget(back_btn)

        self.add_widget(self.layout)

    def register(self, instance):
        username = self.username_input.text
        email = self.email_input.text
        password = self.password_input.text

        if not username or not email or not password:
            print('Заполните все поля')
            return

        try:
            user_role = Role.get(Role.name == 'user')
            user = User(username=username, email=email, role=user_role)
            user.set_password(password)
            user.save()
            print('Регистрация успешна')
            self.manager.current = 'login'
        except Exception as e:
            print(f'Ошибка регистрации: {e}')

    def go_back(self, instance):
        self.manager.current = 'login'

class TodoItem(MDCard):
    def __init__(self, todo, **kwargs):
        super().__init__(**kwargs)
        self.todo = todo
        self.size_hint_y = None
        self.height = dp(80)
        self.padding = dp(10)
        self.elevation = 2

        layout = BoxLayout(orientation='horizontal')

        # Чекбокс для завершения
        self.checkbox = CheckBox(active=todo.completed)
        self.checkbox.bind(active=self.toggle_completed)

        # Текст задачи
        text_layout = BoxLayout(orientation='vertical')
        self.title_label = MDLabel(text=todo.title, font_style='Body1')
        self.desc_label = MDLabel(text=todo.description or '', font_style='Body2', theme_text_color='Secondary')

        text_layout.add_widget(self.title_label)
        text_layout.add_widget(self.desc_label)

        # Кнопки действий
        actions_layout = BoxLayout(orientation='vertical', size_hint_x=None, width=dp(80))
        edit_btn = MDRaisedButton(text='Edit', size_hint=(None, None), size=(dp(70), dp(30)))
        edit_btn.bind(on_press=self.edit_todo)
        delete_btn = MDRaisedButton(text='Del', size_hint=(None, None), size=(dp(70), dp(30)))
        delete_btn.bind(on_press=self.delete_todo)

        actions_layout.add_widget(edit_btn)
        actions_layout.add_widget(delete_btn)

        layout.add_widget(self.checkbox)
        layout.add_widget(text_layout)
        layout.add_widget(actions_layout)

        self.add_widget(layout)

    def toggle_completed(self, instance, value):
        self.todo.completed = value
        if value and not self.todo.due_date:
            self.todo.due_date = datetime.utcnow()
        elif not value:
            self.todo.due_date = None
        self.todo.save()

    def edit_todo(self, instance):
        app = MDApp.get_running_app()
        app.edit_todo(self.todo)

    def delete_todo(self, instance):
        self.todo.delete_instance()
        app = MDApp.get_running_app()
        app.refresh_todos()

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        # Верхняя панель
        self.toolbar = MDTopAppBar(
            title='Задачи',
            left_action_items=[['logout', lambda x: self.logout()]],
            right_action_items=[['plus', lambda x: self.add_todo()]]
        )

        # Список задач
        self.scroll_view = ScrollView()
        self.todos_layout = MDList()
        self.scroll_view.add_widget(self.todos_layout)

        self.layout.add_widget(self.toolbar)
        self.layout.add_widget(self.scroll_view)

        self.add_widget(self.layout)

    def on_enter(self):
        self.refresh_todos()

    def refresh_todos(self):
        self.todos_layout.clear_widgets()
        todos = Todo.select()
        for todo in todos:
            self.todos_layout.add_widget(TodoItem(todo))

    def add_todo(self):
        app = MDApp.get_running_app()
        app.add_todo()

    def logout(self):
        app = MDApp.get_running_app()
        app.current_user = None
        self.manager.current = 'login'

class TodoFormScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.todo = None
        self.layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        self.title_input = MDTextField(
            hint_text='Название задачи',
            size_hint_y=None,
            height=dp(48)
        )
        self.desc_input = MDTextField(
            hint_text='Описание',
            multiline=True,
            size_hint_y=None,
            height=dp(100)
        )

        save_btn = MDRaisedButton(
            text='Сохранить',
            size_hint_y=None,
            height=dp(48)
        )
        save_btn.bind(on_press=self.save_todo)

        cancel_btn = MDFlatButton(
            text='Отмена',
            size_hint_y=None,
            height=dp(48)
        )
        cancel_btn.bind(on_press=self.cancel)

        self.layout.add_widget(MDLabel(text='Новая задача', halign='center', font_style='H5'))
        self.layout.add_widget(self.title_input)
        self.layout.add_widget(self.desc_input)
        self.layout.add_widget(save_btn)
        self.layout.add_widget(cancel_btn)

        self.add_widget(self.layout)

    def set_todo(self, todo=None):
        self.todo = todo
        if todo:
            self.title_input.text = todo.title
            self.desc_input.text = todo.description or ''
        else:
            self.title_input.text = ''
            self.desc_input.text = ''

    def save_todo(self, instance):
        title = self.title_input.text
        description = self.desc_input.text

        if not title:
            print('Введите название задачи')
            return

        if self.todo:
            self.todo.title = title
            self.todo.description = description
            self.todo.save()
        else:
            Todo.create(title=title, description=description)

        self.manager.current = 'dashboard'
        app = MDApp.get_running_app()
        app.refresh_todos()

    def cancel(self, instance):
        self.manager.current = 'dashboard'

class TodoApp(MDApp):
    current_user = ObjectProperty(None, allownone=True)

    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.theme_style = 'Light'

        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(RegisterScreen(name='register'))
        self.sm.add_widget(DashboardScreen(name='dashboard'))
        self.sm.add_widget(TodoFormScreen(name='todo_form'))

        return self.sm

    def add_todo(self):
        self.sm.get_screen('todo_form').set_todo()
        self.sm.current = 'todo_form'

    def edit_todo(self, todo):
        self.sm.get_screen('todo_form').set_todo(todo)
        self.sm.current = 'todo_form'

    def refresh_todos(self):
        dashboard = self.sm.get_screen('dashboard')
        dashboard.refresh_todos()

if __name__ == '__main__':
    TodoApp().run()