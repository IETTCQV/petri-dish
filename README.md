# petri-dish
 
Симуляция микробов (роботов?).

За одно обновление микроб микроб обрабатывает один ген.
Гены храняться в строке байтов по 2 байта.

Направления:
 - 1 - право
 - 2 - верх
 - 3 - лево
 - 4 - низ

Типы генов и их описание:
 - 1 - передвижение, ходит на клетку, указанную во тором байте.
  (не может ходить на занятую клетку, карта закольцована)
 
 - 2 - мутация, изменяет, добавляет или удаляет ген.
  может изменить цвет или стоимость хода (стоимость обработки гена)
 
 - 3 - копирование, копирует себя на клетку, указанную во втором байте.
  (не может копировать себя на занятую клетку, требует много энергии)
 
 - 4 - поедание, поедает другую клутку, указанную во втором байте.
  получает 50% энергии той клети, которую съел
