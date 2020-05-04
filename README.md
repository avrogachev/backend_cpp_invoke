#  АПИ для одной задачи из игры-изоляции

Стояла задача сделать расчёт характеристик посадки космического корабля - чтобы
пользователь мог играть в посадку корабля на настоящих данных.

Пользователи играют в основном с телефонов (на 5 мая >2000 активных игроков) и
не хотелось грузить их телефон вычислениями прямо внутри айфрэйма (причём, это
  напрямую запрещено правилами ВК). Пришлось научиться оборачивать плюсы в питон
  и лепить из этого бэкенд. Работает хорошо.

Ещё интересная особенность - фронт и бэк разделены, поэтому пришлось купить
домен для дроплета чтобы CORS корректно работал.
## Как с ним работать

https://spacequest.site:81/docs - автоматически сгенерированные доки.

Ну и напрямую https://spacequest.site:81/space/{H}/{F} где H это высота включения
двигателей, F - тяга. Высота от 0 до 9.9 км, тяга от 8000 до 22400 Н. Возвращается JSON
характеристик посадки.

Ну и прямо в игре можно поиграть - https://vk.com/app7383610_-120231180 это последняя загадка второго этапа.

### Что следует установить

Нужно быть аккуратным - обвязка С++ питоном сделана через ctypes. Но ctypes работает только
с C, а не с C++, поэтому вывод нужной функции следует обернуть в extern C.


### Требования к серверу

При общении с фронтом используется CORS, поэтому нужно сделать дроплету https соединение,
а для этого следует найти домен и выпустить на него сертификат (я использовал let's encrypt)


## Лицензия

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Благодарности

* Спасибо команде сообщества Космический рейс за вдохновление разрабатывать подобные вещи
* Если понравилось - задонатьте сюда любую сумму https://yasobe.ru/na/kosmicheskyireis
