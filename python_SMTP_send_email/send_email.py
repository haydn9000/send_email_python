from email.message import EmailMessage
import mimetypes
import smtplib
import os


def main() -> None:
    msg = EmailMessage()
    msg["Subject"] = "Hello this is a test email"
    msg["From"] = "YOUR_EMAIL@EMAIL.COM"
    msg["To"] = "RECIEPIENT_EMAIL@EMAIL.COM"
    msg.set_content("Test email")
    msg = add_attachments(
        msg, ["PATH_TO_FILE"])

    save_local_copy(msg)

    server = smtplib.SMTP("smtp.mailgun.org", 587)
    server.set_debuglevel(1)
    server.send_message(msg)
    server.quit()


def add_attachments(msg: EmailMessage, filenames: list) -> EmailMessage:
    for filename in filenames:
        path = os.path.normpath(filename)

        # Guess the content type based on the file"s extension.  Encoding
        # will be ignored, although we should check for simple things like
        # gzip"d or compressed files.
        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)
        with open(path, "rb") as fp:
            msg.add_attachment(fp.read(),
                               maintype=maintype,
                               subtype=subtype,
                               filename=filename)
    return msg


def save_local_copy(msg: EmailMessage) -> None:
    """Make a local copy of what we are going to send."""
    with open("outgoing.msg", "wb") as fp:
        from email.policy import SMTP
        fp.write(msg.as_bytes(policy=SMTP))


if __name__ == "__main__":
    main()
