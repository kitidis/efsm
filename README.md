
# Генератор тестов для расширенных автоматов
Данный репозиторий содержит пакет программ, позволяющих строить whitebox/blackbox проверяющий тест для расширенных автоматов.
- Whitebox: на основе мутационного расширенного автомата или на основе перебора всех возможных мутантов эквивалентного конечного автомата.
- Blackbox: HSI метод и метод обхода графа переходов, построенного по эквивалентному конечному автомату.

## Параметры командной строки

test.exe [-h] [-i INPUT_EFSM] [-o OUTPUT_TEST] [-m MODEL_TYPE] [-mt METHOD]

параметры:
<table class="tg">
  <col width="45%">
  <col width="65%">
  <tr>
    <td>-h, --help</td>
    <td> выводит справку</td>
  </tr>
  <tr>
    <td>-i INPUT_FSM</td>
    <td>путь к входному файлу конечного автомата </td>
  </tr>
  <tr>
    <td>-o OUTPUT_TEST</td>
    <td>путь к выходному файлу, содержащему тестовые последовательности</td>
  </tr>
  <tr>
    <td>-m MODEL_TYPE</td>
    <td>тестовая гипотеза (test hypothesis): black_box/white_box</td>
  </tr>
  <tr>
    <td>-mt METHOD</td>
    <td>метод генерации теста для модели black_box: transition_tour/hsi<br>
    метод генерации теста для модели white_box: efsm/fsm</td>
  </tr>
</table>

## Пример
**test.fsm**
```2 4 7 2 1 1 1 0
s0
0 2
s1
2 2
0 0 2
1 2 1
0 3 2
1 5 2
w<2
w=w+1
0 0
w==2
w=0
0 1
true

0 0
w<1
w=w+2
0 1
w>=1
w=1
0 0
w<2

0 1
w==2
w=0
0 0
a
0
b
0
w
1
w
0
w
w
0 0
```

Командная строка

    $ test.exe -i test.efsm -o 0.seq -m white_box -mt efsm
    $ test.exe -i test.efsm -o 0.seq -m white_box -mt fsm
    $ test.exe -i test.efsm -o 0.seq -m black_box -mt transition_tour
    $ test.exe -i test.efsm -o 0.seq -m black_box -mt hsi

## Авторы
Программные продукты, включённые в данный пакет прикладных программ, разработаны сотрудниками кафедры информационных технологий в исследовании дискретных структур радиофизического факультета Томского государственного университета
