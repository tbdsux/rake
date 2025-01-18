from textwrap import fill
from urllib.parse import urljoin, urlparse

from markdownify import MarkdownConverter, chomp


class CustomProcessor(MarkdownConverter):
    base_url: str = ""
    url_host = ""

    def process_tag(self, node, convert_as_inline, children_only=False):
        # Remove <noscript> tags
        if node.name == "noscript":
            return ""

        if node.name == "title":
            title = node.text.strip()
            return f"Title: {title}\nURL: {self.base_url}\n\nCONTENT:\n\n\n"

        return super().process_tag(node, convert_as_inline, children_only)

    def convert_a(self, el, text, convert_as_inline):
        prefix, suffix, text = chomp(text)
        if not text:
            return ""
        href = el.get("href")
        title = el.get("title")
        # For the replacement see #29: text nodes underscores are escaped
        if (
            self.options["autolinks"]
            and text.replace(r"\_", "_") == href
            and not title
            and not self.options["default_title"]
        ):
            # Shortcut syntax
            return "<%s>" % href
        if self.options["default_title"] and not title:
            title = href
        title_part = ' "%s"' % title.replace('"', r"\"") if title else ""

        # Add base url to href if it is not absolute
        if (
            href is not None
            and not href.startswith("http://")
            and not href.startswith("https://")
        ):
            href = urljoin(self.base_url, href)

        return (
            "%s[%s](%s%s)%s" % (prefix, text, href, title_part, suffix)
            if href
            else text
        )

    def convert_img(self, el, text, convert_as_inline):
        alt = el.attrs.get("alt", None) or ""
        src = el.attrs.get("src", None) or ""
        title = el.attrs.get("title", None) or ""
        title_part = ' "%s"' % title.replace('"', r"\"") if title else ""
        if (
            convert_as_inline
            and el.parent.name not in self.options["keep_inline_images_in"]
        ):
            return alt

        # Do not parse data URI images with no alt texts
        if alt == "" and src.startswith("data:image/"):
            return ""

        # Add base url to src if it is not absolute
        if not src.startswith("http://") and not src.startswith("https://"):
            src = urljoin(self.url_host, src)

        return "![%s](%s%s)" % (alt, src, title_part)

    def convert_p(self, el, text, convert_as_inline):
        if convert_as_inline:
            return " " + text.strip() + " "

        # Join text line breaks.
        text = " ".join(text.split("\n"))

        if self.options["wrap"]:
            # Preserve newlines (and preceding whitespace) resulting
            # from <br> tags.  Newlines in the input have already been
            # replaced by spaces.
            lines = text.split("\n")
            new_lines = []
            for line in lines:
                line = line.lstrip()
                line_no_trailing = line.rstrip()
                trailing = line[len(line_no_trailing) :]
                line = fill(
                    line,
                    width=self.options["wrap_width"],
                    break_long_words=False,
                    break_on_hyphens=False,
                )
                new_lines.append(line + trailing)
            text = "\n".join(new_lines)
        return "\n\n%s\n\n" % text if text else ""


class Markdownify:
    def __init__(self, text: str):
        self.text = text

    @classmethod
    def process(cls, text, base_url: str):
        processor = CustomProcessor(wrap_width=50)
        processor.base_url = base_url

        parsed_url = urlparse(base_url)
        processor.url_host = f"{parsed_url.scheme}://{parsed_url.netloc}"

        md = processor.convert(text)

        return cls(md)
