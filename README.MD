# User Profile With Django

This project builds a form that takes in details about a registered user and displays those details on a profile page. The profile page is only visible once the user has logged in.The profile page includes first name, last name, email, date of birth, confirm email, short bio and the option to upload an avatar.

Also set up validation for email, date of birth and the biography. The Date of Birth validation accepts three date formats: YYYY-MM-DD, MM/DD/YYYY, or MM/DD/YY. The Email validation checks if the email addresses match and are in a valid format. The bio validation checks that the bio is 10 characters or longer and properly escapes HTML formatting.

Also created a "change password page" that updates the user’s password. This page will ask for current password, new password and confirm password. Set up validation which checks that the current password is valid, that the new password and confirm password fields match, and that the new password follows the following policy:

- must not be the same as the current password
- minimum password length of 14 characters.
- must use of both uppercase and lowercase letters
- must include of one or more numerical digits
- must include of special characters, such as @, #, $
- cannot contain the username or parts of the user’s full name, such as his first name

To run the server in Django, please run the following command in bash:

```bash
$ python3 manage.py runserver
```

### Application Requirements

Run the following in bash:

```bash
$ pip3 install requirements.txt
```

### Notes

The application uses some third-party plug-ins

- [TinyMCE](https://www.tinymce.com/): enhanced editor for profile editing
- [jQuery PWStrength](http://matoilic.github.com/jquery.pwstrength): display password strength meter when creating new password.