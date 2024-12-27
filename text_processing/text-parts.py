class Document:
    def __init__(self, filename, main_title):
        self.filename = filename
        self.main_title = main_title
        self.page_list = []

    def _add_page(self, page):
        self.page_list.append(page)

    def __len__(self):
        return len(self.page_list)


class Page:
    def __init__(self, document, cursor_location):
        self.document = document
        self.cursor_location = cursor_location
        self.
