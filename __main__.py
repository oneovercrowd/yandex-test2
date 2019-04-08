from datetime import datetime
import re


class WorkData:
    def __init__(self, microtasks, delt_time):
        self.microtasks = microtasks
        self.delt_time = delt_time
        self.aver_time = delt_time / microtasks


class Assessor:
    def __init__(self, login, start_dtime):
        self.total_mtasks = 0
        self.login = login
        self.work_data = []
        return

    def add_work_data(self, microtasks, delt_time):
        self.work_data.append(WorkData(microtasks, delt_time))
        self.total_mtasks += microtasks
        return

    def get_average_time(self):
        self.work_data.sort(key=(lambda x: x.delt_time))
        # Возьмем медиану, чтобы снизить влияние аномально долгих промежутков времени
        length = len(self.work_data)
        if length % 2 == 1:
            return self.work_data[length//2].aver_time
        else:
            return (self.work_data[length//2].aver_time + self.work_data[length//2 - 1].aver_time) / 2


def main():
    # храним в словаре по ключу - логину
    assessors = {}

    data_file = open("data_task4_old.txt")
    data_file.readline()  # пропускаем строку заголовка
    for line in data_file:
        # парсим строку
        cells = re.split('\t|\n', line)
        login, microtasks, assigned_ts, closed_ts = cells[0], cells[2], cells[3], cells[4]
        assigned_dtime = datetime.strptime(assigned_ts, "%Y-%m-%d %H:%M:%S")
        closed_dtime = datetime.strptime(closed_ts, "%Y-%m-%d %H:%M:%S")

        if login not in assessors.keys():
            assessors[login] = Assessor(login, assigned_dtime)
        assessors[login].add_work_data(float(microtasks), (closed_dtime - assigned_dtime).total_seconds())

    results = []
    for login in assessors.keys():
        results.append((login, assessors[login].get_average_time(), assessors[login].total_mtasks))

    results.sort(key=(lambda x: x[1]))
    #for line in results:
    #    print(line[0] + ' ' + str(line[1]))

    # необходимо отсечь самых "ленивых", а так же сделать поправку на небольшие задержки
    # поэтому возьмем первые 50% результатов
    #
    # в качестве результата возьмем взвешенное по количеству задач среднее,
    # так как время, вычисленное по небольшому кол-ву задач, менее адекватно отражает среднее
    total_time = 0
    total_mtasks = 0
    for i in range(len(results)//2):
        total_time += results[i][1]*results[i][2]
        total_mtasks += results[i][2]

    print("По результатам", str(len(results)//2)," лучших ассессоров среднее время:", str(total_time / total_mtasks))
    print("Рекомендуемая оплата за одну микрозадачу: N*" + str(total_time / total_mtasks / 30))


if __name__ == "__main__":
    main()