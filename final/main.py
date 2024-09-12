import sys
sys.path.append('tables')

from project_config import *
from dbconnection import *

from tables.routes_table import *
from tables.station_table import *


class Main:
    
    
    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        stat = StationTable()
        rout = RoutesTable()
        stat.create()
        rout.create()
        return

    def db_insert_somethings(self):
        stat = StationTable()
        rout = RoutesTable()
        
        stat.example_insert()
        rout.example_insert()
        
    def db_drop(self):
        stat = StationTable()
        rout = RoutesTable()
        rout.drop()
        stat.drop()
        return

    def show_main_menu(self):
        menu = """Привутствуем в меню, выберите действие:
        1 - просмотр станций;
        2 - сброс и инициализация БД;
        9 - выход;"""

        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return "0"
        elif next_step != "1" and next_step != "9":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step
            
    def show_station(self):
        self.station_id = -1
        self.station_arr = []

        self.max_len_name = -9000
        lst = StationTable().all()
        self.max_station_index = (len(lst))
        for i in lst:
            self.station_arr.append([i[0], str(i[2]), str(i[3]), str(i[1])]) 
            # 0 - id, 1 - name, 2 - tarrif_id, 3 - index
            self.max_len_name = max(self.max_len_name, len(str(i[2])))
            
            
        menu = f"""Просмотр списка станций.
№\tНазвание {" "*(self.max_len_name-4)}Тарифная зона   Индекс\n{"-"*100}"""
        print(menu)    
        for i in range(len(self.station_arr)):
            output = f"""{str(i+1)}\t{self.station_arr[i][1]} {" "*(4+self.max_len_name - len(self.station_arr[i][1]))}\
{str(self.station_arr[i][2])}   {" "*(13-len(str(self.station_arr[i][2])))}{str(self.station_arr[i][3])}"""
            print(output)
            
        menu = f"""{"-"*100}\nДальнейшие операции: 
    0 - возврат в главное меню;
    3 - добавление новой станции;
    4 - удаление станции;
    5 - просмотр маршрутов по станции;
    6 - добавление маршрута;
    8 - обновить станцию;
    9 - выход."""
        print(menu)
        return
    
    def after_show_station(self, next_step):
        """Выбор действий после вывода категорий
        """        
        while True:
            if next_step == "4": # Удаление станции
                x = add_func.validate_input('Введите номер удаляемой станции (0 - для отмены): ', 0, self.max_station_index)
                if(x!=-1):
                    StationTable().delete(self.station_arr[int(x)-1])
                return "1"
            
            elif next_step == "6": #Добавление маршрута
                RoutesTable().insert_route_one(self.max_station_index)
                next_step = "5"
                
            elif next_step == "7":#Удаление маршрута
                x = add_func.validate_input('Введите номер удаляемого маршрута (0 - для отмены): ', 0, self.max_routes_index)
                if(x!=-1):
                    RoutesTable().delete(self.routes_arr[int(x)-1][2])
                else:
                    return "1"     
                next_step = "5"
                
            elif next_step == "5":
                next_step = self.show_routes_with_station()
                
            elif next_step == "8": # Обновление названия станции
                x = add_func.validate_input('Введите номер обновляемой станции (0 - для отмены): ', 0, self.max_station_index)
                if(x!=-1):
                    StationTable().update(self.station_arr[int(x)-1])
                return "1"
                    
            elif next_step != "0" and next_step != "9" and next_step != "3":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step

    def add_station(self):
        while True:
            st_name = input('Введите название добавляемой станции (0 - отмена): ').strip()
            if len(st_name) > 20:
                print('Недопустмая длина названия станции')
            elif st_name == '0':
                return "1"
            else:
                break
        tarrif_zone_id = add_func.validate_input('Введите номер тарифной зоны(0-отмена): ', 0, 7)
        if(tarrif_zone_id==-1) or tarrif_zone_id == '1':
            return "1"
        st_index = add_func.validate_input('Введите индекс добавляемой станции(0-отмена): ', 0, 100)
        if(st_index==-1) or st_index == '0':
            return "1"
        insert = [st_index, st_name, tarrif_zone_id]
        StationTable().insert_one(insert)
        
    def show_routes_with_station(self):
        """Вывод всех маршрутов по введенной станции
        """       
        self.routes_arr = []
        if self.station_id == -1:
            while True:
                t = add_func.validate_input('Вывести маршрут по:\
            \n1 - начальной станции;\
            \n2 - конечной станции;\n(0 - отмена);\n', 0, 2)
                if t == 1:
                    x = add_func.validate_input('Выберите номер интересуемой строки с начальной станцией (0 - отмена): ', 0, self.max_station_index)
                    if(x==-1):
                        return
                    
                    self.station_id = self.station_arr[x-1][0]
                    self.station_obj = self.station_arr[x-1]
                    space_lenth = len(self.station_obj[1])
                    lst = RoutesTable().all_by_station_id(self.station_id, 1)
                    self.max_routes_index = len(lst)
                    
                    if lst == []:
                        print('Нет маршрута с такой начальной станцией')
                    else:
                        print("Выбрана station: " + self.station_obj[1])
                        print("Маршруты:")
                        print(f"""№\tНомер маршрута\tВыбранная станция {" "*8} Конечная станция\n{"-"*100}-""")
                        
                        for i in lst:
                            self.routes_arr.append([str(i[0]), str(i[2]), i[1]])
                                
                        for i in range(len(self.routes_arr)):
                            output = f"""{str(i+1)}\t{str(self.routes_arr[i][2])}\
{" " * 15}{self.station_obj[1]} {"-" * (24 - space_lenth)}> {str(StationTable().name_by_id(self.routes_arr[i][1])[0])}"""
                            print(output)
                        menu = """Дальнейшие операции:
0 - возврат в главное меню;
1 - возврат в просмотр станций;
7 - удаление маршрута;
9 - выход."""
                        print(menu)
                        return self.read_next_step()
                
                elif t == 2:
                    x = add_func.validate_input('Выберите номер интересуемой строки с конечной станцией (0 - отмена): ', 0, self.max_station_index)
                    if(x==0):
                        return
                    self.station_id = self.station_arr[x-1][0]
                    self.station_obj = self.station_arr[x-1]
                    space_lenth = len(self.station_obj[1])
                    lst = RoutesTable().all_by_station_id(self.station_id, 2)
                    self.max_routes_index = len(lst)
                    
                    if lst == []:
                        print('Нет маршрута с такой конечной станцией')
                    else:
                        print("Выбрана station: " + self.station_obj[1])
                        print("Маршруты:")
                        print(f"""№\tНомер маршрута\tВыбранная станция {" "*8} Начальная станция\n{"-"*100}""")
                        
                        for i in lst:
                            self.routes_arr.append([str(i[0]), str(i[2]), i[1]])
                                
                        for i in range(len(self.routes_arr)):
                            output = f"""{str(i+1)}\t{str(self.routes_arr[i][2])}\
{" " * 15}{self.station_obj[1]} <{"-" * (24 - space_lenth)} {str(StationTable().name_by_id(self.routes_arr[i][2])[0])}"""
                            print(output)
                        menu = f"""{"-"*100}\nДальнейшие операции:
0 - возврат в главное меню;
1 - возврат в просмотр станций;
7 - удаление маршрута;
9 - выход."""
                        print(menu)
                        return self.read_next_step()
                else:
                    return "5"
            
        

    def main_cycle(self):
        """Основной цикл программы, регулирующий порядок действий
        """        
        current_menu = "0"
        next_step = None
        
        while(current_menu != "9"):
            
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
                
            elif current_menu == "1":
                self.show_station()
                next_step = self.read_next_step()
                current_menu = self.after_show_station(next_step)
                
            elif current_menu == "2":
                self.show_main_menu()
                
            elif current_menu == "3":
                self.add_station()
                current_menu = "1"
                
        print("До свидания!")    
        return

    def test(self):
        DbTable.dbconn.test()

m = Main()
# m.test()
m.main_cycle() 