import os
import ibis
from ibis import _


# con = ibis.sqlflite.connect(host="localhost",
#                             user=os.getenv("SQLFLITE_USERNAME", "sqlflite_username"),
#                             password=os.getenv("SQLFLITE_PASSWORD", "sqlflite_password"),
#                             port=31337,
#                             use_encryption=True,
#                             disable_certificate_verification=True
#                             )

# DuckDB
con = ibis.connect("sqlflite://sqlflite_username:sqlflite_password@localhost:31337?disableCertificateVerification=True&useEncryption=True")

# SQLite
# con = ibis.connect("sqlflite://sqlflite_username:joe@localhost:31338?useEncryption=False")

print(con.tables)

# assign the LINEITEM table to variable t (an Ibis table object)
t = con.table('lineitem')

# use the Ibis dataframe API to run TPC-H query 1
results = (t.filter(_.l_shipdate.cast('date') <= ibis.date('1998-12-01') + ibis.interval(days=90))
       .mutate(discount_price=_.l_extendedprice * (1 - _.l_discount))
       .mutate(charge=_.discount_price * (1 + _.l_tax))
       .group_by([_.l_returnflag,
                  _.l_linestatus
                  ]
                 )
       .aggregate(
            sum_qty=_.l_quantity.sum(),
            sum_base_price=_.l_extendedprice.sum(),
            sum_disc_price=_.discount_price.sum(),
            sum_charge=_.charge.sum(),
            avg_qty=_.l_quantity.mean(),
            avg_price=_.l_extendedprice.mean(),
            avg_disc=_.l_discount.mean(),
            count_order=_.count()
        )
       .order_by([_.l_returnflag,
                  _.l_linestatus
                  ]
                 )
       )

print(results.execute())
