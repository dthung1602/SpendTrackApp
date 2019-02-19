def provide_data_test_register_success():
    return [
        [
            {
                'username': 'abc',
                'email': 'someone@somewhere.com',
                'password1': 'strong_enough123',
                'password2': 'strong_enough123',
            }
        ],
        [
            {
                'username': 'What_ever136',
                'email': 'someone@somewhere.somedormain',
                'password1': 'long password',
                'password2': 'long password',
            }
        ],
        [
            {
                'username': 'hello-+@.',
                'email': 'me123@mycomputer.com',
                'password1': '%^)asdf123',
                'password2': '%^)asdf123',
            }
        ],
    ]


def provide_data_test_register_fail():
    return [
        [
            {
                'username': '',
                'email': 'someone@somewhere.com',
                'password1': 'strong_enough123',
                'password2': 'strong_enough123',
            },
            {'username'}
        ],
        [
            {
                'username': 'abc*',
                'email': 'someone@somewhere.com',
                'password1': 'strong_enough123',
                'password2': 'strong_enough123',
            },
            {'username'}
        ],
        [
            {
                'username': 'dtrump',
                'email': 'someone@somewhere.com',
                'password1': 'strong_enough123',
                'password2': 'strong_enough123',
            },
            {'username'}
        ],

        [
            {
                'username': 'abc',
                'email': '',
                'password1': 'strong_enough123',
                'password2': 'strong_enough123',
            },
            {'email'}
        ],
        [
            {
                'username': 'abc',
                'email': 'someonesomewhere',
                'password1': 'strong_enough123',
                'password2': 'strong_enough123',
            },
            {'email'}
        ],
        [
            {
                'username': 'abc',
                'email': 'someone@somewhere',
                'password1': 'strong_enough123',
                'password2': 'strong_enough123',
            },
            {'email'}
        ],

        [
            {
                'username': 'abc',
                'email': 'someone@somewhere.com',
                'password1': 'short',
                'password2': 'short',
            },
            {'password2'}
        ],
        [
            {
                'username': 'abc',
                'email': 'someone@somewhere.com',
                'password1': 'qwertyuiop',
                'password2': 'qwertyuiop',
            },
            {'password2'}
        ],
        [
            {
                'username': 'abc',
                'email': 'someone@somewhere.com',
                'password1': '1234567890',
                'password2': '1234567890',
            },
            {'password2'}
        ],
        [
            {
                'username': 'abc',
                'email': 'someone@somewhere.com',
                'password1': 'strong_enough123',
                'password2': 'strong_enough13',
            },
            {'password2'}
        ],
    ]


def provide_data_test_reset_password():
    return [
        ['trump@white-house.gov', 'dtrump'],
        ['clinton@white-house.gov', 'hclinton'],
    ]


def provide_data_test_edit_account_success():
    return [
        [
            {
                'username': 'abc',
                'email': 'someone@somewhere.com',
                'first_name': 'This is 1 first name',
                'last_name': 'LLLAAASSSTTT NNNAAAMMMEEE',
            }
        ],
        [
            {
                'username': 'abc',
                'email': 'someone@somewhere.com',
            }
        ],
        [
            {
                'username': 'hello-+@.',
                'email': 'me123@mycomputer.com',
                'first_name': '%',
                'last_name': '',
            }
        ]
    ]


def provide_data_test_edit_account_fail():
    return [
        [
            {
                'email': 'someone@somewhere.com',
                'first_name': 'This is first name',
                'last_name': 'New last name',
            },
            {'username'}
        ],
        [
            {
                'username': '',
                'email': 'someone@somewhere.com',
                'first_name': 'This is first name',
                'last_name': 'New last name',
            },
            {'username'}
        ],
        [
            {
                'username': 'abc*',
                'email': 'someone@somewhere.com',
                'first_name': 'This is first name',
                'last_name': 'New last name',
            },
            {'username'}
        ],

        [
            {
                'username': 'abc',
                'email': '',
                'first_name': 'This is first name',
                'last_name': 'New last name',
            },
            {'email'}
        ],
        [
            {
                'username': 'abc',
                'email': 'someonesomewherecom',
                'first_name': 'This is first name',
                'last_name': 'New last name',
            },
            {'email'}
        ],
        [
            {
                'username': 'abc',
                'email': 'someone@somewhere',
                'first_name': 'This is first name',
                'last_name': 'New last name',
            },
            {'email'}
        ],

        [
            {
                'username': 'abc*',
                'email': 'someone@somewhere',
                'first_name': 'This is first name',
                'last_name': 'New last name',
            },
            {'email', 'username'}
        ],
    ]


def provide_data_test_delete_account():
    return [
        [1], [2]
    ]


def provide_data_test_password_change_success():
    return [
        [
            {
                'old_password': 'unitedstates',
                'new_password1': 'new password',
                'new_password2': 'new password',
            }
        ],
        [
            {
                'old_password': 'new password',
                'new_password1': 'random123-*',
                'new_password2': 'random123-*',
            },
        ]
    ]


def provide_data_test_password_change_fail():
    return [
        [
            {
                'new_password1': 'random123-*-',
                'new_password2': 'random123-*-',
            },
            {'old_password'}
        ],
        [
            {
                'old_password': 'ussr',
                'new_password1': 'new password',
                'new_password2': 'new password',
            },
            {'old_password'}
        ],

        [
            {
                'old_password': 'unitedstates',
            },
            {'new_password1', 'new_password2'}
        ],
        [
            {
                'old_password': 'unitedstates',
                'new_password1': '',
                'new_password2': '',
            },
            {'new_password2', 'new_password1'}
        ],

        [
            {
                'old_password': 'unitedstates',
                'new_password1': 'random123-*-',
                'new_password2': 'random123',
            },
            {'new_password2'}
        ],

        [
            {
                'old_password': 'unitedstates',
                'new_password1': '123456789',
                'new_password2': '123456789',
            },
            {'new_password2'}
        ],
        [
            {
                'old_password': 'unitedstates',
                'new_password1': 'short',
                'new_password2': 'short',
            },
            {'new_password2'}
        ],
    ]
