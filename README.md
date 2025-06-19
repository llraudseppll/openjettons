
OpenJettons — это открытый реестр jetton'ов в блокчейне TON (The Open Network). Проект предоставляет автоматизированную систему для добавления и проверки jetton'ов с помощью YAML-файлов и их валидации через TON Center API. Проверенные jetton'ы включаются в файл jettons.json, который служит публичным списком.
Основные возможности

Добавление jetton'ов: Создайте YAML-файл в директории jettons/ с метаданными jetton'а (адрес, имя, символ и т.д.).
Автоматическая проверка: GitHub Actions проверяет YAML-файлы на соответствие данным TON Center API.
Генерация реестра: Валидные jetton'ы автоматически добавляются в jettons.json.
Открытый вклад: Любой может предложить новый jetton через Pull Request.

Как добавить новый jetton

Создайте YAML-файл:

В директории jettons/ создайте файл, например, YouCoin.yaml:address: EQCz................................
name: YouCoin
symbol: YOC
decimals: 9
image: https://youcoin.example.com/logo.png
description: A token for the TruckCoin project
website: https://youcoin.example.com


Убедитесь, что address — это валидный мастер-контракт jetton'а (TEP-74), проверенный на tonviewer.com.


Проверьте локально:

Установите зависимости:pip install requests pyyaml


Запустите проверку:python scripts/verify_jetton.py jettons/YouCoin.yaml


Если валидация прошла, скрипт выведет:Jetton at <address> validated successfully!
Generated jettons.json




Создайте Pull Request:

Сделайте форк репозитория и клонируйте его:git clone https://github.com/your-username/openjettons.git
cd openjettons


Добавьте ваш YAML-файл:git add jettons/YouCoin.yaml
git commit -m "Добавлен YouCoin.yaml"
git push origin main


Создайте Pull Request в основной репозиторий. GitHub Actions автоматически запустит проверку через verify-jettons.yml.


Проверка и слияние:

После успешной проверки ваш jetton будет добавлен в jettons.json и включён в реестр.



Структура репозитория

jettons/: Директория с YAML-файлами jetton'ов (например, YouCoin.yaml).
scripts/verify_jetton.py: Скрипт для проверки jetton'ов через TON Center API.
jettons.json: Сгенерированный список валидных jetton'ов.
.github/workflows/verify-jettons.yml: Workflow для автоматической проверки в GitHub Actions.

Настройка GitHub Actions
Workflow .github/workflows/verify-jettons.yml автоматически запускается при пушах в ветки main или feature/**. Он:

Проверяет изменённые YAML-файлы в jettons/.
Использует verify_jetton.py для валидации через TON Center API.
Обновляет jettons.json, если валидация успешна.

Чтобы настроить workflow локально:

Убедитесь, что зависимости установлены:pip install requests pyyaml


Протестируйте:python scripts/verify_jetton.py jettons/*.yaml



Требования

Python 3.9+
Библиотеки: requests, pyyaml
Доступ к TON Center API (без ключа для публичных запросов)

Лицензия
MIT License. См. LICENSE для подробностей.
Контакты
Если у вас есть вопросы или предложения, создайте Issue или свяжитесь через Discussions.

Последнее обновление: июнь 2025
