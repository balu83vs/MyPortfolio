class Page_selection:
    """
    класс отвечающий за навигацию по страницам
    """
    def __init__(self, records_data, count_records: int) -> None:
        self.records_data = records_data
        self.count_records = count_records
        self.index = 1
        if len(records_data) % self.count_records > 0:
            self.max_page = len(records_data) // self.count_records + 1
        else:
            self.max_page = int(len(records_data) / self.count_records)

    # метод вывода диапазона страниц
    def show_range(self) -> list:
        res_list = list()
        for key in list(self.records_data.keys())[
            self.count_records * (self.index - 1) : self.count_records * self.index
        ]:
            res_list.append(self.records_data.get(key))
        return res_list

    # метод вывода следующей страницы
    def next_page(self):
        self.index += 1
        self.index = self.check_number()
        return self

    # метод вывода предыдущей страницы
    def prev_page(self):
        self.index -= 1
        self.index = self.check_number()
        return self

    # метод вывода первой страницы
    def first_page(self):
        self.index = 1
        return self

    # метод вывода последней страницы
    def last_page(self):
        self.index = self.max_page
        return self

    # метод вывода n-ой страницы
    def go_to_page(self, page):
        self.index = page
        self.index = self.check_number()
        return self

    # метод удержания номера страницы в диапазоне
    def check_number(self) -> int:
        # проверка правой границы
        if self.index > self.max_page:
            self.index = self.max_page
        # проверка левой границы    
        if self.index < 1:
            self.index = 1
        return self.index

    @property
    def total_pages(self):
        return self.max_page

    @property
    def current_page(self):
        return self.index
