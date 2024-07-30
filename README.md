# exp_testing_framework
Пример фреймворка для тестирования API сервиса `DM`
____

Установка необходимых библиотек и пакетов:
```shell
pip install -r requirements.txt 
```

Запуск тестов:
```shell
pytest tests
```
Запуск тестов с формированием отчёта Allure:
```shell
pytest tests --alluredir=./allure-results
```
Генерация отчёта Allure:
```shell
allure generate -c ./allure-results -o ./allure-report
```
Запуск локального HTTP сервера для просмотра отчёта Allure:
```shell
allure serve  
```
