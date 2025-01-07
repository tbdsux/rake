from html2text import HTML2Text as BaseHTML2Text


class HTML2Text:
    def __init__(self, text: str):
        self.text = text

    @classmethod
    def process(cls, text: str, base_url: str):
        processor = BaseHTML2Text(baseurl=base_url)
        processor.ignore_links = False
        processor.bypass_tables = False

        md = processor.handle(text)

        return cls(md)
