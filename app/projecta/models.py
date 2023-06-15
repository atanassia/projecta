from datetime import datetime

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users require an email field")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    STATUS_CHOICES = (
        ("Director", "Руководитель"),
        ("Engineer", "Инженер"),
        ("Accountant", "Бухгалтер"),
        ("Plumber", "Слесарь"),
    )
    email = models.EmailField(
        blank=False, null=False, unique=True, verbose_name="Почта"
    )
    username = None
    date_joined = None
    first_name = models.CharField(max_length=150, blank=False, verbose_name="Имя")
    middle_name = models.CharField(max_length=150, blank=True, verbose_name="Отчество")
    last_name = models.CharField(max_length=150, blank=False, verbose_name="Фамилия")
    phone = models.CharField(max_length=20, blank=False, verbose_name="Номер телефона")
    position = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Plumber", verbose_name="Позиция"
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    executor = models.ForeignKey(
        "Executor", on_delete=models.CASCADE, related_name="workers", null=True
    )
    is_sys_user = models.BooleanField(default=False, verbose_name="Системный ли пользователь?")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "middle_name", "last_name", "phone"]
    objects = UserManager()

    class Meta:
        db_table = "worker"
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"
        ordering = (
            "created",
        )

    def __str__(self):
        return f"{self.first_name} {self.last_name} "

    @staticmethod
    def xlsx_columns():
        return [
            "id",
            "last_name",
            "first_name",
            "middle_name",
            "email",
            "phone",
            "position",
            "is_active",
        ]

    def get_absolute_url(self):
        return reverse("projecta:workers")

class Executor(models.Model):
    org_form_choices = (
        ("Не определено", "Не определено"),
        ("ООО", "ООО"),
        ("ИП", "ИП"),
        ("ОАО", "ОАО"),
        ("ЗАО", "ЗАО"),
        ("АО", "АО"),
        ("ПАО", "ПАО"),
        ("НАО", "НАО"),
        ("НКО", "НКО"),
        ("гр.", "гр."),
        ("МБОУ", "МБОУ"),
        ("ТСН", "ТСН"),
    )
    inn = models.CharField(max_length=12, unique=True, verbose_name="ИНН")
    kpp = models.CharField(max_length=10, verbose_name="КПП")
    org_form = models.CharField(
        max_length=15,
        verbose_name="Форма организации",
        default="Не определено",
        choices=org_form_choices,
    )
    name = models.CharField(max_length=255, null=False, verbose_name="Наименование")
    legal_address = models.CharField(max_length=1023, verbose_name="Юр. адрес")
    index = models.CharField(max_length=6, verbose_name="Индекс")
    phone = models.CharField(max_length=20, null=False, verbose_name="Номер телефона")
    email = models.EmailField(blank=False, unique=True, verbose_name="Почта")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    REQUIRED_FIELDS = ["inn", "name", "phone"]

    def serialize(self):
        return {
            "inn": self.inn,
            "kpp": self.kpp,
            "name": self.name,
            "legal_address": self.legal_address,
            "index": self.index,
            "phone": self.phone,
            "email": self.email,
        }

    class Meta:
        db_table = "executor"
        verbose_name_plural = "Компании исполнители"
        verbose_name = "Компания исполнитель"
        ordering = (
            "-updated",
            "-created",
        )

    def __str__(self):
        return self.org_form + ' "' + self.name + '"'

class Client(models.Model):
    org_form_choices = (
        ("Не определено", "Не определено"),
        ("ООО", "ООО"),
        ("ИП", "ИП"),
        ("ОАО", "ОАО"),
        ("ЗАО", "ЗАО"),
        ("АО", "АО"),
        ("ПАО", "ПАО"),
        ("НАО", "НАО"),
        ("НКО", "НКО"),
        ("гр.", "гр."),
        ("МБОУ", "МБОУ"),
        ("ТСН", "ТСН"),
    )
    inn = models.CharField(max_length=12, verbose_name="ИНН")
    kpp = models.CharField(max_length=10, verbose_name="КПП")
    org_form = models.CharField(
        max_length=15,
        verbose_name="Форма организации",
        default="Не определено",
        choices=org_form_choices,
    )
    name = models.CharField(max_length=255, null=False, verbose_name="Наименование")
    legal_address = models.CharField(max_length=1023, verbose_name="Юр. адрес")
    index = models.CharField(max_length=6, verbose_name="Индекс")
    phone = models.CharField(max_length=20, null=False, verbose_name="Номер телефона")
    email = models.EmailField(blank=False, unique=False, verbose_name="Почта")
    status = models.CharField(
        max_length=255, null=False, default="Б/С", verbose_name="Статус"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="clients", verbose_name="Автор"
    )
    executor = models.ForeignKey(
        Executor,
        on_delete=models.CASCADE,
        related_name="clients",
        verbose_name="Исполнитель",
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен?")
    is_delete = models.BooleanField(default=False, verbose_name="Удален?")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    REQUIRED_FIELDS = ["inn", "name", "phone"]

    class Meta:
        db_table = "client"
        verbose_name_plural = "Клиент"
        verbose_name = "Клиент"
        ordering = (
            "name",
            "-updated",
            "-created",
        )

    def __str__(self):
        return self.org_form + ' "' + self.name + '"'

    def get_absolute_url(self):
        return reverse("projecta:client_detail", kwargs={"pk": self.pk})

    @staticmethod
    def xlsx_columns():
        return [
            "id",
            "inn",
            "kpp",
            "org_form",
            "name",
            "legal_address",
            "index",
            "phone",
            "email",
            "status",
            "is_active",
        ]

class ClientContact(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="contacts", verbose_name="Клиент"
    )
    fio = models.CharField(max_length=255, blank=True, verbose_name="ФИО")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Номер телефона")
    email = models.EmailField(verbose_name="Почта", blank=True)
    priority = models.CharField(max_length=255, blank=True, verbose_name="Приоритет")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta:
        db_table = "client_contact"
        verbose_name_plural = "Контакты клиентов"
        verbose_name = "Контакты клиента"
        ordering = (
            "-updated",
            "-created",
        )

    def __str__(self):
        return self.fio

    def get_absolute_url(self):
        return reverse("projecta:client_detail", kwargs={"pk": self.client.pk})

    @staticmethod
    def xlsx_columns():
        return ["id", "fio", "email", "phone", "priority", "client"]

class ClientStatus(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="statuses", verbose_name="Клиент"
    )
    executor = models.IntegerField(default=0, verbose_name="Компания исполнитель")
    author = models.IntegerField(verbose_name="Автор")
    status = models.CharField(max_length=255, verbose_name="Статус")
    is_active = models.BooleanField(default=True, verbose_name="Активен?")
    is_delete = models.BooleanField(default=False, verbose_name="Удален?")
    is_actual = models.BooleanField(default=True, verbose_name="Актуален?")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta:
        db_table = "client_status"
        verbose_name_plural = "Статусы клиентов"
        verbose_name = "Статус клиента"
        ordering = (
            "-updated",
            "-created",
        )

class License(models.Model):
    CLASS_CHOICES = (
        ("Нет класса", "Нет класса"),
        ("1 класс", "1 класс"),
        ("2 класс", "2 класс"),
        ("3 класс", "3 класс"),
        ("4 класс", "4 класс"),
    )

    license = models.TextField(verbose_name="Лицензия")
    date_reg = models.DateField(verbose_name="Дата регистрации")
    class_danger = models.CharField(
        max_length=255,
        default="Нет",
        choices=CLASS_CHOICES,
        verbose_name="Класс опасности",
    )
    executor = models.ForeignKey(
        Executor,
        related_name="licenses",
        on_delete=models.CASCADE,
        verbose_name="Компания",
    )

    class Meta:
        db_table = "licence"
        verbose_name_plural = "Лицензии"
        verbose_name = "Лицензия"

    def get_absolute_url(self):
        return reverse("projecta:company")

class Agreement(models.Model):
    STATUS_CHOICES = (
        ("Б/С", "Б/С"),
        ("У клиента", "У клиента"),
        ("Подписан", "Подписан"),
        ("ЭДО", "ЭДО"),
        ("Расторгнут", "Расторгнут"),
    )

    agreement_number = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        verbose_name="Номер договора",
        error_messages={"unique": "Required error"},
    )
    status = models.CharField(
        max_length=255,
        null=False,
        choices=STATUS_CHOICES,
        default="Б/С",
        verbose_name="Статус",
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="agreements", verbose_name="Автор"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="agreements",
        verbose_name="Клиент",
    )
    executor = models.ForeignKey(
        Executor,
        on_delete=models.CASCADE,
        related_name="agreements",
        verbose_name="Исполнитель",
    )
    date_from = models.DateField(null=False, verbose_name="Дата начала")
    date_to = models.DateField(null=False, verbose_name="Дата конца")
    address = models.CharField(max_length=1024, verbose_name="Адрес объекта")
    responsible = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Ответственный",
        related_name="responsible",
    )
    num_reg_certificate = models.CharField(
        max_length=255, verbose_name="Регистрационный №"
    )
    date_reg_certificate = models.DateField(
        verbose_name="Дата регистрации", default="1970-01-01", null=True, blank=True
    )
    class_danger = models.CharField(
        max_length=255, default="3 класс", verbose_name="Класс опасности"
    )
    license = models.TextField(verbose_name="Лицензия", null=True, blank=True)
    reasons_termination = models.TextField(verbose_name="Причины расторжения договора", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен?")
    is_delete = models.BooleanField(default=False, verbose_name="Удален?")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    def get_absolute_url(self):
        return reverse("projecta:agreement_detail", kwargs={"pk": self.pk})

    def serialize(self):
        return {
            "client": self.client,
            "agreement_number": self.agreement_number,
            "status": self.status,
            "reasons_termination": self.reasons_termination,
            "date_from": self.date_from,
            "date_to": self.date_to,
            "address": self.address,
            "responsible": (self.responsible.pk, self.responsible),
            "num_reg_certificate": self.num_reg_certificate,
            "date_reg_certificate": self.date_reg_certificate,
            "class_danger": self.class_danger,
        }

    class Meta:
        db_table = "agreement"
        verbose_name_plural = "Договоры"
        verbose_name = "Договор"
        ordering = (
            "-updated",
            "-created",
        )
        unique_together = (
            "agreement_number",
            "executor",
        )

    def __str__(self):
        return f"№{self.agreement_number} - {self.client}"

    @staticmethod
    def xlsx_columns():
        return [
            "id",
            "agreement_number",
            "address",
            "date_from",
            "date_to",
            "date_reg_certificate",
            "num_reg_certificate",
            "license",
            "class_danger",
            "responsible",
            "status",
            "reasons_termination",
            "client",
            "is_active",
        ]

class AgreementStatus(models.Model):
    agreement = models.ForeignKey(
        Agreement, on_delete=models.CASCADE, related_name="statuses"
    )
    executor = models.IntegerField(default=0, verbose_name="Компания исполнитель")
    status = models.CharField(max_length=255, verbose_name="Статус")
    author = models.IntegerField(verbose_name="Автор")
    responsible = models.IntegerField(verbose_name="Ответственный", null=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен?")
    is_delete = models.BooleanField(default=False, verbose_name="Удален?")
    is_actual = models.BooleanField(default=True, verbose_name="Актуален?")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta:
        db_table = "agreement_status"
        verbose_name_plural = "Статусы договоров"
        verbose_name = "Статус догвора"
        ordering = (
            "-updated",
            "-created",
        )

class InsurancePolicy(models.Model):
    name_insurance_company = models.CharField(max_length=1024, verbose_name="Страховая организация")
    date_from = models.DateField(null=False, verbose_name="Дата начала")
    date_to = models.DateField(null=False, verbose_name="Дата конца")
    agreement = models.ForeignKey(
        Agreement,
        on_delete=models.CASCADE,
        related_name="insurances",
        verbose_name="Договор",
    )
    executor = models.ForeignKey(
        Executor,
        on_delete=models.CASCADE,
        related_name="insurances",
        verbose_name="Исполнитель",
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta:
        db_table = "insurance_policy"
        verbose_name_plural = "Страховые полисы"
        verbose_name = "Страховой полис"

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse("projecta:agreement_detail", kwargs={"pk": self.agreement.pk})

class Equipment(models.Model):
    TYPE_CHOICES = (
        ("ГРПШ", "ГРПШ"),
        ("Котел газового оборудования", "Котел газового оборудования"),
        ("Сигнализаторы загазованности", "Сигнализаторы загазованности"),
        ("Узел учета газа", "Узел учета газа"),
        ("Не определён", "Не определён"),
    )

    agreement = models.ForeignKey(
        Agreement,
        on_delete=models.CASCADE,
        related_name="equipment",
        verbose_name="Соглашение",
    )
    type = models.CharField(
        max_length=255,
        null=False,
        choices=TYPE_CHOICES,
        default="Не определён",
        verbose_name="Тип",
    )
    executor = models.ForeignKey(
        Executor,
        on_delete=models.CASCADE,
        verbose_name="Испонитель",
        related_name="equipment",
    )
    description = models.TextField(null=False, verbose_name="Описание")
    amount = models.IntegerField(null=False, verbose_name="Количество")
    date_from = models.DateField(verbose_name="Начало эксплуатации")
    date_to = models.DateField(verbose_name="Конец эксплуатации")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta:
        db_table = "equipment"
        verbose_name_plural = "Оборудования"
        verbose_name = "Оборудование"
        ordering = (
            "-updated",
            "-created",
        )

    def __str__(self):
        return self.type

    def get_absolute_url(self):
        return reverse("projecta:agreement_detail", kwargs={"pk": self.agreement.pk})

    @staticmethod
    def xlsx_columns():
        return [
            "id",
            "type",
            "description",
            "amount",
            "date_from",
            "date_to",
            "agreement",
        ]

class Ticket(models.Model):
    TYPE_CHOICES = (
        ("ТО", "ТО"),
        ("Инцидент", "Инцидент"),
        ("Ремонт", "Ремонт"),
        ("Замена", "Замена"),
        ("Установка", "Установка"),
    )

    STATUS_CHOICES = (
        ("Б/С", "Б/С"),
        ("В работе", "В работе"),
        ("Выполнил", "Выполнил"),
    )

    type = models.CharField(
        max_length=255,
        null=False,
        choices=TYPE_CHOICES,
        default="Нет типа",
        verbose_name="Тип",
    )
    executor = models.ForeignKey(
        Executor,
        on_delete=models.CASCADE,
        verbose_name="Испонитель",
        related_name="tickets",
    )
    status = models.CharField(
        max_length=255,
        null=False,
        choices=STATUS_CHOICES,
        default="Б/С",
        verbose_name="Статус",
    )
    execution_date = models.DateField(verbose_name="Дата выполнения")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="Комментарий", null=True, blank=True)
    agreement = models.ForeignKey(
        Agreement,
        on_delete=models.CASCADE,
        related_name="tickets",
        verbose_name="Соглашение",
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    is_active = models.BooleanField(default=True, verbose_name="Активен?")
    REQUIRED_FIELDS = ["type"]

    class Meta:
        db_table = "ticket"
        verbose_name_plural = "Заявки"
        verbose_name = "Заявка"
        ordering = (
            "-updated",
            "-created",
        )

    def get_absolute_url(self):
        return reverse("projecta:ticket_detail", kwargs={"pk": self.pk})

    @staticmethod
    def xlsx_columns():
        return [
            "id",
            "type",
            "comment",
            "execution_date",
            "status",
            "agreement",
            "is_active",
        ]

class TicketStatus(models.Model):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="ticket_status",
        verbose_name="Заявка",
    )
    executor = models.IntegerField(default=0, verbose_name="Компания исполнитель")
    status = models.CharField(
        max_length=255, null=False, default="Б/С", verbose_name="Статус"
    )
    author = models.IntegerField(verbose_name="Автор")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    is_active = models.BooleanField(default=True, verbose_name="Активен?")
    is_actual = models.BooleanField(default=True, verbose_name="Актуален?")

    class Meta:
        db_table = "ticket_status"
        verbose_name_plural = "Статусы заявок"
        verbose_name = "Статус заявки"
        ordering = (
            "-updated",
            "-created",
        )

class Act(models.Model):
    STATUS_CHOICES = (
        ("Б/С", "Б/С"),
        ("У клиента", "У клиента"),
        ("Подписан", "Подписан"),
        ("ЭДО", "ЭДО"),
    )
    CHECK_STATUSES = (
        ("Не выставлен", "Не выставлен"),
        ("Выставлен", "Выставлен"),
        ("Не оплачен", "Не оплачен"),
        ("Оплачен", "Оплачен"),
    )
    act_number = models.CharField(max_length=255, verbose_name="Номер акта")
    agreement = models.ForeignKey(
        Agreement,
        on_delete=models.CASCADE,
        related_name="acts",
        verbose_name="Соглашение",
    )
    act_date = models.DateField(null=False, verbose_name="Дата акта")
    act_status = models.CharField(
        max_length=255,
        null=False,
        verbose_name="Статус акта",
        choices=STATUS_CHOICES,
        default="Б/С",
    )
    check_number = models.CharField(max_length=255, verbose_name="Номер счёта")
    check_status = models.CharField(
        max_length=255,
        choices=CHECK_STATUSES,
        default="Не выставлен",
        verbose_name="Статус счёта",
    )
    executor = models.ForeignKey(
        Executor,
        on_delete=models.CASCADE,
        verbose_name="Испонитель",
        related_name="acts",
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="acts", verbose_name="Автор"
    )
    created = models.DateTimeField(auto_now=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "act"
        verbose_name_plural = "Акты"
        verbose_name = "Акт"
        ordering = (
            "-act_date",
            "-created",
        )
        unique_together = (
            "act_number",
            "agreement",
        )

    def get_absolute_url(self):
        return reverse("projecta:agreement_detail", kwargs={"pk": self.agreement.pk})

    def save(self, *args, **kwargs):
        queryset = self.agreement.acts.filter(
            act_date__startswith=datetime.strptime(
                str(self.act_date), "%Y-%m-%d"
            ).strftime("%Y-%m-%d")
        )
        if queryset.exists() and self not in queryset:
            raise ValidationError("Акт за эту дату уже существует")
        super(Act, self).save(*args, **kwargs)

    @staticmethod
    def xlsx_columns():
        return [
            "id",
            "act_number",
            "act_date",
            "act_status",
            "check_number",
            "check_status",
            "agreement",
            "is_active",
        ]

class ActStatus(models.Model):
    act = models.ForeignKey(
        Act, on_delete=models.CASCADE, related_name="statuses", verbose_name="Акт"
    )
    executor = models.IntegerField(default=0, verbose_name="Компания исполнитель")
    act_status = models.CharField(max_length=255, null=False, verbose_name="Статус")
    check_status = models.CharField(max_length=255)
    author = models.IntegerField(verbose_name="Автор")
    created = models.DateTimeField(auto_now=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    is_active = models.BooleanField(default=True, verbose_name="Активен?")
    is_actual = models.BooleanField(default=True, verbose_name="Актуален?")

    class Meta:
        db_table = "act_status"
        verbose_name_plural = "Статусы Актов"
        verbose_name = "Статус Акта"
        ordering = (
            "-updated",
            "-created",
        )

class EquipmentPhoto(models.Model):
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="photos", verbose_name="Заявка"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="photos", verbose_name="Автор"
    )
    executor = models.ForeignKey(
        Executor,
        on_delete=models.CASCADE,
        related_name="photos",
        verbose_name="Исполнитель",
    )

    photo = models.FileField(upload_to="equipment/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "equip_photo"
        verbose_name_plural = "Фото оборудования"
        verbose_name = "Фото оборудования"
