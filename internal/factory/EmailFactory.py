
from internal.Entities import Email
from internal.viewmodel.EmailViewModel import EmailLiteViewModel

class EmailFactory:

    def create_lite_viewmodel(self, email: Email) -> EmailLiteViewModel:
        return EmailLiteViewModel(
            id=email.id,
            user_from_id=email.user_from_id,
            user_to_id=email.user_to_id,
            code=email.code,
            subject=email.subject,
            text_message=email.text_message,
            is_sent=True if email.is_sent == 1 else False,
            date_of_add=email.date_of_add.strftime("%Y-%m-%d %H:%M:%S") if email.date_of_add is not None else None,
            date_of_sent=email.date_of_sent.strftime("%Y-%m-%d %H:%M:%S") if email.date_of_sent is not None else None,
        )