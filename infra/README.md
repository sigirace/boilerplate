# Mongodb

## 1. key file

```
openssl rand -base64 756 > mongok-keyfile
chmod 600 mongo-keyfile
```

## 2. build & run

```
docker-compose -f docker-compose.yml up --build -d
```

## 3. Replica setting

```
docker exec -it mongo-db mongosh -u admin -p admin1234!
```

```
rs.initiate({
  _id: "rs0",
  members: [{ _id: 0, host: "mongo-db:27017" }]
});
```

## 4. Restart

```
docker-compose restart
```

# Mysql

```
mysql -u root -p
admin1234!
```

```
CREATE DATABASE python_fastapi;
GRANT ALL PRIVILEGES ON python_fastapi.* TO 'admin'@'%';
```
