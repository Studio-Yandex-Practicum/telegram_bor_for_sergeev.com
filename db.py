import sqlite3


def insert_into_db(chat_id, username):
    try:
        connect = sqlite3.connect('db.sqlite3')
        cur = connect.cursor()
        cur.execute(
            'INSERT INTO telegram VALUES(?, ?);',
            (chat_id,  username)
        )
        connect.commit()
        connect.close()
    except sqlite3.Error as er:
        print(er)
    finally:
        if connect:
            connect.close()


def look_for_me(chat_id):
    try:
        connect = sqlite3.connect('db.sqlite3')
        cur = connect.cursor()
        cur.execute('''
            SELECT *
            FROM telegram
            WHERE chat_id = ?;
        ''', (chat_id, ))
        data = [tup for tup in cur]
        connect.close()
        return data
    except sqlite3.Error as er:
        print(er)
    finally:
        if connect:
            connect.close()


def update_username(chat_id, username):
    try:
        connect = sqlite3.connect('db.sqlite3')
        cur = connect.cursor()
        cur.execute(
            'UPDATE telegram SET username_trello = ? WHERE chat_id = ?;',
            (f'{username}', chat_id)
        )
        connect.commit()
        connect.close()
    except sqlite3.Error as er:
        print(er)
    finally:
        if connect:
            connect.close()


def get_ids(usernames):
    try:
        connect = sqlite3.connect('db.sqlite3')
        cur = connect.cursor()
        usernames = '", "'.join(usernames)
        usernames = f'("{usernames}")'
        cur.execute(f'''
        SELECT *
        FROM telegram
        WHERE username_trello IN {usernames};
        ''')
        data = []
        for result in cur:
            chat_id, _ = result
            data.append(chat_id)
        return data
    except sqlite3.Error as er:
        print(er)
    finally:
        if connect:
            connect.close()


if __name__ == '__main__':
    try:
        connect = sqlite3.connect('db.sqlite3')
        cur = connect.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS telegram(
            chat_id INTEGER PRIMARY KEY,
            username_trello TEXT
        );
        ''')
        connect.commit()
        print('Successfuly created')
        connect.close()
    except sqlite3.Error as er:
        print(er)
    finally:
        if connect:
            connect.close()
