# Data

Before creating the docker container with the MongoDB server, request from the admins a copy of the queried alex2mongo pipeline data `db.tar.gz`. Then extract the file to this directory with the following command:

```shell
tar xzf db.tar.gz db
```

Once completed, the tree should look like this: 

```shell
data
├── db
│   ├── collection-0-1658338005162308688.wt
│   ├── collection-10-1640006532910113381.wt
│   ├── collection-2-1658338005162308688.wt
│   ├── collection-4-1658338005162308688.wt
│   ├── diagnostic.data
│   ├── index-11-1640006532910113381.wt
│   ├── index-1-1658338005162308688.wt
│   ├── index-3-1658338005162308688.wt
│   ├── index-5-1658338005162308688.wt
│   ├── index-6-1658338005162308688.wt
│   ├── journal
│   ├── _mdb_catalog.wt
│   ├── sizeStorer.wt
│   ├── storage.bson
│   ├── WiredTiger
│   ├── WiredTigerHS.wt
│   ├── WiredTiger.turtle
│   └── WiredTiger.wt
├── db.tar.gz
├── Journal_List_Clarivate_Scopus_v1.xlsx
├── Kaggle_GDPbyCountry1999-2022.csv
└── README.md
```

Note that if, for whatever reason, building the Docker container fails, then it is possible the `data/db` directory will have to be deleted and re-extracted. This is due to an ownership conflict once the volume is created and used by the MongoDB server. 

