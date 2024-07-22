import ibis

con = ibis.sqlflite.connect(host="localhost",
                            user="sqlflite_username",
                            password="sqlflite_password",
                            port=31337,
                            use_encryption=True,
                            disable_certificate_verification=True
                            )

print(con.tables)

