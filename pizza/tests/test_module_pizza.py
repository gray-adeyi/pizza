import unittest
from ..pizza import (
    Gender,
    MailTemplate,
    User,
    AddressBook,
    Setting,
    MailTemplateBook,
)


class PizzaTest(unittest.TestCase):

    def test_user_model(self):
        user = User('gbenga', 'adeyi', 'adeyigbenga005@gmail.com', Gender.male)
        self.assertEqual(user.gender, Gender.male)
        self.assertEqual(user.fullname(), 'adeyi gbenga')
        self.assertEqual(user.fullname(order='fl'), 'gbenga adeyi')

    def test_address_book(self):
        book = AddressBook()
        self.assertIsInstance(book, AddressBook)
        self.assertEqual(book.contact_list, [])
        book.add_contact('gbenga', 'adeyi',
                         'adeyigbena005@gmail.com', Gender.male)
        self.assertListEqual(book.contact_list, [
            User('gbenga', 'adeyi', 'adeyigbenga005@gmail.com', Gender.male)])  # TODO: find a way to compare the two list to pass the test

    def test_settings(self):
        settings = Setting()
        self.assertEqual(settings.settings, {})
        settings.update_setting('PORT', 587)
        self.assertDictEqual(settings.settings, {'PORT': 587})

    def test_mail_template_book(self):
        mail_template_book = MailTemplateBook()
        self.assertListEqual(mail_template_book.mail_template_list, [])
        mail_template_book.add_template(
            'Newsletter', 'Dear {{}}, How have you been?')
        self.assertListEqual(mail_template_book.mail_template_list, [
                             MailTemplate('Newsletter', 'Dear {{}}, How have you been?')])


if __name__ == '__main__':
    unittest.main()
