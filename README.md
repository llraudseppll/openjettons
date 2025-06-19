OpenJettons
OpenJettons is an open registry of jettons on The Open Network (TON) blockchain. The project provides an automated system for adding and verifying jettons using YAML files, validated against the TON Center API. Verified jettons are included in the jettons.json file, serving as a public registry.
Key Features

Add Jettons: Create a YAML file in the jettons/ directory with jetton metadata (address, name, symbol, etc.).
Automated Verification: GitHub Actions verifies YAML files against TON Center API data.
Registry Generation: Valid jettons are automatically added to jettons.json.
Open Contribution: Anyone can propose a new jetton via a Pull Request.

How to Add a New Jetton

Create a YAML File:

In the jettons/ directory, create a file, e.g., TruckCoin.yaml:address: EQCzGUyJocAlZcZmIcQniLaP4X7nepnXM8QAaQSmbISZEtvF
name: TruckCoin
symbol: TRCK
decimals: 9
image: https://truckcoin.example.com/logo.png
description: A token for the TruckCoin project
website: https://truckcoin.example.com


Ensure the address is a valid jetton master contract (TEP-74), verified on tonviewer.com.


Test Locally:

Install dependencies:pip install requests pyyaml


Run the verification script:python scripts/verify_jetton.py jettons/TruckCoin.yaml


On success, the script outputs:Jetton at <address> validated successfully!
Generated jettons.json




Create a Pull Request:

Fork the repository and clone it:git clone https://github.com/your-username/openjettons.git
cd openjettons


Add your YAML file:git add jettons/TruckCoin.yaml
git commit -m "Add TruckCoin.yaml"
git push origin main


Open a Pull Request to the main repository. GitHub Actions will automatically verify the jetton using verify-jettons.yml.


Review and Merge:

Once the verification passes, your jetton will be added to jettons.json and included in the registry.



Repository Structure

jettons/: Directory containing jetton YAML files (e.g., TruckCoin.yaml).
scripts/verify_jetton.py: Script for validating jettons using TON Center API.
jettons.json: Generated list of valid jettons.
.github/workflows/verify-jettons.yml: GitHub Actions workflow for automated verification.

GitHub Actions Setup
The .github/workflows/verify-jettons.yml workflow runs automatically on pushes to main or feature/** branches. It:

Checks for changed YAML files in jettons/.
Uses verify_jetton.py to validate against TON Center API.
Updates jettons.json if verification succeeds.

To test the workflow locally:

Ensure dependencies are installed:pip install requests pyyaml


Run the script:python scripts/verify_jetton.py jettons/*.yaml



Requirements

Python 3.9+
Libraries: requests, pyyaml
Access to TON Center API (no key required for public requests)

License
MIT License. See LICENSE for details.
Contact
For questions or suggestions, create an Issue or join the Discussions.

Last updated: June 2025



OpenJettons
OpenJettons — это открытый реестр jetton'ов в блокчейне TON (The Open Network). Проект предоставляет автоматизированную систему для добавления и проверки jetton'ов с помощью YAML-файлов и их валидации через TON Center API. Проверенные jetton'ы включаются в файл jettons.json, который служит публичным списком.
Основные возможности

Добавление jetton'ов: Создайте YAML-файл в директории jettons/ с метаданными jetton'а (адрес, имя, символ и т.д.).
Автоматическая проверка: GitHub Actions проверяет YAML-файлы на соответствие данным TON Center API.
Генерация реестра: Валидные jetton'ы автоматически добавляются в jettons.json.
Открытый вклад: Любой может предложить новый jetton через Pull Request.

Как добавить новый jetton

Создайте YAML-файл:

В директории jettons/ создайте файл, например, TruckCoin.yaml:address: EQCzGUyJocAlZcZmIcQniLaP4X7nepnXM8QAaQSmbISZEtvF
name: TruckCoin
symbol: TRCK
decimals: 9
image: https://truckcoin.example.com/logo.png
description: A token for the TruckCoin project
website: https://truckcoin.example.com


Убедитесь, что address — это валидный мастер-контракт jetton'а (TEP-74), проверенный на tonviewer.com.


Проверьте локально:

Установите зависимости:pip install requests pyyaml


Запустите проверку:python scripts/verify_jetton.py jettons/TruckCoin.yaml


Если валидация прошла, скрипт выведет:Jetton at <address> validated successfully!
Generated jettons.json




Создайте Pull Request:

Сделайте форк репозитория и клонируйте его:git clone https://github.com/your-username/openjettons.git
cd openjettons


Добавьте ваш YAML-файл:git add jettons/TruckCoin.yaml
git commit -m "Добавлен TruckCoin.yaml"
git push origin main


Создайте Pull Request в основной репозиторий. GitHub Actions автоматически запустит проверку через verify-jettons.yml.


Проверка и слияние:

После успешной проверки ваш jetton будет добавлен в jettons.json и включён в реестр.



Структура репозитория

jettons/: Директория с YAML-файлами jetton'ов (например, TruckCoin.yaml).
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
