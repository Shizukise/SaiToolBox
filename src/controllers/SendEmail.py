from email.message import EmailMessage
import mimetypes
import smtplib
from src.config import to_email

def send_email(from_email, password, attachment_path=None):

    body = (
    "Bonjour,\n\n"
    "Veuillez trouver ci-joint la revue des matériaux spécifiques pour lesquels nous aurons des commandes dans un futur proche.\n\n"
    "Ces informations visent à vous donner une visibilité sur les articles concernés et à faciliter leur gestion.\n\n"
    "Merci pour votre collaboration.\n\n"
    "Cordialement")

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = "Rapport commandes specifiques"
    msg['From'] = from_email
    msg['To'] = to_email

    # Attach a file if a path is provided
    if attachment_path:
        try:
            # Detect MIME type and encoding of the file
            mime_type, _ = mimetypes.guess_type(attachment_path)
            mime_type = mime_type or "application/octet-stream"  # Default to binary if type is unknown
            main_type, sub_type = mime_type.split("/", 1)

            with open(attachment_path, "rb") as file:
                # Attach the file to the email
                msg.add_attachment(file.read(), maintype=main_type, subtype=sub_type, filename=attachment_path.split("/")[-1])
        except Exception as e:
            print(f"Error attaching file: {e}")
            return

    # Send the email
    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)