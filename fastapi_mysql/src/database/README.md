## Alembic으로 테이블 생성 및 리비전 관리

### 1. Alembic을 이용해 테이블 생성

1. 테이블 초기화 수행

```
alembic init migrations
```

- alembic.ini 파일과 함께 magrations 디렉터리 아래에 파일이 생성됨

2. ini 파일 수정

> alembic은 수행 과정에서 alembic.ini 파일의 설정값을 읽음

- file_template 주석 해제 - 리비전 파일을 순서대로 확인하기 위함
- sqlalchemy.url 설정은 env.py에서 수행함

```
sqlalchemy.url = placeholder
```

3. env.py 수정

```
import database.mysql
from src.infra import models
from src.config import settings

...

config.set_main_option(
    "sqlalchemy.url",
    settings.mysql.sync_url(),
)

...

target_metadata = database.mysql.metadata
```

- Base.metadata는 모든 SQLAlchemy 모델의 메타데이터(테이블, 컬럼 정의 등)를 담고 있음
- alembic은 이를 사용해 자동으로 마이그레이션 스크립트를 생성함 (alembic revision --autogenerate)
- db에 포함할 모델들도 추가함


4. rivision 파일 생성

```
alembic revision --autogenerate -m "add User Table"
```

- migrations/versions 디렉터리 내 파일이 생성됨
- `upgrade`와 `downgrade` 함수는 각각 마이그레이션을 실행하고 롤백할 때 수행되는 코드
- revision id: 현재 리비전 파일이 어떤 리비전 파일에 의존하는지 나타냄
- 이를 통해 리비전 파일만 있으면 데이터베이스를 새로 생성할 때 순서대로 마이그레이션 할 수 있음


5. rivision 실행

```
alembic upgrade head
```

- head: 가장 최신의 리비전 파일까지 수행


6. DB 재설정

```
PYTHONPATH=./src alembic upgrade head
```