Contributing to OpenJettons
Спасибо за ваш интерес к OpenJettons! Вот инструкции по добавлению jetton'ов.
Правила

Jetton должен соответствовать стандарту TEP-74.
Запрещены токены с мошенническим или запрещённым контентом.
Все .yaml файлы проверяются автоматически через GitHub Actions.

Шаги

Форкните репозиторий.
Создайте файл jetton-name.yaml в jettons/:address: EQ...
name: MyJetton
symbol: MJT
decimals: 9
image: https://example.com/logo.png
description: A sample jetton
website: https://example.com


Для ручной проверки (опционально):pip install requests pyyaml
python scripts/verify_jetton.py jettons/your-jetton.yaml


Создайте Pull Request с:
Описанием токена.
Подтверждением, что токен не содержит запрещённого контента.


Дождитесь результатов автоматической проверки в PR.
Если проверка не пройдена, проверьте логи GitHub Actions, исправьте .yaml и обновите PR.



Автоматическая проверка

При создании PR GitHub Actions запускает verify_jetton.py для всех новых или изменённых .yaml файлов в jettons/.
Проверка завершается с ошибкой, если:
Контракт не является jetton'ом.
Метаданные (name, symbol, decimals) не совпадают с данными tonscan.
YAML-файл содержит ошибки.



Проверка PR

Модераторы проверят PR на соответствие правилам после успешной автоматической проверки.
Jetton будет добавлен в jettons.json после одобрения.

Вопросы
Создайте Issue для обсуждения или обратной связи.

