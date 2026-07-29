from io import BytesIO
from django.template.loader import get_template
from django.conf import settings
import xhtml2pdf.pisa as pisa
import uuid
import os


def save_pdf(params):
    template = get_template("pdf.html")
    html = template.render(params)

    file_name = f"{uuid.uuid4()}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    with open(file_path, "wb") as f:
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), dest=f)

    if pdf.err:
        return "", False

    return file_name, True