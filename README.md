# course_project

** Getting started:**

**How to generate a token?**
  1. Open an account in Tinkoff Investments

  2. Generate a Tinkoff access token (Токен доступа - T-Invest API (russianinvestments.github.io))

  3. Put this token into my_token.py file

**Hyperparameters search**
In our project we used the GridSearchCV method from the sklearn.model_selection library. In order to successfully implement this method to your algorithm you need to create a sklearn-compatible model or use one of sklearn algorithms for your analysis. In our project we created several sklearn-compatible models, as an example (for moving average (MA) and relative strength index (RSI)).
Sklearn-compatible model needs to have the following functions:
  1. \_\_init\_\_ model initialisation, for example, specifying window size for the RSI model
  2. fit - fit the model with the data. In case of the RSI and MA this is a technical step, required only for proper work of the other functions
  3. predict - 
  4. score
You can see examples of such models in relative_strength_index.py (relative_strength_index model) and moving_average.py (moving_average class)

**База данных**
Файл с созданием и заплонением базы данных называется db.py. При его запуске он создает или находит уже существующий файл invest.db, в котором хранится сама база данных. Она состоит из двух таблиц - hourly_prices и daily_prices, которые содержат чаовые и дневные котировки соответственно. Массив codes содержит figi-коды компаний, для которых осуществляется сбор данных. При запуске файла для компаний, указанных в списке, собираются все исторические данные. Для того, чтобы поддерживать актуальность базы данных, созданы функции fill_table_with_latest_values_hourly() и fill_table_with_latest_values_daily(), которые для каждой компании в таблице загружают все новые данные. Эти функции рекомендуется вызывать перед использованием самих алгоритмов, чтобы использовать максимально свежие данные.


**Алгоритмы**
У нас в роботе реализовано два различных алгоритма - RSI, или Индекс Относительной Силы, и Moving Average, или Скользящая Средняя. Они реализованы в файлах RSI.py и MA.py соответственно. RSI измеряет скорость и изменение ценовых движений, показывая перекупленность или перепроданность актива на основе его недавних ценовых изменений. Он колеблется между 0 и 100, где значения выше 70 указывают на перекупленность, а ниже 30 — на перепроданность. MA - скользящий средний, который вычисляется путем усреднения цен актива за заданный период времени. Он сглаживает колебания цен, помогая выявить общие направления тренда, и используется для определения уровней поддержки и сопротивления. Для того, чтобы подобрать оптимальные параметры окон для обоих алгоритмов, был реализован алгоритм Grid_Search. 

**Визуализация и взаимодействие**
Реализовано взаимодействие клиента и робота в интерактивном окне. Пользователь имеет возможность выбрать акцию для трейдинга, желаемый алгоритм (RSI/MA) и временной промежуток исторических данных, на которых будет обучаться робот. После завершения трейдинга пользователь получает фидбэк от робота в виде решения по трейдингу (покупка/продажа), итоговой прибыли и графика торгов, с динамичным обновлением через определенный промежуток времени. Интерфейс направлен на упрощение работы с роботом клиентов, не имеющих опыт в трейдинге, а его простота несомненно улучшает пользовательский experience.
