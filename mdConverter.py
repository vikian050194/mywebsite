import datetime
import markdown

from dataclasses import dataclass

from markdown.extensions.tables import TableExtension


CONTENT_PLACEHOLDER = "{{content}}"
BUILD_PLACEHOLDER = "{{build}}"


@dataclass
class ConvertionDescription():
    source: str
    destination: str
    start_from: int = 0


def md_to_html(description: ConvertionDescription) -> None:
    source = f"src/{description.source}.md"
    template_path = "src/template.html"
    output_path = f"src/{description.destination}.html"

    with open(template_path, "r") as f:
        template = f.read()

    with open(source, "r") as f:
        sourceMd= f.read()
        sourceMd = sourceMd.splitlines()

    sourceMd = sourceMd[description.start_from:]
    sourceMd = "\n".join(sourceMd)
    htmlContent = markdown.markdown(sourceMd, extensions=[TableExtension(use_align_attribute=True)])
    buildDate = datetime.datetime.now()

    with open(output_path, "w") as f:
        result = template.replace(CONTENT_PLACEHOLDER, htmlContent).replace(BUILD_PLACEHOLDER, buildDate.isoformat(sep='T', timespec='seconds'))
        f.write(result)

files = [
    ConvertionDescription(source="index", destination="index")
]

for description in files:
    md_to_html(description)
