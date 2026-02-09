# ADVANCED TRAFFIC ANALYZER
Скріпт який виконує аналіз логів веб сервера з підтримкою фільтраці та агрегації.

## Format input file
<**timestamp**: *int*> <**ip_address**: *str*> <**http_method**: *str*> <**url**: *str*> <**status_code**: *int*> <**response_size**: *int*>

## Use example
$`python bin/advanced_traffic_analyzer.py parse`

Params:
```
-f --filepath   - Path to . required.
--method        - Http method: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS.
--status        - HTTP status code.
--start         - Start timestamp
--end           - End timestamp
--top           - Top
```

Example:

$`python bin/advanced_traffic_analyzer.py parse --filepath test/test_access.log`


## Принцип роботи
Програма поділяється на 3 частини:
1. Entity - Сюди розмістив, ReportData та FilterOpt.
2. Kernal - той вже AdvancedTrafficAnalyzer та утіліти.
3. View - Перегляд даних. ViewReport.

Кожна з частин є залежною від попередньої частини, View залежить від Kernal, Kernal від Entity. А Entity це вже головні моделі які не від кого не залежать.

Як працює:
перша за все, створюються основні моделі та фільтри, такі як FilterOpt. Потім на основі фільтру створюється модель аналізу, яка і буде аналізувати логи і видавати звіт. далі створюється View модель за допомогою якої виводиться відповідь в термінал.

## Можливі покращення
Можна буде краще прописати View модель.
Можна буде логічніше розмістити entity
Симпатичніше написати report format (у view)# advanced_traffic_analyzer
